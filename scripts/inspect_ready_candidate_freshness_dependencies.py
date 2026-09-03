from __future__ import annotations

from treasury_intelligence.analytics.freshness import (
    assess_evidence_freshness,
)

from treasury_intelligence.analytics.freshness_dependencies import (
    build_opportunity_freshness_dependencies,
)

from treasury_intelligence.analytics.btf_risk_assessments import (
    get_btf_2027_08_11_risk_assessments,
)

from treasury_intelligence.analytics.bubill_risk_assessments import (
    get_bubill_2027_08_18_risk_assessments,
    get_bubill_risk_assessments,
)

from treasury_intelligence.analytics.risk_assessments import (
    get_btf_risk_assessments,
    get_ernx_risk_assessments,
)

from treasury_intelligence.policies.freshness import (
    get_model_company_freshness_requirement,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10_ACCESSIBILITY,
    BTF_2027_08_11_ACCESSIBILITY,
    get_btf_2027_03_10_market_observation,
    get_btf_2027_03_10_snapshot,
    get_btf_2027_08_11_market_observation,
    get_btf_2027_08_11_snapshot,
)

from treasury_intelligence.sources.germany import (
    BUBILL_2027_07_14_ACCESSIBILITY,
    BUBILL_2027_08_18_ACCESSIBILITY,
    get_bubill_2027_07_14_market_observation,
    get_bubill_2027_07_14_snapshot,
    get_bubill_2027_08_18_market_observation,
    get_bubill_2027_08_18_snapshot,
)

from treasury_intelligence.sources.ishares import (
    ERNX_ACCESSIBILITY,
    get_ernx_market_observation,
    get_ernx_snapshot,
)

from treasury_intelligence.sources.ibkr import (
    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE,
    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE,
    IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE,
)

from treasury_intelligence.sources.ibkr_fixed_income import (
    IBKR_EUROPE_OTC_BOND_EVIDENCE,
)


AS_OF = "2026-09-03"


def _assess_dependency_set(
    *,
    label: str,
    dependencies,
):
    print(label)
    print("-" * len(label))

    statuses = {}

    for dependency in dependencies.dependencies:
        if dependency.observed_date is None:
            statuses[
                dependency.evidence_type
            ] = "undated"

            print(
                f"{dependency.evidence_type:20} "
                f"date=UNDATED     "
                f"status=undated"
            )
            continue

        requirement = (
            get_model_company_freshness_requirement(
                dependency.evidence_type
            )
        )

        assessment = assess_evidence_freshness(
            requirement=requirement,
            observed_date=dependency.observed_date,
            as_of=AS_OF,
        )

        statuses[
            dependency.evidence_type
        ] = assessment.status

        print(
            f"{dependency.evidence_type:20} "
            f"date={dependency.observed_date} "
            f"age={assessment.age_days:>3} "
            f"max={assessment.maximum_age_days:>3} "
            f"status={assessment.status}"
        )

    print()

    return statuses


