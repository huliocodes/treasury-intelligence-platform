from __future__ import annotations

from treasury_intelligence.analytics.broker_risk_evidence import (
    build_ibkr_ireland_recommendation_risk_observations,
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
    instrument_specific_observations = (
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
        RiskObservation(
            observation_id=(
                "btf_2027_03_10_direct_sovereign_security"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "direct_sovereign_security_structure"
            ),
            value_text=(
                "Direct French Republic Treasury bill "
                "with no fund or derivative wrapper"
            ),
            evidence_level="published",
            source="Agence France Trésor",
            source_url=AFT_BTF_2027_03_10_URL,
            notes=(
                "AFT identifies the instrument directly "
                "as a French Treasury bill. The modeled "
                "position therefore does not depend on a "
                "fund issuer, swap counterparty, token "
                "issuer, lending protocol, or other "
                "investment wrapper for its principal "
                "economic claim."
            ),
        ),
        RiskObservation(
            observation_id=(
                "btf_2027_03_10_redemption_structure"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "sovereign_bill_redemption_structure"
            ),
            value_text=(
                "Zero-coupon BTF redeemed in full at "
                "par on 10 March 2027"
            ),
            evidence_level="published",
            source="Agence France Trésor",
            source_url=AFT_BTF_2027_03_10_URL,
            notes=(
                "The security is a conventional "
                "zero-coupon sovereign obligation "
                "redeemable at par at maturity. "
                "Secondary-market price risk before "
                "maturity remains a market-risk issue, "
                "not an additional investment-wrapper "
                "counterparty layer."
            ),
        ),
    )

    broker_observations = (
        build_ibkr_ireland_recommendation_risk_observations(
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observation_id_prefix=(
                "btf_2027_03_10"
            ),
        )
    )

    return (
        instrument_specific_observations
        + broker_observations
    )