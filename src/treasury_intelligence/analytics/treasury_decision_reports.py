from __future__ import annotations

from treasury_intelligence.analytics.approvals import (
    execution_authorized,
)

from treasury_intelligence.models.approvals import (
    ApprovalRecord,
)

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.portfolio_construction import (
    PortfolioConstructionAssessment,
)

from treasury_intelligence.models.recommendations import (
    RecommendationDecision,
)

from treasury_intelligence.models.treasury_decision_reports import (
    TreasuryDecisionReport,
    TreasuryUniverseSummary,
)


CAPITAL_TOLERANCE_EUR = 0.01


def build_treasury_universe_summary(
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> TreasuryUniverseSummary:
    ready = tuple(
        candidate.label
        for candidate in candidates
        if (
            candidate.candidate_status
            == "recommendation_ready"
        )
    )

    needs_evidence = tuple(
        candidate.label
        for candidate in candidates
        if (
            candidate.candidate_status
            == "needs_evidence"
        )
    )

    blocked = tuple(
        candidate.label
        for candidate in candidates
        if candidate.candidate_status == "blocked"
    )

    classified_count = (
        len(ready)
        + len(needs_evidence)
        + len(blocked)
    )

    if classified_count != len(candidates):
        raise ValueError(
            "Every universe candidate must have a "
            "recognized candidate status."
        )

    return TreasuryUniverseSummary(
        opportunity_count=len(candidates),
        recommendation_ready_count=len(ready),
        needs_evidence_count=len(needs_evidence),
        blocked_count=len(blocked),
        recommendation_ready_labels=ready,
        needs_evidence_labels=needs_evidence,
        blocked_labels=blocked,
    )


def _index_candidates(
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> dict[
    str,
    PortfolioCandidateAssessment,
]:
    indexed = {}

    for candidate in candidates:
        if candidate.assessment_id in indexed:
            raise ValueError(
                "Duplicate portfolio candidate assessment "
                f"ID: {candidate.assessment_id}"
            )

        indexed[candidate.assessment_id] = candidate

    return indexed


def _portfolio_return(
    construction: PortfolioConstructionAssessment,
    allocation_candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> tuple[
    float | None,
    float | None,
]:
    if construction.allocated_capital_eur <= 0:
        return (
            None,
            None,
        )

    indexed = _index_candidates(
        allocation_candidates
    )

    annual_return_eur = 0.0

    for line in construction.allocation_lines:
        candidate = indexed.get(
            line.candidate_assessment_id
        )

        if candidate is None:
            raise ValueError(
                "Allocation line references a candidate "
                "not supplied for portfolio return "
                "calculation."
            )

        if not candidate.recommendation_ready:
            raise ValueError(
                f"{candidate.label}: allocated candidate "
                "is not recommendation-ready."
            )

        if candidate.defensible_return_pct is None:
            raise ValueError(
                f"{candidate.label}: allocated candidate "
                "has no defensible return."
            )

        if (
            abs(
                candidate.position_size_eur
                - line.allocation_eur
            )
            > CAPITAL_TOLERANCE_EUR
        ):
            raise ValueError(
                f"{candidate.label}: allocated capital "
                "does not match analyzed candidate "
                "position size."
            )

        annual_return_eur += (
            line.allocation_eur
            * candidate.defensible_return_pct
            / 100.0
        )

    portfolio_return_pct = (
        annual_return_eur
        / construction.allocated_capital_eur
        * 100.0
    )

    return (
        portfolio_return_pct,
        annual_return_eur,
    )


def _validate_alignment(
    mandate: TreasuryMandate,
    construction: PortfolioConstructionAssessment,
    recommendation: RecommendationDecision,
    approval: ApprovalRecord | None,
) -> None:
    if (
        construction.mandate_id
        != mandate.mandate_id
    ):
        raise ValueError(
            "Portfolio construction mandate does not "
            "match report mandate."
        )

    if (
        recommendation.mandate_id
        != mandate.mandate_id
    ):
        raise ValueError(
            "Recommendation mandate does not match "
            "report mandate."
        )

    if (
        recommendation.treasury_capital_eur
        != mandate.treasury_capital_eur
    ):
        raise ValueError(
            "Recommendation treasury capital does not "
            "match report mandate."
        )

    if (
        construction.treasury_capital_eur
        != mandate.treasury_capital_eur
    ):
        raise ValueError(
            "Construction treasury capital does not "
            "match report mandate."
        )

    if (
        abs(
            recommendation.allocated_capital_eur
            - construction.allocated_capital_eur
        )
        > CAPITAL_TOLERANCE_EUR
    ):
        raise ValueError(
            "Recommendation allocated capital does not "
            "match portfolio construction."
        )

    if (
        recommendation.allocation_lines
        != construction.allocation_lines
    ):
        raise ValueError(
            "Recommendation allocation lines do not "
            "match portfolio construction."
        )

    if approval is not None:
        if (
            approval.recommendation_id
            != recommendation.recommendation_id
        ):
            raise ValueError(
                "Approval does not belong to the supplied "
                "recommendation."
            )

        if approval.mandate_id != mandate.mandate_id:
            raise ValueError(
                "Approval mandate does not match report "
                "mandate."
            )

        if (
            approval.allocation_lines
            != recommendation.allocation_lines
        ):
            raise ValueError(
                "Approval allocation lines do not match "
                "the recommendation."
            )


def build_treasury_decision_report(
    *,
    report_id: str,
    mandate: TreasuryMandate,
    universe_candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
    construction: PortfolioConstructionAssessment,
    allocation_candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
    recommendation: RecommendationDecision,
    approval: ApprovalRecord | None = None,
    notes: str | None = None,
) -> TreasuryDecisionReport:
    if not report_id:
        raise ValueError(
            "report_id is required."
        )

    _validate_alignment(
        mandate=mandate,
        construction=construction,
        recommendation=recommendation,
        approval=approval,
    )

    universe = build_treasury_universe_summary(
        universe_candidates
    )

    (
        portfolio_return_pct,
        annual_return_eur,
    ) = _portfolio_return(
        construction=construction,
        allocation_candidates=allocation_candidates,
    )

    target_yield_gap_pct = None
    target_yield_gap_eur = None

    if (
        mandate.target_yield_pct is not None
        and portfolio_return_pct is not None
    ):
        target_yield_gap_pct = (
            mandate.target_yield_pct
            - portfolio_return_pct
        )

        target_yield_gap_eur = (
            mandate.treasury_capital_eur
            * target_yield_gap_pct
            / 100.0
        )

    approval_status = (
        approval.approval_status
        if approval is not None
        else None
    )

    authorized_allocation_eur = (
        approval.authorized_allocation_eur
        if approval is not None
        else 0.0
    )

    is_execution_authorized = (
        execution_authorized(approval)
        if approval is not None
        else False
    )

    report_status = (
        "review_required"
        if recommendation.requires_review
        else "decision_ready"
    )

    return TreasuryDecisionReport(
        report_id=report_id,
        mandate_id=mandate.mandate_id,
        mandate_name=mandate.name,
        treasury_capital_eur=(
            mandate.treasury_capital_eur
        ),
        target_yield_pct=(
            mandate.target_yield_pct
        ),
        target_yield_is_hard_constraint=(
            mandate.target_yield_is_hard_constraint
        ),
        universe=universe,
        allocated_capital_eur=(
            construction.allocated_capital_eur
        ),
        unallocated_capital_eur=(
            construction.unallocated_capital_eur
        ),
        allocation_lines=(
            construction.allocation_lines
        ),
        portfolio_defensible_return_pct=(
            portfolio_return_pct
        ),
        portfolio_annual_return_eur=(
            annual_return_eur
        ),
        target_yield_gap_pct=(
            target_yield_gap_pct
        ),
        target_yield_gap_eur=(
            target_yield_gap_eur
        ),
        recommended_action=(
            recommendation.recommended_action
        ),
        recommendation_status=(
            recommendation.recommendation_status
        ),
        approval_status=approval_status,
        authorized_allocation_eur=(
            authorized_allocation_eur
        ),
        execution_authorized=(
            is_execution_authorized
        ),
        report_status=report_status,
        rationale=(
            recommendation.rationale
        ),
        notes=notes,
    )