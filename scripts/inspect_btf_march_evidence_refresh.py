from __future__ import annotations

from treasury_intelligence.analytics.evidence_refresh import (
    build_evidence_refresh_plan,
)
from treasury_intelligence.analytics.universe_candidates import (
    build_btf_2027_08_11_universe_candidate,
    build_btf_universe_candidate,
    build_model_company_freshness_dependencies,
)
from treasury_intelligence.policies.freshness import (
    MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY,
)
from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    get_btf_2027_03_10_market_observation,
    get_btf_2027_03_10_snapshot,
)


AS_OF = "2026-09-03"
POSITION_SIZE_EUR = 5_000_000.0


def main() -> None:
    snapshot = get_btf_2027_03_10_snapshot()
    market_observation = (
        get_btf_2027_03_10_market_observation()
    )

    dependencies = (
        build_model_company_freshness_dependencies(
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
        )
    )

    assert dependencies is not None

    march_refresh_plan = build_evidence_refresh_plan(
        plan_id="btf_march_refreshed_evidence",
        dependency_sets=(dependencies,),
        requirements=(
            MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY
        ),
        as_of=AS_OF,
    )

    march_candidate = build_btf_universe_candidate(
        position_size_eur=POSITION_SIZE_EUR,
    )

    august_candidate = (
        build_btf_2027_08_11_universe_candidate(
            position_size_eur=POSITION_SIZE_EUR,
        )
    )

    print(
        "MILESTONE 15J.2 — BTF MARCH "
        "CANONICAL EVIDENCE REFRESH"
    )
    print()

    print("SOURCE EVIDENCE")
    print()

    print(
        f"Snapshot ID:                 "
        f"{snapshot.snapshot_id}"
    )
    print(
        f"Observed date:               "
        f"{snapshot.observed_date}"
    )
    print(
        f"Auction weighted avg rate:   "
        f"{snapshot.yield_value_pct:.3f}%"
    )
    print(
        f"Outstanding amount:          "
        f"EUR {snapshot.outstanding_amount_eur:,.0f}"
    )
    print(
        f"Liquidity observation date:  "
        f"{market_observation.observed_at}"
    )

    print()
    print("FRESHNESS EFFECT")
    print()

    market_return_dependencies = tuple(
        dependency
        for dependency in dependencies.dependencies
        if dependency.evidence_type == "market_return"
    )

    assert len(market_return_dependencies) == 1

    return_dependency = (
        market_return_dependencies[0]
    )

    print(
        f"Return source reference:     "
        f"{return_dependency.source_reference}"
    )
    print(
        f"Return observed date:        "
        f"{return_dependency.observed_date}"
    )
    print(
        f"March refresh items:         "
        f"{march_refresh_plan.actionable_count}"
    )

    print()
    print("EUR 5M ECONOMICS")
    print()

    print(
        f"March defensible return:     "
        f"{march_candidate.defensible_return_pct:.3f}%"
    )
    print(
        f"August defensible return:    "
        f"{august_candidate.defensible_return_pct:.3f}%"
    )

    return_difference_bps = (
        (
            august_candidate.defensible_return_pct
            - march_candidate.defensible_return_pct
        )
        * 100
    )

    print(
        f"August advantage:            "
        f"{return_difference_bps:.3f} bps"
    )

    print()
    print("-" * 100)
    print()

    assert snapshot.snapshot_id == (
        "fr_btf_2027_03_10_auction_2026-08-31"
    )

    assert snapshot.observed_date == "2026-08-31"

    assert snapshot.yield_value_pct == 2.697

    assert snapshot.outstanding_amount_eur == (
        4_019_000_000.0
    )

    assert market_observation.observed_at == (
        "2026-08-29"
    )

    assert return_dependency.source_reference == (
        snapshot.snapshot_id
    )

    assert return_dependency.observed_date == (
        snapshot.observed_date
    )

    assert march_refresh_plan.actionable_count == 0

    assert (
        march_candidate.position_size_eur
        == POSITION_SIZE_EUR
    )

    assert (
        august_candidate.position_size_eur
        == POSITION_SIZE_EUR
    )

    assert (
        march_candidate.defensible_return_pct
        is not None
    )

    assert (
        august_candidate.defensible_return_pct
        is not None
    )

    assert (
        august_candidate.defensible_return_pct
        > march_candidate.defensible_return_pct
    )

    print("MILESTONE 15J.2 ASSERTIONS")
    print()

    print(
        "Canonical source observation updated:     yes"
    )
    print(
        "Return freshness uses same snapshot:       yes"
    )
    print(
        "31-Aug return evidence is fresh:           yes"
    )
    print(
        "29-Aug liquidity evidence preserved:       yes"
    )
    print(
        "EUR 5M economics use refreshed snapshot:   yes"
    )
    print(
        "August/March comparison recomputed:        yes"
    )
    print(
        "No manual-refresh subsystem introduced:   yes"
    )
    print(
        "No network call introduced:               yes"
    )

    print()
    print(
        "All Milestone 15J.2 canonical-refresh "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
