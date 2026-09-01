from __future__ import annotations

from collections import Counter

from treasury_intelligence.analytics.discovery_screening import (
    screen_discovery_universe,
)
from treasury_intelligence.discovery_catalog import (
    build_expanded_discovery_catalog,
)
from treasury_intelligence.models.discovery_screening import (
    DiscoveryScreeningContext,
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
    context = build_screening_context()
    opportunities = build_expanded_discovery_catalog()

    results = screen_discovery_universe(
        opportunities=opportunities,
        context=context,
    )

    opportunity_by_id = {
        opportunity.opportunity_id: opportunity
        for opportunity in opportunities
    }

    status_counts = Counter(
        result.status
        for result in results
    )

    category_counts = Counter(
        opportunity.category
        for opportunity in opportunities
    )

    strategy_counts = Counter(
        opportunity.strategy_id
        for opportunity in opportunities
    )

    print("===== EXPANDED DISCOVERY SCREENING =====")
    print(
        f"treasury_capital_eur={context.treasury_capital_eur:,.0f}"
    )
    print(
        "minimum_useful_allocation_eur="
        f"{context.minimum_useful_allocation_eur:,.0f}"
    )
    print(
        "require_verified_corporate_access="
        f"{context.require_verified_corporate_access}"
    )
    print(
        f"opportunity_count={len(opportunities)}"
    )
    print(
        f"strategy_count={len(strategy_counts)}"
    )
    print(
        f"category_count={len(category_counts)}"
    )

    print()
    print("===== SCREENING RESULTS =====")

    for result in results:
        opportunity = opportunity_by_id[result.opportunity_id]

        print(
            f"{result.opportunity_id}: "
            f"{result.status} | "
            f"priority={result.research_priority} | "
            f"category={result.category} | "
            f"strategy={opportunity.strategy_id} | "
            f"implementation={opportunity.implementation_id}"
        )

        for reason in result.screening_reasons:
            print(f"  reason: {reason}")

        for requirement in result.evidence_requirements:
            print(f"  evidence: {requirement}")

    print()
    print("===== STATUS COUNTS =====")

    for status in (
        "research_candidate",
        "access_unknown",
        "access_blocked",
        "screened_out",
        "discovered",
    ):
        print(
            f"{status}={status_counts.get(status, 0)}"
        )

    print()
    print("===== CATEGORY COUNTS =====")

    for category in sorted(category_counts):
        print(
            f"{category}={category_counts[category]}"
        )

    print()
    print("===== RESEARCH CANDIDATES =====")

    research_candidates = [
        result
        for result in results
        if result.suitable_for_full_research
    ]

    for result in research_candidates:
        print(
            f"{result.opportunity_id} | "
            f"{result.display_name} | "
            f"priority={result.research_priority}"
        )

    print()
    print(
        "research_candidate_count="
        f"{len(research_candidates)}"
    )


if __name__ == "__main__":
    main()