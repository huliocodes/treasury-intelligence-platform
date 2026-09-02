from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    MarketObservation,
    OpportunitySnapshot,
)


FRANKLIN_EURO_SHORT_MATURITY_INSTRUMENT = Instrument(
    instrument_id="franklin_euro_short_maturity",
    provider="Franklin Templeton",
    name="Franklin Euro Short Maturity UCITS ETF",
    instrument_type="short_duration_ig_bond_etf",
    legal_structure="Irish UCITS ETF",
    currency="EUR",
    yield_source=(
        "short_maturity_eur_government_and_corporate_bonds"
    ),
    fx_exposure_currency="EUR",
    isin="IE000STIHQB2",
    replication="active_physical_portfolio",
    income_treatment="accumulating",
)


FRANKLIN_EURO_SHORT_MATURITY_MARKET = Market(
    market_id="franklin_euro_short_maturity_xetra",
    instrument_id=(
        FRANKLIN_EURO_SHORT_MATURITY_INSTRUMENT.instrument_id
    ),
    venue="Xetra",
    venue_type="exchange",
    trading_currency="EUR",
    ticker="FVSA",
    settlement_cycle="T+2",
)


FRANKLIN_EURO_SHORT_MATURITY_IBKR_ACCESS = AccessRoute(
    access_route_id=(
        "franklin_euro_short_maturity_xetra_ibkr"
    ),
    market_id=(
        FRANKLIN_EURO_SHORT_MATURITY_MARKET.market_id
    ),
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


FRANKLIN_EURO_SHORT_MATURITY_ACCESSIBILITY = Accessibility(
    access_route_id=(
        FRANKLIN_EURO_SHORT_MATURITY_IBKR_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "The exact accumulating UCITS ETF share class "
        "IE000STIHQB2 is listed on Xetra in EUR as FVSA. "
        "The existing V1 IBKR route supports Slovenian "
        "organization accounts and Xetra ETF trading. "
        "Account-specific permissions remain an "
        "execution-stage operational check."
    ),
)


FRANKLIN_EURO_SHORT_MATURITY_AUM_EUR = (
    597_730_000.0
)


def get_franklin_euro_short_maturity_snapshot(
) -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id=(
            "franklin_euro_short_maturity_"
            "xetra_ibkr_2026-08-31"
        ),
        instrument_id=(
            FRANKLIN_EURO_SHORT_MATURITY_INSTRUMENT.instrument_id
        ),
        market_id=(
            FRANKLIN_EURO_SHORT_MATURITY_MARKET.market_id
        ),
        access_route_id=(
            FRANKLIN_EURO_SHORT_MATURITY_IBKR_ACCESS.access_route_id
        ),
        observed_date="2026-08-31",
        yield_measure="portfolio_yield_to_maturity",
        yield_value_pct=2.78,
        yield_basis=(
            "Franklin Templeton published portfolio yield "
            "to maturity separately from the fund's 0.15% "
            "total expense ratio. YTM is an observable "
            "portfolio characteristic and is not a "
            "guaranteed realized investor return."
        ),
        annual_fee_pct=0.15,
        duration_years=0.76,
        average_maturity_years=1.15,
        fund_aum_eur=(
            FRANKLIN_EURO_SHORT_MATURITY_AUM_EUR
        ),
        share_class_aum_eur=(
            FRANKLIN_EURO_SHORT_MATURITY_AUM_EUR
        ),
        holdings_count=80,
        source="Franklin Templeton",
        source_url=(
            "https://www.franklintempleton.lu/"
            "our-funds/price-and-performance-etfs/"
            "products/27049/ETA/"
            "franklin-euro-short-maturity-ucits-etf/"
            "IE000STIHQB2"
        ),
        notes=(
            "As of 31 Aug 2026 Franklin reported fund AUM "
            "of approximately EUR 597.73 million. Portfolio "
            "characteristics reported around 27 Aug 2026 "
            "included 2.78% YTM, 2.73% YTW, 0.76-year "
            "effective duration, 1.15-year weighted average "
            "maturity, AA- average credit quality and "
            "80 holdings. The model treats published YTM "
            "as pre-product-fee because the 0.15% TER is "
            "published separately."
        ),
    )


def get_franklin_euro_short_maturity_market_observation(
) -> MarketObservation:
    return MarketObservation(
        observation_id=(
            "franklin_fvsa_xetra_2026_09_02_listing"
        ),
        instrument_id=(
            FRANKLIN_EURO_SHORT_MATURITY_INSTRUMENT.instrument_id
        ),
        market_id=(
            FRANKLIN_EURO_SHORT_MATURITY_MARKET.market_id
        ),
        observed_at="2026-09-02",
        observation_type=(
            "verified_exchange_market_structure"
        ),
        source="Deutsche Börse / Xetra",
        source_url=(
            "https://live.deutsche-boerse.com/en/etf/"
            "franklin-euro-short-maturity-ucits-etf-acc"
        ),
        notes=(
            "Deutsche Börse identifies exact ISIN "
            "IE000STIHQB2 as Franklin Euro Short Maturity "
            "UCITS ETF (Acc), ticker FVSA, trading on Xetra "
            "in EUR. This verifies secondary-market venue "
            "and ETF market structure but does not provide "
            "position-size executable depth or observed "
            "daily turnover. The generic ETF position "
            "analysis must therefore rely on product scale "
            "only within its existing conservative threshold."
        ),
    )
