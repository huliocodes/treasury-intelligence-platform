from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    MarketObservation,
    OpportunitySnapshot,
)


BUBILL_2027_07_14 = Instrument(
    instrument_id="de_bubill_2027_07_14",
    provider="German Finance Agency",
    issuer="Federal Republic of Germany",
    name="Bubill 14 July 2027",
    instrument_type="sovereign_bill",
    legal_structure=(
        "German Treasury Discount Paper"
    ),
    currency="EUR",
    yield_source="sovereign_borrowing",
    isin="DE000BU0E436",
    maturity_date="2027-07-14",
    coupon_type="zero_coupon_discount",
)


BUBILL_2027_07_14_MARKET = Market(
    market_id="de_bubill_2027_07_14_ibkr",
    instrument_id=BUBILL_2027_07_14.instrument_id,
    venue="European Government Bond market",
    venue_type="brokered_otc_secondary",
    trading_currency="EUR",
    settlement_cycle="T+2",
)


BUBILL_2027_07_14_IBKR_ACCESS = AccessRoute(
    access_route_id="de_bubill_2027_07_14_ibkr",
    market_id=BUBILL_2027_07_14_MARKET.market_id,
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


BUBILL_2027_07_14_ACCESSIBILITY = Accessibility(
    access_route_id=(
        BUBILL_2027_07_14_IBKR_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "IBKR supports European Government Bonds and "
        "non-US sovereign bonds for organization "
        "accounts. The security itself is not "
        "stock-exchange listed, so access is modeled "
        "through a brokered European government-bond "
        "secondary-market route rather than Xetra. "
        "Exact ISIN availability, account permissions "
        "and executable quotes remain execution-stage "
        "requirements."
    ),
)


BUBILL_2027_07_14_ISSUANCE_VOLUME_EUR = (
    5_500_000_000.0
)


def get_bubill_2027_07_14_snapshot(
) -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id=(
            "de_bubill_2027_07_14_auction_2026-08-24"
        ),
        instrument_id=BUBILL_2027_07_14.instrument_id,
        market_id=BUBILL_2027_07_14_MARKET.market_id,
        access_route_id=(
            BUBILL_2027_07_14_IBKR_ACCESS.access_route_id
        ),
        observed_date="2026-08-24",
        yield_measure="auction_average_yield",
        yield_value_pct=2.647,
        yield_basis=(
            "Average yield from the 24 August 2026 "
            "German Finance Agency reopening auction. "
            "This is primary-market auction evidence, "
            "not a current secondary-market executable "
            "yield."
        ),
        outstanding_amount_eur=(
            BUBILL_2027_07_14_ISSUANCE_VOLUME_EUR
        ),
        price_status="published",
        quote_firmness="indicative",
        early_exit_possible=True,
        source="German Finance Agency",
        source_url=(
            "https://www.deutsche-finanzagentur.de/"
            "bundeswertpapiere/factsheet/isin/"
            "DE000BU0E436"
        ),
        notes=(
            "EUR zero-coupon German Treasury discount "
            "paper maturing 14 July 2027. The German "
            "Finance Agency reports that the security "
            "is not stock-exchange listed. The auction "
            "yield provides reference economics only; "
            "secondary-market executable price, spread "
            "and available size remain unresolved."
        ),
    )


def get_bubill_2027_07_14_market_observation(
) -> MarketObservation:
    return MarketObservation(
        observation_id=(
            "de_bubill_2027_07_14_auction_2026-08-24"
        ),
        instrument_id=BUBILL_2027_07_14.instrument_id,
        market_id=BUBILL_2027_07_14_MARKET.market_id,
        observed_at="2026-08-24",
        observation_type="primary_auction_result",
        price_pct_of_par=97.68716,
        yield_pct=2.647,
        yield_measure="auction_average_yield",
        source="German Finance Agency",
        source_url=(
            "https://www.deutsche-finanzagentur.de/"
            "bundeswertpapiere/factsheet/isin/"
            "DE000BU0E436"
        ),
        notes=(
            "Official 24 August 2026 reopening auction "
            "result. Average price was 97.68716 and "
            "average yield was 2.647%. This observation "
            "does not represent a secondary-market "
            "executable bid or ask."
        ),
    )


