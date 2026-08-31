from __future__ import annotations

from treasury_intelligence.analytics.sovereign_bill_risk_evidence import (
    build_direct_sovereign_bill_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.sources.germany import (
    BUBILL_2027_07_14,
    BUBILL_2027_07_14_MARKET,
)


GERMAN_FINANCE_AGENCY_RATINGS_URL = (
    "https://www.deutsche-finanzagentur.de/en/"
    "federal-funding/government-as-issuer/ratings"
)

GERMAN_FINANCE_AGENCY_BUBILL_URL = (
    "https://www.deutsche-finanzagentur.de/"
    "bundeswertpapiere/factsheet/isin/"
    "DE000BU0E436"
)


def get_bubill_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    instrument_specific_observations = (
        RiskObservation(
            observation_id=(
                "de_bubill_2027_07_14_"
                "multi_agency_ratings"
            ),
            instrument_id=(
                BUBILL_2027_07_14.instrument_id
            ),
            market_id=(
                BUBILL_2027_07_14_MARKET.market_id
            ),
            observed_at="2026-08-31",
            risk_dimension="principal_credit",
            observation_type=(
                "sovereign_multi_agency_credit_ratings"
            ),
            value_text=(
                "Germany carries AAA or Aaa long-term "
                "sovereign ratings with stable outlooks "
                "across Fitch, DBRS Morningstar, "
                "Standard & Poor's, Moody's, Scope "
                "and KBRA"
            ),
            evidence_level="published",
            source="German Finance Agency",
            source_url=(
                GERMAN_FINANCE_AGENCY_RATINGS_URL
            ),
            notes=(
                "The German Finance Agency's current "
                "ratings table reports AAA/Aaa long-term "
                "ratings with stable outlooks across all "
                "six listed international rating "
                "agencies. This supports exceptionally "
                "strong sovereign credit quality while "
                "not implying zero sovereign or fiscal "
                "risk."
            ),
        ),
        RiskObservation(
            observation_id=(
                "de_bubill_2027_07_14_"
                "fitch_sovereign_rating"
            ),
            instrument_id=(
                BUBILL_2027_07_14.instrument_id
            ),
            market_id=(
                BUBILL_2027_07_14_MARKET.market_id
            ),
            observed_at="2026-05-15",
            risk_dimension="principal_credit",
            observation_type="sovereign_credit_rating",
            value_text="Fitch AAA / Stable",
            evidence_level="published",
            source="German Finance Agency",
            source_url=(
                GERMAN_FINANCE_AGENCY_RATINGS_URL
            ),
            notes=(
                "The German Finance Agency reports "
                "Fitch's latest sovereign rating as "
                "AAA with a Stable Outlook dated "
                "15 May 2026."
            ),
        ),
        RiskObservation(
            observation_id=(
                "de_bubill_2027_07_14_"
                "instrument_structure"
            ),
            instrument_id=(
                BUBILL_2027_07_14.instrument_id
            ),
            market_id=(
                BUBILL_2027_07_14_MARKET.market_id
            ),
            observed_at="2026-08-31",
            risk_dimension="market",
            observation_type="instrument_structure",
            value_text=(
                "12-month zero-coupon German "
                "Treasury discount paper"
            ),
            evidence_level="published",
            source="German Finance Agency",
            source_url=(
                GERMAN_FINANCE_AGENCY_BUBILL_URL
            ),
            notes=(
                "The German Finance Agency classifies "
                "DE000BU0E436 as a 12-month "
                "Unverzinsliche Schatzanweisung. "
                "The security has no periodic coupon "
                "payment."
            ),
        ),
        RiskObservation(
            observation_id=(
                "de_bubill_2027_07_14_maturity"
            ),
            instrument_id=(
                BUBILL_2027_07_14.instrument_id
            ),
            market_id=(
                BUBILL_2027_07_14_MARKET.market_id
            ),
            observed_at="2026-08-31",
            risk_dimension="market",
            observation_type="maturity_date",
            value_text="2027-07-14",
            evidence_level="published",
            source="German Finance Agency",
            source_url=(
                GERMAN_FINANCE_AGENCY_BUBILL_URL
            ),
            notes=(
                "The bill matures on 14 July 2027. "
                "Market-price exposure before maturity "
                "is distinct from redemption at par "
                "at maturity."
            ),
        ),
        RiskObservation(
            observation_id=(
                "de_bubill_2027_07_14_currency"
            ),
            instrument_id=(
                BUBILL_2027_07_14.instrument_id
            ),
            market_id=(
                BUBILL_2027_07_14_MARKET.market_id
            ),
            observed_at="2026-08-31",
            risk_dimension="currency_asset",
            observation_type="denomination_currency",
            value_text="EUR",
            evidence_level="published",
            source="German Finance Agency",
            source_url=(
                GERMAN_FINANCE_AGENCY_BUBILL_URL
            ),
            notes=(
                "The German Finance Agency reports "
                "the issue currency as euro."
            ),
        ),
    )

    shared_sovereign_observations = (
        build_direct_sovereign_bill_recommendation_risk_observations(
            instrument_id=(
                BUBILL_2027_07_14.instrument_id
            ),
            market_id=(
                BUBILL_2027_07_14_MARKET.market_id
            ),
            observation_id_prefix=(
                "de_bubill_2027_07_14"
            ),
            issuer_name=(
                "Federal Republic of Germany"
            ),
            instrument_name=(
                "Bubill 14 July 2027"
            ),
            maturity_date_text=(
                "14 July 2027"
            ),
            source_name="German Finance Agency",
            source_url=(
                GERMAN_FINANCE_AGENCY_BUBILL_URL
            ),
        )
    )

    return (
        instrument_specific_observations
        + shared_sovereign_observations
    )