from __future__ import annotations

from dataclasses import dataclass


RETURN_COMPONENT_TYPES = (
    "reference_yield",
    "product_fee",
    "access_fee",
    "entry_execution_cost",
    "exit_execution_cost",
    "slippage_price_impact",
    "network_cost",
    "fx_hedging_cost",
    "operational_cost",
    "tax_cost",
    "liquidity_cost",
    "other_cost",
)


RETURN_COMPONENT_STATUSES = (
    "observed",
    "published",
    "model_derived",
    "estimated",
    "known_zero",
    "unknown",
    "not_applicable",
)


RETURN_COMPONENT_BASIS = (
    "annualized_pct",
    "position_bps",
    "fixed_eur",
)


@dataclass(frozen=True)
class ReturnComponent:
    component_id: str

    component_type: str
    label: str

    status: str
    basis: str

    value: float | None

    source: str | None = None
    source_url: str | None = None

    notes: str | None = None

    def __post_init__(self) -> None:
        if (
            self.component_type
            not in RETURN_COMPONENT_TYPES
        ):
            raise ValueError(
                "Unsupported return component type: "
                f"{self.component_type}"
            )

        if (
            self.status
            not in RETURN_COMPONENT_STATUSES
        ):
            raise ValueError(
                "Unsupported return component status: "
                f"{self.status}"
            )

        if self.basis not in RETURN_COMPONENT_BASIS:
            raise ValueError(
                "Unsupported return component basis: "
                f"{self.basis}"
            )

        if (
            self.status
            in (
                "unknown",
                "not_applicable",
            )
            and self.value is not None
        ):
            raise ValueError(
                "unknown or not_applicable components "
                "must not contain a value."
            )

        if (
            self.status
            not in (
                "unknown",
                "not_applicable",
            )
            and self.value is None
        ):
            raise ValueError(
                "Known return components require a value."
            )

        if (
            self.value is not None
            and self.value < 0
        ):
            raise ValueError(
                "Return component values cannot be negative."
            )


@dataclass(frozen=True)
class ReturnAnalysis:
    analysis_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float
    holding_period_days: int

    reference_yield_pct: float | None

    known_recurring_annualized_cost_pct: float

    known_one_time_cost_eur: float
    known_one_time_cost_bps: float

    known_one_time_cost_annualized_pct: float

    known_total_annualized_cost_pct: float

    return_after_known_costs_pct: float | None

    realistic_expected_return_pct: float | None

    economics_complete: bool

    unknown_cost_component_count: int

    components: tuple[ReturnComponent, ...]

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.position_size_eur <= 0:
            raise ValueError(
                "position_size_eur must be greater than zero."
            )

        if self.holding_period_days <= 0:
            raise ValueError(
                "holding_period_days must be greater than zero."
            )

        if (
            self.known_recurring_annualized_cost_pct
            < 0
        ):
            raise ValueError(
                "known recurring annualized cost cannot "
                "be negative."
            )

        if self.known_one_time_cost_eur < 0:
            raise ValueError(
                "known one-time cost EUR cannot be negative."
            )

        if self.known_one_time_cost_bps < 0:
            raise ValueError(
                "known one-time cost bps cannot be negative."
            )

        if (
            self.known_one_time_cost_annualized_pct
            < 0
        ):
            raise ValueError(
                "annualized one-time cost cannot be negative."
            )

        if (
            self.known_total_annualized_cost_pct
            < 0
        ):
            raise ValueError(
                "known total annualized cost cannot be negative."
            )

        if self.unknown_cost_component_count < 0:
            raise ValueError(
                "unknown cost component count cannot "
                "be negative."
            )

        if (
            self.economics_complete
            and self.realistic_expected_return_pct is None
        ):
            raise ValueError(
                "Complete economics require a realistic "
                "expected return."
            )

        if (
            not self.economics_complete
            and self.realistic_expected_return_pct
            is not None
        ):
            raise ValueError(
                "Incomplete economics must not present a "
                "realistic expected return as known."
            )