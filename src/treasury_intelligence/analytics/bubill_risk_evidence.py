from __future__ import annotations

from treasury_intelligence.analytics.sovereign_bill_risk_evidence import (
    build_direct_sovereign_bill_recommendation_risk_observations,
)

from treasury_intelligence.models.opportunities import (
    Instrument,
    Market,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.sources.germany import (
    BUBILL_2027_07_14,
    BUBILL_2027_07_14_MARKET,
    BUBILL_2027_08_18,
    BUBILL_2027_08_18_MARKET,
)


GERMAN_FINANCE_AGENCY_RATINGS_URL = (
    "https://www.deutsche-finanzagentur.de/en/"
    "federal-funding/government-as-issuer/ratings"
)


def _build_bubill_recommendation_risk_observations(
    *,
    instrument: Instrument,
    market: Market,
    observation_id_prefix: str,
    instrument_name: str,
    maturity_date: str,
    maturity_date_text: str,
    factsheet_url: str,
) -> tuple[RiskObservation, ...]:
    instrument_specific_observations = (
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "multi_agency_ratings"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observed_at="2026-09-01",
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
                f"{observation_id_prefix}_"
                "fitch_sovereign_rating"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
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
                f"{observation_id_prefix}_"
                "instrument_structure"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observed_at="2026-09-01",
            risk_dimension="market",
            observation_type="instrument_structure",
            value_text=(
                "12-month zero-coupon German "
                "Treasury discount paper"
            ),
            evidence_level="published",
            source="German Finance Agency",
            source_url=factsheet_url,
            notes=(
                "The German Finance Agency classifies "
                f"{instrument.isin} as a 12-month "
                "Unverzinsliche Schatzanweisung. "
                "The security has no periodic coupon "
                "payment."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_maturity"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observed_at="2026-09-01",
            risk_dimension="market",
            observation_type="maturity_date",
            value_text=maturity_date,
            evidence_level="published",
            source="German Finance Agency",
            source_url=factsheet_url,
            notes=(
                f"The bill matures on "
                f"{maturity_date_text}. "
                "Market-price exposure before maturity "
                "is distinct from redemption at par "
                "at maturity."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_currency"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observed_at="2026-09-01",
            risk_dimension="currency_asset",
            observation_type="denomination_currency",
            value_text="EUR",
            evidence_level="published",
            source="German Finance Agency",
            source_url=factsheet_url,
            notes=(
                "The German Finance Agency reports "
                "the issue currency as euro."
            ),
        ),
    )

    shared_sovereign_observations = (
        build_direct_sovereign_bill_recommendation_risk_observations(
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observation_id_prefix=(
                observation_id_prefix
            ),
            issuer_name=(
                "Federal Republic of Germany"
            ),
            instrument_name=instrument_name,
            maturity_date_text=maturity_date_text,
            source_name="German Finance Agency",
            source_url=factsheet_url,
        )
    )

    return (
        instrument_specific_observations
        + shared_sovereign_observations
    )


def get_bubill_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        _build_bubill_recommendation_risk_observations(
            instrument=BUBILL_2027_07_14,
            market=BUBILL_2027_07_14_MARKET,
            observation_id_prefix=(
                "de_bubill_2027_07_14"
            ),
            instrument_name=(
                "Bubill 14 July 2027"
            ),
            maturity_date="2027-07-14",
            maturity_date_text="14 July 2027",
            factsheet_url=(
                "https://www.deutsche-finanzagentur.de/"
                "bundeswertpapiere/factsheet/isin/"
                "DE000BU0E436"
            ),
        )
    )


def get_bubill_2027_08_18_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        _build_bubill_recommendation_risk_observations(
            instrument=BUBILL_2027_08_18,
            market=BUBILL_2027_08_18_MARKET,
            observation_id_prefix=(
                "de_bubill_2027_08_18"
            ),
            instrument_name=(
                "Bubill 18 August 2027"
            ),
            maturity_date="2027-08-18",
            maturity_date_text="18 August 2027",
            factsheet_url=(
                "https://www.deutsche-finanzagentur.de/"
                "bundeswertpapiere/factsheet/isin/"
                "DE000BU0E444"
            ),
        )
    )