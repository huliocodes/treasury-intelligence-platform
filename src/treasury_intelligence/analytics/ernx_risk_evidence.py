from __future__ import annotations

from treasury_intelligence.analytics.broker_risk_evidence import (
    build_ibkr_ireland_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.sources.ishares import (
    ERNX_INSTRUMENT,
    ERNX_MARKET,
)


ISHARES_ERNX_SOURCE_URL = (
    "https://www.ishares.com/uk/professionals/en/"
    "products/327355/"
    "ishares-ultrashort-bond-ucits-etf"
)


def get_ernx_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    instrument_specific_observations = (
        RiskObservation(
            observation_id=(
                "ernx_custodian"
            ),
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type="fund_custodian",
            value_text=(
                "State Street Custodial Services "
                "(Ireland) Limited"
            ),
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_ERNX_SOURCE_URL,
            notes=(
                "BlackRock identifies State Street "
                "Custodial Services (Ireland) Limited "
                "as custodian of the Irish UCITS ETF."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ernx_securities_lending_average_pct"
            ),
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-06-30",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "securities_lending_average_on_loan"
            ),
            value_numeric=4.25,
            unit="pct_of_aum",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_ERNX_SOURCE_URL,
            notes=(
                "BlackRock reports average securities "
                "on loan equal to 4.25% of AUM for the "
                "year ending 30 June 2026."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ernx_securities_lending_maximum_pct"
            ),
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-06-30",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "securities_lending_maximum_on_loan"
            ),
            value_numeric=6.67,
            unit="pct_of_aum",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_ERNX_SOURCE_URL,
            notes=(
                "BlackRock reports maximum securities "
                "on loan equal to 6.67% of AUM for the "
                "year ending 30 June 2026."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ernx_securities_lending_collateral_pct"
            ),
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-06-30",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "securities_lending_collateralisation"
            ),
            value_numeric=106.09,
            unit="pct_of_loan",
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_ERNX_SOURCE_URL,
            notes=(
                "BlackRock reports securities-lending "
                "collateralisation equal to 106.09% of "
                "the value of securities on loan for the "
                "year ending 30 June 2026."
            ),
        ),
        RiskObservation(
            observation_id=(
                "ernx_securities_lending_loss_mechanism"
            ),
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "securities_lending_loss_mechanism"
            ),
            value_text=(
                "Borrower default and collateral-value "
                "shortfall can cause loss"
            ),
            evidence_level="published",
            source="iShares / BlackRock",
            source_url=ISHARES_ERNX_SOURCE_URL,
            notes=(
                "BlackRock explicitly identifies loss "
                "risk if a securities-lending borrower "
                "defaults and collateral becomes "
                "insufficient because of market moves."
            ),
        ),
    )

    broker_observations = (
        build_ibkr_ireland_recommendation_risk_observations(
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observation_id_prefix="ernx",
        )
    )

    return (
        instrument_specific_observations
        + broker_observations
    )