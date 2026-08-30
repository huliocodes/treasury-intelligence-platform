from __future__ import annotations

from treasury_intelligence.models.portfolio_proposals import (
    PortfolioProposal,
)

from treasury_intelligence.models.recommendations import (
    RecommendationDecision,
)


def _recommendation_state(
    proposal: PortfolioProposal,
) -> tuple[
    str,
    str,
    bool,
    bool,
    str,
]:
    if (
        proposal.proposal_status
        == "no_actionable_allocation"
    ):
        return (
            "hold_unallocated",
            "decision_ready",
            False,
            False,
            (
                "No candidate is recommendation-ready. "
                "No capital should be moved based on the "
                "current evidence."
            ),
        )

    if (
        proposal.proposal_status
        == "no_allocation_proposed"
    ):
        return (
            "needs_review",
            "review_required",
            False,
            True,
            (
                "Recommendation-ready candidates exist, "
                "but no allocation has been proposed. "
                "The treasury proposal requires review "
                "before an action recommendation can be "
                "made."
            ),
        )

    if (
        proposal.proposal_status
        == "allocation_proposed"
    ):
        return (
            "submit_for_approval",
            "decision_ready",
            True,
            False,
            (
                "A positive allocation has passed the "
                "portfolio construction policy. The "
                "proposal may proceed to human approval, "
                "but it is not approved for execution yet."
            ),
        )

    raise ValueError(
        "Unsupported portfolio proposal status: "
        f"{proposal.proposal_status}"
    )


def build_recommendation_decision(
    recommendation_id: str,
    proposal: PortfolioProposal,
    notes: str | None = None,
) -> RecommendationDecision:
    (
        recommended_action,
        recommendation_status,
        requires_human_approval,
        requires_review,
        rationale,
    ) = _recommendation_state(
        proposal
    )

    return RecommendationDecision(
        recommendation_id=(
            recommendation_id
        ),
        proposal_id=(
            proposal.proposal_id
        ),
        mandate_id=(
            proposal.mandate_id
        ),
        treasury_capital_eur=(
            proposal.treasury_capital_eur
        ),
        proposal_status=(
            proposal.proposal_status
        ),
        recommended_action=(
            recommended_action
        ),
        recommendation_status=(
            recommendation_status
        ),
        allocated_capital_eur=(
            proposal.allocated_capital_eur
        ),
        unallocated_capital_eur=(
            proposal.unallocated_capital_eur
        ),
        allocation_lines=(
            proposal.allocation_lines
        ),
        requires_human_approval=(
            requires_human_approval
        ),
        requires_review=(
            requires_review
        ),
        rationale=rationale,
        notes=notes,
    )