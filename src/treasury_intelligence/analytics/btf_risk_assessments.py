from __future__ import annotations

from treasury_intelligence.analytics.btf_risk_evidence import (
    get_btf_2027_08_11_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)

from treasury_intelligence.sources.france import (
    BTF_2027_08_11,
    BTF_2027_08_11_MARKET,
)


BTF_2027_08_11_ASSESSED_AT = "2026-09-01"


def _observation_ids(
    observations: tuple[RiskObservation, ...],
    risk_dimension: str,
) -> tuple[str, ...]:
    return tuple(
        observation.observation_id
        for observation in observations
        if observation.risk_dimension
        == risk_dimension
    )


def get_btf_2027_08_11_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = (
        get_btf_2027_08_11_recommendation_risk_observations()
    )

    instrument_id = (
        BTF_2027_08_11.instrument_id
    )

    market_id = (
        BTF_2027_08_11_MARKET.market_id
    )

    return (
        RiskAssessment(
            assessment_id=(
                "fr_btf_2027_08_11_principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            risk_level="low",
            rationale=(
                "The security is a direct short-term "
                "obligation of the French Republic. "
                "France remains strongly investment-grade: "
                "Fitch affirmed its A+ sovereign rating "
                "with a Stable Outlook on 28 August 2026, "
                "while Agence France Trésor reports a "
                "broader set of major-agency sovereign "
                "ratings spanning A+ through the AA and "
                "AAA ranges. Sovereign default, fiscal "
                "deterioration and rating migration remain "
                "non-zero risks, supporting a low rather "
                "than very-low classification."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "principal_credit",
                )
            ),
            assessed_at=BTF_2027_08_11_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Low does not mean equivalent to insured "
                "cash or a risk-free asset. The assessment "
                "reflects strong investment-grade French "
                "sovereign credit quality together with "
                "non-zero fiscal, political, downgrade "
                "and sovereign-default risk."
            ),
        ),
        RiskAssessment(
            assessment_id=(
                "fr_btf_2027_08_11_market"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="market",
            risk_level="low",
            rationale=(
                "FR0129704187 is a short-dated "
                "zero-coupon French Treasury bill "
                "maturing on 11 August 2027. Its "
                "secondary-market price can change "
                "before maturity, but the short remaining "
                "term limits interest-rate sensitivity "
                "relative to longer-duration fixed-income "
                "securities."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "market",
                )
            ),
            assessed_at=BTF_2027_08_11_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                "fr_btf_2027_08_11_liquidity"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="liquidity",
            risk_level="unknown",
            rationale=(
                "Base liquidity remains intentionally "
                "ungraded because liquidity is "
                "position-size dependent. The position "
                "analysis separately evaluates the "
                "EUR 8.135 billion issue scale and can "
                "support strong inferred liquidity for "
                "positions sufficiently small relative "
                "to that scale."
            ),
            supporting_observation_ids=(),
            assessed_at=BTF_2027_08_11_ASSESSED_AT,
            evidence_sufficient=False,
            notes=(
                "Liquidity is excluded from the current "
                "base-risk mandate gate because the "
                "position-aware liquidity layer handles "
                "this dimension."
            ),
        ),
        RiskAssessment(
            assessment_id=(
                "fr_btf_2027_08_11_currency_asset"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="currency_asset",
            risk_level="very_low",
            rationale=(
                "The security is issued in EUR, matching "
                "the model treasury's EUR base currency. "
                "The position therefore introduces no "
                "material conventional foreign-exchange "
                "mismatch."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "currency_asset",
                )
            ),
            assessed_at=BTF_2027_08_11_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                "fr_btf_2027_08_11_"
                "structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            risk_level="low",
            rationale=(
                "The position is a direct French Republic "
                "Treasury bill rather than a fund share, "
                "structured product, derivative claim, "
                "tokenized wrapper or lending-protocol "
                "position. It therefore avoids material "
                "investment-wrapper and derivative-"
                "counterparty dependencies. Residual "
                "broker, custodian, depository, settlement "
                "and administrative dependencies remain, "
                "so structural risk is low rather than "
                "negligible or not applicable."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
            assessed_at=BTF_2027_08_11_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "This assessment does not assert that "
                "brokerage or settlement infrastructure "
                "cannot fail. It reflects the relatively "
                "simple direct-sovereign-security "
                "structure."
            ),
        ),
        RiskAssessment(
            assessment_id=(
                "fr_btf_2027_08_11_technical"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="technical",
            risk_level="not_applicable",
            rationale=(
                "No smart-contract, oracle, blockchain "
                "or protocol-level technical dependency "
                "is modeled for this conventional "
                "sovereign security. Ordinary brokerage "
                "and settlement infrastructure belongs "
                "to the structural or operational risk "
                "dimensions."
            ),
            supporting_observation_ids=(),
            assessed_at=BTF_2027_08_11_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                "fr_btf_2027_08_11_"
                "operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "operational_regulatory"
            ),
            risk_level="low",
            rationale=(
                "The modeled route uses a conventional "
                "regulated corporate brokerage to hold "
                "a conventional sovereign security. "
                "Existing IBKR Ireland recommendation "
                "evidence covers segregation, custody "
                "and reconciliation controls for the "
                "same brokerage architecture. These "
                "controls provide sufficient "
                "recommendation-stage evidence for a "
                "low operational and regulatory risk "
                "assessment while ordinary broker, "
                "custody, settlement, account-"
                "configuration and administrative "
                "risks remain."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "operational_regulatory",
                )
            ),
            assessed_at=BTF_2027_08_11_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Company-specific accounting, tax "
                "treatment, internal authorization, "
                "final account setup and instrument "
                "permissions remain execution-stage "
                "checks unless a specific restriction "
                "is discovered."
            ),
        ),
    )