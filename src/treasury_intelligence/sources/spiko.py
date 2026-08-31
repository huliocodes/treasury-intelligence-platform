from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    OpportunitySnapshot,
)


SPIKO_EU_TBILLS_INSTRUMENT = Instrument(
    instrument_id="spiko_eu_tbills",
    provider="Spiko / Twenty First Capital",
    name="Spiko EU T-Bills Money Market Fund",
    instrument_type="tokenized_money_market_fund",
    legal_structure="UCITS Short-Term VNAV Money Market Fund",
    currency="EUR",
    yield_source="eurozone_treasury_bills",
    isin="FR001400ODL1",
    income_treatment="accumulating",
)


SPIKO_EU_TBILLS_MARKET = Market(
    market_id="spiko_eu_tbills_direct",
    instrument_id=SPIKO_EU_TBILLS_INSTRUMENT.instrument_id,
    venue="Spiko",
    venue_type="tokenized_fund_subscription_redemption",
    trading_currency="EUR",
    settlement_cycle="T+0",
)


SPIKO_EU_TBILLS_DIRECT_ACCESS = AccessRoute(
    access_route_id="spiko_eu_tbills_direct",
    market_id=SPIKO_EU_TBILLS_MARKET.market_id,
    provider="Spiko",
    route_type="direct_fund_account",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


SPIKO_EU_TBILLS_ACCESSIBILITY = Accessibility(
    access_route_id=(
        SPIKO_EU_TBILLS_DIRECT_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="supported",
    corporate_operational_access="unverified",
    status="research_eligible_not_actionable",
    evidence_level="partial",
    notes=(
        "Spiko publicly supports business and corporate "
        "treasury accounts and provides direct treasury "
        "account infrastructure. Public evidence reviewed "
        "does not yet establish that a Slovenian d.o.o. "
        "can currently complete onboarding in Slovenia. "
        "Country-specific corporate access must therefore "
        "be verified before this opportunity becomes "
        "actionable."
    ),
)


SPIKO_EU_TBILLS_MINIMUM_EUR = 1.0
SPIKO_EU_TBILLS_FUND_AUM_EUR = 768_899_333.0


def get_spiko_eu_tbills_snapshot(
) -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id="spiko_eu_tbills_2026-08-30",
        instrument_id=SPIKO_EU_TBILLS_INSTRUMENT.instrument_id,
        market_id=SPIKO_EU_TBILLS_MARKET.market_id,
        access_route_id=(
            SPIKO_EU_TBILLS_DIRECT_ACCESS.access_route_id
        ),
        observed_date="2026-08-30",
        yield_measure="seven_day_net_yield",
        yield_value_pct=2.09,
        yield_basis=(
            "Published annualized seven-day net yield. "
            "The yield is net of fund fees and fluctuates "
            "with the underlying Treasury-bill portfolio."
        ),
        annual_fee_pct=0.25,
        fund_aum_eur=SPIKO_EU_TBILLS_FUND_AUM_EUR,
        price_status="published_nav",
        quote_firmness="fund_dealing_terms",
        early_exit_possible=True,
        source="Spiko",
        source_url=(
            "https://data.spiko.io/eutbl/"
        ),
        notes=(
            "EUR-denominated short-term VNAV money-market "
            "fund with tokenized fund shares. Published "
            "minimum initial subscription is EUR 1. "
            "Published subscription and redemption fees "
            "are zero. Tokenization describes the fund-share "
            "registry and operating infrastructure; it is "
            "not itself the economic source of yield. "
            "Slovenian corporate onboarding remains "
            "unverified."
        ),
    )