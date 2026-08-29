from __future__ import annotations

import re

from treasury_intelligence.models.eligibility import (
    EligibilityCheck,
    EligibilityResult,
)

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.opportunities import (
    Accessibility,
    Instrument,
    Market,
    PositionAnalysis,
)


def _check_minimum_allocation(
    mandate: TreasuryMandate,
    position: PositionAnalysis,
) -> EligibilityCheck:
    required_amount = (
        mandate.minimum_useful_allocation_eur
    )

    passes = (
        position.position_size_eur
        >= required_amount
    )

    return EligibilityCheck(
        check_name="minimum_useful_allocation",
        status="pass" if passes else "fail",
        required=True,
        actual_value=(
            f"EUR {position.position_size_eur:,.0f}"
        ),
        required_value=(
            f">= EUR {required_amount:,.0f}"
        ),
        reason=(
            None
            if passes
            else "position is below the minimum useful allocation"
        ),
    )


def _check_maximum_single_position(
    mandate: TreasuryMandate,
    position: PositionAnalysis,
) -> EligibilityCheck:
    if mandate.treasury_capital_eur <= 0:
        return EligibilityCheck(
            check_name="maximum_single_position",
            status="unknown",
            required=True,
            reason="treasury capital must be greater than zero",
        )

    position_pct = (
        position.position_size_eur
        / mandate.treasury_capital_eur
        * 100
    )

    passes = (
        position_pct
        <= mandate.maximum_single_position_pct
    )

    return EligibilityCheck(
        check_name="maximum_single_position",
        status="pass" if passes else "fail",
        required=True,
        actual_value=f"{position_pct:.2f}%",
        required_value=(
            f"<= {mandate.maximum_single_position_pct:.2f}%"
        ),
        reason=(
            None
            if passes
            else "position exceeds mandate single-position limit"
        ),
    )


def _check_currency(
    mandate: TreasuryMandate,
    instrument: Instrument,
) -> EligibilityCheck:
    fx_currency = (
        instrument.fx_exposure_currency
        or instrument.currency
    )

    passes = (
        fx_currency
        in mandate.allowed_currencies
    )

    return EligibilityCheck(
        check_name="fx_currency",
        status="pass" if passes else "fail",
        required=True,
        actual_value=fx_currency,
        required_value=", ".join(
            mandate.allowed_currencies
        ),
        reason=(
            None
            if passes
            else (
                "instrument FX exposure is not explicitly "
                "allowed by the mandate"
            )
        ),
    )


def _parse_settlement_days(
    settlement_cycle: str | None,
) -> int | None:
    if settlement_cycle is None:
        return None

    match = re.fullmatch(
        r"T\+(\d+)",
        settlement_cycle.strip().upper(),
    )

    if match is None:
        return None

    return int(match.group(1))


def _check_settlement(
    mandate: TreasuryMandate,
    market: Market,
) -> EligibilityCheck:
    if mandate.maximum_settlement_days is None:
        return EligibilityCheck(
            check_name="settlement",
            status="not_applicable",
            required=False,
            reason="mandate has no maximum settlement constraint",
        )

    if (
        market.venue_type == "defi_protocol"
        and market.settlement_cycle is None
    ):
        return EligibilityCheck(
            check_name="settlement",
            status="not_applicable",
            required=False,
            actual_value="onchain",
            reason=(
                "T+N securities settlement is not applicable "
                "to this DeFi protocol market; position liquidity "
                "is evaluated separately"
            ),
        )

    settlement_days = _parse_settlement_days(
        market.settlement_cycle
    )

    if settlement_days is None:
        return EligibilityCheck(
            check_name="settlement",
            status="unknown",
            required=True,
            actual_value=market.settlement_cycle,
            required_value=(
                f"<= T+{mandate.maximum_settlement_days}"
            ),
            reason=(
                "settlement cycle is unavailable or not "
                "expressed as T+N"
            ),
        )

    passes = (
        settlement_days
        <= mandate.maximum_settlement_days
    )

    return EligibilityCheck(
        check_name="settlement",
        status="pass" if passes else "fail",
        required=True,
        actual_value=f"T+{settlement_days}",
        required_value=(
            f"<= T+{mandate.maximum_settlement_days}"
        ),
        reason=(
            None
            if passes
            else "settlement exceeds mandate maximum"
        ),
    )


def _check_corporate_access(
    mandate: TreasuryMandate,
    accessibility: Accessibility,
) -> EligibilityCheck:
    if not mandate.require_verified_corporate_access:
        return EligibilityCheck(
            check_name="corporate_access",
            status="not_applicable",
            required=False,
            reason=(
                "verified corporate access is not required "
                "by this mandate"
            ),
        )

    passes = (
        accessibility.status
        in mandate.allowed_accessibility_statuses
    )

    return EligibilityCheck(
        check_name="corporate_access",
        status="pass" if passes else "fail",
        required=True,
        actual_value=accessibility.status,
        required_value=", ".join(
            mandate.allowed_accessibility_statuses
        ),
        reason=(
            None
            if passes
            else (
                "accessibility status does not satisfy "
                "the corporate-access mandate"
            )
        ),
    )


