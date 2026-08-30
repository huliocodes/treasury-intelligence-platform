from __future__ import annotations

from dataclasses import dataclass

from treasury_intelligence.models.portfolio_construction import (
    PortfolioAllocationLine,
)


RECOMMENDATION_STATUSES = (
    "decision_ready",
    "review_required",
)

RECOMMENDED_ACTIONS = (
    "hold_unallocated",
    "submit_for_approval",
    "needs_review",
)


@dataclass(frozen=True)
class RecommendationDecision:
    recommendation_id: str

    proposal_id: str
    mandate_id: str

    treasury_capital_eur: float

    proposal_status: str

    recommended_action: str
    recommendation_status: str

    allocated_capital_eur: float
    unallocated_capital_eur: float

    allocation_lines: tuple[
        PortfolioAllocationLine,
        ...
    ]

    requires_human_approval: bool
    requires_review: bool

    rationale: str

    notes: str | None = None

    def __post_init__(self) -> None:
        if (
            self.recommendation_status
            not in RECOMMENDATION_STATUSES
        ):
            raise ValueError(
                "Unsupported recommendation status: "
                f"{self.recommendation_status}"
            )

        if (
            self.recommended_action
            not in RECOMMENDED_ACTIONS
        ):
            raise ValueError(
                "Unsupported recommended action: "
                f"{self.recommended_action}"
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be greater than zero."
            )

        if self.allocated_capital_eur < 0:
            raise ValueError(
                "allocated_capital_eur cannot be negative."
            )

        if self.unallocated_capital_eur < 0:
            raise ValueError(
                "unallocated_capital_eur cannot be negative."
            )

        capital_difference = abs(
            (
                self.allocated_capital_eur
                + self.unallocated_capital_eur
            )
            - self.treasury_capital_eur
        )

        if capital_difference > 0.01:
            raise ValueError(
                "Allocated plus unallocated capital must "
                "equal treasury capital."
            )

        if (
            self.recommended_action
            == "hold_unallocated"
        ):
            if self.allocated_capital_eur != 0:
                raise ValueError(
                    "hold_unallocated cannot contain "
                    "allocated capital."
                )

            if self.requires_human_approval:
                raise ValueError(
                    "hold_unallocated must not require "
                    "allocation approval."
                )

            if self.requires_review:
                raise ValueError(
                    "hold_unallocated must not be marked "
                    "as requiring review."
                )

            if (
                self.recommendation_status
                != "decision_ready"
            ):
                raise ValueError(
                    "hold_unallocated must be "
                    "decision_ready."
                )

        if (
            self.recommended_action
            == "submit_for_approval"
        ):
            if self.allocated_capital_eur <= 0:
                raise ValueError(
                    "submit_for_approval requires a "
                    "positive proposed allocation."
                )

            if not self.allocation_lines:
                raise ValueError(
                    "submit_for_approval requires at "
                    "least one allocation line."
                )

            if not self.requires_human_approval:
                raise ValueError(
                    "submit_for_approval must require "
                    "human approval."
                )

            if self.requires_review:
                raise ValueError(
                    "submit_for_approval must not also "
                    "be marked as requiring review."
                )

            if (
                self.recommendation_status
                != "decision_ready"
            ):
                raise ValueError(
                    "submit_for_approval must be "
                    "decision_ready."
                )

        if (
            self.recommended_action
            == "needs_review"
        ):
            if not self.requires_review:
                raise ValueError(
                    "needs_review must be marked as "
                    "requiring review."
                )

            if self.requires_human_approval:
                raise ValueError(
                    "needs_review is not yet an "
                    "allocation approval request."
                )

            if (
                self.recommendation_status
                != "review_required"
            ):
                raise ValueError(
                    "needs_review must use "
                    "review_required status."
                )