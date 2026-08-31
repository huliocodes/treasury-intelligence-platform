from __future__ import annotations

from dataclasses import dataclass

from treasury_intelligence.models.portfolio_construction import (
    PortfolioAllocationLine,
)


TREASURY_DECISION_REPORT_STATUSES = (
    "decision_ready",
    "review_required",
)


@dataclass(frozen=True)
class TreasuryUniverseSummary:
    opportunity_count: int

    recommendation_ready_count: int
    needs_evidence_count: int
    blocked_count: int

    recommendation_ready_labels: tuple[
        str,
        ...
    ]

    needs_evidence_labels: tuple[
        str,
        ...
    ]

    blocked_labels: tuple[
        str,
        ...
    ]

    def __post_init__(self) -> None:
        counts = (
            self.recommendation_ready_count
            + self.needs_evidence_count
            + self.blocked_count
        )

        if self.opportunity_count < 0:
            raise ValueError(
                "opportunity_count cannot be negative."
            )

        if counts != self.opportunity_count:
            raise ValueError(
                "Universe status counts must sum to "
                "opportunity_count."
            )

        if (
            len(self.recommendation_ready_labels)
            != self.recommendation_ready_count
        ):
            raise ValueError(
                "recommendation_ready_labels count does "
                "not match recommendation_ready_count."
            )

        if (
            len(self.needs_evidence_labels)
            != self.needs_evidence_count
        ):
            raise ValueError(
                "needs_evidence_labels count does not "
                "match needs_evidence_count."
            )

        if (
            len(self.blocked_labels)
            != self.blocked_count
        ):
            raise ValueError(
                "blocked_labels count does not match "
                "blocked_count."
            )


@dataclass(frozen=True)
class TreasuryDecisionReport:
    report_id: str

    mandate_id: str
    mandate_name: str

    treasury_capital_eur: float

    target_yield_pct: float | None
    target_yield_is_hard_constraint: bool

    universe: TreasuryUniverseSummary

    allocated_capital_eur: float
    unallocated_capital_eur: float

    allocation_lines: tuple[
        PortfolioAllocationLine,
        ...
    ]

    portfolio_defensible_return_pct: float | None
    portfolio_annual_return_eur: float | None

    target_yield_gap_pct: float | None
    target_yield_gap_eur: float | None

    recommended_action: str
    recommendation_status: str

    approval_status: str | None
    authorized_allocation_eur: float

    execution_authorized: bool

    report_status: str

    rationale: str

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.report_id:
            raise ValueError(
                "report_id is required."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id is required."
            )

        if not self.mandate_name:
            raise ValueError(
                "mandate_name is required."
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be greater "
                "than zero."
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
            self.report_status
            not in TREASURY_DECISION_REPORT_STATUSES
        ):
            raise ValueError(
                "Unsupported treasury decision report "
                f"status: {self.report_status}"
            )

        if self.authorized_allocation_eur < 0:
            raise ValueError(
                "authorized_allocation_eur cannot be "
                "negative."
            )

        if (
            self.authorized_allocation_eur
            > self.allocated_capital_eur + 0.01
        ):
            raise ValueError(
                "Authorized allocation cannot exceed "
                "proposed allocated capital."
            )

        if (
            self.execution_authorized
            and self.approval_status != "approved"
        ):
            raise ValueError(
                "Execution cannot be authorized without "
                "approved status."
            )

        if (
            self.execution_authorized
            and abs(
                self.authorized_allocation_eur
                - self.allocated_capital_eur
            )
            > 0.01
        ):
            raise ValueError(
                "Execution authorization must cover the "
                "exact proposed allocation."
            )

        if self.portfolio_defensible_return_pct is None:
            if self.portfolio_annual_return_eur is not None:
                raise ValueError(
                    "Portfolio annual return EUR requires "
                    "a defensible return percentage."
                )
        else:
            if self.portfolio_annual_return_eur is None:
                raise ValueError(
                    "Defensible portfolio return requires "
                    "portfolio annual return EUR."
                )

        if self.target_yield_pct is None:
            if self.target_yield_gap_pct is not None:
                raise ValueError(
                    "Target yield gap cannot exist without "
                    "a target yield."
                )

            if self.target_yield_gap_eur is not None:
                raise ValueError(
                    "Target yield gap EUR cannot exist "
                    "without a target yield."
                )