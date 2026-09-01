from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    MarketObservation,
    OpportunitySnapshot,
)


BTF_2027_03_10 = Instrument(
    instrument_id="fr_btf_2027_03_10",
    provider="Agence France Trésor",
    issuer="French Republic",
    name="BTF 10 March 2027",
    instrument_type="sovereign_bill",
    legal_structure="French Treasury Bill",
    currency="EUR",
    yield_source="sovereign_borrowing",
    isin="FR0129704153",
    maturity_date="2027-03-10",
    coupon_type="zero_coupon_discount",
)


BTF_2027_03_10_MARKET = Market(
    market_id="fr_btf_2027_03_10_ibkr",
    instrument_id=BTF_2027_03_10.instrument_id,
    venue="European Government Bond market",
    venue_type="brokered_otc_secondary",
    trading_currency="EUR",
    settlement_cycle="T+2",
)


BTF_2027_03_10_IBKR_ACCESS = AccessRoute(
    access_route_id="fr_btf_2027_03_10_ibkr",
    market_id=BTF_2027_03_10_MARKET.market_id,
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


BTF_2027_03_10_ACCESSIBILITY = Accessibility(
    access_route_id=(
        BTF_2027_03_10_IBKR_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "IBKR supports European Government Bonds and "
        "non-US sovereign bonds. Final availability, "
        "account permissions and executable quote for "
        "this exact ISIN must be verified at execution."
    ),
)


BTF_2027_08_11 = Instrument(
    instrument_id="fr_btf_2027_08_11",
    provider="Agence France Trésor",
    issuer="French Republic",
    name="BTF 11 August 2027",
    instrument_type="sovereign_bill",
    legal_structure="French Treasury Bill",
    currency="EUR",
    yield_source="sovereign_borrowing",
    isin="FR0129704187",
    maturity_date="2027-08-11",
    coupon_type="zero_coupon_discount",
)


BTF_2027_08_11_MARKET = Market(
    market_id="fr_btf_2027_08_11_ibkr",
    instrument_id=BTF_2027_08_11.instrument_id,
    venue="European Government Bond market",
    venue_type="brokered_otc_secondary",
    trading_currency="EUR",
    settlement_cycle="T+2",
)


BTF_2027_08_11_IBKR_ACCESS = AccessRoute(
    access_route_id="fr_btf_2027_08_11_ibkr",
    market_id=BTF_2027_08_11_MARKET.market_id,
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


BTF_2027_08_11_ACCESSIBILITY = Accessibility(
    access_route_id=(
        BTF_2027_08_11_IBKR_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "IBKR supports European Government Bonds and "
        "non-US sovereign bonds for supported corporate "
        "accounts. The same verified French BTF access "
        "architecture used by the existing March 2027 "
        "security is applied to this exact BTF. Final "
        "account permissions and executable quote remain "
        "execution-stage checks."
    ),
)


def get_btf_2027_03_10_snapshot() -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id=(
            "fr_btf_2027_03_10_auction_2026-08-24"
        ),
        instrument_id=BTF_2027_03_10.instrument_id,
        market_id=BTF_2027_03_10_MARKET.market_id,
        access_route_id=(
            BTF_2027_03_10_IBKR_ACCESS.access_route_id
        ),
        observed_date="2026-08-24",
        yield_measure="auction_weighted_average_rate",
        yield_value_pct=2.675,
        yield_basis=(
            "Weighted-average rate from the latest "
            "completed Agence France Trésor auction. "
            "This is not a current secondary-market "
            "executable yield."
        ),
        outstanding_amount_eur=2_323_000_000.0,
        price_status="published",
        quote_firmness="indicative",
        early_exit_possible=True,
        source="Agence France Trésor",
        source_url=(
            "https://www.aft.gouv.fr/en/titre/"
            "fr0129704153"
        ),
        notes=(
            "Zero-coupon EUR French Treasury bill. "
            "Redeemed at par at maturity. Secondary "
            "market exit is possible before maturity, "
            "but price, spread and market impact must "
            "be evaluated using a live broker quote."
        ),
    )


def get_btf_2027_03_10_market_observation(
) -> MarketObservation:
    return MarketObservation(
        observation_id=(
            "fr_btf_2027_03_10_public_market_2026-08-29"
        ),
        instrument_id=BTF_2027_03_10.instrument_id,
        market_id=BTF_2027_03_10_MARKET.market_id,
        observed_at="2026-08-29",
        observation_type="delayed_public_market",
        price_pct_of_par=98.60,
        source="finanzen.net",
        source_url=(
            "https://www.finanzen.net/"
        ),
        notes=(
            "Public secondary-market price observation. "
            "Not a firm executable quote. Bid, ask and "
            "available size are unknown."
        ),
    )


def get_btf_2027_08_11_snapshot() -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id=(
            "fr_btf_2027_08_11_auction_2026-08-31"
        ),
        instrument_id=BTF_2027_08_11.instrument_id,
        market_id=BTF_2027_08_11_MARKET.market_id,
        access_route_id=(
            BTF_2027_08_11_IBKR_ACCESS.access_route_id
        ),
        observed_date="2026-08-31",
        yield_measure="auction_weighted_average_rate",
        yield_value_pct=2.860,
        yield_basis=(
            "Weighted-average rate from the 31 August "
            "2026 Agence France Trésor auction. The "
            "auction received EUR 7.805 billion of bids "
            "and served EUR 1.898 billion, producing a "
            "4.11 bid-to-cover ratio. This is published "
            "primary-market evidence rather than a firm "
            "secondary-market executable yield."
        ),
        outstanding_amount_eur=8_135_000_000.0,
        price_status="published",
        quote_firmness="indicative",
        early_exit_possible=True,
        source="Agence France Trésor",
        source_url=(
            "https://www.aft.gouv.fr/fr/titre/"
            "fr0129704187"
        ),
        notes=(
            "Zero-coupon EUR French Treasury bill "
            "redeemed at par on 11 August 2027. AFT "
            "reports EUR 8.135 billion outstanding "
            "after four August 2026 auctions. Secondary "
            "market exit is possible before maturity, "
            "but the snapshot does not claim a firm "
            "position-size executable quote."
        ),
    )


def get_btf_2027_08_11_market_observation(
) -> MarketObservation:
    return MarketObservation(
        observation_id=(
            "fr_btf_2027_08_11_market_2026-08-31"
        ),
        instrument_id=BTF_2027_08_11.instrument_id,
        market_id=BTF_2027_08_11_MARKET.market_id,
        observed_at="2026-08-31",
        observation_type="published_primary_market",
        source="Agence France Trésor",
        source_url=(
            "https://www.aft.gouv.fr/en/publications/"
            "communiques-presse/31-august-2026-"
            "issuance-btfs"
        ),
        notes=(
            "AFT reports EUR 7.805 billion bid and "
            "EUR 1.898 billion served for this security "
            "at the 31 August 2026 reopening, with a "
            "4.11 bid-to-cover ratio. No firm secondary-"
            "market bid, ask or displayed position-size "
            "quote is claimed. Position liquidity is "
            "therefore inferred separately from issue "
            "scale and market structure."
        ),
    )