def _check_immediate_liquidity(
    mandate: TreasuryMandate,
    position: PositionAnalysis,
) -> EligibilityCheck:
    minimum_coverage = (
        mandate.minimum_immediate_liquidity_coverage_pct
    )

    if minimum_coverage is None:
        return EligibilityCheck(
            check_name="immediate_liquidity",
            status="not_applicable",
            required=False,
            reason=(
                "mandate has no minimum immediate-liquidity "
                "coverage constraint"
            ),
        )

    coverage = (
        position.immediate_exit_coverage_pct
    )

    if coverage is not None:
        passes = coverage >= minimum_coverage

        return EligibilityCheck(
            check_name="immediate_liquidity",
            status="pass" if passes else "fail",
            required=True,
            actual_value=f"{coverage:.2f}%",
            required_value=f">= {minimum_coverage:.2f}%",
            reason=(
                None
                if passes
                else (
                    "known immediate exit liquidity is below "
                    "the mandate requirement"
                )
            ),
        )

    if position.immediate_exit_supported is True:
        return EligibilityCheck(
            check_name="immediate_liquidity",
            status="pass",
            required=True,
            actual_value="supported",
            required_value=(
                f">= {minimum_coverage:.2f}% coverage"
            ),
        )

    if position.immediate_exit_supported is False:
        return EligibilityCheck(
            check_name="immediate_liquidity",
            status="fail",
            required=True,
            actual_value="not supported",
            required_value=(
                f">= {minimum_coverage:.2f}% coverage"
            ),
            reason=(
                "immediate exit is known not to satisfy "
                "the mandate"
            ),
        )

    return EligibilityCheck(
        check_name="immediate_liquidity",
        status="unknown",
        required=True,
        actual_value="unknown",
        required_value=(
            f">= {minimum_coverage:.2f}% coverage"
        ),
        reason=(
            "position-level immediate exit liquidity "
            "has not been established"
        ),
    )


def _check_instrument_type(
    mandate: TreasuryMandate,
    instrument: Instrument,
) -> EligibilityCheck:
    if mandate.allowed_instrument_types is None:
        return EligibilityCheck(
            check_name="instrument_type",
            status="not_applicable",
            required=False,
            actual_value=instrument.instrument_type,
            reason=(
                "mandate does not yet restrict "
                "instrument types"
            ),
        )

    passes = (
        instrument.instrument_type
        in mandate.allowed_instrument_types
    )

    return EligibilityCheck(
        check_name="instrument_type",
        status="pass" if passes else "fail",
        required=True,
        actual_value=instrument.instrument_type,
        required_value=", ".join(
            mandate.allowed_instrument_types
        ),
        reason=(
            None
            if passes
            else "instrument type is not allowed by mandate"
        ),
    )


def _check_target_yield(
    mandate: TreasuryMandate,
    position: PositionAnalysis,
) -> EligibilityCheck:
    if mandate.target_yield_pct is None:
        return EligibilityCheck(
            check_name="target_yield",
            status="not_applicable",
            required=False,
            reason="mandate has no target yield",
        )

    if not mandate.target_yield_is_hard_constraint:
        return EligibilityCheck(
            check_name="target_yield",
            status="not_applicable",
            required=False,
            actual_value=(
                None
                if position.reference_yield_pct is None
                else f"{position.reference_yield_pct:.3f}%"
            ),
            required_value=(
                f"target {mandate.target_yield_pct:.3f}%"
            ),
            reason=(
                "target yield is a preference, "
                "not a hard eligibility constraint"
            ),
        )

    if position.reference_yield_pct is None:
        return EligibilityCheck(
            check_name="target_yield",
            status="unknown",
            required=True,
            required_value=(
                f">= {mandate.target_yield_pct:.3f}%"
            ),
            reason="reference yield is unavailable",
        )

    passes = (
        position.reference_yield_pct
        >= mandate.target_yield_pct
    )

    return EligibilityCheck(
        check_name="target_yield",
        status="pass" if passes else "fail",
        required=True,
        actual_value=(
            f"{position.reference_yield_pct:.3f}%"
        ),
        required_value=(
            f">= {mandate.target_yield_pct:.3f}%"
        ),
        reason=(
            None
            if passes
            else "yield is below hard mandate minimum"
        ),
    )


def _determine_overall_status(
    checks: tuple[EligibilityCheck, ...],
) -> str:
    required_checks = tuple(
        check
        for check in checks
        if check.required
    )

    if any(
        check.status == "fail"
        for check in required_checks
    ):
        return "ineligible"

    if any(
        check.status == "unknown"
        for check in required_checks
    ):
        return "needs_evidence"

    return "eligible"


def evaluate_eligibility(
    mandate: TreasuryMandate,
    instrument: Instrument,
    market: Market,
    accessibility: Accessibility,
    position: PositionAnalysis,
) -> EligibilityResult:
    checks = (
        _check_minimum_allocation(
            mandate,
            position,
        ),
        _check_maximum_single_position(
            mandate,
            position,
        ),
        _check_currency(
            mandate,
            instrument,
        ),
        _check_settlement(
            mandate,
            market,
        ),
        _check_corporate_access(
            mandate,
            accessibility,
        ),
        _check_immediate_liquidity(
            mandate,
            position,
        ),
        _check_instrument_type(
            mandate,
            instrument,
        ),
        _check_target_yield(
            mandate,
            position,
        ),
    )

    return EligibilityResult(
        result_id=(
            f"{mandate.mandate_id}_"
            f"{instrument.instrument_id}_"
            f"{int(position.position_size_eur)}"
        ),
        mandate_id=mandate.mandate_id,
        instrument_id=instrument.instrument_id,
        market_id=market.market_id,
        access_route_id=position.access_route_id,
        position_size_eur=position.position_size_eur,
        overall_status=_determine_overall_status(
            checks
        ),
        checks=checks,
    )