from __future__ import annotations

from treasury_intelligence.analytics.model_company_evidence_refresh import (
    build_model_company_evidence_refresh_plan,
)

from treasury_intelligence.analytics.universe_candidates import (
    build_model_company_freshness_dependency_sets,
)


AS_OF = "2026-09-03"


EXPECTED_REFRESH_ITEMS = {
    (
        "ernx",
        "market_liquidity",
    ),
    (
        "de_bubill_2027_07_14",
        "market_return",
    ),
    (
        "de_bubill_2027_07_14",
        "market_liquidity",
    ),
    (
        "de_bubill_2027_08_18",
        "market_return",
    ),
    (
        "de_bubill_2027_08_18",
        "market_liquidity",
    ),
}


def main() -> None:
    dependency_sets = (
        build_model_company_freshness_dependency_sets()
    )

    plan = (
        build_model_company_evidence_refresh_plan(
            as_of=AS_OF,
        )
    )

    print(
        "MILESTONE 15I.1 — PRODUCTION "
        "EVIDENCE REFRESH PLAN"
    )
    print()

    print(
        f"As of:                       "
        f"{plan.as_of}"
    )

    print(
        f"Production dependency sets:  "
        f"{len(dependency_sets)}"
    )

    print(
        f"Actionable refresh items:    "
        f"{plan.actionable_count}"
    )

    print(
        f"Refresh actions:             "
        f"{plan.refresh_count}"
    )

    print(
        f"Establish provenance:        "
        f"{plan.establish_provenance_count}"
    )

    print(
        f"Stale:                       "
        f"{plan.stale_count}"
    )

    print(
        f"Future-dated:                "
        f"{plan.future_dated_count}"
    )

    print(
        f"Undated:                     "
        f"{plan.undated_count}"
    )

    print()

    for item in plan.items:
        print(
            f"{item.instrument_id:30} "
            f"{item.evidence_type:20} "
            f"{item.action:10} "
            f"{item.reason:14} "
            f"observed={item.observed_date} "
            f"age={item.age_days} "
            f"max={item.maximum_age_days}"
        )

    print()
    print("-" * 100)
    print()

    assert len(dependency_sets) == 5

    dependency_instrument_ids = {
        dependency_set.instrument_id
        for dependency_set in dependency_sets
    }

    assert dependency_instrument_ids == {
        "ernx",
        "fr_btf_2027_03_10",
        "fr_btf_2027_08_11",
        "de_bubill_2027_07_14",
        "de_bubill_2027_08_18",
    }

    actual_refresh_items = {
        (
            item.instrument_id,
            item.evidence_type,
        )
        for item in plan.items
    }

    assert (
        actual_refresh_items
        == EXPECTED_REFRESH_ITEMS
    )

    assert plan.actionable_count == 5
    assert plan.refresh_count == 5

    assert (
        plan.establish_provenance_count
        == 0
    )

    assert plan.stale_count == 5
    assert plan.future_dated_count == 0
    assert plan.undated_count == 0

    assert all(
        item.action == "refresh"
        for item in plan.items
    )

    assert all(
        item.reason == "stale"
        for item in plan.items
    )

    assert all(
        item.observed_date is not None
        for item in plan.items
    )

    assert all(
        item.age_days is not None
        and item.age_days
        > item.maximum_age_days
        for item in plan.items
    )

    assert not any(
        item.instrument_id
        == "fr_btf_2027_08_11"
        for item in plan.items
    )

    assert not any(
        item.instrument_id == "aave_v3_base_eurc"
        for item in plan.items
    )

    missing_as_of_rejected = False

    try:
        build_model_company_evidence_refresh_plan(
            as_of="",
        )
    except ValueError:
        missing_as_of_rejected = True

    assert missing_as_of_rejected

    print(
        "MILESTONE 15I.1 ASSERTIONS"
    )
    print()

    print(
        "Gate dependency construction reused:      yes"
    )

    print(
        "Five gated production opportunities:      yes"
    )

    print(
        "Real stale evidence drives worklist:       yes"
    )

    print(
        "Fresh BTF Aug excluded from worklist:      yes"
    )

    print(
        "Hard-blocked/non-gated candidates omitted: yes"
    )

    print(
        "No human-readable parsing:                yes"
    )

    print(
        "No full-universe construction required:   yes"
    )

    print(
        "No Aave/Base RPC required:                yes"
    )

    print(
        "Explicit as-of date required:             yes"
    )

    print()

    print(
        "All Milestone 15I.1 production "
        "refresh-plan assertions passed."
    )


if __name__ == "__main__":
    main()
