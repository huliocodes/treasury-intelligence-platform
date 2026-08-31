from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    OpportunitySnapshot,
)
from treasury_intelligence.sources.banks import (
    BankDepositRate,
)


ADDIKO_CORPORATE_RATE_SOURCE_URL = (
    "https://www.addiko.si/static/uploads/"
    "Obrestne-mere_Podjetja_Veljavnost-od-01.04.2026.pdf"
)


def get_addiko_corporate_eur_deposit_rates() -> list[BankDepositRate]:
    """
    Return Addiko Bank's published corporate EUR term-deposit curve.

    These are published but non-binding rates.

    Addiko states that actual corporate deposit rates can depend on:
    - money-market conditions,
    - the bank's liquidity needs,
    - deposit amount,
    - and the scope of the client relationship.

    Therefore these rates must not be interpreted as executable quotes.
    """

    common = {
        "bank": "Addiko Bank",
        "product": "Corporate EUR term deposit",
        "investor_type": "legal_entity",
        "currency": "EUR",
        "rate_type": "nominal_annual",
        "price_status": "published",
        "quote_firmness": "indicative",
        "minimum_amount_eur": 400.0,
        "maximum_amount_eur": None,
        "fixed_rate": True,
        "negotiated": True,
        "early_withdrawal": False,
        "effective_date": "2026-04-01",
        "source": "Addiko Bank",
        "source_url": ADDIKO_CORPORATE_RATE_SOURCE_URL,
    }

    return [
        BankDepositRate(
            **common,
            term_label="91–180 days",
            min_term_days=91,
            max_term_days=180,
            annual_rate_pct=1.50,
            notes=(
                "Published rate is informational and "
                "non-binding."
            ),
        ),
        BankDepositRate(
            **common,
            term_label="181–270 days",
            min_term_days=181,
            max_term_days=270,
            annual_rate_pct=1.55,
            notes=(
                "Published rate is informational and "
                "non-binding."
            ),
        ),
        BankDepositRate(
            **common,
            term_label="271 days–1 year",
            min_term_days=271,
            max_term_days=365,
            annual_rate_pct=1.60,
            notes=(
                "Published rate is informational and "
                "non-binding."
            ),
        ),
        BankDepositRate(
            **common,
            term_label=">1–2 years",
            min_term_days=366,
            max_term_days=730,
            annual_rate_pct=1.70,
            notes=(
                "Published rate is informational and "
                "non-binding."
            ),
        ),
        BankDepositRate(
            **common,
            term_label=">2–3 years",
            min_term_days=731,
            max_term_days=1095,
            annual_rate_pct=1.70,
            notes=(
                "Published rate is informational and "
                "non-binding."
            ),
        ),
        BankDepositRate(
            **common,
            term_label=">3 years",
            min_term_days=1096,
            max_term_days=None,
            annual_rate_pct=1.70,
            notes=(
                "Published rate is informational and "
                "non-binding."
            ),
        ),
    ]


ADDIKO_91_180_DAY_RATE = (
    get_addiko_corporate_eur_deposit_rates()[0]
)


ADDIKO_91_180_DAY_INSTRUMENT = Instrument(
    instrument_id="addiko_corporate_deposit_91_180d",
    provider="Addiko Bank",
    issuer="Addiko Bank",
    name="Addiko Corporate EUR Term Deposit 91–180 Days",
    instrument_type="bank_term_deposit",
    legal_structure="Corporate bank term deposit",
    currency="EUR",
    yield_source="bank_deposit_interest",
    fx_exposure_currency="EUR",
    maturity_date=None,
    coupon_type="fixed_deposit_interest",
)


ADDIKO_91_180_DAY_MARKET = Market(
    market_id="addiko_corporate_deposit_91_180d_direct",
    instrument_id=(
        ADDIKO_91_180_DAY_INSTRUMENT.instrument_id
    ),
    venue="Addiko Bank",
    venue_type="bank_deposit",
    trading_currency="EUR",
    settlement_cycle="T+0",
)


ADDIKO_91_180_DAY_ACCESS = AccessRoute(
    access_route_id=(
        "addiko_corporate_deposit_91_180d_direct"
    ),
    market_id=ADDIKO_91_180_DAY_MARKET.market_id,
    provider="Addiko Bank",
    route_type="direct_bank_deposit",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


ADDIKO_91_180_DAY_ACCESSIBILITY = Accessibility(
    access_route_id=(
        ADDIKO_91_180_DAY_ACCESS.access_route_id
    ),
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="published_corporate_product",
    notes=(
        "Addiko publishes the EUR term-deposit rate "
        "schedule specifically for corporate/legal-entity "
        "customers in Slovenia. This establishes a direct "
        "corporate access route for V1 research. The actual "
        "rate remains subject to an individual bank quote "
        "and is not established by the published schedule."
    ),
)


ADDIKO_91_180_DAY_MINIMUM_EUR = (
    ADDIKO_91_180_DAY_RATE.minimum_amount_eur
    or 0.0
)


def get_addiko_91_180_day_snapshot(
) -> OpportunitySnapshot:
    rate = ADDIKO_91_180_DAY_RATE

    return OpportunitySnapshot(
        snapshot_id=(
            "addiko_corporate_deposit_91_180d_"
            f"{rate.effective_date}"
        ),
        instrument_id=(
            ADDIKO_91_180_DAY_INSTRUMENT.instrument_id
        ),
        market_id=(
            ADDIKO_91_180_DAY_MARKET.market_id
        ),
        access_route_id=(
            ADDIKO_91_180_DAY_ACCESS.access_route_id
        ),
        observed_date=rate.effective_date,
        yield_measure="published_nominal_annual_rate",
        yield_value_pct=rate.annual_rate_pct,
        yield_basis=(
            "Published indicative annual nominal rate for "
            "a 91–180 day corporate EUR term deposit. "
            "The actual rate can depend on deposit amount, "
            "market conditions, bank liquidity needs and "
            "the client relationship."
        ),
        annual_fee_pct=None,
        duration_years=None,
        average_maturity_years=None,
        price_status=rate.price_status,
        quote_firmness=rate.quote_firmness,
        early_exit_possible=rate.early_withdrawal,
        source=rate.source,
        source_url=rate.source_url,
        notes=(
            "The published 1.50% rate is informational "
            "and non-binding. A bank quote is required "
            "before executable economics are known. "
            "Published terms state that early withdrawal "
            "is not available, so the deposit does not "
            "satisfy the model treasury's immediate "
            "liquidity requirement while the term is active."
        ),
    )