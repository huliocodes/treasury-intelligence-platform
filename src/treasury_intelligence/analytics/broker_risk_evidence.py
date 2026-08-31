from __future__ import annotations

from treasury_intelligence.models.risk import (
    RiskObservation,
)


IBKR_IRELAND_CLIENT_PROTECTION_URL = (
    "https://www.interactivebrokers.ie/en/general/"
    "security-investor-protection.php"
)

IBKR_IRELAND_FINANCIAL_STRENGTH_URL = (
    "https://www.interactivebrokers.ie/en/general/"
    "financial-strength.php"
)


def build_ibkr_ireland_recommendation_risk_observations(
    *,
    instrument_id: str,
    market_id: str,
    observation_id_prefix: str,
) -> tuple[RiskObservation, ...]:
    if not instrument_id:
        raise ValueError(
            "instrument_id is required."
        )

    if not market_id:
        raise ValueError(
            "market_id is required."
        )

    if not observation_id_prefix:
        raise ValueError(
            "observation_id_prefix is required."
        )

    return (
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "ibkr_client_money_segregation"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "operational_regulatory"
            ),
            observation_type=(
                "broker_client_money_segregation"
            ),
            value_text=(
                "IBKR Ireland segregates client money "
                "for the exclusive benefit of clients"
            ),
            evidence_level="published",
            source="Interactive Brokers Ireland",
            source_url=(
                IBKR_IRELAND_CLIENT_PROTECTION_URL
            ),
            notes=(
                "IBKR Ireland states that client money "
                "is maintained in segregated client "
                "accounts rather than commingled with "
                "the broker's own funds."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "ibkr_fully_paid_securities_custody"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "operational_regulatory"
            ),
            observation_type=(
                "broker_securities_custody"
            ),
            value_text=(
                "Fully paid client securities are held "
                "at depositories and custodians for the "
                "exclusive benefit of clients"
            ),
            evidence_level="published",
            source="Interactive Brokers Ireland",
            source_url=(
                IBKR_IRELAND_CLIENT_PROTECTION_URL
            ),
            notes=(
                "This supports the modeled "
                "self-directed corporate brokerage "
                "custody route. It does not eliminate "
                "broker, custodian, settlement, or "
                "administrative risk."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "ibkr_daily_reconciliation"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "operational_regulatory"
            ),
            observation_type=(
                "broker_daily_reconciliation"
            ),
            value_text=(
                "IBKR Ireland reconciles client money "
                "and securities positions daily"
            ),
            evidence_level="published",
            source="Interactive Brokers Ireland",
            source_url=(
                IBKR_IRELAND_CLIENT_PROTECTION_URL
            ),
            notes=(
                "IBKR Ireland states that client money "
                "and customer-owned securities positions "
                "are reconciled daily. This is a "
                "recommendation-stage operational control "
                "rather than proof of a specific future "
                "corporate account configuration."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "ibkr_client_asset_regulation"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "operational_regulatory"
            ),
            observation_type=(
                "broker_client_asset_regulation"
            ),
            value_text=(
                "IBKR Ireland client assets are subject "
                "to Irish client-asset segregation and "
                "reconciliation requirements"
            ),
            evidence_level="published",
            source="Interactive Brokers Ireland",
            source_url=(
                IBKR_IRELAND_FINANCIAL_STRENGTH_URL
            ),
            notes=(
                "IBKR Ireland identifies segregation, "
                "designation and registration, daily "
                "reconciliation, daily calculation, "
                "risk management, and annual external "
                "examination among its client-asset "
                "control principles."
            ),
        ),
    )