from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    OpportunitySnapshot,
)


XEON_INSTRUMENT = Instrument(
    instrument_id="xeon",
    provider="Xtrackers by DWS",
    name=(
        "Xtrackers II EUR Overnight Rate Swap "
        "UCITS ETF 1C"
    ),
    instrument_type="overnight_rate_tracking_etf",
    legal_structure="UCITS ETF",
    currency="EUR",
    yield_source="euro_overnight_rates",
    isin="LU0290358497",
    replication="synthetic_swap",
    income_treatment="accumulating",
)


XEON_MARKET = Market(
    market_id="xeon_xetra",
    instrument_id=XEON_INSTRUMENT.instrument_id,
    venue="Xetra",
    venue_type="exchange",
    trading_currency="EUR",
    ticker="XEON",
    settlement_cycle="T+2",
)


XEON_IBKR_ACCESS = AccessRoute(
    access_route_id="xeon_xetra_ibkr",
    market_id=XEON_MARKET.market_id,
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


XEON_ACCESSIBILITY = Accessibility(
    access_route_id=XEON_IBKR_ACCESS.access_route_id,
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "IBKR supports Slovenian organization accounts "
        "and Xetra ETF trading. Final account-specific "
        "trading permissions must be checked at execution."
    ),
)


XEON_BENCHMARK_SPREAD_BPS = 8.5
XEON_ANNUAL_FEE_PCT = 0.10
XEON_FUND_AUM_EUR = 22_210_000_000.0


def build_xeon_snapshot(
    estr_rate_pct: float,
    estr_reference_date: str,
) -> OpportunitySnapshot:
    benchmark_spread_pct = (
        XEON_BENCHMARK_SPREAD_BPS / 100
    )

    implied_rate_pct = (
        estr_rate_pct
        + benchmark_spread_pct
        - XEON_ANNUAL_FEE_PCT
    )

    return OpportunitySnapshot(
        snapshot_id=(
            f"xeon_xetra_ibkr_{estr_reference_date}"
        ),
        instrument_id=XEON_INSTRUMENT.instrument_id,
        market_id=XEON_MARKET.market_id,
        access_route_id=XEON_IBKR_ACCESS.access_route_id,
        observed_date=estr_reference_date,
        yield_measure="benchmark_linked_estimate",
        yield_value_pct=implied_rate_pct,
        yield_basis=(
            "€STR + 8.5 bps less annual fund fee; "
            "before trading costs and tracking differences"
        ),
        annual_fee_pct=XEON_ANNUAL_FEE_PCT,
        benchmark_id="estr",
        benchmark_spread_bps=XEON_BENCHMARK_SPREAD_BPS,
        fund_aum_eur=XEON_FUND_AUM_EUR,
        source="Xtrackers by DWS",
        source_url="https://etf.dws.com/",
        notes=(
            "Estimated rate only. Not a guaranteed "
            "or executable yield."
        ),
    )