from __future__ import annotations

from treasury_intelligence.sources.etfs import (
    BenchmarkLinkedReturnEstimate,
    ExchangeTradedCashInstrument,
)


XEON_SOURCE_URL = (
    "https://etf.dws.com/"
)


XEON = ExchangeTradedCashInstrument(
    provider="Xtrackers by DWS",
    name=(
        "Xtrackers II EUR Overnight Rate Swap "
        "UCITS ETF 1C"
    ),
    isin="LU0290358497",
    instrument_type="overnight_rate_tracking_etf",
    legal_structure="UCITS ETF",
    fund_currency="EUR",
    trading_currency="EUR",
    replication="synthetic_swap",
    income_treatment="capitalizing",
    benchmark_name=(
        "Solactive €STR +8.5 Daily Total Return Index"
    ),
    benchmark_spread_bps=8.5,
    annual_fee_pct=0.10,
    fund_aum_eur=22_210_000_000.0,
    exchange="Xetra",
    ticker="XEON",
    access_route="Interactive Brokers / Xetra",
    access_status="supported_route",
    source="Xtrackers by DWS",
    source_url=XEON_SOURCE_URL,
)


def estimate_xeon_rate(
    estr_rate_pct: float,
) -> BenchmarkLinkedReturnEstimate:
    """
    Estimate XEON's benchmark-linked annual rate before
    brokerage commissions, bid/ask spread, slippage,
    taxes and tracking differences.

    This is not a guaranteed or executable ETF yield.
    """

    benchmark_spread_pct = (
        XEON.benchmark_spread_bps / 100
    )

    implied_rate = (
        estr_rate_pct
        + benchmark_spread_pct
        - XEON.annual_fee_pct
    )

    return BenchmarkLinkedReturnEstimate(
        benchmark_rate_pct=estr_rate_pct,
        benchmark_spread_bps=(
            XEON.benchmark_spread_bps
        ),
        annual_fee_pct=XEON.annual_fee_pct,
        implied_rate_before_trading_costs_pct=(
            implied_rate
        ),
    )