from __future__ import annotations

from treasury_intelligence.models.allocation_deltas import (
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.economic_comparisons import (
    TreasuryEconomicComparison,
)

from treasury_intelligence.models.monthly_reviews import (
    MonthlyReviewReport,
)

from treasury_intelligence.models.portfolio_proposals import (
    PortfolioProposal,
)

from treasury_intelligence.models.rebalance import (
    RebalanceDecision,
)

from treasury_intelligence.models.switching_friction import (
    SwitchingFrictionAssessment,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryState,
)


def _deduplicate(
    values: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        dict.fromkeys(
            values
        )
    )


def build_monthly_review_report(
    review_id: str,
    state: TreasuryState,
    proposal: PortfolioProposal,
    delta: TreasuryAllocationDelta,
    economic_comparison: TreasuryEconomicComparison,
    switching_friction: SwitchingFrictionAssessment,
    rebalance_decision: RebalanceDecision,
    notes: str | None = None,
) -> MonthlyReviewReport:
    mandate_ids = {
        state.mandate_id,
        proposal.mandate_id,
        delta.mandate_id,
        economic_comparison.mandate_id,
        switching_friction.mandate_id,
        rebalance_decision.mandate_id,
    }

    if len(mandate_ids) != 1:
        raise ValueError(
            "All monthly review components must use "
            "the same mandate."
        )

    if delta.state_id != state.state_id:
        raise ValueError(
            "Allocation delta does not belong to the "
            "supplied treasury state."
        )

    if delta.proposal_id != proposal.proposal_id:
        raise ValueError(
            "Allocation delta does not belong to the "
            "supplied portfolio proposal."
        )

    if (
        economic_comparison.state_id
        != state.state_id
    ):
        raise ValueError(
            "Economic comparison does not belong to "
            "the supplied treasury state."
        )

    if (
        economic_comparison.proposal_id
        != proposal.proposal_id
    ):
        raise ValueError(
            "Economic comparison does not belong to "
            "the supplied portfolio proposal."
        )

    if (
        economic_comparison.delta_id
        != delta.delta_id
    ):
        raise ValueError(
            "Economic comparison does not belong to "
            "the supplied allocation delta."
        )

    if (
        switching_friction.delta_id
        != delta.delta_id
    ):
        raise ValueError(
            "Switching friction does not belong to "
            "the supplied allocation delta."
        )

    if (
        switching_friction.economic_comparison_id
        != economic_comparison.comparison_id
    ):
        raise ValueError(
            "Switching friction does not belong to "
            "the supplied economic comparison."
        )

    if (
        rebalance_decision.delta_id
        != delta.delta_id
    ):
        raise ValueError(
            "Rebalance decision does not belong to "
            "the supplied allocation delta."
        )

    if (
        rebalance_decision.economic_comparison_id
        != economic_comparison.comparison_id
    ):
        raise ValueError(
            "Rebalance decision does not belong to "
            "the supplied economic comparison."
        )

    if (
        rebalance_decision
        .switching_friction_assessment_id
        != switching_friction.assessment_id
    ):
        raise ValueError(
            "Rebalance decision does not belong to "
            "the supplied switching-friction assessment."
        )

    treasury_capital_values = (
        state.treasury_capital_eur,
        proposal.treasury_capital_eur,
        delta.treasury_capital_eur,
        economic_comparison.treasury_capital_eur,
        rebalance_decision.treasury_capital_eur,
    )

    reference_capital = (
        treasury_capital_values[0]
    )

    for value in treasury_capital_values[1:]:
        if (
            abs(
                value
                - reference_capital
            )
            > 0.01
        ):
            raise ValueError(
                "Monthly review components disagree "
                "on treasury capital."
            )

    evidence_requirements = (
        _deduplicate(
            tuple(
                rebalance_decision
                .evidence_requirements
            )
            + tuple(
                economic_comparison
                .missing_evidence
            )
            + tuple(
                switching_friction
                .missing_evidence
            )
        )
    )

    blocked_candidates = (
        _deduplicate(
            tuple(
                proposal
                .evidence_blocked_candidate_labels
            )
        )
    )

    follow_up_required = (
        bool(blocked_candidates)
        or bool(evidence_requirements)
    )

    if follow_up_required:
        review_status = (
            "follow_up_required"
        )
    else:
        review_status = "complete"

    if rebalance_decision.decision == "rebalance":
        action_summary = (
            "The proposed allocation meets the "
            "rebalance policy threshold."
        )

    elif (
        rebalance_decision.decision
        == "needs_review"
    ):
        action_summary = (
            "No defensible rebalance decision can "
            "be made until required evidence is "
            "resolved."
        )

    else:
        if delta.change_required:
            action_summary = (
                "The current allocation should be "
                "retained because the proposed change "
                "does not justify rebalancing under "
                "the current policy."
            )
        else:
            action_summary = (
                "The current allocation should be "
                "retained because no portfolio change "
                "is currently proposed."
            )

    if follow_up_required:
        evidence_summary = (
            " Evidence follow-up remains required "
            "before all researched opportunities can "
            "be treated as fully decision-ready."
        )
    else:
        evidence_summary = (
            " No unresolved monthly-review evidence "
            "items remain."
        )

    summary = (
        action_summary
        + evidence_summary
    )

    return MonthlyReviewReport(
        review_id=review_id,
        mandate_id=state.mandate_id,
        state_id=state.state_id,
        proposal_id=proposal.proposal_id,
        delta_id=delta.delta_id,
        economic_comparison_id=(
            economic_comparison.comparison_id
        ),
        switching_friction_assessment_id=(
            switching_friction.assessment_id
        ),
        rebalance_decision_id=(
            rebalance_decision.decision_id
        ),
        as_of=state.as_of,
        treasury_capital_eur=(
            state.treasury_capital_eur
        ),
        current_invested_capital_eur=(
            state.invested_capital_eur
        ),
        current_unallocated_capital_eur=(
            state.unallocated_capital_eur
        ),
        proposed_allocated_capital_eur=(
            proposal.allocated_capital_eur
        ),
        proposed_unallocated_capital_eur=(
            proposal.unallocated_capital_eur
        ),
        gross_position_movement_eur=(
            delta.gross_position_movement_eur
        ),
        rebalance_decision=(
            rebalance_decision.decision
        ),
        rebalance_decision_status=(
            rebalance_decision.decision_status
        ),
        first_year_net_benefit_eur=(
            rebalance_decision
            .first_year_net_benefit_eur
        ),
        first_year_net_improvement_bps_of_treasury=(
            rebalance_decision
            .first_year_net_improvement_bps_of_treasury
        ),
        review_status=review_status,
        evidence_blocked_candidate_labels=(
            blocked_candidates
        ),
        evidence_requirements=(
            evidence_requirements
        ),
        summary=summary,
        notes=notes,
    )