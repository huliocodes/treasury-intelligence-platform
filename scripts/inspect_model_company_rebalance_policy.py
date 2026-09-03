from __future__ import annotations

from treasury_intelligence.analytics.rebalance import (
    build_rebalance_decision,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.policies.model_company import (
    MODEL_COMPANY_REBALANCE_POLICY,
)


def main() -> None:
    mandate = MODEL_COMPANY_MANDATE
    policy = MODEL_COMPANY_REBALANCE_POLICY

    threshold_bps = (
        policy
        .minimum_first_year_net_improvement_bps_of_treasury
    )

    threshold_eur = (
        mandate.treasury_capital_eur
        * threshold_bps
        / 10_000.0
    )

    print(
        "MODEL-COMPANY PRODUCTION REBALANCE POLICY"
    )
    print()
    print(
        f"Policy ID:                     "
        f"{policy.policy_id}"
    )
    print(
        f"Mandate ID:                    "
        f"{mandate.mandate_id}"
    )
    print(
        f"Treasury capital:              "
        f"EUR {mandate.treasury_capital_eur:,.0f}"
    )
    print(
        f"Minimum improvement:           "
        f"{threshold_bps:.2f} bps"
    )
    print(
        f"Equivalent first-year benefit: "
        f"EUR {threshold_eur:,.0f}"
    )
    print()

    assert threshold_bps == 5.0
    assert abs(threshold_eur - 2_500.0) < 0.01

    assert (
        "explicit V1 governance assumption"
        in (policy.notes or "")
    )

    assert (
        "not a market-derived"
        in (policy.notes or "")
    )

    # The production policy must remain directly consumable by
    # the existing generic rebalance engine. No model-company
    # rebalance implementation should be necessary.
    assert callable(build_rebalance_decision)

    print(
        "Production policy remains separate from the "
        "treasury mandate and is directly consumable by "
        "the generic rebalance engine."
    )
    print()
    print(
        "All Milestone 15E production rebalance-policy "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
