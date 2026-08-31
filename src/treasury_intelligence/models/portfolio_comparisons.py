from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioComparisonSide:
    construction_id: str

    allocated_capital_eur: float
    unallocated_capital_eur: float

    position_count: int
    largest_position_pct: float

    annual_return_pct: float
    annual_return_eur: float

    def __post_init__(self) -> None:
        if not self.construction_id:
            raise ValueError(
                "construction_id is required."
            )

        if self.allocated_capital_eur <= 0:
            raise ValueError(
                "allocated_capital_eur must be greater "
                "than zero."
            )

        if self.unallocated_capital_eur < 0:
            raise ValueError(
                "unallocated_capital_eur cannot be "
                "negative."
            )

        if self.position_count <= 0:
            raise ValueError(
                "position_count must be greater than zero."
            )

        if (
            self.largest_position_pct <= 0
            or self.largest_position_pct > 100
        ):
            raise ValueError(
                "largest_position_pct must be greater "
                "than zero and no more than 100."
            )


@dataclass(frozen=True)
class PortfolioAlternativeComparison:
    comparison_id: str
    mandate_id: str

    treasury_capital_eur: float

    selected: PortfolioComparisonSide
    alternative: PortfolioComparisonSide

    return_difference_bps: float
    annual_return_difference_eur: float

    position_count_difference: int
    largest_position_pct_difference: float

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.comparison_id:
            raise ValueError(
                "comparison_id is required."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id is required."
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be greater "
                "than zero."
            )