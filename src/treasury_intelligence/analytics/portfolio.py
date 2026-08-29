from __future__ import annotations

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)


def build_portfolio_candidate_assessment(
    assessment_id: str,
    mandate_id: str,
    instrument_id: str,
    market_id: str,
    access_route_id: str,
    label: str,
    position_size_eur: float,
    eligibility_status: str,
    liquidity_position_status: str,
    economics_status: str,
    base_risk_unknown_dimension_count: int,
    defensible_return_pct: float | None,
    defensible_return_measure: str | None,
    blocking_reasons: tuple[str, ...] = (),
    evidence_requirements: tuple[str, ...] = (),
    notes: str | None = None,
) -> PortfolioCandidateAssessment:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    final_blocking_reasons = list(
        blocking_reasons
    )

    final_evidence_requirements = list(
        evidence_requirements
    )

    has_supplied_blocking_reasons = bool(
        final_blocking_reasons
    )

    has_supplied_evidence_requirements = bool(
        final_evidence_requirements
    )

    if eligibility_status == "ineligible":
        if not has_supplied_blocking_reasons:
            final_blocking_reasons.append(
                "The modeled position fails one or more "
                "required treasury-mandate eligibility "
                "checks."
            )

    elif eligibility_status == "needs_evidence":
        if not has_supplied_evidence_requirements:
            final_evidence_requirements.append(
                "Resolve the required eligibility evidence "
                "gaps before portfolio recommendation."
            )

    elif eligibility_status != "eligible":
        raise ValueError(
            "Unsupported eligibility status: "
            f"{eligibility_status}"
        )

    if liquidity_position_status == "not_supported":
        if not has_supplied_blocking_reasons:
            final_blocking_reasons.append(
                "Direct position-size evidence shows that "
                "the modeled immediate-liquidity requirement "
                "is not currently supported."
            )

    elif liquidity_position_status == "unknown":
        if not has_supplied_evidence_requirements:
            final_evidence_requirements.append(
                "Obtain position-size liquidity evidence "
                "sufficient to establish whether the modeled "
                "position can satisfy the mandate."
            )

    elif liquidity_position_status in (
        "supported",
        "not_position_sensitive",
    ):
        pass

    else:
        raise ValueError(
            "Unsupported liquidity position status: "
            f"{liquidity_position_status}"
        )

    if economics_status == "incomplete":
        if not has_supplied_evidence_requirements:
            final_evidence_requirements.append(
                "Resolve blocking return-cost evidence gaps "
                "before claiming a realistic expected return."
            )

    elif economics_status == "complete":
        pass

    else:
        raise ValueError(
            "Unsupported economics status: "
            f"{economics_status}"
        )

    final_blocking_reasons = tuple(
        dict.fromkeys(
            final_blocking_reasons
        )
    )

    final_evidence_requirements = tuple(
        dict.fromkeys(
            final_evidence_requirements
        )
    )

    if final_blocking_reasons:
        candidate_status = "blocked"
        recommendation_ready = False

    elif final_evidence_requirements:
        candidate_status = "needs_evidence"
        recommendation_ready = False

    else:
        candidate_status = (
            "recommendation_ready"
        )
        recommendation_ready = True

    return PortfolioCandidateAssessment(
        assessment_id=assessment_id,
        mandate_id=mandate_id,
        instrument_id=instrument_id,
        market_id=market_id,
        access_route_id=access_route_id,
        label=label,
        position_size_eur=position_size_eur,
        eligibility_status=eligibility_status,
        liquidity_position_status=(
            liquidity_position_status
        ),
        economics_status=economics_status,
        base_risk_unknown_dimension_count=(
            base_risk_unknown_dimension_count
        ),
        defensible_return_pct=(
            defensible_return_pct
        ),
        defensible_return_measure=(
            defensible_return_measure
        ),
        candidate_status=candidate_status,
        blocking_reasons=(
            final_blocking_reasons
        ),
        evidence_requirements=(
            final_evidence_requirements
        ),
        recommendation_ready=(
            recommendation_ready
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