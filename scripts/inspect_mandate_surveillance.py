from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.analytics.mandate_surveillance import (
    assess_current_holding_mandate,
    build_treasury_mandate_surveillance,
)

from treasury_intelligence.analytics.treasury_state import (
    build_treasury_state,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.eligibility import (
    EligibilityCheck,
    EligibilityResult,
)

from treasury_intelligence.models.position_risk import (
    PositionRiskAssessment,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryPosition,
)


AS_OF = "2026-09-02T21:00:00Z"

POSITION_SIZE_EUR = 1_000_000.0

INSTRUMENT_ID = "fixture_instrument"
MARKET_ID = "fixture_market"
ACCESS_ROUTE_ID = "fixture_access"


def build_position() -> TreasuryPosition:
    return TreasuryPosition(
        position_id="fixture_current_position",
        instrument_id=INSTRUMENT_ID,
        market_id=MARKET_ID,
        access_route_id=ACCESS_ROUTE_ID,
        label="CURRENT FIXTURE",
        current_value_eur=POSITION_SIZE_EUR,
    )


def build_eligibility(
    *,
    corporate_access_status: str = "pass",
) -> EligibilityResult:
    checks = (
        EligibilityCheck(
            check_name="minimum_useful_allocation",
            status="pass",
            required=True,
        ),
        EligibilityCheck(
            check_name="maximum_single_position",
            status="pass",
            required=True,
        ),
        EligibilityCheck(
            check_name="fx_currency",
            status="pass",
            required=True,
        ),
        EligibilityCheck(
            check_name="settlement",
            status="pass",
            required=True,
        ),
        EligibilityCheck(
            check_name="corporate_access",
            status=corporate_access_status,
            required=True,
            reason=(
                None
                if corporate_access_status == "pass"
                else (
                    "Current corporate access evidence "
                    "requires review."
                    if corporate_access_status == "unknown"
                    else (
                        "Current corporate access no longer "
                        "satisfies the mandate."
                    )
                )
            ),
        ),
        EligibilityCheck(
            check_name="immediate_liquidity",
            status="pass",
            required=True,
        ),
        EligibilityCheck(
            check_name="instrument_type",
            status="pass",
            required=True,
        ),
        EligibilityCheck(
            check_name="target_yield",
            status="pass",
            required=False,
        ),
    )

    if any(
        check.required
        and check.status == "fail"
        for check in checks
    ):
        overall_status = "ineligible"

    elif any(
        check.required
        and check.status == "unknown"
        for check in checks
    ):
        overall_status = "needs_evidence"

    else:
        overall_status = "eligible"

    return EligibilityResult(
        result_id="fixture_eligibility",
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        instrument_id=INSTRUMENT_ID,
        market_id=MARKET_ID,
        access_route_id=ACCESS_ROUTE_ID,
        position_size_eur=POSITION_SIZE_EUR,
        overall_status=overall_status,
        checks=checks,
    )


def build_position_risk(
    *,
    liquidity_status: str = "supported",
) -> tuple[PositionRiskAssessment, ...]:
    liquidity_evidence_sufficient = (
        liquidity_status != "unknown"
    )

    assessments = []

    dimensions = (
        "principal_credit",
        "market",
        "liquidity",
        "currency_asset",
        "structural_counterparty",
        "technical",
        "operational_regulatory",
    )

    for dimension in dimensions:
        if dimension == "liquidity":
            assessments.append(
                PositionRiskAssessment(
                    assessment_id=(
                        "fixture_liquidity_risk"
                    ),
                    instrument_id=INSTRUMENT_ID,
                    market_id=MARKET_ID,
                    access_route_id=ACCESS_ROUTE_ID,
                    position_size_eur=(
                        POSITION_SIZE_EUR
                    ),
                    risk_dimension="liquidity",
                    base_risk_level="low",
                    position_sensitive=True,
                    position_risk_status=(
                        liquidity_status
                    ),
                    evidence_sufficient=(
                        liquidity_evidence_sufficient
                    ),
                    rationale=(
                        "Immediate liquidity is supported "
                        "for the current position."
                        if liquidity_status == "supported"
                        else (
                            "Current evidence shows the "
                            "position cannot be fully exited "
                            "immediately."
                            if liquidity_status
                            == "not_supported"
                            else (
                                "Current liquidity evidence "
                                "is insufficient for the "
                                "position."
                            )
                        )
                    ),
                    supporting_risk_assessment_id=(
                        "fixture_liquidity_base_risk"
                    ),
                    supporting_position_analysis_id=(
                        "fixture_position_analysis"
                    ),
                    supporting_liquidity_assessment_id=(
                        "fixture_liquidity_evidence"
                    ),
                )
            )

        else:
            assessments.append(
                PositionRiskAssessment(
                    assessment_id=(
                        f"fixture_{dimension}_risk"
                    ),
                    instrument_id=INSTRUMENT_ID,
                    market_id=MARKET_ID,
                    access_route_id=ACCESS_ROUTE_ID,
                    position_size_eur=(
                        POSITION_SIZE_EUR
                    ),
                    risk_dimension=dimension,
                    base_risk_level=(
                        "not_applicable"
                        if dimension == "technical"
                        else "low"
                    ),
                    position_sensitive=False,
                    position_risk_status=(
                        "not_position_sensitive"
                    ),
                    evidence_sufficient=True,
                    rationale=(
                        "Deterministic non-position-sensitive "
                        "fixture."
                    ),
                    supporting_risk_assessment_id=(
                        f"fixture_{dimension}_base_risk"
                    ),
                    supporting_position_analysis_id=(
                        "fixture_position_analysis"
                    ),
                )
            )

    return tuple(assessments)


def build_risk_sufficiency():
    from treasury_intelligence.analytics.risk_sufficiency import (
        RiskEvidenceSufficiencyAssessment,
    )

    return RiskEvidenceSufficiencyAssessment(
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        instrument_id=INSTRUMENT_ID,
        market_id=MARKET_ID,
        required_dimensions=(
            "principal_credit",
            "market",
            "currency_asset",
            "structural_counterparty",
            "technical",
            "operational_regulatory",
        ),
        insufficient_dimensions=(),
        unacceptable_dimensions=(),
        evidence_requirements=(),
        risk_blocking_reasons=(),
        evidence_sufficient=True,
        risk_acceptable=True,
        sufficient_for_recommendation=True,
    )


def print_case(
    *,
    label: str,
    assessment,
) -> None:
    print(label)
    print()
    print(
        f"Status:                       "
        f"{assessment.status}"
    )
    print(
        f"Blocking reasons:             "
        f"{len(assessment.blocking_reasons)}"
    )
    print(
        f"Evidence requirements:        "
        f"{len(assessment.evidence_requirements)}"
    )

    for reason in assessment.blocking_reasons:
        print(f"  BLOCK: {reason}")

    for requirement in (
        assessment.evidence_requirements
    ):
        print(f"  EVIDENCE: {requirement}")

    print()
    print("-" * 100)
    print()


def main() -> None:
    position = build_position()

    state = build_treasury_state(
        state_id="fixture_surveillance_state",
        mandate=MODEL_COMPANY_MANDATE,
        as_of=AS_OF,
        positions=(position,),
    )

    base_risk_sufficiency = (
        build_risk_sufficiency()
    )

    compliant = assess_current_holding_mandate(
        assessment_id="fixture_compliant",
        position=position,
        eligibility=build_eligibility(),
        position_risk_assessments=(
            build_position_risk()
        ),
        risk_sufficiency=(
            base_risk_sufficiency
        ),
    )

    print_case(
        label="CASE 1 — CURRENT HOLDING COMPLIANT",
        assessment=compliant,
    )

    risk_breach_sufficiency = replace(
        base_risk_sufficiency,
        unacceptable_dimensions=(
            "principal_credit",
        ),
        risk_blocking_reasons=(
            "Principal-credit risk is now moderate and "
            "outside the mandate tolerance.",
        ),
        risk_acceptable=False,
        sufficient_for_recommendation=False,
    )

    risk_breach = assess_current_holding_mandate(
        assessment_id="fixture_risk_breach",
        position=position,
        eligibility=build_eligibility(),
        position_risk_assessments=(
            build_position_risk()
        ),
        risk_sufficiency=(
            risk_breach_sufficiency
        ),
    )

    print_case(
        label="CASE 2 — CURRENT HOLDING RISK BREACH",
        assessment=risk_breach,
    )

    liquidity_breach = (
        assess_current_holding_mandate(
            assessment_id=(
                "fixture_liquidity_breach"
            ),
            position=position,
            eligibility=build_eligibility(),
            position_risk_assessments=(
                build_position_risk(
                    liquidity_status="not_supported"
                )
            ),
            risk_sufficiency=(
                base_risk_sufficiency
            ),
        )
    )

    print_case(
        label=(
            "CASE 3 — CURRENT HOLDING "
            "LIQUIDITY BREACH"
        ),
        assessment=liquidity_breach,
    )

    evidence_required_sufficiency = replace(
        base_risk_sufficiency,
        insufficient_dimensions=(
            "structural_counterparty",
        ),
        evidence_requirements=(
            "Current structural-counterparty evidence "
            "must be refreshed.",
        ),
        evidence_sufficient=False,
        sufficient_for_recommendation=False,
    )

    evidence_required = (
        assess_current_holding_mandate(
            assessment_id=(
                "fixture_evidence_required"
            ),
            position=position,
            eligibility=build_eligibility(
                corporate_access_status="unknown"
            ),
            position_risk_assessments=(
                build_position_risk(
                    liquidity_status="unknown"
                )
            ),
            risk_sufficiency=(
                evidence_required_sufficiency
            ),
        )
    )

    print_case(
        label=(
            "CASE 4 — CURRENT HOLDING "
            "EVIDENCE REQUIRED"
        ),
        assessment=evidence_required,
    )

    surveillance = (
        build_treasury_mandate_surveillance(
            surveillance_id=(
                "fixture_surveillance"
            ),
            state=state,
            holding_assessments=(
                compliant,
            ),
            notes=(
                "Deterministic Milestone 14B "
                "surveillance fixture."
            ),
        )
    )

    print("AGGREGATE SURVEILLANCE — COMPLIANT")
    print()
    print(
        f"Status:                       "
        f"{surveillance.status}"
    )
    print(
        f"Compliant positions:          "
        f"{surveillance.compliant_position_count}"
    )
    print(
        f"Evidence-required positions:  "
        f"{surveillance.evidence_required_position_count}"
    )
    print(
        f"Breached positions:           "
        f"{surveillance.breach_position_count}"
    )

    assert compliant.status == "compliant"
    assert risk_breach.status == "breach"
    assert liquidity_breach.status == "breach"
    assert (
        evidence_required.status
        == "evidence_required"
    )
    assert surveillance.status == "compliant"

    breach_surveillance = (
        build_treasury_mandate_surveillance(
            surveillance_id=(
                "fixture_breach_surveillance"
            ),
            state=state,
            holding_assessments=(
                risk_breach,
            ),
        )
    )

    assert breach_surveillance.status == "breach"

    evidence_surveillance = (
        build_treasury_mandate_surveillance(
            surveillance_id=(
                "fixture_evidence_surveillance"
            ),
            state=state,
            holding_assessments=(
                evidence_required,
            ),
        )
    )

    assert (
        evidence_surveillance.status
        == "evidence_required"
    )

    print()
    print(
        "All Milestone 14B surveillance assertions passed."
    )


if __name__ == "__main__":
    main()