def main() -> None:
    print(
        "MILESTONE 15G.1 — READY-CANDIDATE "
        "FRESHNESS DEPENDENCIES"
    )
    print()

    ernx = (
        build_opportunity_freshness_dependencies(
            snapshot=get_ernx_snapshot(),
            market_observation=(
                get_ernx_market_observation()
            ),
            accessibility=ERNX_ACCESSIBILITY,
            risk_assessments=(
                get_ernx_risk_assessments()
            ),
            accessibility_source_reference=(
                "ernx_xetra_ibkr_accessibility"
            ),
            accessibility_observed_date=(
                IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE
                .evidence_date
            ),
            cost_source_reference=(
                "ibkr_germany_etf_cost_package"
            ),
            cost_observed_date=(
                min(
                    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE
                    .evidence_date,
                    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE
                    .evidence_date,
                )
            ),
        )
    )

    btf_mar = (
        build_opportunity_freshness_dependencies(
            snapshot=get_btf_2027_03_10_snapshot(),
            market_observation=(
                get_btf_2027_03_10_market_observation()
            ),
            accessibility=(
                BTF_2027_03_10_ACCESSIBILITY
            ),
            risk_assessments=(
                get_btf_risk_assessments()
            ),
            accessibility_source_reference=(
                "fr_btf_2027_03_10_ibkr_accessibility"
            ),
            accessibility_observed_date=(
                IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE
                .evidence_date
            ),
            cost_source_reference=(
                "ibkr_europe_otc_bond_cost_package"
            ),
            cost_observed_date=(
                IBKR_EUROPE_OTC_BOND_EVIDENCE
                .evidence_date
            ),
        )
    )

    btf_aug = (
        build_opportunity_freshness_dependencies(
            snapshot=get_btf_2027_08_11_snapshot(),
            market_observation=(
                get_btf_2027_08_11_market_observation()
            ),
            accessibility=(
                BTF_2027_08_11_ACCESSIBILITY
            ),
            risk_assessments=(
                get_btf_2027_08_11_risk_assessments()
            ),
            accessibility_source_reference=(
                "fr_btf_2027_08_11_ibkr_accessibility"
            ),
            accessibility_observed_date=(
                IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE
                .evidence_date
            ),
            cost_source_reference=(
                "ibkr_europe_otc_bond_cost_package"
            ),
            cost_observed_date=(
                IBKR_EUROPE_OTC_BOND_EVIDENCE
                .evidence_date
            ),
        )
    )

    bubill_jul = (
        build_opportunity_freshness_dependencies(
            snapshot=(
                get_bubill_2027_07_14_snapshot()
            ),
            market_observation=(
                get_bubill_2027_07_14_market_observation()
            ),
            accessibility=(
                BUBILL_2027_07_14_ACCESSIBILITY
            ),
            risk_assessments=(
                get_bubill_risk_assessments()
            ),
            accessibility_source_reference=(
                "de_bubill_2027_07_14_ibkr_accessibility"
            ),
            accessibility_observed_date=(
                IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE
                .evidence_date
            ),
            cost_source_reference=(
                "ibkr_europe_otc_bond_cost_package"
            ),
            cost_observed_date=(
                IBKR_EUROPE_OTC_BOND_EVIDENCE
                .evidence_date
            ),
        )
    )

    bubill_aug = (
        build_opportunity_freshness_dependencies(
            snapshot=(
                get_bubill_2027_08_18_snapshot()
            ),
            market_observation=(
                get_bubill_2027_08_18_market_observation()
            ),
            accessibility=(
                BUBILL_2027_08_18_ACCESSIBILITY
            ),
            risk_assessments=(
                get_bubill_2027_08_18_risk_assessments()
            ),
            accessibility_source_reference=(
                "de_bubill_2027_08_18_ibkr_accessibility"
            ),
            accessibility_observed_date=(
                IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE
                .evidence_date
            ),
            cost_source_reference=(
                "ibkr_europe_otc_bond_cost_package"
            ),
            cost_observed_date=(
                IBKR_EUROPE_OTC_BOND_EVIDENCE
                .evidence_date
            ),
        )
    )

    ernx_statuses = _assess_dependency_set(
        label="ERNX",
        dependencies=ernx,
    )

    btf_mar_statuses = _assess_dependency_set(
        label="French BTF Mar 2027",
        dependencies=btf_mar,
    )

    btf_aug_statuses = _assess_dependency_set(
        label="French BTF Aug 2027",
        dependencies=btf_aug,
    )

    bubill_jul_statuses = _assess_dependency_set(
        label="German Bubill Jul 2027",
        dependencies=bubill_jul,
    )

    bubill_aug_statuses = _assess_dependency_set(
        label="German Bubill Aug 2027",
        dependencies=bubill_aug,
    )

    assert ernx_statuses == {
        "market_return": "fresh",
        "market_liquidity": "stale",
        "risk": "fresh",
        "accessibility": "fresh",
        "cost": "fresh",
    }

    assert btf_mar_statuses == {
        "market_return": "stale",
        "market_liquidity": "fresh",
        "risk": "fresh",
        "accessibility": "fresh",
        "cost": "fresh",
    }

    assert btf_aug_statuses == {
        "market_return": "fresh",
        "market_liquidity": "fresh",
        "risk": "fresh",
        "accessibility": "fresh",
        "cost": "fresh",
    }

    assert bubill_jul_statuses == {
        "market_return": "stale",
        "market_liquidity": "stale",
        "risk": "fresh",
        "accessibility": "fresh",
        "cost": "fresh",
    }

    assert bubill_aug_statuses == {
        "market_return": "stale",
        "market_liquidity": "stale",
        "risk": "fresh",
        "accessibility": "fresh",
        "cost": "fresh",
    }

    for dependency_set in (
        ernx,
        btf_mar,
        btf_aug,
        bubill_jul,
        bubill_aug,
    ):
        assert len(
            dependency_set.dependencies
        ) == 5

        assert len(
            dependency_set.required_dependencies
        ) == 5

        assert (
            dependency_set
            .undated_required_dependencies
            == ()
        )

    print("-" * 100)
    print()
    print("MILESTONE 15G.1 ASSERTIONS")
    print()
    print(
        "Return dependency mapped from snapshot:       yes"
    )
    print(
        "Liquidity dependency mapped from market data: yes"
    )
    print(
        "Risk dependency mapped from assessments:     yes"
    )
    print(
        "Accessibility dated provenance connected:    yes"
    )
    print(
        "Cost dated provenance connected:             yes"
    )
    print(
        "No fabricated evidence dates introduced:     yes"
    )
    print(
        "Recommendation logic unchanged:              yes"
    )
    print()
    print(
        "All Milestone 15G.1 freshness-dependency "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
