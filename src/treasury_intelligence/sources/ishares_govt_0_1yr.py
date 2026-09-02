from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    MarketObservation,
    OpportunitySnapshot,
)


ISHARES_GOVT_0_1YR_INSTRUMENT = Instrument(
    instrument_id="ishares_govt_bond_0_1yr",
    provider="iShares / BlackRock",
    name="iShares € Govt Bond 0-1yr UCITS ETF EUR (Acc)",
    instrument_type="short_euro_government_bond_etf",
    legal_structure="UCITS ETF",
    currency="EUR",
    yield_source="eurozone_short_sovereign_bonds",
    isin="IE000WV38GP5",
    replication="physical_sampling",
    income_treatment="accumulating",
)


ISHARES_GOVT_0_1YR_MARKET = Market(
    market_id="ishares_govt_0_1yr_xetra",
    instrument_id=(
        ISHARES_GOVT_0_1YR_INSTRUMENT.instrument_id
    ),
    venue="Xetra",
    venue_type="exchange",
    trading_currency="EUR",
    ticker="CEMK",
    settlement_cycle="T+2",
)


ISHARES_GOVT_0_1YR_IBKR_ACCESS = AccessRoute(
    access_route_id="ishares_govt_0_1yr_xetra_ibkr",
    market_id=ISHARES_GOVT_0_1YR_MARKET.market_id,
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


ISHARES_GOVT_0_1YR_ACCESSIBILITY = Accessibility(
    access_route_id=(
        ISHARES_GOVT_0_1YR_IBKR_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "IBKR supports Slovenian organization accounts and "
        "Xetra ETF trading. The exact accumulating UCITS "
        "share class is listed on Xetra in EUR. "
        "Account-specific permissions remain an "
        "execution-stage operational check rather than a "
        "V1 accessibility blocker."
    ),
)


def get_ishares_govt_0_1yr_snapshot(
) -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id=(
            "ishares_govt_0_1yr_xetra_"
            "ibkr_2026_08_31"
        ),
        instrument_id=(
            ISHARES_GOVT_0_1YR_INSTRUMENT.instrument_id
        ),
        market_id=(
            ISHARES_GOVT_0_1YR_MARKET.market_id
        ),
        access_route_id=(
            ISHARES_GOVT_0_1YR_IBKR_ACCESS.access_route_id
        ),
        observed_date="2026-08-31",
        yield_measure="weighted_average_ytm",
        yield_value_pct=2.66,
        yield_basis=(
            "Portfolio weighted average yield to maturity; "
            "published separately from the fund TER and "
            "not guaranteed realized return"
        ),
        annual_fee_pct=0.09,
        duration_years=0.55,
        average_maturity_years=0.55,
        fund_aum_eur=1_195_000_000.0,
        share_class_aum_eur=161_470_000.0,
        holdings_count=37,
        source="iShares / BlackRock",
        source_url=(
            "https://www.ishares.com/uk/individual/en/"
            "products/345319/"
        ),
        notes=(
            "BlackRock reported approximately 2.66% "
            "weighted-average YTM, 0.55-year effective "
            "duration, 0.55-year weighted-average maturity "
            "and 37 holdings as of 31 Aug 2026. TER is "
            "0.09%. The accumulating CEMK share class had "
            "approximately EUR 161.47 million of assets, "
            "while the broader fund was approximately "
            "EUR 1.195 billion. Position analysis should "
            "therefore prefer exact share-class AUM. The "
            "KID separately estimates approximately 0.01% "
            "annual portfolio transaction costs; this is "
            "recorded as evidence but is not introduced as "
            "a new custom return component during 13E.4."
        ),
    )


def get_ishares_govt_0_1yr_market_observation(
) -> MarketObservation:
    return MarketObservation(
        observation_id=(
            "ishares_govt_0_1yr_xetra_"
            "2026_09_02_market_structure"
        ),
        instrument_id=(
            ISHARES_GOVT_0_1YR_INSTRUMENT.instrument_id
        ),
        market_id=(
            ISHARES_GOVT_0_1YR_MARKET.market_id
        ),
        observed_at="2026-09-02",
        observation_type="verified_exchange_listing",
        source="Deutsche Börse",
        source_url=(
            "https://live.deutsche-boerse.com/en/etf/"
            "ishares-govt-bond-0-1yr-ucits-etf-eur-acc"
        ),
        notes=(
            "Deutsche Börse verifies the exact CEMK Xetra "
            "listing. No reliable fresh public exact "
            "turnover, bid/ask or position-depth observation "
            "is modeled. The observation supplies verified "
            "ETF market-structure evidence only; it does "
            "not independently establish executable depth."
        ),
    )
