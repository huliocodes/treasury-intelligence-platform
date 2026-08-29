from __future__ import annotations

from treasury_intelligence.analytics.liquidity import (
    LIQUIDITY_EVIDENCE_RANKS,
)

from treasury_intelligence.models.evidence import (
    EvidenceGap,
)

from treasury_intelligence.models.eligibility import (
    EligibilityResult,
)

from treasury_intelligence.models.liquidity import (
    LiquidityEvidenceAssessment,
)


def _build_generic_gap(
    eligibility: EligibilityResult,
    check,
) -> EvidenceGap:
    evidence_type_by_check = {
        "minimum_useful_allocation": (
            "allocation_constraint"
        ),
        "maximum_single_position": (
            "allocation_constraint"
        ),
        "fx_currency": (
            "currency_exposure"
        ),
        "settlement": (
            "settlement_terms"
        ),
        "corporate_access": (
            "corporate_access"
        ),
        "immediate_liquidity": (
            "position_liquidity"
        ),
        "instrument_type": (
            "instrument_classification"
        ),
        "target_yield": (
            "yield_evidence"
        ),
    }

    resolution_action_by_check = {
        "minimum_useful_allocation": (
            "Verify that the proposed allocation satisfies the "
            "treasury mandate's minimum useful allocation."
        ),
        "maximum_single_position": (
            "Verify the proposed position against the mandate's "
            "maximum single-position constraint."
        ),
        "fx_currency": (
            "Verify the instrument's economic FX exposure relative "
            "to the treasury mandate's permitted currencies."
        ),
        "settlement": (
            "Verify the applicable settlement cycle for the exact "
            "market and access route."
        ),
        "corporate_access": (
            "Verify that the Slovenian corporate entity can legally "
            "and operationally access, purchase, hold, and exit the "
            "instrument through the stated access route."
        ),
        "immediate_liquidity": (
            "Obtain position-size-specific evidence of immediate "
            "exit liquidity, including executable bid/ask pricing "
            "and available size where applicable."
        ),
        "instrument_type": (
            "Verify the instrument classification against the "
            "mandate's permitted instrument types."
        ),
        "target_yield": (
            "Obtain sufficiently current yield evidence for the "
            "exact instrument, market, and access route."
        ),
    }

    evidence_type = evidence_type_by_check.get(
        check.check_name,
        "other",
    )

    resolution_action = (
        resolution_action_by_check.get(
            check.check_name,
            (
                "Obtain the missing evidence required to resolve "
                "this eligibility check."
            ),
        )
    )

    required_evidence = (
        check.required_value
        if check.required_value is not None
        else "Required eligibility evidence"
    )

    return EvidenceGap(
        evidence_gap_id=(
            f"{eligibility.result_id}_"
            f"{check.check_name}_evidence_gap"
        ),
        mandate_id=eligibility.mandate_id,
        instrument_id=eligibility.instrument_id,
        market_id=eligibility.market_id,
        access_route_id=(
            eligibility.access_route_id
        ),
        position_size_eur=(
            eligibility.position_size_eur
        ),
        check_name=check.check_name,
        evidence_type=evidence_type,
        priority="high",
        current_status=check.status,
        required_evidence=required_evidence,
        resolution_action=resolution_action,
        blocking=True,
        notes=(
            "This gap exists because a required eligibility "
            "check remains unknown."
        ),
    )


def _build_liquidity_gap(
    eligibility: EligibilityResult,
    check,
    liquidity_assessment: (
        LiquidityEvidenceAssessment
    ),
) -> EvidenceGap:
    current_level = (
        liquidity_assessment.evidence_level
    )

    required_level = "position_depth"

    current_rank = LIQUIDITY_EVIDENCE_RANKS[
        current_level
    ]

    required_rank = LIQUIDITY_EVIDENCE_RANKS[
        required_level
    ]

    evidence_level_gap = max(
        required_rank - current_rank,
        0,
    )

    required_evidence = (
        check.required_value
        if check.required_value is not None
        else (
            "Position-size-specific immediate liquidity "
            "evidence"
        )
    )

    if current_level == "none":
        resolution_action = (
            "No direct liquidity evidence is currently available. "
            "Obtain market evidence and progress toward "
            "position-size-specific executable depth sufficient "
            "to determine immediate exit coverage."
        )

    elif current_level == "market_activity":
        resolution_action = (
            "Market activity is already observed, but daily "
            "turnover does not establish executable depth. "
            "Obtain stronger quote evidence and ultimately "
            "position-size-specific executable depth sufficient "
            "to determine immediate exit coverage."
        )

    elif current_level == "displayed_quote":
        resolution_action = (
            "A public two-sided quote is available, but displayed "
            "prices without size do not establish full exit "
            "capacity. Obtain displayed size and ultimately "
            "position-size-specific executable depth."
        )

    elif current_level == "displayed_quote_with_size":
        resolution_action = (
            "Displayed bid/ask size is available, but displayed "
            "size does not prove executable liquidity for the "
            "entire proposed position. Obtain position-size-"
            "specific executable depth or equivalent firm "
            "execution evidence."
        )

    elif current_level == "executable_quote":
        resolution_action = (
            "Executable pricing evidence exists, but full "
            "position coverage remains unproven. Obtain evidence "
            "that executable liquidity covers the entire proposed "
            "position."
        )

    else:
        resolution_action = (
            "Position-depth evidence is available. Re-evaluate "
            "the underlying eligibility check using the observed "
            "position-size liquidity result."
        )

    return EvidenceGap(
        evidence_gap_id=(
            f"{eligibility.result_id}_"
            f"{check.check_name}_evidence_gap"
        ),
        mandate_id=eligibility.mandate_id,
        instrument_id=eligibility.instrument_id,
        market_id=eligibility.market_id,
        access_route_id=(
            eligibility.access_route_id
        ),
        position_size_eur=(
            eligibility.position_size_eur
        ),
        check_name=check.check_name,
        evidence_type="position_liquidity",
        priority="high",
        current_status=check.status,
        required_evidence=required_evidence,
        resolution_action=resolution_action,
        blocking=True,
        current_evidence_level=current_level,
        required_evidence_level=required_level,
        evidence_level_gap=evidence_level_gap,
        notes=(
            liquidity_assessment.strongest_supported_claim
        ),
    )


def build_evidence_gaps(
    eligibility: EligibilityResult,
    liquidity_assessment: (
        LiquidityEvidenceAssessment | None
    ) = None,
) -> tuple[EvidenceGap, ...]:
    gaps: list[EvidenceGap] = []

    for check in eligibility.checks:
        if not check.required:
            continue

        if check.status != "unknown":
            continue

        if (
            check.check_name
            == "immediate_liquidity"
            and liquidity_assessment is not None
        ):
            gap = _build_liquidity_gap(
                eligibility=eligibility,
                check=check,
                liquidity_assessment=(
                    liquidity_assessment
                ),
            )

        else:
            gap = _build_generic_gap(
                eligibility=eligibility,
                check=check,
            )

        gaps.append(gap)

    return tuple(gaps)