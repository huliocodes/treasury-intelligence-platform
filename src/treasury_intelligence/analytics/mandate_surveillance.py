from __future__ import annotations

from treasury_intelligence.analytics.risk_sufficiency import (
    RiskEvidenceSufficiencyAssessment,
)

from treasury_intelligence.models.eligibility import (
    EligibilityResult,
)

from treasury_intelligence.models.mandate_surveillance import (
    CurrentHoldingMandateAssessment,
    TreasuryMandateSurveillance,
)

from treasury_intelligence.models.position_risk import (
    PositionRiskAssessment,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryPosition,
    TreasuryState,
)


def _liquidity_position_risk(
    position_risk_assessments: tuple[
        PositionRiskAssessment,
        ...
    ],
) -> PositionRiskAssessment:
    matches = tuple(
        assessment
        for assessment in position_risk_assessments
        if assessment.risk_dimension == "liquidity"
    )

    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one liquidity "
            "position-risk assessment."
        )

    return matches[0]


def _validate_holding_alignment(
    *,
    position: TreasuryPosition,
    eligibility: EligibilityResult,
    position_risk_assessments: tuple[
        PositionRiskAssessment,
        ...
    ],
    risk_sufficiency: (
        RiskEvidenceSufficiencyAssessment
    ),
) -> None:
    if (
        eligibility.instrument_id
        != position.instrument_id
    ):
        raise ValueError(
            "Eligibility instrument does not match "
            "current treasury position."
        )

    if eligibility.market_id != position.market_id:
        raise ValueError(
            "Eligibility market does not match "
            "current treasury position."
        )

    if (
        eligibility.access_route_id
        != position.access_route_id
    ):
        raise ValueError(
            "Eligibility access route does not match "
            "current treasury position."
        )

    if (
        abs(
            eligibility.position_size_eur
            - position.current_value_eur
        )
        > 0.01
    ):
        raise ValueError(
            "Eligibility position size does not match "
            "current treasury position value."
        )

    if (
        risk_sufficiency.mandate_id
        != eligibility.mandate_id
    ):
        raise ValueError(
            "Risk-sufficiency mandate does not match "
            "eligibility result."
        )

    if (
        risk_sufficiency.instrument_id
        != position.instrument_id
    ):
        raise ValueError(
            "Risk-sufficiency instrument does not match "
            "current treasury position."
        )

    if (
        risk_sufficiency.market_id
        != position.market_id
    ):
        raise ValueError(
            "Risk-sufficiency market does not match "
            "current treasury position."
        )

    if not position_risk_assessments:
        raise ValueError(
            "Position-risk assessments are required."
        )

    for assessment in position_risk_assessments:
        if (
            assessment.instrument_id
            != position.instrument_id
        ):
            raise ValueError(
                "Position-risk instrument does not match "
                "current treasury position."
            )

        if assessment.market_id != position.market_id:
            raise ValueError(
                "Position-risk market does not match "
                "current treasury position."
            )

        if (
            assessment.access_route_id
            != position.access_route_id
        ):
            raise ValueError(
                "Position-risk access route does not match "
                "current treasury position."
            )

        if (
            abs(
                assessment.position_size_eur
                - position.current_value_eur
            )
            > 0.01
        ):
            raise ValueError(
                "Position-risk size does not match "
                "current treasury position value."
            )


def _eligibility_blocking_reasons(
    eligibility: EligibilityResult,
) -> tuple[str, ...]:
    return tuple(
        check.reason
        or (
            "Required current-holding eligibility check "
            f"'{check.check_name}' failed."
        )
        for check in eligibility.checks
        if (
            check.required
            and check.status == "fail"
            and check.check_name
            != "immediate_liquidity"
        )
    )


def _eligibility_evidence_requirements(
    eligibility: EligibilityResult,
) -> tuple[str, ...]:
    return tuple(
        check.reason
        or (
            "Required current-holding eligibility check "
            f"'{check.check_name}' remains unknown."
        )
        for check in eligibility.checks
        if (
            check.required
            and check.status == "unknown"
            and check.check_name
            != "immediate_liquidity"
        )
    )


