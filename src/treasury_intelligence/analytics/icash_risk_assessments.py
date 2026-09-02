from __future__ import annotations

from treasury_intelligence.analytics.icash_risk_evidence import (
    get_icash_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


ICASH_ASSESSED_AT = "2026-09-02"


def _observation_ids(
    observations: tuple[RiskObservation, ...],
    risk_dimension: str,
) -> tuple[str, ...]:
    return tuple(
        observation.observation_id
        for observation in observations
        if observation.risk_dimension == risk_dimension
    )


def get_icash_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = (
        get_icash_recommendation_risk_observations()
    )

    instrument_id = observations[0].instrument_id
    market_id = observations[0].market_id

    return (
        RiskAssessment(
            assessment_id="icash_principal_credit",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            risk_level="low",
            rationale=(
                "The current portfolio is dominated by "
                "short French Treasury bills with the "
                "remainder primarily in bank deposits. "
                "This supports low principal-credit risk, "
                "but sovereign, bank and fund losses remain "
                "possible and capital is not guaranteed."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "principal_credit",
                )
            ),
            assessed_at=ICASH_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id="icash_market",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="market",
            risk_level="low",
            rationale=(
                "The portfolio has a very short money-market "
                "maturity profile, materially limiting "
                "interest-rate sensitivity. ETF NAV and "
                "secondary-market price can nevertheless "
                "move, so market risk is not treated as "
                "negligible."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "market",
                )
            ),
            assessed_at=ICASH_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id="icash_liquidity",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="liquidity",
            risk_level="unknown",
            rationale=(
                "The fund is exchange listed and has a "
                "market maker, but published minimum quote "
                "obligations are small relative to corporate "
                "treasury allocations. Position-size "
                "liquidity is therefore resolved by the "
                "generic position-aware ETF layer rather "
                "than claimed at base risk level."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "liquidity",
                )
            ),
            assessed_at=ICASH_ASSESSED_AT,
            evidence_sufficient=False,
        ),
        RiskAssessment(
            assessment_id="icash_currency_asset",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="currency_asset",
            risk_level="very_low",
            rationale=(
                "The fund and LJSE trading currency are EUR, "
                "aligning with the model company's EUR "
                "treasury mandate without a material "
                "conventional FX mismatch."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "currency_asset",
                )
            ),
            assessed_at=ICASH_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                "icash_structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="structural_counterparty",
            risk_level="low",
            rationale=(
                "ICASH is a regulated UCITS ETF with a "
                "separate depositary. Fund, depositary, bank, "
                "derivative and other counterparty "
                "dependencies remain possible, supporting "
                "a low rather than negligible structural "
                "risk assessment."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
            assessed_at=ICASH_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id="icash_technical",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="technical",
            risk_level="not_applicable",
            rationale=(
                "No blockchain, smart-contract, oracle or "
                "protocol-level technical dependency is "
                "modeled for this conventional UCITS ETF."
            ),
            supporting_observation_ids=(),
            assessed_at=ICASH_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                "icash_operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="operational_regulatory",
            risk_level="low",
            rationale=(
                "ICASH is a regulated UCITS ETF listed on "
                "the Ljubljana Stock Exchange and a "
                "Slovenian corporate brokerage route through "
                "LJSE members is supported. Ordinary broker, "
                "custody, settlement, onboarding and "
                "administrative risks remain."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "operational_regulatory",
                )
            ),
            assessed_at=ICASH_ASSESSED_AT,
            evidence_sufficient=True,
        ),
    )
