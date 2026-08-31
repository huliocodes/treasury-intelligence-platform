from __future__ import annotations

from treasury_intelligence.analytics.sovereign_bill_risk_evidence import (
    build_direct_sovereign_bill_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_MARKET,
)


AFT_BTF_2027_03_10_URL = (
    "https://www.aft.gouv.fr/fr/titre/fr0129704153"
)

AFT_FRANCE_CREDIT_RATINGS_URL = (
    "https://www.aft.gouv.fr/en/frances-credit-ratings"
)

FITCH_FRANCE_2026_08_28_URL = (
    "https://www.fitchratings.com/research/sovereigns/"
    "fitch-affirms-france-at-a-outlook-stable-28-08-2026"
)


def get_btf_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    credit_observations = (
        RiskObservation(
            observation_id=(
                "btf_2027_03_10_fitch_sovereign_rating"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
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
                "btf_2027_03_10_multi_agency_ratings"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
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
    )

    shared_sovereign_observations = (
        build_direct_sovereign_bill_recommendation_risk_observations(
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observation_id_prefix=(
                "btf_2027_03_10"
            ),
            issuer_name="French Republic",
            instrument_name="BTF 10 March 2027",
            maturity_date_text="10 March 2027",
            source_name="Agence France Trésor",
            source_url=AFT_BTF_2027_03_10_URL,
        )
    )

    return (
        credit_observations
        + shared_sovereign_observations
    )