from __future__ import annotations

from treasury_intelligence.analytics.ishares_govt_0_1yr_risk_evidence import (
    get_ishares_govt_0_1yr_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


ISHARES_GOVT_0_1YR_ASSESSED_AT = "2026-09-02"


def _observation_ids(
    observations: tuple[RiskObservation, ...],
    risk_dimension: str,
) -> tuple[str, ...]:
    return tuple(
        observation.observation_id
        for observation in observations
        if observation.risk_dimension == risk_dimension
    )


def get_ishares_govt_0_1yr_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = (
        get_ishares_govt_0_1yr_recommendation_risk_observations()
    )

    instrument_id = observations[0].instrument_id
    market_id = observations[0].market_id

    return (
        RiskAssessment(
            assessment_id=(
                "ishares_govt_0_1yr_principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            risk_level="low",
            rationale=(
                "The portfolio focuses on short-dated, "
                "euro-denominated investment-grade eurozone "
                "government debt across multiple sovereign "
                "issuers. Sovereign credit deterioration and "
                "loss remain possible, and the ETF itself "
                "does not provide capital protection, so the "
                "position is not treated as risk-free."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "principal_credit",
                )
            ),
            assessed_at=ISHARES_GOVT_0_1YR_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id="ishares_govt_0_1yr_market",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="market",
            risk_level="low",
            rationale=(
                "Effective duration and weighted-average "
                "maturity of approximately 0.55 years limit "
                "interest-rate sensitivity relative to "
                "longer-duration government-bond portfolios. "
                "NAV and exchange price can nevertheless "
                "move with rates, sovereign spreads and "
                "market conditions."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "market",
                )
            ),
            assessed_at=ISHARES_GOVT_0_1YR_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id="ishares_govt_0_1yr_liquidity",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="liquidity",
            risk_level="unknown",
            rationale=(
                "Exact share-class AUM and verified Xetra "
                "market structure provide product-scale "
                "context but do not directly establish "
                "position-size executable exit depth. "
                "Liquidity is intentionally resolved by the "
                "generic position-aware ETF layer."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "liquidity",
                )
            ),
            assessed_at=ISHARES_GOVT_0_1YR_ASSESSED_AT,
            evidence_sufficient=False,
        ),
        RiskAssessment(
            assessment_id=(
                "ishares_govt_0_1yr_currency_asset"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="currency_asset",
            risk_level="very_low",
            rationale=(
                "The fund targets euro-denominated eurozone "
                "government debt and the exact accumulating "
                "share class trades on Xetra in EUR. This "
                "aligns with the model treasury's EUR base "
                "and avoids a material conventional FX "
                "mismatch."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "currency_asset",
                )
            ),
            assessed_at=ISHARES_GOVT_0_1YR_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                "ishares_govt_0_1yr_"
                "structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="structural_counterparty",
            risk_level="low",
            rationale=(
                "The instrument is a physically replicated "
                "Irish UCITS ETF with State Street "
                "Custodial Services (Ireland) Limited "
                "identified as custodian. Derivatives, "
                "securities lending, depositary and other "
                "counterparty dependencies remain possible, "
                "supporting a low rather than negligible "
                "structural risk assessment."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
            assessed_at=ISHARES_GOVT_0_1YR_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Low does not mean risk-free. Custodian, "
                "service-provider, securities-lending or "
                "derivative-counterparty failures can still "
                "cause loss."
            ),
        ),
        RiskAssessment(
            assessment_id="ishares_govt_0_1yr_technical",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="technical",
            risk_level="not_applicable",
            rationale=(
                "No smart-contract, oracle, blockchain or "
                "protocol-level technical dependency is "
                "modeled for this conventional UCITS ETF."
            ),
            supporting_observation_ids=(),
            assessed_at=ISHARES_GOVT_0_1YR_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                "ishares_govt_0_1yr_"
                "operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="operational_regulatory",
            risk_level="low",
            rationale=(
                "The modeled route uses an Irish UCITS ETF "
                "traded on Xetra through the already "
                "verified IBKR Ireland corporate brokerage "
                "route. Published broker segregation and "
                "custody controls provide sufficient V1 "
                "evidence while ordinary broker, custodian, "
                "settlement, onboarding and administrative "
                "risks remain."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "operational_regulatory",
                )
            ),
            assessed_at=ISHARES_GOVT_0_1YR_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Company-specific accounting, tax treatment, "
                "internal authorization and final account "
                "permissions remain execution-stage checks "
                "unless a specific restriction is discovered."
            ),
        ),
    )
