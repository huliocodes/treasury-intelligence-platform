from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    instrument_id: str

    provider: str
    name: str
    instrument_type: str
    legal_structure: str

    currency: str
    yield_source: str

    fx_exposure_currency: str | None = None

    issuer: str | None = None

    isin: str | None = None
    contract_address: str | None = None

    maturity_date: str | None = None
    coupon_type: str | None = None

    replication: str | None = None
    income_treatment: str | None = None


@dataclass(frozen=True)
class Market:
    market_id: str
    instrument_id: str

    venue: str
    venue_type: str

    trading_currency: str

    ticker: str | None = None
    settlement_cycle: str | None = None


@dataclass(frozen=True)
class AccessRoute:
    access_route_id: str
    market_id: str

    provider: str
    route_type: str

    investor_type: str
    jurisdiction: str


@dataclass(frozen=True)
class Accessibility:
    access_route_id: str

    entity_type: str
    jurisdiction: str

    technical_access: str
    corporate_operational_access: str

    status: str
    evidence_level: str

    notes: str | None = None


@dataclass(frozen=True)
class OpportunitySnapshot:
    snapshot_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    observed_date: str

    yield_measure: str
    yield_value_pct: float

    yield_basis: str

    annual_fee_pct: float | None = None

    benchmark_id: str | None = None
    benchmark_spread_bps: float | None = None

    duration_years: float | None = None
    average_maturity_years: float | None = None

    fund_aum_eur: float | None = None
    share_class_aum_eur: float | None = None

    outstanding_amount_eur: float | None = None

    holdings_count: int | None = None

    price_status: str | None = None
    quote_firmness: str | None = None

    early_exit_possible: bool | None = None

    source: str | None = None
    source_url: str | None = None

    notes: str | None = None
    

@dataclass(frozen=True)
class MarketObservation:
    observation_id: str

    instrument_id: str
    market_id: str

    observed_at: str
    observation_type: str

    price_pct_of_par: float | None = None
    last_price: float | None = None

    bid_price: float | None = None
    ask_price: float | None = None

    bid_size: float | None = None
    ask_size: float | None = None

    daily_volume_units: float | None = None
    daily_turnover_eur: float | None = None

    yield_pct: float | None = None
    yield_measure: str | None = None

    source: str | None = None
    source_url: str | None = None

    notes: str | None = None


@dataclass(frozen=True)
class PositionAnalysis:
    analysis_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float

    entry_supported: bool | None
    immediate_exit_supported: bool | None

    remaining_entry_capacity_eur: float | None = None
    immediate_exit_coverage_pct: float | None = None

    position_pct_of_market: float | None = None
    position_pct_reference: str | None = None

    observed_daily_turnover_eur: float | None = None
    position_pct_of_daily_turnover: float | None = None

    liquidity_evidence_level: str | None = None

    reference_yield_pct: float | None = None
    executable_yield_pct: float | None = None
    position_adjusted_yield_pct: float | None = None

    executable_economics_known: bool = False

    rejection_reason: str | None = None
    notes: str | None = None