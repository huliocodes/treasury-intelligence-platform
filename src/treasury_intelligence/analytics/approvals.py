from __future__ import annotations

from treasury_intelligence.models.approvals import (
    ApprovalRecord,
)

from treasury_intelligence.models.recommendations import (
    RecommendationDecision,
)


def _validate_approvable_recommendation(
    recommendation: RecommendationDecision,
) -> None:
    if (
        recommendation.recommended_action
        != "submit_for_approval"
    ):
        raise ValueError(
            "Only recommendations with "
            "recommended_action='submit_for_approval' "
            "may enter the approval layer."
        )

    if (
        recommendation.recommendation_status
        != "decision_ready"
    ):
        raise ValueError(
            "Only decision-ready recommendations may "
            "enter the approval layer."
        )

    if not recommendation.requires_human_approval:
        raise ValueError(
            "Recommendation does not require human "
            "approval."
        )

    if recommendation.requires_review:
        raise ValueError(
            "A recommendation requiring review cannot "
            "enter approval."
        )

    if recommendation.allocated_capital_eur <= 0:
        raise ValueError(
            "An approvable recommendation must contain "
            "a positive proposed allocation."
        )

    if not recommendation.allocation_lines:
        raise ValueError(
            "An approvable recommendation must contain "
            "at least one allocation line."
        )


def create_pending_approval(
    approval_id: str,
    recommendation: RecommendationDecision,
    notes: str | None = None,
) -> ApprovalRecord:
    _validate_approvable_recommendation(
        recommendation
    )

    return ApprovalRecord(
        approval_id=approval_id,
        recommendation_id=(
            recommendation.recommendation_id
        ),
        mandate_id=(
            recommendation.mandate_id
        ),
        approval_status="pending",
        proposed_allocation_eur=(
            recommendation.allocated_capital_eur
        ),
        authorized_allocation_eur=0.0,
        allocation_lines=(
            recommendation.allocation_lines
        ),
        decided_by=None,
        decided_at=None,
        rationale=None,
        notes=notes,
    )


def approve_recommendation(
    approval_id: str,
    recommendation: RecommendationDecision,
    decided_by: str,
    decided_at: str,
    rationale: str | None = None,
    notes: str | None = None,
) -> ApprovalRecord:
    _validate_approvable_recommendation(
        recommendation
    )

    return ApprovalRecord(
        approval_id=approval_id,
        recommendation_id=(
            recommendation.recommendation_id
        ),
        mandate_id=(
            recommendation.mandate_id
        ),
        approval_status="approved",
        proposed_allocation_eur=(
            recommendation.allocated_capital_eur
        ),
        authorized_allocation_eur=(
            recommendation.allocated_capital_eur
        ),
        allocation_lines=(
            recommendation.allocation_lines
        ),
        decided_by=decided_by,
        decided_at=decided_at,
        rationale=rationale,
        notes=notes,
    )


def reject_recommendation(
    approval_id: str,
    recommendation: RecommendationDecision,
    decided_by: str,
    decided_at: str,
    rationale: str | None = None,
    notes: str | None = None,
) -> ApprovalRecord:
    _validate_approvable_recommendation(
        recommendation
    )

    return ApprovalRecord(
        approval_id=approval_id,
        recommendation_id=(
            recommendation.recommendation_id
        ),
        mandate_id=(
            recommendation.mandate_id
        ),
        approval_status="rejected",
        proposed_allocation_eur=(
            recommendation.allocated_capital_eur
        ),
        authorized_allocation_eur=0.0,
        allocation_lines=(
            recommendation.allocation_lines
        ),
        decided_by=decided_by,
        decided_at=decided_at,
        rationale=rationale,
        notes=notes,
    )


def execution_authorized(
    approval: ApprovalRecord,
) -> bool:
    return (
        approval.approval_status == "approved"
        and approval.authorized_allocation_eur > 0
    )