BUBILL_2027_08_18 = Instrument(
    instrument_id="de_bubill_2027_08_18",
    provider="German Finance Agency",
    issuer="Federal Republic of Germany",
    name="Bubill 18 August 2027",
    instrument_type="sovereign_bill",
    legal_structure=(
        "German Treasury Discount Paper"
    ),
    currency="EUR",
    yield_source="sovereign_borrowing",
    isin="DE000BU0E444",
    maturity_date="2027-08-18",
    coupon_type="zero_coupon_discount",
)


BUBILL_2027_08_18_MARKET = Market(
    market_id="de_bubill_2027_08_18_ibkr",
    instrument_id=BUBILL_2027_08_18.instrument_id,
    venue="European Government Bond market",
    venue_type="brokered_otc_secondary",
    trading_currency="EUR",
    settlement_cycle="T+2",
)


BUBILL_2027_08_18_IBKR_ACCESS = AccessRoute(
    access_route_id="de_bubill_2027_08_18_ibkr",
    market_id=BUBILL_2027_08_18_MARKET.market_id,
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


BUBILL_2027_08_18_ACCESSIBILITY = Accessibility(
    access_route_id=(
        BUBILL_2027_08_18_IBKR_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "IBKR supports European Government Bonds and "
        "non-US sovereign bonds for organization "
        "accounts. The security itself is not "
        "stock-exchange listed, so access is modeled "
        "through the same supported brokered European "
        "government-bond secondary-market route as "
        "the existing German Bubill analysis. Exact "
        "ISIN availability, account permissions and "
        "executable quotes remain execution-stage "
        "requirements."
    ),
)


BUBILL_2027_08_18_ISSUANCE_VOLUME_EUR = (
    3_000_000_000.0
)


def get_bubill_2027_08_18_snapshot(
) -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id=(
            "de_bubill_2027_08_18_auction_2026-08-17"
        ),
        instrument_id=BUBILL_2027_08_18.instrument_id,
        market_id=BUBILL_2027_08_18_MARKET.market_id,
        access_route_id=(
            BUBILL_2027_08_18_IBKR_ACCESS.access_route_id
        ),
        observed_date="2026-08-17",
        yield_measure="auction_average_yield",
        yield_value_pct=2.656,
        yield_basis=(
            "Average yield from the 17 August 2026 "
            "German Finance Agency new-issue auction. "
            "This is primary-market auction evidence, "
            "not a current secondary-market executable "
            "yield."
        ),
        outstanding_amount_eur=(
            BUBILL_2027_08_18_ISSUANCE_VOLUME_EUR
        ),
        price_status="published",
        quote_firmness="indicative",
        early_exit_possible=True,
        source="German Finance Agency",
        source_url=(
            "https://www.deutsche-finanzagentur.de/"
            "bundeswertpapiere/factsheet/isin/"
            "DE000BU0E444"
        ),
        notes=(
            "EUR zero-coupon German Treasury discount "
            "paper issued on 17 August 2026 and "
            "maturing 18 August 2027. Current modeled "
            "issue volume is EUR 3.0 billion. Planned "
            "future reopenings are deliberately not "
            "included in current issue scale. The "
            "German Finance Agency reports that the "
            "security is not stock-exchange listed. "
            "The auction yield provides reference "
            "economics only; secondary-market "
            "executable price, spread and available "
            "size remain execution-stage variables."
        ),
    )


def get_bubill_2027_08_18_market_observation(
) -> MarketObservation:
    return MarketObservation(
        observation_id=(
            "de_bubill_2027_08_18_auction_2026-08-17"
        ),
        instrument_id=BUBILL_2027_08_18.instrument_id,
        market_id=BUBILL_2027_08_18_MARKET.market_id,
        observed_at="2026-08-17",
        observation_type="primary_auction_result",
        price_pct_of_par=97.38472,
        yield_pct=2.656,
        yield_measure="auction_average_yield",
        source="German Finance Agency",
        source_url=(
            "https://www.deutsche-finanzagentur.de/"
            "bundeswertpapiere/factsheet/isin/"
            "DE000BU0E444"
        ),
        notes=(
            "Official 17 August 2026 new-issue auction "
            "result. Average price was 97.38472 and "
            "average yield was 2.656%. Total bids were "
            "EUR 6.355 billion against EUR 3.0 billion "
            "issuance volume; the published bid-to-"
            "cover ratio was 2.8. This observation "
            "does not represent a secondary-market "
            "executable bid or ask."
        ),
    )