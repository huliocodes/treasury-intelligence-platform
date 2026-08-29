from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.aave import (
    analyze_position_support,
    fetch_aave_v3_base_eurc,
)


POSITION_SIZES = [
    50_000,
    100_000,
    500_000,
    1_000_000,
    5_000_000,
]


def format_amount(value: float) -> str:
    return f"{value:,.2f}"


def main() -> None:
    observation = fetch_aave_v3_base_eurc()

    print(
        f"{observation.protocol} "
        f"{observation.version} / "
        f"{observation.chain} / "
        f"{observation.asset}"
    )
    print()

    print(
        f"Supply APY:          "
        f"{observation.supply_apy_pct:.3f}%"
    )

    print(
        f"Total supplied:      "
        f"{format_amount(observation.total_supplied)} EURC"
    )

    print(
        f"Total borrowed:      "
        f"{format_amount(observation.total_borrowed)} EURC"
    )

    print(
        f"Available liquidity: "
        f"{format_amount(observation.available_liquidity)} EURC"
    )

    print(
        f"Utilization:         "
        f"{observation.utilization_pct:.2f}%"
    )

    if observation.supply_cap is None:
        supply_cap_text = "uncapped"
    else:
        supply_cap_text = (
            f"{format_amount(observation.supply_cap)} EURC"
        )

    print(
        f"Supply cap:          "
        f"{supply_cap_text}"
    )

    print(
        f"Observed at:         "
        f"{observation.observed_at.isoformat()}"
    )

    print()
    print("Position-size support")
    print()

    for position_size in POSITION_SIZES:
        support = analyze_position_support(
            observation,
            position_size,
        )

        entry_text = (
            "yes"
            if support.entry_supported
            else "no"
        )

        print(
            f"{format_amount(position_size):>14} EURC"
            f" | entry: {entry_text:<3}"
            f" | immediate exit coverage: "
            f"{support.immediate_exit_coverage_pct:>6.2f}%"
        )


if __name__ == "__main__":
    main()