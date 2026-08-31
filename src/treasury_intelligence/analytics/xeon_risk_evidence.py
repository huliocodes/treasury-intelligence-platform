from __future__ import annotations

from treasury_intelligence.analytics.broker_risk_evidence import (
    build_ibkr_ireland_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_INSTRUMENT,
    XEON_MARKET,
)


XTRACKERS_XEON_FACTSHEET_URL = (
    "https://etf.dws.com/download/asset/"
    "42e11275-ddf0-45d2-8319-ad55635c3a08"
)

XTRACKERS_ETF_FAQ_URL = (
    "https://etf.dws.com/en-gb/knowledge/"
    "faq-etfs/"
)

XTRACKERS_ETF_RISK_FACTORS_URL = (
    "https://etf.dws.com/en-us/"
    "risks-and-terms/etf-risk-factors/"
)


def get_xeon_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    instrument_specific_observations = (
        RiskObservation(
            observation_id=(
                "xeon_indirect_swap_replication"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "replication_method"
            ),
            value_text=(
                "Indirect replication using swaps"
            ),
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=(
                XTRACKERS_XEON_FACTSHEET_URL
            ),
            notes=(
                "The XEON factsheet identifies the "
                "portfolio methodology as Indirect "
                "Replication (Swap)."
            ),
        ),
        RiskObservation(
            observation_id=(
                "xeon_fund_custodian"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type="fund_custodian",
            value_text=(
                "State Street Bank International GmbH, "
                "Luxembourg Branch"
            ),
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=(
                XTRACKERS_XEON_FACTSHEET_URL
            ),
            notes=(
                "The XEON factsheet identifies State "
                "Street Bank International GmbH, "
                "Luxembourg Branch as custodian."
            ),
        ),
        RiskObservation(
            observation_id=(
                "xeon_ucits_single_counterparty_limit"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-31",
            risk_dimension="principal_credit",
            observation_type=(
                "swap_counterparty_exposure_limit"
            ),
            value_numeric=10.0,
            unit="pct_of_nav",
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=XTRACKERS_ETF_FAQ_URL,
            notes=(
                "DWS states that Xtrackers UCITS ETFs "
                "may be exposed to a maximum of 10% net "
                "counterparty risk on transactions with "
                "a single counterparty in accordance "
                "with UCITS investment restrictions."
            ),
        ),
        RiskObservation(
            observation_id=(
                "xeon_swap_counterparty_default_loss"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-31",
            risk_dimension="principal_credit",
            observation_type=(
                "swap_counterparty_default_loss"
            ),
            value_numeric=10.0,
            unit="pct_of_nav",
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=(
                XTRACKERS_ETF_RISK_FACTORS_URL
            ),
            notes=(
                "DWS states that if the financial "
                "institution acting as OTC derivative "
                "counterparty defaults, an indirectly "
                "replicated Xtrackers UCITS ETF may be "
                "liquidated and investors could lose "
                "up to 10% of ETF NAV from that "
                "counterparty-default mechanism."
            ),
        ),
        RiskObservation(
            observation_id=(
                "xeon_swap_default_trading_disruption"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "counterparty_default_operational_effect"
            ),
            value_text=(
                "Counterparty default may cause dealing "
                "suspension or fund liquidation"
            ),
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=XTRACKERS_ETF_FAQ_URL,
            notes=(
                "DWS states that failure by a derivative "
                "counterparty can cause losses, impair "
                "the ETF's investment objective, and "
                "may lead to suspension of dealings."
            ),
        ),
        RiskObservation(
            observation_id=(
                "xeon_emir_collateral_mitigation"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "swap_collateral_mitigation"
            ),
            value_text=(
                "EMIR requires collateral exchange to "
                "reduce OTC derivative counterparty "
                "exposure, subject to a minimum "
                "transfer amount"
            ),
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=XTRACKERS_ETF_FAQ_URL,
            notes=(
                "DWS describes EMIR risk-mitigation "
                "procedures requiring counterparties "
                "to exchange collateral to reduce OTC "
                "swap counterparty exposure. DWS also "
                "notes a EUR 500,000-equivalent minimum "
                "transfer amount, so this control does "
                "not establish zero loss risk."
            ),
        ),
    )

    broker_observations = (
        build_ibkr_ireland_recommendation_risk_observations(
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observation_id_prefix="xeon",
        )
    )

    return (
        instrument_specific_observations
        + broker_observations
    )