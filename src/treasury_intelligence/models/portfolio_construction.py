from __future__ import annotations

from dataclasses import dataclass


PORTFOLIO_CONSTRUCTION_STATUSES = (
    "no_actionable_allocation",
    "valid_allocation",
    "invalid_allocation",
)


@dataclass(frozen=True)
class AllocationInstruction:
    candidate_assessment_id: str
    allocation_eur: float

    def __post_init__(self) -> None:
        if self.allocation_eur <= 0:
            raise ValueError(
                "allocation_eur must be greater than zero."
            )


@dataclass(frozen=True)
class PortfolioAllocationLine:
    candidate_assessment_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    label: str

    allocation_eur: float
    allocation_pct_of_treasury: float

    candidate_position_size_eur: float


@dataclass(frozen=True)
class PortfolioConstructionAssessment:
    construction_id: str
    mandate_id: str

    treasury_capital_eur: float

    candidate_count: int
    recommendation_ready_candidate_count: int

    allocated_capital_eur: float
    unallocated_capital_eur: float

    allocation_lines: tuple[
        PortfolioAllocationLine,
        ...
    ]

    construction_status: str

    validation_issues: tuple[
        str,
        ...
    ]

    notes: str | None = None

    def __post_init__(self) -> None:
        if (
            self.construction_status
            not in PORTFOLIO_CONSTRUCTION_STATUSES
        ):
            raise ValueError(
                "Unsupported portfolio construction status: "
                f"{self.construction_status}"
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
            self.construction_status
            == "no_actionable_allocation"
            and self.allocated_capital_eur != 0
        ):
            raise ValueError(
                "no_actionable_allocation cannot contain "
                "allocated capital."
            )

        if (
            self.construction_status
            == "valid_allocation"
            and self.validation_issues
        ):
            raise ValueError(
                "A valid allocation cannot contain "
                "validation issues."
            )

        if (
            self.construction_status
            == "invalid_allocation"
            and not self.validation_issues
        ):
            raise ValueError(
                "An invalid allocation must contain at "
                "least one validation issue."
            )