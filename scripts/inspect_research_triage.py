from __future__ import annotations

from collections import Counter

from treasury_intelligence.analytics.discovery_screening import (
    screen_discovery_universe,
)
from treasury_intelligence.analytics.research_triage import (
    build_research_triage,
)
from treasury_intelligence.discovery_catalog import (
    build_expanded_discovery_catalog,
)
from treasury_intelligence.models.discovery_screening import (
    DiscoveryScreeningContext,
)
from treasury_intelligence.research_triage_catalog import (
    build_model_company_research_evidence_states,
)


def build_screening_context() -> DiscoveryScreeningContext:
    return DiscoveryScreeningContext(
        base_currency="EUR",
        treasury_capital_eur=5_000_000.0,
        minimum_useful_allocation_eur=100_000.0,
        allowed_currencies=("EUR",),
        require_verified_corporate_access=True,
    )


def main() -> None:
    opportunities = build_expanded_discovery_catalog()

    screening_results = screen_discovery_universe(
        opportunities=opportunities,
        context=build_screening_context(),
    )

    evidence_states = (
        build_model_company_research_evidence_states()
    )

    triage_results = build_research_triage(
        opportunities=opportunities,
        screening_results=screening_results,
        evidence_states=evidence_states,
    )

    action_counts = Counter(
        result.action
        for result in triage_results
    )

    print("===== RESEARCH TRIAGE =====")
    print(
        f"research_candidate_count={len(triage_results)}"
    )
    print(
        "reuse_existing_analysis="
        f"{action_counts.get('reuse_existing_analysis', 0)}"
    )
    print(
        "refresh_existing_analysis="
        f"{action_counts.get('refresh_existing_analysis', 0)}"
    )
    print(
        "complete_missing_analysis="
        f"{action_counts.get('complete_missing_analysis', 0)}"
    )

    print()
    print("===== ACTIVE RESEARCH QUEUE =====")

    active_queue = [
        result
        for result in triage_results
        if result.research_required
    ]

    for result in active_queue:
        print(
            f"{result.research_rank}. "
            f"{result.opportunity_id} | "
            f"{result.display_name} | "
            f"{result.action} | "
            f"priority={result.discovery_priority}"
        )

        print(
            "   missing="
            + ",".join(result.missing_evidence)
        )

    print()
    print("===== REUSABLE COMPLETE ANALYSES =====")

    reusable = [
        result
        for result in triage_results
        if not result.research_required
    ]

    for result in reusable:
        print(
            f"{result.opportunity_id} | "
            f"{result.display_name}"
        )

    print()
    print(
        f"active_research_count={len(active_queue)}"
    )
    print(
        f"reusable_complete_count={len(reusable)}"
    )


if __name__ == "__main__":
    main()