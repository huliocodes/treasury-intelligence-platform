from __future__ import annotations

from treasury_intelligence.analytics.broker_risk_evidence import (
    build_ibkr_ireland_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.sources.franklin import (
    FRANKLIN_EURO_SHORT_MATURITY_INSTRUMENT,
    FRANKLIN_EURO_SHORT_MATURITY_MARKET,
)


FRANKLIN_PRODUCT_SOURCE_URL = (
    "https://www.franklintempleton.lu/"
    "our-funds/price-and-performance-etfs/"
    "products/27049/ETA/"
    "franklin-euro-short-maturity-ucits-etf/"
    "IE000STIHQB2"
)

FRANKLIN_KID_SOURCE_URL = (
    "https://www.franklintempleton.lu/"
    "download/en-lu/key-information-document/"
    "bbb5df56-59f2-4daf-9ad5-aa90c47a9144/"
    "PRIIPSEU_IE000STIHQB2_en_LU.pdf"
)


def get_franklin_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    instrument_id = (
        FRANKLIN_EURO_SHORT_MATURITY_INSTRUMENT.instrument_id
    )

    market_id = (
        FRANKLIN_EURO_SHORT_MATURITY_MARKET.market_id
    )

    instrument_specific_observations = (
        RiskObservation(
            observation_id="franklin_credit_quality",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-27",
            risk_dimension="principal_credit",
            observation_type="average_credit_quality",
            value_text="AA-",
            evidence_level="published",
            source="Franklin Templeton",
            source_url=FRANKLIN_PRODUCT_SOURCE_URL,
            notes=(
                "Franklin reported average portfolio credit "
                "quality of AA-. Average quality is portfolio "
                "context and does not eliminate issuer-level "
                "credit risk."
            ),
        ),
        RiskObservation(
            observation_id="franklin_holdings_count",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-27",
            risk_dimension="principal_credit",
            observation_type="holdings_count",
            value_numeric=80,
            unit="securities",
            evidence_level="published",
            source="Franklin Templeton",
            source_url=FRANKLIN_PRODUCT_SOURCE_URL,
            notes=(
                "The portfolio held approximately 80 "
                "securities, providing diversification "
                "context without guaranteeing principal."
            ),
        ),
        RiskObservation(
            observation_id="franklin_credit_universe",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="principal_credit",
            observation_type="permitted_credit_exposure",
            value_text=(
                "Primarily investment-grade short-maturity "
                "EUR government and corporate debt"
            ),
            evidence_level="published",
            source="Franklin Templeton KID",
            source_url=FRANKLIN_KID_SOURCE_URL,
            notes=(
                "The KID states that the fund mainly invests "
                "in short-maturity EUR-denominated investment-"
                "grade corporate and government bonds. It may "
                "to a lesser extent hold lower-quality or "
                "defaulted debt and other permitted assets."
            ),
        ),
        RiskObservation(
            observation_id="franklin_no_capital_guarantee",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="principal_credit",
            observation_type="capital_guarantee",
            value_text="No capital guarantee",
            evidence_level="published",
            source="Franklin Templeton KID",
            source_url=FRANKLIN_KID_SOURCE_URL,
            notes=(
                "The KID explicitly states that invested "
                "capital is not guaranteed."
            ),
        ),
        RiskObservation(
            observation_id="franklin_effective_duration",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-27",
            risk_dimension="market",
            observation_type="effective_duration",
            value_numeric=0.76,
            unit="years",
            evidence_level="published",
            source="Franklin Templeton",
            source_url=FRANKLIN_PRODUCT_SOURCE_URL,
            notes=(
                "Effective duration is an observable "
                "interest-rate sensitivity measure rather "
                "than a qualitative risk rating."
            ),
        ),
        RiskObservation(
            observation_id="franklin_average_maturity",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-27",
            risk_dimension="market",
            observation_type="weighted_average_maturity",
            value_numeric=1.15,
            unit="years",
            evidence_level="published",
            source="Franklin Templeton",
            source_url=FRANKLIN_PRODUCT_SOURCE_URL,
        ),
        RiskObservation(
            observation_id="franklin_currency",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="currency_asset",
            observation_type="portfolio_currency_policy",
            value_text=(
                "Primarily EUR-denominated debt; "
                "Xetra share class trades in EUR"
            ),
            evidence_level="published",
            source="Franklin Templeton",
            source_url=FRANKLIN_KID_SOURCE_URL,
            notes=(
                "The KID describes the main investment "
                "universe as EUR-denominated corporate and "
                "government bonds. The exact share class "
                "also trades on Xetra in EUR."
            ),
        ),
        RiskObservation(
            observation_id="franklin_ucits_structure",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="structural_counterparty",
            observation_type="legal_structure",
            value_text="Irish UCITS ETF sub-fund",
            evidence_level="published",
            source="Franklin Templeton KID",
            source_url=FRANKLIN_KID_SOURCE_URL,
            notes=(
                "The fund is an Irish UCITS ETF sub-fund. "
                "The KID states that liabilities of sub-funds "
                "are segregated."
            ),
        ),
        RiskObservation(
            observation_id="franklin_depositary",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="structural_counterparty",
            observation_type="fund_depositary",
            value_text=(
                "The Bank of New York Mellon SA/NV, "
                "Dublin Branch"
            ),
            evidence_level="published",
            source="Franklin Templeton KID",
            source_url=FRANKLIN_KID_SOURCE_URL,
            notes=(
                "The KID identifies BNY Mellon as the "
                "depositary for the fund."
            ),
        ),
        RiskObservation(
            observation_id="franklin_counterparty_risk",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="structural_counterparty",
            observation_type="counterparty_risk",
            value_text=(
                "Derivative and counterparty default can "
                "cause loss"
            ),
            evidence_level="published",
            source="Franklin Templeton KID",
            source_url=FRANKLIN_KID_SOURCE_URL,
            notes=(
                "The KID explicitly identifies counterparty "
                "risk and permits derivatives within the "
                "investment strategy."
            ),
        ),
        RiskObservation(
            observation_id="franklin_aum",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="liquidity",
            observation_type="fund_aum",
            value_numeric=597_730_000.0,
            unit="EUR",
            evidence_level="published",
            source="Franklin Templeton",
            source_url=FRANKLIN_PRODUCT_SOURCE_URL,
            notes=(
                "Fund AUM provides scale context but does "
                "not establish position-size executable "
                "secondary-market liquidity."
            ),
        ),
    )

    broker_observations = (
        build_ibkr_ireland_recommendation_risk_observations(
            instrument_id=instrument_id,
            market_id=market_id,
            observation_id_prefix="franklin",
        )
    )

    return (
        instrument_specific_observations
        + broker_observations
    )
