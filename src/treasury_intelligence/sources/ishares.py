from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    MarketObservation,
    OpportunitySnapshot,
)


ERNX_INSTRUMENT = Instrument(
    instrument_id="ernx",
    provider="iShares / BlackRock",
    name="iShares € Ultrashort Bond UCITS ETF",
    instrument_type="ultrashort_ig_bond_etf",
    legal_structure="UCITS ETF",
    currency="EUR",
    yield_source="investment_grade_short_credit",
    isin="IE000RHYOR04",
    replication="physical_sampling",
    income_treatment="accumulating",
)


ERNX_MARKET = Market(
    market_id="ernx_xetra",
    instrument_id=ERNX_INSTRUMENT.instrument_id,
    venue="Xetra",
    venue_type="exchange",
    trading_currency="EUR",
    ticker="ERNX",
    settlement_cycle="T+2",
)


ERNX_IBKR_ACCESS = AccessRoute(
    access_route_id="ernx_xetra_ibkr",
    market_id=ERNX_MARKET.market_id,
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


ERNX_ACCESSIBILITY = Accessibility(
    access_route_id=ERNX_IBKR_ACCESS.access_route_id,
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


def get_ernx_snapshot() -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id="ernx_xetra_ibkr_2026-08-26",
        instrument_id=ERNX_INSTRUMENT.instrument_id,
        market_id=ERNX_MARKET.market_id,
        access_route_id=ERNX_IBKR_ACCESS.access_route_id,
        observed_date="2026-08-26",
        yield_measure="weighted_average_ytm",
        yield_value_pct=2.88,
        yield_basis=(
            "Portfolio weighted average yield to maturity; "
            "not guaranteed realized return"
        ),
        annual_fee_pct=0.09,
        duration_years=0.36,
        average_maturity_years=0.62,
        fund_aum_eur=6_131_000_000.0,
        share_class_aum_eur=2_793_000_000.0,
        holdings_count=671,
        source="iShares / BlackRock",
        source_url="https://www.ishares.com/",
        notes=(
            "Short-duration EUR investment-grade credit "
            "exposure. YTM is an observable portfolio "
            "characteristic, not APY."
        ),
    )


def get_ernx_market_observation() -> MarketObservation:
    last_price = 5.605
    daily_volume_units = 265_072

    daily_turnover_eur = (
        last_price
        * daily_volume_units
    )

    return MarketObservation(
        observation_id=(
            "ernx_xetra_2026_08_21_market_activity"
        ),
        instrument_id=ERNX_INSTRUMENT.instrument_id,
        market_id=ERNX_MARKET.market_id,
        observed_at="2026-08-21",
        observation_type=(
            "delayed_public_market_activity"
        ),
        last_price=last_price,
        daily_volume_units=daily_volume_units,
        daily_turnover_eur=daily_turnover_eur,
        source="MarketScreener",
        source_url=(
            "https://www.marketscreener.com/quote/etf/"
            "ISHARES-ULTRASHORT-BOND-U-137131876/"
        ),
        notes=(
            "Delayed Xetra market observation. Daily volume is "
            "market-activity evidence only and does not establish "
            "immediate executable depth for a proposed position."
        ),
    )