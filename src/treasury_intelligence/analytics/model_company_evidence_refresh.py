from __future__ import annotations

from treasury_intelligence.analytics.evidence_refresh import (
    build_evidence_refresh_plan,
)

from treasury_intelligence.analytics.universe_candidates import (
    build_model_company_freshness_dependency_sets,
)

from treasury_intelligence.models.evidence_refresh import (
    EvidenceRefreshPlan,
)

from treasury_intelligence.policies.freshness import (
    MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY,
)


def build_model_company_evidence_refresh_plan(
    *,
    as_of: str,
) -> EvidenceRefreshPlan:
    if not as_of:
        raise ValueError(
            "as_of is required."
        )

    return build_evidence_refresh_plan(
        plan_id=(
            "model_company_production_refresh_"
            f"{as_of.replace('-', '_')}"
        ),
        dependency_sets=(
            build_model_company_freshness_dependency_sets()
        ),
        requirements=(
            MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY
        ),
        as_of=as_of,
        notes=(
            "Production evidence-refresh worklist for "
            "the model-company opportunities governed "
            "by the recommendation freshness gate. "
            "Hard-blocked and otherwise non-gated "
            "opportunities are intentionally excluded."
        ),
    )
