from __future__ import annotations

from dataclasses import dataclass


ECONOMIC_COMPARISON_STATUSES = (
    "complete",
    "incomplete",
)


@dataclass(frozen=True)
class AllocationReturnInput:
    instrument_id: str
    market_id: str
    access_route_id: str

    label: str

    annual_return_pct: float | None
    evidence_available: bool

    source_reference: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.instrument_id:
            raise ValueError(
                "instrument_id cannot be empty."
            )

        if not self.market_id:
            raise ValueError(
                "market_id cannot be empty."
            )

        if not self.access_route_id:
            raise ValueError(
                "access_route_id cannot be empty."
            )

        if not self.label:
            raise ValueError(
                "label cannot be empty."
            )

        if (
            self.evidence_available
            and self.annual_return_pct is None
        ):
            raise ValueError(
                "evidence_available=True requires "
                "annual_return_pct."
            )

        if (
            not self.evidence_available
            and self.annual_return_pct is not None
        ):
            raise ValueError(
                "annual_return_pct must be None when "
                "evidence_available=False."
            )


@dataclass(frozen=True)
class UnallocatedReturnInput:
    annual_return_pct: float | None
    evidence_available: bool

    source_reference: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if (
            self.evidence_available
            and self.annual_return_pct is None
        ):
            raise ValueError(
                "evidence_available=True requires "
                "annual_return_pct."
            )

        if (
            not self.evidence_available
            and self.annual_return_pct is not None
        ):
            raise ValueError(
                "annual_return_pct must be None when "
                "evidence_available=False."
            )


@dataclass(frozen=True)
class EconomicComparisonLine:
    side: str
    allocation_type: str

    label: str

    value_eur: float
    annual_return_pct: float | None
    annual_return_eur: float | None

    evidence_available: bool

    instrument_id: str | None = None
    market_id: str | None = None
    access_route_id: str | None = None

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.side not in (
            "current",
            "proposed",
        ):
            raise ValueError(
                "side must be current or proposed."
            )

        if self.allocation_type not in (
            "position",
            "unallocated",
        ):
            raise ValueError(
                "allocation_type must be position "
                "or unallocated."
            )

        if not self.label:
            raise ValueError(
                "label cannot be empty."
            )

        if self.value_eur < 0:
            raise ValueError(
                "value_eur cannot be negative."
            )

        if self.evidence_available:
            if self.annual_return_pct is None:
                raise ValueError(
                    "Available evidence requires "
                    "annual_return_pct."
                )

            if self.annual_return_eur is None:
                raise ValueError(
                    "Available evidence requires "
                    "annual_return_eur."
                )

        else:
            if self.annual_return_pct is not None:
                raise ValueError(
                    "Unavailable evidence requires "
                    "annual_return_pct=None."
                )

            if self.annual_return_eur is not None:
                raise ValueError(
                    "Unavailable evidence requires "
                    "annual_return_eur=None."
                )


@dataclass(frozen=True)
class TreasuryEconomicComparison:
    comparison_id: str

    mandate_id: str
    state_id: str
    proposal_id: str
    delta_id: str

    treasury_capital_eur: float

    comparison_status: str

    current_annual_return_eur: float | None
    proposed_annual_return_eur: float | None

    incremental_annual_benefit_eur: float | None
    incremental_annual_benefit_pct_of_treasury: (
        float | None
    )

    current_lines: tuple[
        EconomicComparisonLine,
        ...
    ]

    proposed_lines: tuple[
        EconomicComparisonLine,
        ...
    ]

    missing_evidence: tuple[
        str,
        ...
    ]

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.comparison_id:
            raise ValueError(
                "comparison_id cannot be empty."
            )

        if self.comparison_status not in (
            ECONOMIC_COMPARISON_STATUSES
        ):
            raise ValueError(
                "Unsupported economic comparison status: "
                f"{self.comparison_status}"
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be "
                "greater than zero."
            )

        if self.comparison_status == "complete":
            if self.current_annual_return_eur is None:
                raise ValueError(
                    "Complete comparison requires "
                    "current_annual_return_eur."
                )

            if self.proposed_annual_return_eur is None:
                raise ValueError(
                    "Complete comparison requires "
                    "proposed_annual_return_eur."
                )

            if (
                self.incremental_annual_benefit_eur
                is None
            ):
                raise ValueError(
                    "Complete comparison requires "
                    "incremental_annual_benefit_eur."
                )

            if (
                self.incremental_annual_benefit_pct_of_treasury
                is None
            ):
                raise ValueError(
                    "Complete comparison requires "
                    "incremental benefit percentage."
                )

            if self.missing_evidence:
                raise ValueError(
                    "Complete comparison cannot contain "
                    "missing evidence."
                )

        if self.comparison_status == "incomplete":
            if (
                self.incremental_annual_benefit_eur
                is not None
            ):
                raise ValueError(
                    "Incomplete comparison cannot expose "
                    "incremental annual benefit."
                )

            if (
                self.incremental_annual_benefit_pct_of_treasury
                is not None
            ):
                raise ValueError(
                    "Incomplete comparison cannot expose "
                    "incremental benefit percentage."
                )

            if not self.missing_evidence:
                raise ValueError(
                    "Incomplete comparison requires "
                    "missing evidence."
                )