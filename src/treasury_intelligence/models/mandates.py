from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TreasuryMandate:
    mandate_id: str
    name: str

    base_currency: str
    treasury_capital_eur: float

    minimum_useful_allocation_eur: float
    maximum_single_position_pct: float

    target_yield_pct: float | None
    target_yield_is_hard_constraint: bool

    capital_preservation_priority: str
    liquidity_requirement: str

    allowed_currencies: tuple[str, ...]
    maximum_unhedged_fx_exposure_pct: float

    minimum_immediate_liquidity_coverage_pct: float | None
    maximum_settlement_days: int | None

    allowed_instrument_types: tuple[str, ...] | None

    require_verified_corporate_access: bool
    allowed_accessibility_statuses: tuple[str, ...]

    review_frequency_days: int

    notes: str | None = None