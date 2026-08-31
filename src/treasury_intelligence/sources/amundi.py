from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    OpportunitySnapshot,
)


AMUNDI_SMART_OVERNIGHT_INSTRUMENT = Instrument(
    instrument_id="amundi_smart_overnight",
    provider="Amundi",
    name=(
        "Amundi Smart Overnight Return "
        "UCITS ETF Acc"
    ),
    instrument_type="overnight_rate_tracking_etf",
    legal_structure="UCITS ETF",
    currency="EUR",
    yield_source="euro_overnight_rates",
    isin="LU1190417599",
    replication="synthetic",
    income_treatment="accumulating",
)


AMUNDI_SMART_OVERNIGHT_MARKET = Market(
    market_id="amundi_smart_overnight_xetra",
    instrument_id=(
        AMUNDI_SMART_OVERNIGHT_INSTRUMENT.instrument_id
    ),
    venue="Xetra",
    venue_type="exchange",
    trading_currency="EUR",
    settlement_cycle="T+2",
)


AMUNDI_SMART_OVERNIGHT_IBKR_ACCESS = AccessRoute(
    access_route_id=(
        "amundi_smart_overnight_xetra_ibkr"
    ),
    market_id=(
        AMUNDI_SMART_OVERNIGHT_MARKET.market_id
    ),
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


AMUNDI_SMART_OVERNIGHT_ACCESSIBILITY = Accessibility(
    access_route_id=(
        AMUNDI_SMART_OVERNIGHT_IBKR_ACCESS
        .access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "IBKR supports Slovenian organization accounts "
        "and Xetra ETF trading. The product is modeled "
        "through the same general corporate brokerage "
        "route used for other Xetra-listed UCITS ETFs. "
        "Final account-specific product availability and "
        "trading permissions must be checked at execution."
    ),
)


AMUNDI_SMART_OVERNIGHT_ANNUAL_FEE_PCT = 0.10

AMUNDI_SMART_OVERNIGHT_FUND_AUM_EUR = (
    17_198_000_000.0
)


def build_amundi_smart_overnight_snapshot(
    estr_rate_pct: float,
    estr_reference_date: str,
) -> OpportunitySnapshot:
    implied_rate_pct = (
        estr_rate_pct
        - AMUNDI_SMART_OVERNIGHT_ANNUAL_FEE_PCT
    )

    return OpportunitySnapshot(
        snapshot_id=(
            "amundi_smart_overnight_xetra_ibkr_"
            f"{estr_reference_date}"
        ),
        instrument_id=(
            AMUNDI_SMART_OVERNIGHT_INSTRUMENT
            .instrument_id
        ),
        market_id=(
            AMUNDI_SMART_OVERNIGHT_MARKET.market_id
        ),
        access_route_id=(
            AMUNDI_SMART_OVERNIGHT_IBKR_ACCESS
            .access_route_id
        ),
        observed_date=estr_reference_date,
        yield_measure="benchmark_linked_estimate",
        yield_value_pct=implied_rate_pct,
        yield_basis=(
            "Capitalized €STR less annual fund fee; "
            "before trading costs and tracking "
            "differences"
        ),
        annual_fee_pct=(
            AMUNDI_SMART_OVERNIGHT_ANNUAL_FEE_PCT
        ),
        benchmark_id="estr",
        benchmark_spread_bps=0.0,
        fund_aum_eur=(
            AMUNDI_SMART_OVERNIGHT_FUND_AUM_EUR
        ),
        source="Amundi",
        source_url=(
            "https://www.amundietf.com/"
        ),
        notes=(
            "Benchmark-linked estimate only. "
            "The fund uses synthetic replication. "
            "This is not a guaranteed or executable "
            "yield, and position-size execution "
            "economics remain separate."
        ),
    )