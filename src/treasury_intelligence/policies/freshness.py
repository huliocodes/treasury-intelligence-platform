from __future__ import annotations

from treasury_intelligence.models.freshness import (
    EvidenceFreshnessRequirement,
)


MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY = (
    EvidenceFreshnessRequirement(
        evidence_type="market_return",
        maximum_age_days=7,
    ),
    EvidenceFreshnessRequirement(
        evidence_type="market_liquidity",
        maximum_age_days=7,
    ),
    EvidenceFreshnessRequirement(
        evidence_type="benchmark",
        maximum_age_days=3,
    ),
    EvidenceFreshnessRequirement(
        evidence_type="risk",
        maximum_age_days=30,
    ),
    EvidenceFreshnessRequirement(
        evidence_type="accessibility",
        maximum_age_days=90,
    ),
    EvidenceFreshnessRequirement(
        evidence_type="cost",
        maximum_age_days=90,
    ),
)


def get_model_company_freshness_requirement(
    evidence_type: str,
) -> EvidenceFreshnessRequirement:
    for requirement in (
        MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY
    ):
        if requirement.evidence_type == evidence_type:
            return requirement

    raise ValueError(
        "Unsupported model-company evidence freshness "
        f"type: {evidence_type}"
    )


MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY_NOTES = (
    "Production V1 evidence-freshness thresholds are "
    "explicit governance assumptions for recurring "
    "treasury review. They are not market conventions "
    "or claims about how frequently every underlying "
    "fact economically changes. Fast-moving return, "
    "liquidity and benchmark evidence receives shorter "
    "maximum ages than structural accessibility, cost "
    "and risk evidence."
)
