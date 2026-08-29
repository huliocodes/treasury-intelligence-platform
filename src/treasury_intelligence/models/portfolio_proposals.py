from __future__ import annotations

from dataclasses import dataclass

from treasury_intelligence.models.portfolio_construction import (
    PortfolioAllocationLine,
)


PORTFOLIO_PROPOSAL_STATUSES = (
    "no_actionable_allocation",
    "no_allocation_proposed",
    "allocation_proposed",
)

PORTFOLIO_DECISIONS = (
    "hold_unallocated",
    "propose_allocation",
)


@dataclass(frozen=True)
class PortfolioProposal:
    proposal_id: str

    mandate_id: str
    construction_id: str

    treasury_capital_eur: float

    candidate_count: int
    recommendation_ready_candidate_count: int

    allocated_capital_eur: float
    unallocated_capital_eur: float

    proposal_status: str
    decision: str

    allocation_lines: tuple[
        PortfolioAllocationLine,
        ...
    ]

    evidence_blocked_candidate_labels: tuple[
        str,
        ...
    ]

    rationale: str

    notes: str | None = None

    def __post_init__(self) -> None:
        if (
            self.proposal_status
            not in PORTFOLIO_PROPOSAL_STATUSES
        ):
            raise ValueError(
                "Unsupported portfolio proposal status: "
                f"{self.proposal_status}"
            )

        if self.decision not in PORTFOLIO_DECISIONS:
            raise ValueError(
                "Unsupported portfolio decision: "
                f"{self.decision}"
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be greater than zero."
            )

        if self.candidate_count < 0:
            raise ValueError(
                "candidate_count cannot be negative."
            )

        if (
            self.recommendation_ready_candidate_count
            < 0
        ):
            raise ValueError(
                "recommendation_ready_candidate_count "
                "cannot be negative."
            )

        if (
            self.recommendation_ready_candidate_count
            > self.candidate_count
        ):
            raise ValueError(
                "recommendation_ready_candidate_count "
                "cannot exceed candidate_count."
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
            self.proposal_status
            == "no_actionable_allocation"
        ):
            if self.recommendation_ready_candidate_count != 0:
                raise ValueError(
                    "no_actionable_allocation requires zero "
                    "recommendation-ready candidates."
                )

            if self.allocated_capital_eur != 0:
                raise ValueError(
                    "no_actionable_allocation cannot contain "
                    "allocated capital."
                )

            if self.decision != "hold_unallocated":
                raise ValueError(
                    "no_actionable_allocation must result in "
                    "hold_unallocated."
                )

        if (
            self.proposal_status
            == "no_allocation_proposed"
        ):
            if self.allocated_capital_eur != 0:
                raise ValueError(
                    "no_allocation_proposed cannot contain "
                    "allocated capital."
                )

            if self.decision != "hold_unallocated":
                raise ValueError(
                    "no_allocation_proposed must result in "
                    "hold_unallocated."
                )

        if (
            self.proposal_status
            == "allocation_proposed"
        ):
            if self.allocated_capital_eur <= 0:
                raise ValueError(
                    "allocation_proposed requires positive "
                    "allocated capital."
                )

            if self.decision != "propose_allocation":
                raise ValueError(
                    "allocation_proposed must result in "
                    "propose_allocation."
                )

            if not self.allocation_lines:
                raise ValueError(
                    "allocation_proposed requires at least "
                    "one allocation line."
                )