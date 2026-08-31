from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    OpportunitySnapshot,
)


BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0 = Instrument(
    instrument_id="blackrock_ics_euro_liquidity_core_t0",
    provider="BlackRock",
    name=(
        "BlackRock ICS Euro Liquidity Fund "
        "Core Acc T0"
    ),
    instrument_type="money_market_fund",
    legal_structure="UCITS LVNAV Money Market Fund",
    currency="EUR",
    yield_source="short_term_money_markets",
    isin="IE0005023803",
    income_treatment="accumulating",
)


BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MARKET = Market(
    market_id="blackrock_ics_euro_liquidity_core_t0_direct",
    instrument_id=(
        BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0.instrument_id
    ),
    venue="BlackRock Institutional Cash Series",
    venue_type="fund_subscription_redemption",
    trading_currency="EUR",
    settlement_cycle="T+0",
)


BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_ACCESS = AccessRoute(
    access_route_id=(
        "blackrock_ics_euro_liquidity_core_t0_direct"
    ),
    market_id=(
        BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MARKET.market_id
    ),
    provider="BlackRock",
    route_type="direct_fund_subscription",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_ACCESSIBILITY = (
    Accessibility(
        access_route_id=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_ACCESS
            .access_route_id
        ),
        entity_type="Slovenian d.o.o.",
        jurisdiction="Slovenia",
        technical_access="unknown",
        corporate_operational_access="unverified",
        status="research_eligible_not_actionable",
        evidence_level="insufficient",
        notes=(
            "The fund is a EUR UCITS institutional money-market "
            "fund whose published minimum investment is compatible "
            "with the model treasury. Public product evidence does "
            "not yet establish the exact subscription or "
            "distribution route available to a Slovenian d.o.o. "
            "Do not treat this opportunity as actionable until "
            "that access route is verified."
        ),
    )
)


BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MINIMUM_EUR = (
    1_000_000.0
)

BLACKROCK_ICS_EURO_LIQUIDITY_FUND_AUM_EUR = (
    64_152_316_465.74
)


def get_blackrock_ics_euro_liquidity_core_t0_snapshot(
) -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id=(
            "blackrock_ics_euro_liquidity_core_t0_"
            "2026-08-28"
        ),
        instrument_id=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0
            .instrument_id
        ),
        market_id=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MARKET
            .market_id
        ),
        access_route_id=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_ACCESS
            .access_route_id
        ),
        observed_date="2026-08-28",
        yield_measure="seven_day_net_yield",
        yield_value_pct=2.21,
        yield_basis=(
            "Published seven-day yield net of fund charges. "
            "The yield is backward-looking/current portfolio "
            "evidence and is not a guaranteed future return."
        ),
        annual_fee_pct=0.20,
        average_maturity_years=(52.0 / 365.0),
        fund_aum_eur=(
            BLACKROCK_ICS_EURO_LIQUIDITY_FUND_AUM_EUR
        ),
        price_status="published_nav",
        quote_firmness="fund_dealing_terms",
        early_exit_possible=True,
        source="BlackRock",
        source_url=(
            "https://www.blackrock.com/cash/en-gb/"
            "products/229226/blackrock-ics-euro-"
            "liquidity-core-acc-t0-fund"
        ),
        notes=(
            "Irish UCITS Low Volatility NAV money-market "
            "fund. Published minimum initial investment is "
            "EUR 1,000,000. Dealing frequency is daily and "
            "published dealing settlement is trade date. "
            "The fund reported 33.2% daily-maturing assets "
            "and 47.0% weekly-maturing assets as of "
            "28 August 2026. Slovenian corporate access "
            "remains unverified."
        ),
    )