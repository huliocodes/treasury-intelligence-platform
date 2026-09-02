from __future__ import annotations

from treasury_intelligence.sources.slovenia_treasury_bills import (
    DZ125,
    ILIRIKA_SLOVENIA_TBILL_PRIMARY_COSTS,
    LATEST_PREDECESSOR_YIELDS_PCT,
    SLOVENIA_TBILL_PRIMARY_ACCESS,
    SZ163,
    TZ233,
    get_september_2026_scheduled_auctions,
)


def main() -> None:
    print(
        "===== SLOVENIA TREASURY-BILL "
        "PRIMARY MARKET ====="
    )

    print()
    print("ACCESS")

    access = SLOVENIA_TBILL_PRIMARY_ACCESS

    print(
        "legal_persons_supported="
        f"{access.legal_persons_supported}"
    )

    print(
        "orders_via_primary_dealer="
        f"{access.orders_via_primary_dealer}"
    )

    print(
        "settlement_days_after_auction="
        f"{access.settlement_days_after_auction}"
    )

    print(
        "primary_dealer_count="
        f"{len(access.primary_dealers)}"
    )

    for dealer in access.primary_dealers:
        print(
            f"primary_dealer={dealer}"
        )

    print()
    print("SEPTEMBER 2026 AUCTIONS")

    for auction in (
        get_september_2026_scheduled_auctions()
    ):
        print()
        print(
            f"designation={auction.designation}"
        )
        print(
            f"state={auction.state}"
        )
        print(
            f"auction_date={auction.auction_date}"
        )
        print(
            f"settlement_date={auction.settlement_date}"
        )
        print(
            f"maturity_date={auction.maturity_date}"
        )
        print(
            f"days_to_maturity="
            f"{auction.days_to_maturity}"
        )
        print(
            f"auction_yield_pct="
            f"{auction.auction_yield_pct}"
        )
        print(
            f"issued_nominal_eur="
            f"{auction.issued_nominal_eur}"
        )
        print(
            f"isin={auction.isin}"
        )

    print()
    print("LATEST PREDECESSOR YIELDS")

    for designation, yield_pct in (
        LATEST_PREDECESSOR_YIELDS_PCT.items()
    ):
        print(
            f"{designation}={yield_pct:.3f}%"
        )

    print()
    print("ILIRIKA PRIMARY ROUTE COST EVIDENCE")

    costs = (
        ILIRIKA_SLOVENIA_TBILL_PRIMARY_COSTS
    )

    print(
        "primary_subscription_commission_pct="
        f"{costs.primary_subscription_commission_pct}"
    )

    print(
        "provider_custody_pct_per_month="
        f"{costs.provider_custody_pct_per_month:.5f}%"
    )

    print(
        "kdd_custody_pct_per_month="
        f"{costs.kdd_custody_pct_per_month:.5f}%"
    )

    print(
        "kdd_custody_fixed_eur_per_month="
        f"{costs.kdd_custody_fixed_eur_per_month:.2f}"
    )

    print(
        "kdd_settlement_pct="
        f"{costs.kdd_settlement_pct:.3f}%"
    )

    print(
        "kdd_settlement_max_eur="
        f"{costs.kdd_settlement_max_eur:.2f}"
    )

    print(
        "kdd_order_matching_eur="
        f"{costs.kdd_order_matching_eur:.2f}"
    )

    print(
        "kdd_maturity_payment_eur="
        f"{costs.kdd_maturity_payment_eur:.2f}"
    )

    print(
        "provider_maturity_payment_eur="
        f"{costs.provider_maturity_payment_eur:.2f}"
    )

    print()
    print("STATE INVARIANTS")

    assert TZ233.state == "scheduled"
    assert SZ163.state == "scheduled"
    assert DZ125.state == "scheduled"

    assert TZ233.auction_yield_pct is None
    assert SZ163.auction_yield_pct is None
    assert DZ125.auction_yield_pct is None

    assert TZ233.issued_nominal_eur is None
    assert SZ163.issued_nominal_eur is None
    assert DZ125.issued_nominal_eur is None

    assert TZ233.isin is None
    assert SZ163.isin is None
    assert DZ125.isin is None

    print(
        "scheduled_auction_facts_not_invented=True"
    )

    print()
    print(
        "production_candidate_ready=False"
    )

    print(
        "reason=awaiting_2026_09_08_auction_results"
    )


if __name__ == "__main__":
    main()