def assess_current_holding_mandate(
    *,
    assessment_id: str,
    position: TreasuryPosition,
    eligibility: EligibilityResult,
    position_risk_assessments: tuple[
        PositionRiskAssessment,
        ...
    ],
    risk_sufficiency: (
        RiskEvidenceSufficiencyAssessment
    ),
    notes: str | None = None,
) -> CurrentHoldingMandateAssessment:
    if not assessment_id:
        raise ValueError(
            "assessment_id is required."
        )

    _validate_holding_alignment(
        position=position,
        eligibility=eligibility,
        position_risk_assessments=(
            position_risk_assessments
        ),
        risk_sufficiency=risk_sufficiency,
    )

    liquidity_risk = _liquidity_position_risk(
        position_risk_assessments
    )

    blocking_reasons = list(
        _eligibility_blocking_reasons(
            eligibility
        )
    )

    evidence_requirements = list(
        _eligibility_evidence_requirements(
            eligibility
        )
    )

    if (
        liquidity_risk.position_risk_status
        == "not_supported"
    ):
        blocking_reasons.append(
            liquidity_risk.rationale
        )

    elif (
        liquidity_risk.position_risk_status
        == "unknown"
    ):
        evidence_requirements.append(
            liquidity_risk.rationale
        )

    blocking_reasons.extend(
        risk_sufficiency.risk_blocking_reasons
    )

    evidence_requirements.extend(
        risk_sufficiency.evidence_requirements
    )

    blocking_reasons = tuple(
        dict.fromkeys(blocking_reasons)
    )

    evidence_requirements = tuple(
        dict.fromkeys(evidence_requirements)
    )

    if blocking_reasons:
        status = "breach"

    elif evidence_requirements:
        status = "evidence_required"

    else:
        status = "compliant"

    return CurrentHoldingMandateAssessment(
        assessment_id=assessment_id,
        mandate_id=eligibility.mandate_id,
        position_id=position.position_id,
        instrument_id=position.instrument_id,
        market_id=position.market_id,
        access_route_id=position.access_route_id,
        position_size_eur=(
            position.current_value_eur
        ),
        status=status,
        blocking_reasons=blocking_reasons,
        evidence_requirements=(
            evidence_requirements
        ),
        notes=notes,
    )


def build_treasury_mandate_surveillance(
    *,
    surveillance_id: str,
    state: TreasuryState,
    holding_assessments: tuple[
        CurrentHoldingMandateAssessment,
        ...
    ],
    notes: str | None = None,
) -> TreasuryMandateSurveillance:
    if not surveillance_id:
        raise ValueError(
            "surveillance_id is required."
        )

    assessment_by_position_id = {}

    for assessment in holding_assessments:
        if (
            assessment.position_id
            in assessment_by_position_id
        ):
            raise ValueError(
                "Duplicate current-holding mandate "
                "assessment for position: "
                f"{assessment.position_id}"
            )

        assessment_by_position_id[
            assessment.position_id
        ] = assessment

    state_position_ids = {
        position.position_id
        for position in state.positions
    }

    assessment_position_ids = set(
        assessment_by_position_id
    )

    if (
        state_position_ids
        != assessment_position_ids
    ):
        missing = (
            state_position_ids
            - assessment_position_ids
        )

        unexpected = (
            assessment_position_ids
            - state_position_ids
        )

        details = []

        if missing:
            details.append(
                "missing assessments for: "
                + ", ".join(sorted(missing))
            )

        if unexpected:
            details.append(
                "unexpected assessments for: "
                + ", ".join(sorted(unexpected))
            )

        raise ValueError(
            "Holding assessments must exactly cover "
            "current treasury positions; "
            + "; ".join(details)
        )

    for assessment in holding_assessments:
        if assessment.mandate_id != state.mandate_id:
            raise ValueError(
                "Holding-assessment mandate does not "
                "match treasury state mandate."
            )

    breach_position_count = sum(
        1
        for assessment in holding_assessments
        if assessment.status == "breach"
    )

    evidence_required_position_count = sum(
        1
        for assessment in holding_assessments
        if assessment.status
        == "evidence_required"
    )

    compliant_position_count = sum(
        1
        for assessment in holding_assessments
        if assessment.status == "compliant"
    )

    if breach_position_count > 0:
        status = "breach"

    elif evidence_required_position_count > 0:
        status = "evidence_required"

    else:
        status = "compliant"

    blocking_reasons = tuple(
        dict.fromkeys(
            reason
            for assessment in holding_assessments
            for reason in assessment.blocking_reasons
        )
    )

    evidence_requirements = tuple(
        dict.fromkeys(
            requirement
            for assessment in holding_assessments
            for requirement
            in assessment.evidence_requirements
        )
    )

    return TreasuryMandateSurveillance(
        surveillance_id=surveillance_id,
        mandate_id=state.mandate_id,
        treasury_state_id=state.state_id,
        as_of=state.as_of,
        holding_assessments=holding_assessments,
        status=status,
        breach_position_count=(
            breach_position_count
        ),
        evidence_required_position_count=(
            evidence_required_position_count
        ),
        compliant_position_count=(
            compliant_position_count
        ),
        blocking_reasons=blocking_reasons,
        evidence_requirements=(
            evidence_requirements
        ),
        notes=notes,
    )
