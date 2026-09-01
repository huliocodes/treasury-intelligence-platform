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

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_MARKET,
    BTF_2027_08_11,
    BTF_2027_08_11_MARKET,
)


AFT_BTF_2027_03_10_URL = (
    "https://www.aft.gouv.fr/fr/titre/fr0129704153"
)

AFT_BTF_2027_08_11_URL = (
    "https://www.aft.gouv.fr/fr/titre/fr0129704187"
)

AFT_FRANCE_CREDIT_RATINGS_URL = (
    "https://www.aft.gouv.fr/en/frances-credit-ratings"
)

FITCH_FRANCE_2026_08_28_URL = (
    "https://www.fitchratings.com/research/sovereigns/"
    "fitch-affirms-france-at-a-outlook-stable-28-08-2026"
)


def build_french_btf_recommendation_risk_observations(
    *,
    instrument: Instrument,
    market: Market,
    observation_id_prefix: str,
    instrument_name: str,
    maturity_date_text: str,
    security_source_url: str,
) -> tuple[RiskObservation, ...]:
    if instrument.issuer != "French Republic":
        raise ValueError(
            "French BTF risk evidence requires a "
            "French Republic instrument."
        )

    if instrument.instrument_type != "sovereign_bill":
        raise ValueError(
            "French BTF risk evidence requires a "
            "sovereign_bill instrument."
        )

    if market.instrument_id != instrument.instrument_id:
        raise ValueError(
            "Market instrument_id must match instrument."
        )

    credit_observations = (
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "fitch_sovereign_rating"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observed_at="2026-08-28",
            risk_dimension="principal_credit",
            observation_type="sovereign_credit_rating",
            value_text="Fitch A+ / Stable",
            evidence_level="published",
            source="Fitch Ratings",
            source_url=FITCH_FRANCE_2026_08_28_URL,
            notes=(
                "Fitch affirmed France's Long-Term "
                "Issuer Default Rating at A+ with a "
                "Stable Outlook on 28 August 2026. "
                "This is strong investment-grade "
                "credit evidence but does not imply "
                "zero sovereign-default or fiscal risk."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "multi_agency_ratings"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observed_at="2026-08-31",
            risk_dimension="principal_credit",
            observation_type=(
                "sovereign_multi_agency_credit_ratings"
            ),
            value_text=(
                "France carries strong investment-grade "
                "sovereign ratings across major agencies, "
                "with published ratings including A+, "
                "AA-, AA, Aa3 and AAA"
            ),
            evidence_level="published",
            source="Agence France Trésor",
            source_url=(
                AFT_FRANCE_CREDIT_RATINGS_URL
            ),
            notes=(
                "Agence France Trésor publishes the "
                "current cross-agency sovereign rating "
                "set. Several ratings remain in the AA "
                "range while the lowest published major "
                "agency ratings are A+. Some agencies "
                "carry negative outlooks, so the evidence "
                "supports low rather than negligible "
                "sovereign credit risk."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "short_dated_zero_coupon"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observed_at="2026-08-31",
            risk_dimension="market",
            observation_type=(
                "short_dated_zero_coupon_sovereign_bill"
            ),
            value_text=(
                f"{instrument_name} is a zero-coupon "
                f"French Treasury bill maturing "
                f"{maturity_date_text}"
            ),
            evidence_level="published",
            source="Agence France Trésor",
            source_url=security_source_url,
            notes=(
                "The short remaining maturity limits "
                "interest-rate sensitivity relative to "
                "longer-duration fixed-income securities, "
                "although secondary-market price can "
                "still change before maturity."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_currency"
            ),
            instrument_id=instrument.instrument_id,
            market_id=market.market_id,
            observed_at="2026-08-31",
            risk_dimension="currency_asset",
            observation_type="security_currency",
            value_text="EUR",
            evidence_level="published",
            source="Agence France Trésor",
            source_url=security_source_url,
            notes=(
                "AFT identifies the BTF issuance "
                "currency as euro."
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
            issuer_name="French Republic",
            instrument_name=instrument_name,
            maturity_date_text=maturity_date_text,
            source_name="Agence France Trésor",
            source_url=security_source_url,
        )
    )

    return (
        credit_observations
        + shared_sovereign_observations
    )


def get_btf_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        build_french_btf_recommendation_risk_observations(
            instrument=BTF_2027_03_10,
            market=BTF_2027_03_10_MARKET,
            observation_id_prefix="btf_2027_03_10",
            instrument_name="BTF 10 March 2027",
            maturity_date_text="10 March 2027",
            security_source_url=(
                AFT_BTF_2027_03_10_URL
            ),
        )
    )


def get_btf_2027_08_11_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        build_french_btf_recommendation_risk_observations(
            instrument=BTF_2027_08_11,
            market=BTF_2027_08_11_MARKET,
            observation_id_prefix="btf_2027_08_11",
            instrument_name="BTF 11 August 2027",
            maturity_date_text="11 August 2027",
            security_source_url=(
                AFT_BTF_2027_08_11_URL
            ),
        )
    )