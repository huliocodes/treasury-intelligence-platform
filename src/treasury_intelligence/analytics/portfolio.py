from __future__ import annotations

from treasury_intelligence.analytics.risk_sufficiency import (
    RiskEvidenceSufficiencyAssessment,
)

from treasury_intelligence.models.economics import (
    EconomicsEvidenceAssessment,
)

from treasury_intelligence.models.eligibility import (
    EligibilityResult,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.position_risk import (
    PositionRiskAssessment,
)

from treasury_intelligence.models.returns import (
    ReturnAnalysis,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


def _validate_entity_alignment(
    eligibility: EligibilityResult,
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
    position_risk_assessments: tuple[
        PositionRiskAssessment,
        ...
    ],
    risk_sufficiency: (
        RiskEvidenceSufficiencyAssessment
    ),
    economics: EconomicsEvidenceAssessment,
    return_analysis: ReturnAnalysis,
) -> None:
    instrument_id = eligibility.instrument_id
    market_id = eligibility.market_id
    access_route_id = eligibility.access_route_id
    position_size_eur = (
        eligibility.position_size_eur
    )

    for assessment in risk_assessments:
        if (
            assessment.instrument_id
            != instrument_id
        ):
            raise ValueError(
                "Risk assessment instrument does not "
                "match eligibility result."
            )

        if (
            assessment.market_id
            != market_id
        ):
            raise ValueError(
                "Risk assessment market does not match "
                "eligibility result."
            )

    for assessment in (
        position_risk_assessments
    ):
        if (
            assessment.instrument_id
            != instrument_id
        ):
            raise ValueError(
                "Position-risk instrument does not "
                "match eligibility result."
            )

        if (
            assessment.market_id
            != market_id
        ):
            raise ValueError(
                "Position-risk market does not match "
                "eligibility result."
            )

        if (
            assessment.access_route_id
            != access_route_id
        ):
            raise ValueError(
                "Position-risk access route does not "
                "match eligibility result."
            )

        if (
            assessment.position_size_eur
            != position_size_eur
        ):
            raise ValueError(
                "Position-risk position size does not "
                "match eligibility result."
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
        != instrument_id
    ):
        raise ValueError(
            "Risk-sufficiency instrument does not match "
            "eligibility result."
        )

    if (
        risk_sufficiency.market_id
        != market_id
    ):
        raise ValueError(
            "Risk-sufficiency market does not match "
            "eligibility result."
        )

    if (
        economics.instrument_id
        != instrument_id
    ):
        raise ValueError(
            "Economics assessment instrument does not "
            "match eligibility result."
        )

    if (
        economics.market_id
        != market_id
    ):
        raise ValueError(
            "Economics assessment market does not match "
            "eligibility result."
        )

    if (
        economics.access_route_id
        != access_route_id
    ):
        raise ValueError(
            "Economics assessment access route does not "
            "match eligibility result."
        )

    if (
        economics.position_size_eur
        != position_size_eur
    ):
        raise ValueError(
            "Economics assessment position size does not "
            "match eligibility result."
        )

    if (
        return_analysis.instrument_id
        != instrument_id
    ):
        raise ValueError(
            "Return analysis instrument does not match "
            "eligibility result."
        )

    if (
        return_analysis.market_id
        != market_id
    ):
        raise ValueError(
            "Return analysis market does not match "
            "eligibility result."
        )

    if (
        return_analysis.access_route_id
        != access_route_id
    ):
        raise ValueError(
            "Return analysis access route does not match "
            "eligibility result."
        )

    if (
        return_analysis.position_size_eur
        != position_size_eur
    ):
        raise ValueError(
            "Return analysis position size does not match "
            "eligibility result."
        )

    if (
        economics.return_analysis_id
        != return_analysis.analysis_id
    ):
        raise ValueError(
            "Economics assessment does not reference "
            "the supplied return analysis."
        )


def _unknown_base_risk_count(
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
) -> int:
    return sum(
        1
        for assessment in risk_assessments
        if assessment.risk_level == "unknown"
    )


def _liquidity_position_risk(
    position_risk_assessments: tuple[
        PositionRiskAssessment,
        ...
    ],
) -> PositionRiskAssessment:
    matches = tuple(
        assessment
        for assessment in (
            position_risk_assessments
        )
        if assessment.risk_dimension
        == "liquidity"
    )

    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one liquidity "
            "position-risk assessment."
        )

    return matches[0]


def _eligibility_blocking_reasons(
    eligibility: EligibilityResult,
    excluded_check_names: tuple[str, ...] = (),
) -> tuple[str, ...]:
    return tuple(
        check.reason
        or (
            f"Required eligibility check "
            f"'{check.check_name}' failed."
        )
        for check in eligibility.checks
        if (
            check.required
            and check.status == "fail"
            and check.check_name
            not in excluded_check_names
        )
    )


def _eligibility_evidence_requirements(
    eligibility: EligibilityResult,
    excluded_check_names: tuple[str, ...] = (),
) -> tuple[str, ...]:
    return tuple(
        check.reason
        or (
            f"Required eligibility check "
            f"'{check.check_name}' remains unknown."
        )
        for check in eligibility.checks
        if (
            check.required
            and check.status == "unknown"
            and check.check_name
            not in excluded_check_names
        )
    )


def _economics_evidence_requirements(
    economics: EconomicsEvidenceAssessment,
) -> tuple[str, ...]:
    return tuple(
        gap.required_evidence
        for gap in economics.evidence_gaps
        if gap.blocking
    )


def _defensible_return(
    return_analysis: ReturnAnalysis,
) -> tuple[
    float | None,
    str | None,
]:
    if (
        return_analysis
        .realistic_expected_return_pct
        is not None
    ):
        return (
            return_analysis
            .realistic_expected_return_pct,
            (
                "Realistic expected return with all "
                "modeled blocking economics resolved."
            ),
        )

    if (
        return_analysis
        .return_after_known_costs_pct
        is not None
    ):
        return (
            return_analysis
            .return_after_known_costs_pct,
            (
                "Return after currently known costs. "
                "This is not a realistic expected return "
                "while blocking economics remain unknown."
            ),
        )

    if (
        return_analysis.reference_yield_pct
        is not None
    ):
        return (
            return_analysis.reference_yield_pct,
            (
                "Reference yield before unresolved "
                "economic frictions."
            ),
        )

    return (
        None,
        None,
    )


def _embedded_one_time_cost_component_types(
    return_analysis: ReturnAnalysis,
) -> tuple[str, ...]:
    component_types = (
        component.component_type
        for component in return_analysis.components
        if (
            component.component_type
            != "reference_yield"
            and component.basis
            in (
                "position_bps",
                "fixed_eur",
            )
            and component.status
            not in (
                "unknown",
                "not_applicable",
            )
        )
    )

    return tuple(
        dict.fromkeys(
            component_types
        )
    )


def build_integrated_portfolio_candidate(
    assessment_id: str,
    label: str,
    eligibility: EligibilityResult,
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
    position_risk_assessments: tuple[
        PositionRiskAssessment,
        ...
    ],
    risk_sufficiency: (
        RiskEvidenceSufficiencyAssessment
    ),
    economics: EconomicsEvidenceAssessment,
    return_analysis: ReturnAnalysis,
    notes: str | None = None,
) -> PortfolioCandidateAssessment:
    _validate_entity_alignment(
        eligibility=eligibility,
        risk_assessments=risk_assessments,
        position_risk_assessments=(
            position_risk_assessments
        ),
        risk_sufficiency=risk_sufficiency,
        economics=economics,
        return_analysis=return_analysis,
    )

    liquidity_risk = (
        _liquidity_position_risk(
            position_risk_assessments
        )
    )

    excluded_eligibility_checks = (
        "immediate_liquidity",
    )

    blocking_reasons = list(
        _eligibility_blocking_reasons(
            eligibility=eligibility,
            excluded_check_names=(
                excluded_eligibility_checks
            ),
        )
    )

    evidence_requirements = list(
        _eligibility_evidence_requirements(
            eligibility=eligibility,
            excluded_check_names=(
                excluded_eligibility_checks
            ),
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

    evidence_requirements.extend(
        _economics_evidence_requirements(
            economics
        )
    )

    blocking_reasons = tuple(
        dict.fromkeys(
            blocking_reasons
        )
    )

    evidence_requirements = tuple(
        dict.fromkeys(
            evidence_requirements
        )
    )

    if blocking_reasons:
        candidate_status = "blocked"
        recommendation_ready = False

    elif evidence_requirements:
        candidate_status = "needs_evidence"
        recommendation_ready = False

    else:
        candidate_status = (
            "recommendation_ready"
        )
        recommendation_ready = True

    (
        defensible_return_pct,
        defensible_return_measure,
    ) = _defensible_return(
        return_analysis
    )

    return PortfolioCandidateAssessment(
        assessment_id=assessment_id,
        mandate_id=eligibility.mandate_id,
        instrument_id=eligibility.instrument_id,
        market_id=eligibility.market_id,
        access_route_id=(
            eligibility.access_route_id
        ),
        label=label,
        position_size_eur=(
            eligibility.position_size_eur
        ),
        eligibility_status=(
            eligibility.overall_status
        ),
        liquidity_position_status=(
            liquidity_risk.position_risk_status
        ),
        economics_status=(
            economics.economics_status
        ),
        base_risk_unknown_dimension_count=(
            _unknown_base_risk_count(
                risk_assessments
            )
        ),
        defensible_return_pct=(
            defensible_return_pct
        ),
        defensible_return_measure=(
            defensible_return_measure
        ),
        candidate_status=(
            candidate_status
        ),
        blocking_reasons=(
            blocking_reasons
        ),
        evidence_requirements=(
            evidence_requirements
        ),
        recommendation_ready=(
            recommendation_ready
        ),
        embedded_one_time_cost_component_types=(
            _embedded_one_time_cost_component_types(
                return_analysis
            )
        ),
        notes=notes,
    )


def recommendation_ready_candidates(
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> tuple[
    PortfolioCandidateAssessment,
    ...
]:
    return tuple(
        candidate
        for candidate in candidates
        if candidate.recommendation_ready
    )


def blocked_candidates(
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> tuple[
    PortfolioCandidateAssessment,
    ...
]:
    return tuple(
        candidate
        for candidate in candidates
        if candidate.candidate_status
        == "blocked"
    )


def evidence_blocked_candidates(
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> tuple[
    PortfolioCandidateAssessment,
        ...
]:
    return tuple(
        candidate
        for candidate in candidates
        if candidate.candidate_status
        == "needs_evidence"
    )
