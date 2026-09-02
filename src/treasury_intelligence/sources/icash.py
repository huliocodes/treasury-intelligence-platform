from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    MarketObservation,
    OpportunitySnapshot,
)


ICASH_INSTRUMENT = Instrument(
    instrument_id="icash",
    provider="InterCapital Asset Management",
    name="InterCapital Euro Money Market UCITS ETF",
    instrument_type="euro_money_market_etf",
    legal_structure="Croatian UCITS ETF",
    currency="EUR",
    yield_source="euro_money_market_portfolio",
    isin="HRICAMFEUMM1",
    replication="actively_managed",
    income_treatment="accumulating",
)


ICASH_MARKET = Market(
    market_id="icash_ljse",
    instrument_id=ICASH_INSTRUMENT.instrument_id,
    venue="Ljubljana Stock Exchange",
    venue_type="exchange",
    trading_currency="EUR",
    ticker="ICASH",
    settlement_cycle="T+2",
)


ICASH_SLOVENIAN_BROKER_ACCESS = AccessRoute(
    access_route_id="icash_ljse_slovenian_broker",
    market_id=ICASH_MARKET.market_id,
    provider="Slovenian LJSE member broker",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


ICASH_ACCESSIBILITY = Accessibility(
    access_route_id=(
        ICASH_SLOVENIAN_BROKER_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "ICASH is listed on the Ljubljana Stock Exchange. "
        "LJSE publishes authorized exchange members and "
        "Slovenian brokers including BKS and ILIRIKA publish "
        "brokerage services for legal persons or companies. "
        "This supports a practical Slovenian corporate "
        "brokerage route. Exact future account approval and "
        "entity-specific terms remain execution-stage checks."
    ),
)


def get_icash_snapshot(
    estr_rate_pct: float,
    estr_reference_date: str,
) -> OpportunitySnapshot:
    if estr_rate_pct < 0:
        raise ValueError(
            "estr_rate_pct must not be negative."
        )

    if not estr_reference_date:
        raise ValueError(
            "estr_reference_date is required."
        )

    return OpportunitySnapshot(
        snapshot_id=(
            "icash_ljse_"
            f"{estr_reference_date.replace('-', '_')}"
        ),
        instrument_id=ICASH_INSTRUMENT.instrument_id,
        market_id=ICASH_MARKET.market_id,
        access_route_id=(
            ICASH_SLOVENIAN_BROKER_ACCESS.access_route_id
        ),
        observed_date=estr_reference_date,
        yield_measure="benchmark_linked_estimate",
        yield_value_pct=estr_rate_pct,
        yield_basis=(
            "Conservative gross forward reference estimate "
            "using the latest ECB euro short-term rate "
            "(€STR) with zero assumed excess return. "
            "The fund's published annual product cost is "
            "deducted separately by the return engine."
        ),
        annual_fee_pct=0.30,
        benchmark_id="estr",
        benchmark_spread_bps=0.0,
        fund_aum_eur=36_520_000.0,
        share_class_aum_eur=36_520_000.0,
        source="ECB + InterCapital Asset Management",
        source_url=(
            "https://data-api.ecb.europa.eu/service/data"
        ),
        notes=(
            "ICASH is modeled conservatively from current "
            "€STR rather than backward-looking YTD fund "
            "performance or a stale promotional forward-yield "
            "estimate. Zero benchmark spread is assumed for "
            "V1. InterCapital reported approximately EUR "
            "36.52 million of net assets as of 31 Aug 2026. "
            "The current portfolio was predominantly short "
            "French Treasury bills with the balance primarily "
            "in bank deposits. The 0.30% annual product-cost "
            "figure is modeled separately from the gross "
            "benchmark-linked reference return."
        ),
    )


def get_icash_market_observation(
) -> MarketObservation:
    return MarketObservation(
        observation_id=(
            "icash_ljse_2026_09_02_market_structure"
        ),
        instrument_id=ICASH_INSTRUMENT.instrument_id,
        market_id=ICASH_MARKET.market_id,
        observed_at="2026-09-02",
        observation_type=(
            "verified_exchange_listing_and_market_maker"
        ),
        source="Ljubljana Stock Exchange",
        source_url=(
            "https://ljse.si/en/papir-311/310"
            "?isin=HRICAMFEUMM1"
        ),
        notes=(
            "LJSE verifies the ICASH listing and market-maker "
            "framework. The published minimum market-maker "
            "quote obligation is 30 shares and the permitted "
            "maximum spread is 5%. These terms do not prove "
            "that only 30 shares can trade, but they also do "
            "not establish position-size executable depth for "
            "large treasury exits. No larger executable depth "
            "is assumed."
        ),
    )
