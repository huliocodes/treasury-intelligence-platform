from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExchangeTradedCashInstrument:
    provider: str
    name: str
    isin: str

    instrument_type: str
    legal_structure: str

    fund_currency: str
    trading_currency: str

    replication: str
    income_treatment: str

    benchmark_name: str
    benchmark_spread_bps: float

    annual_fee_pct: float

    fund_aum_eur: float | None

    exchange: str
    ticker: str

    access_route: str
    access_status: str

    source: str
    source_url: str


@dataclass(frozen=True)
class BenchmarkLinkedReturnEstimate:
    benchmark_rate_pct: float
    benchmark_spread_bps: float
    annual_fee_pct: float

    implied_rate_before_trading_costs_pct: float