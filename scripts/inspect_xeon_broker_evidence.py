from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.ibkr import (
    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE,
    IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
    1_000_000,
)


def calculate_commission_eur(
    position_size_eur: float,
    commission_bps: float,
) -> float:
    return (
        position_size_eur
        * commission_bps
        / 10_000
    )


def main() -> None:
    access = (
        IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE
    )

    costs = (
        IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE
    )

    print(
        "XEON BROKER-ROUTE EVIDENCE"
    )

    print()

    print(
        "This inspection separates evidence for "
        "the brokerage route from evidence for "
        "actual market liquidity and execution."
    )

    print()

    print("-" * 100)
    print()

    print("CORPORATE ACCESS ROUTE")
    print()

    print(
        f"Broker:                        "
        f"{access.broker}"
    )

    print(
        f"Jurisdiction:                  "
        f"{access.jurisdiction}"
    )

    print(
        f"Corporate route supported:     "
        f"{access.corporate_account_route_supported}"
    )

    print(
        f"Specific approval verified:    "
        f"{access.specific_account_approval_verified}"
    )

    print(
        f"Evidence date:                 "
        f"{access.evidence_date}"
    )

    print()

    print(
        "Interpretation:"
    )

    print(
        "A Slovenian company has a documented "
        "corporate-account application route, but "
        "approval of a specific company remains an "
        "account-opening or execution-stage fact."
    )

    print()

    print("-" * 100)
    print()

    print("BROKER TRADING COST")
    print()

    print(
        f"Market country:                "
        f"{costs.market_country}"
    )

    print(
        f"Pricing plan:                  "
        f"{costs.pricing_plan}"
    )

    print(
        f"Routing method:                "
        f"{costs.routing_method}"
    )

    print(
        f"Monthly trade-value band:      "
        f"<= EUR "
        f"{costs.monthly_trade_value_limit_eur:,.0f}"
    )

    print(
        f"Commission:                    "
        f"{costs.commission_pct_of_trade_value:.3f}%"
    )

    print(
        f"Commission:                    "
        f"{costs.commission_bps:.1f} bps"
    )

    print(
        f"Account minimum:               "
        f"USD {costs.account_minimum_usd:,.2f}"
    )

    print(
        f"Inactivity fee:                "
        f"USD {costs.inactivity_fee_usd:,.2f}"
    )

    print()

    print("POSITION-SIZE COSTS")
    print()

    for position_size_eur in POSITION_SIZES_EUR:
        entry_commission_eur = (
            calculate_commission_eur(
                position_size_eur=(
                    position_size_eur
                ),
                commission_bps=(
                    costs.commission_bps
                ),
            )
        )

        exit_commission_eur = (
            entry_commission_eur
        )

        roundtrip_commission_eur = (
            entry_commission_eur
            + exit_commission_eur
        )

        roundtrip_bps = (
            costs.commission_bps
            * 2
        )

        print(
            f"EUR {position_size_eur:>10,.0f}"
        )

        print(
            f"  Entry commission:            "
            f"EUR {entry_commission_eur:,.2f}"
        )

        print(
            f"  Exit commission:             "
            f"EUR {exit_commission_eur:,.2f}"
        )

        print(
            f"  Roundtrip commission:        "
            f"EUR {roundtrip_commission_eur:,.2f}"
        )

        print(
            f"  Roundtrip commission:        "
            f"{roundtrip_bps:.1f} bps"
        )

        print()

    print("-" * 100)
    print()

    print("WHAT THIS EVIDENCE CLOSES")
    print()

    print(
        "  - Slovenian corporate brokerage route: "
        "SUPPORTED"
    )

    print(
        "  - Fixed SmartRouting commission: "
        "KNOWN"
    )

    print(
        "  - Account minimum: KNOWN"
    )

    print(
        "  - Inactivity fee: KNOWN"
    )

    print()

    print("WHAT THIS EVIDENCE DOES NOT CLOSE")
    print()

    print(
        "  - Approval of a specific Slovenian d.o.o."
    )

    print(
        "  - XEON permissions in a future account"
    )

    print(
        "  - XEON bid-ask spread"
    )

    print(
        "  - XEON executable order-book depth"
    )

    print(
        "  - Slippage or market impact"
    )

    print(
        "  - Immediate EUR 500k exit capacity"
    )

    print()

    print("INTERPRETATION")
    print()

    print(
        "The existing 5-basis-point entry and "
        "5-basis-point exit broker-commission "
        "scenario is supported by public pricing."
    )

    print()

    print(
        "Broker commission should therefore not be "
        "treated as an unresolved XEON economics "
        "gap for this access-route scenario."
    )

    print()

    print(
        "However, broker pricing does not establish "
        "the execution price of XEON itself. "
        "Bid-ask spread, order-book depth, slippage, "
        "and market impact remain separate market "
        "evidence requirements."
    )


if __name__ == "__main__":
    main()