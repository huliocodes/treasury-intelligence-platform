from __future__ import annotations

from treasury_intelligence.sources.banks import BankDepositRate


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