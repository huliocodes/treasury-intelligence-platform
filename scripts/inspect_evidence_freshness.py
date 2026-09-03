from __future__ import annotations

from treasury_intelligence.analytics.freshness import (
    assess_evidence_freshness,
)

from treasury_intelligence.policies.freshness import (
    MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY,
    MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY_NOTES,
    get_model_company_freshness_requirement,
)


AS_OF = "2026-09-03"


def assess(
    *,
    evidence_type: str,
    observed_date: str,
):
    requirement = (
        get_model_company_freshness_requirement(
            evidence_type
        )
    )

    return assess_evidence_freshness(
        requirement=requirement,
        observed_date=observed_date,
        as_of=AS_OF,
    )


def main() -> None:
    print(
        "MILESTONE 15G — EVIDENCE FRESHNESS CONTRACT"
    )
    print()

    expected_policy = {
        "market_return": 7,
        "market_liquidity": 7,
        "benchmark": 3,
        "risk": 30,
        "accessibility": 90,
        "cost": 90,
    }

    actual_policy = {
        requirement.evidence_type:
            requirement.maximum_age_days
        for requirement
        in MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY
    }

    print("PRODUCTION V1 FRESHNESS POLICY")
    print()

    for evidence_type, maximum_age_days in (
        actual_policy.items()
    ):
        print(
            f"{evidence_type:20} "
            f"{maximum_age_days:>3} days"
        )

    assert actual_policy == expected_policy

    print()
    print("BOUNDARY CASES")
    print()

    same_day = assess(
        evidence_type="market_return",
        observed_date="2026-09-03",
    )

    exact_boundary = assess(
        evidence_type="market_return",
        observed_date="2026-08-27",
    )

    stale = assess(
        evidence_type="market_return",
        observed_date="2026-08-26",
    )

    future = assess(
        evidence_type="market_return",
        observed_date="2026-09-04",
    )

    benchmark_fresh = assess(
        evidence_type="benchmark",
        observed_date="2026-09-01",
    )

    benchmark_stale = assess(
        evidence_type="benchmark",
        observed_date="2026-08-30",
    )

    accessibility_fresh = assess(
        evidence_type="accessibility",
        observed_date="2026-06-05",
    )

    accessibility_stale = assess(
        evidence_type="accessibility",
        observed_date="2026-06-04",
    )

    cases = (
        ("same-day return", same_day),
        ("7-day return boundary", exact_boundary),
        ("8-day stale return", stale),
        ("future-dated return", future),
        ("2-day benchmark", benchmark_fresh),
        ("4-day benchmark", benchmark_stale),
        (
            "90-day accessibility boundary",
            accessibility_fresh,
        ),
        (
            "91-day stale accessibility",
            accessibility_stale,
        ),
    )

    for label, result in cases:
        print(
            f"{label:32} "
            f"age={result.age_days:>4} "
            f"max={result.maximum_age_days:>3} "
            f"status={result.status}"
        )

    assert same_day.status == "fresh"
    assert same_day.usable

    assert exact_boundary.age_days == 7
    assert exact_boundary.status == "fresh"
    assert exact_boundary.usable

    assert stale.age_days == 8
    assert stale.status == "stale"
    assert not stale.usable

    assert future.age_days == -1
    assert future.status == "future_dated"
    assert not future.usable

    assert benchmark_fresh.status == "fresh"
    assert benchmark_stale.status == "stale"

    assert accessibility_fresh.age_days == 90
    assert accessibility_fresh.status == "fresh"

    assert accessibility_stale.age_days == 91
    assert accessibility_stale.status == "stale"

    invalid_date_rejected = False

    try:
        assess(
            evidence_type="risk",
            observed_date="not-a-date",
        )
    except ValueError:
        invalid_date_rejected = True

    unsupported_type_rejected = False

    try:
        get_model_company_freshness_requirement(
            "unknown"
        )
    except ValueError:
        unsupported_type_rejected = True

    assert invalid_date_rejected
    assert unsupported_type_rejected

    assert (
        "explicit governance assumptions"
        in MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY_NOTES
    )

    assert (
        "not market conventions"
        in MODEL_COMPANY_EVIDENCE_FRESHNESS_POLICY_NOTES
    )

    print()
    print("-" * 100)
    print()
    print("MILESTONE 15G ASSERTIONS")
    print()
    print(
        "Date-based freshness assessment:        yes"
    )
    print(
        "Evidence-type-specific thresholds:      yes"
    )
    print(
        "Exact age boundary remains fresh:       yes"
    )
    print(
        "Over-age evidence becomes stale:        yes"
    )
    print(
        "Future-dated evidence rejected as usable: yes"
    )
    print(
        "Invalid dates rejected:                 yes"
    )
    print(
        "Policy assumptions explicit:            yes"
    )
    print()
    print(
        "All Milestone 15G evidence-freshness "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
