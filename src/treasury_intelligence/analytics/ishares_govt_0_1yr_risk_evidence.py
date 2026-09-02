from __future__ import annotations

from treasury_intelligence.analytics.broker_risk_evidence import (
    build_ibkr_ireland_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.sources.ishares_govt_0_1yr import (
    ISHARES_GOVT_0_1YR_INSTRUMENT,
    ISHARES_GOVT_0_1YR_MARKET,
)


ISHARES_GOVT_0_1YR_SOURCE_URL = (
    "https://www.ishares.com/uk/individual/en/"
    "products/345319/"
)

ISHARES_GOVT_0_1YR_KID_SOURCE_URL = (
    "https://www.blackrock.com/gls-download/"
    "literature/kiid/"
    "eu-priips-ishares-govt-bond-0-1yr-ucits-etf-"
    "eur-acc-ie000wv38gp5-en.pdf"
)


def get_ishares_govt_0_1yr_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    instrument_id = (
        ISHARES_GOVT_0_1YR_INSTRUMENT.instrument_id
    )

    market_id = (
        ISHARES_GOVT_0_1YR_MARKET.market_id
    )

    instrument_specific_observations = (
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_sovereign_universe"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="principal_credit",
            observation_type="investment_universe",
            value_text=(
                "Euro-denominated investment-grade "
                "eurozone government bonds with "
                "0-12 months remaining maturity"
            ),
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_SOURCE_URL,
            notes=(
                "The tracked short Treasury universe is "
                "government-focused and investment-grade. "
                "Sovereign credit deterioration and loss "
                "remain possible."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_holdings_count"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="principal_credit",
            observation_type="holdings_count",
            value_numeric=37.0,
            unit="securities",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_SOURCE_URL,
            notes=(
                "The portfolio contains multiple short-dated "
                "eurozone sovereign securities rather than "
                "one direct sovereign obligation."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_effective_duration"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="market",
            observation_type="effective_duration",
            value_numeric=0.55,
            unit="years",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_SOURCE_URL,
            notes=(
                "Short effective duration limits, but does "
                "not eliminate, interest-rate sensitivity."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_average_maturity"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="market",
            observation_type="weighted_average_maturity",
            value_numeric=0.55,
            unit="years",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_SOURCE_URL,
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_share_class_aum"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-28",
            risk_dimension="liquidity",
            observation_type="share_class_aum",
            value_numeric=161_470_000.0,
            unit="EUR",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_SOURCE_URL,
            notes=(
                "Exact accumulating share-class scale is "
                "relevant to position-size liquidity "
                "inference. It does not by itself prove "
                "immediate executable exit depth."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_eur_exposure"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="currency_asset",
            observation_type="portfolio_currency_policy",
            value_text=(
                "Euro-denominated eurozone government bonds"
            ),
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_SOURCE_URL,
            notes=(
                "The portfolio mandate and Xetra trading "
                "currency align with the EUR-based model "
                "treasury."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_replication_method"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="structural_counterparty",
            observation_type="replication_method",
            value_text="Physical sampled replication",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_SOURCE_URL,
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_custodian"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="structural_counterparty",
            observation_type="fund_custodian",
            value_text=(
                "State Street Custodial Services "
                "(Ireland) Limited"
            ),
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_KID_SOURCE_URL,
            notes=(
                "The Irish UCITS custody structure provides "
                "asset-segregation protections while "
                "custodian and service-provider failure "
                "remain possible."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_structural_risks"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="structural_counterparty",
            observation_type="fund_structural_risk",
            value_text=(
                "Derivatives, securities lending, "
                "depositary and counterparty dependencies"
            ),
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_KID_SOURCE_URL,
            notes=(
                "The KID identifies counterparty-related "
                "dependencies. Physical replication therefore "
                "does not make structural risk negligible."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ishares_govt_0_1yr_ucits_structure"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="operational_regulatory",
            observation_type="regulated_fund_structure",
            value_text="Irish UCITS ETF",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_GOVT_0_1YR_KID_SOURCE_URL,
        ),
    )

    broker_observations = (
        build_ibkr_ireland_recommendation_risk_observations(
            instrument_id=instrument_id,
            market_id=market_id,
            observation_id_prefix="ishares_govt_0_1yr",
        )
    )

    return (
        instrument_specific_observations
        + broker_observations
    )
