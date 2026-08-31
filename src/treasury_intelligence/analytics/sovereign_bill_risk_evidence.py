from __future__ import annotations

from treasury_intelligence.analytics.broker_risk_evidence import (
    build_ibkr_ireland_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)


def build_direct_sovereign_bill_recommendation_risk_observations(
    *,
    instrument_id: str,
    market_id: str,
    observation_id_prefix: str,
    issuer_name: str,
    instrument_name: str,
    maturity_date_text: str,
    source_name: str,
    source_url: str,
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

    if not issuer_name:
        raise ValueError(
            "issuer_name is required."
        )

    if not instrument_name:
        raise ValueError(
            "instrument_name is required."
        )

    if not maturity_date_text:
        raise ValueError(
            "maturity_date_text is required."
        )

    if not source_name:
        raise ValueError(
            "source_name is required."
        )

    if not source_url:
        raise ValueError(
            "source_url is required."
        )

    sovereign_structure_observations = (
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "direct_sovereign_security"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "direct_sovereign_security_structure"
            ),
            value_text=(
                f"Direct {issuer_name} sovereign "
                "security with no fund or derivative "
                "wrapper"
            ),
            evidence_level="published",
            source=source_name,
            source_url=source_url,
            notes=(
                f"{source_name} identifies "
                f"{instrument_name} as a direct "
                f"obligation of {issuer_name}. "
                "The modeled position therefore does "
                "not depend on a fund issuer, swap "
                "counterparty, token issuer, lending "
                "protocol, or other investment wrapper "
                "for its principal economic claim."
            ),
        ),
        RiskObservation(
            observation_id=(
                f"{observation_id_prefix}_"
                "redemption_structure"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension=(
                "structural_counterparty"
            ),
            observation_type=(
                "sovereign_bill_redemption_structure"
            ),
            value_text=(
                "Zero-coupon sovereign bill redeemed "
                f"at par on {maturity_date_text}"
            ),
            evidence_level="published",
            source=source_name,
            source_url=source_url,
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
            instrument_id=instrument_id,
            market_id=market_id,
            observation_id_prefix=(
                observation_id_prefix
            ),
        )
    )

    return (
        sovereign_structure_observations
        + broker_observations
    )