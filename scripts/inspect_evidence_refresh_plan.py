from __future__ import annotations

from treasury_intelligence.analytics.evidence_refresh import (
    build_evidence_refresh_plan,
)

from treasury_intelligence.models.freshness import (
    EvidenceFreshnessRequirement,
)

from treasury_intelligence.models.freshness_dependencies import (
    EvidenceFreshnessDependency,
    OpportunityFreshnessDependencies,
)

from treasury_intelligence.policies.freshness import (
    MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY,
)


AS_OF = "2026-09-03"


def build_dependency_set(
    *,
    instrument_id: str,
    evidence_type: str,
    observed_date: str | None,
    source_reference: str,
) -> OpportunityFreshnessDependencies:
    return OpportunityFreshnessDependencies(
        instrument_id=instrument_id,
        market_id=f"{instrument_id}_market",
        access_route_id=(
            f"{instrument_id}_access"
        ),
        dependencies=(
            EvidenceFreshnessDependency(
                dependency_id=(
                    f"{instrument_id}_"
                    f"{evidence_type}"
                ),
                instrument_id=instrument_id,
                market_id=(
                    f"{instrument_id}_market"
                ),
                access_route_id=(
                    f"{instrument_id}_access"
                ),
                evidence_type=evidence_type,
                source_reference=(
                    source_reference
                ),
                observed_date=observed_date,
                required_for_recommendation=True,
            ),
        ),
    )


def main() -> None:
    requirements = (
        MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY
    )

    dependency_sets = (
        build_dependency_set(
            instrument_id="ernx",
            evidence_type="market_liquidity",
            observed_date="2026-08-21",
            source_reference=(
                "ernx_market_observation"
            ),
        ),
        build_dependency_set(
            instrument_id="fr_btf_2027_03_10",
            evidence_type="market_return",
            observed_date="2026-08-24",
            source_reference=(
                "fr_btf_mar_snapshot"
            ),
        ),
        build_dependency_set(
            instrument_id="fr_btf_2027_08_11",
            evidence_type="market_return",
            observed_date="2026-08-31",
            source_reference=(
                "fr_btf_aug_snapshot"
            ),
        ),
        build_dependency_set(
            instrument_id="de_bubill_2027_07_14",
            evidence_type="market_return",
            observed_date="2026-08-24",
            source_reference=(
                "de_bubill_jul_snapshot"
            ),
        ),
        build_dependency_set(
            instrument_id="de_bubill_2027_07_14",
            evidence_type="market_liquidity",
            observed_date="2026-08-24",
            source_reference=(
                "de_bubill_jul_market"
            ),
        ),
        build_dependency_set(
            instrument_id="de_bubill_2027_08_18",
            evidence_type="market_return",
            observed_date="2026-08-17",
            source_reference=(
                "de_bubill_aug_snapshot"
            ),
        ),
        build_dependency_set(
            instrument_id="de_bubill_2027_08_18",
            evidence_type="market_liquidity",
            observed_date="2026-08-17",
            source_reference=(
                "de_bubill_aug_market"
            ),
        ),
        build_dependency_set(
            instrument_id="undated_access_fixture",
            evidence_type="accessibility",
            observed_date=None,
            source_reference=(
                "corporate_access_source"
            ),
        ),
        build_dependency_set(
            instrument_id="future_cost_fixture",
            evidence_type="cost",
            observed_date="2026-09-04",
            source_reference=(
                "broker_cost_source"
            ),
        ),
    )

    plan = build_evidence_refresh_plan(
        plan_id=(
            "model_company_refresh_plan_"
            "2026_09_03"
        ),
        dependency_sets=dependency_sets,
        requirements=requirements,
        as_of=AS_OF,
        notes=(
            "Milestone 15I deterministic "
            "refresh-plan inspection."
        ),
    )

    print(
        "MILESTONE 15I — STRUCTURED "
        "EVIDENCE REFRESH PLAN"
    )
    print()

    print(
        f"As of:                       "
        f"{plan.as_of}"
    )

    print(
        f"Actionable items:            "
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
            f"{item.action:22} "
            f"{item.reason}"
        )

    item_map = {
        (
            item.instrument_id,
            item.evidence_type,
        ): item
        for item in plan.items
    }

    expected_stale = {
        (
            "ernx",
            "market_liquidity",
        ),
        (
            "fr_btf_2027_03_10",
            "market_return",
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

    for key in expected_stale:
        item = item_map[key]

        assert item.action == "refresh"
        assert item.reason == "stale"
        assert item.age_days is not None
        assert item.age_days > (
            item.maximum_age_days
        )

    assert (
        (
            "fr_btf_2027_08_11",
            "market_return",
        )
        not in item_map
    )

    undated_item = item_map[
        (
            "undated_access_fixture",
            "accessibility",
        )
    ]

    assert (
        undated_item.action
        == "establish_provenance"
    )

    assert undated_item.reason == "undated"
    assert undated_item.observed_date is None
    assert undated_item.age_days is None

    future_item = item_map[
        (
            "future_cost_fixture",
            "cost",
        )
    ]

    assert future_item.action == "refresh"

    assert (
        future_item.reason
        == "future_dated"
    )

    assert future_item.age_days == -1

    assert plan.actionable_count == 8
    assert plan.refresh_count == 7

    assert (
        plan.establish_provenance_count
        == 1
    )

    assert plan.stale_count == 6
    assert plan.future_dated_count == 1
    assert plan.undated_count == 1

    duplicate_requirement = (
        EvidenceFreshnessRequirement(
            evidence_type="market_return",
            maximum_age_days=7,
        )
    )

    duplicate_rejected = False

    try:
        build_evidence_refresh_plan(
            plan_id="duplicate_requirement_test",
            dependency_sets=(
                dependency_sets[0],
            ),
            requirements=(
                *requirements,
                duplicate_requirement,
            ),
            as_of=AS_OF,
        )
    except ValueError:
        duplicate_rejected = True

    assert duplicate_rejected

    print()
    print("-" * 100)
    print()

    print(
        "MILESTONE 15I ASSERTIONS"
    )
    print()

    print(
        "Structured dependencies reused:           yes"
    )

    print(
        "Human-readable requirement parsing:       no"
    )

    print(
        "Fresh evidence excluded from worklist:    yes"
    )

    print(
        "Stale evidence becomes refresh work:      yes"
    )

    print(
        "Future-dated evidence becomes refresh:    yes"
    )

    print(
        "Undated evidence establishes provenance:  yes"
    )

    print(
        "Existing freshness thresholds reused:     yes"
    )

    print(
        "Duplicate policy types rejected:          yes"
    )

    print()

    print(
        "All Milestone 15I evidence-refresh "
        "planning assertions passed."
    )


if __name__ == "__main__":
    main()
