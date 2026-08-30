from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.treasury_state import (
    build_treasury_state,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryPosition,
)


AS_OF = "2026-08-30T15:00:00+02:00"


def print_state(
    label: str,
    state,
) -> None:
    print(label)
    print()

    print(
        f"State ID:                     "
        f"{state.state_id}"
    )

    print(
        f"As of:                        "
        f"{state.as_of}"
    )

    print(
        f"Treasury capital:             "
        f"EUR {state.treasury_capital_eur:,.0f}"
    )

    print(
        f"Invested capital:             "
        f"EUR {state.invested_capital_eur:,.0f}"
    )

    print(
        f"Unallocated capital:          "
        f"EUR {state.unallocated_capital_eur:,.0f}"
    )

    print(
        f"Position count:               "
        f"{len(state.positions)}"
    )

    if state.positions:
        print()
        print("CURRENT POSITIONS")
        print()

        for position in state.positions:
            allocation_pct = (
                position.current_value_eur
                / state.treasury_capital_eur
                * 100
            )

            print(
                f"  {position.label:<20} "
                f"EUR "
                f"{position.current_value_eur:>12,.0f} | "
                f"{allocation_pct:>6.2f}%"
            )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print("TREASURY STATE / CURRENT ALLOCATION")
    print()

    print(
        "The treasury-state layer represents the "
        "company's current modeled allocation before "
        "any review or rebalance decision is made."
    )

    print()

    print("-" * 100)
    print()

    fully_unallocated = (
        build_treasury_state(
            state_id=(
                "fixture_fully_unallocated"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(),
            notes=(
                "Deterministic 7C.1 fixture."
            ),
        )
    )

    print_state(
        label=(
            "CASE 1 — FULLY UNALLOCATED TREASURY"
        ),
        state=fully_unallocated,
    )

    partial_position = TreasuryPosition(
        position_id=(
            "fixture_current_position_1"
        ),
        instrument_id=(
            "fixture_current_instrument"
        ),
        market_id=(
            "fixture_current_market"
        ),
        access_route_id=(
            "fixture_current_access"
        ),
        label="CURRENT FIXTURE",
        current_value_eur=1_000_000,
        notes=(
            "Deterministic existing-position fixture."
        ),
    )

    partially_invested = (
        build_treasury_state(
            state_id=(
                "fixture_partially_invested"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(
                partial_position,
            ),
            notes=(
                "Deterministic 7C.1 fixture."
            ),
        )
    )

    print_state(
        label=(
            "CASE 2 — PARTIALLY INVESTED TREASURY"
        ),
        state=partially_invested,
    )

    position_a = TreasuryPosition(
        position_id=(
            "fixture_position_a"
        ),
        instrument_id=(
            "fixture_instrument_a"
        ),
        market_id=(
            "fixture_market_a"
        ),
        access_route_id=(
            "fixture_access_a"
        ),
        label="POSITION A",
        current_value_eur=2_000_000,
    )

    position_b = TreasuryPosition(
        position_id=(
            "fixture_position_b"
        ),
        instrument_id=(
            "fixture_instrument_b"
        ),
        market_id=(
            "fixture_market_b"
        ),
        access_route_id=(
            "fixture_access_b"
        ),
        label="POSITION B",
        current_value_eur=3_000_000,
    )

    fully_invested = (
        build_treasury_state(
            state_id=(
                "fixture_fully_invested"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(
                position_a,
                position_b,
            ),
            notes=(
                "Deterministic 7C.1 fixture."
            ),
        )
    )

    print_state(
        label=(
            "CASE 3 — FULLY INVESTED TREASURY"
        ),
        state=fully_invested,
    )

    print(
        "CASE 4 — POSITIONS CANNOT EXCEED "
        "TREASURY CAPITAL"
    )
    print()

    oversized_position = TreasuryPosition(
        position_id=(
            "fixture_oversized_position"
        ),
        instrument_id=(
            "fixture_oversized_instrument"
        ),
        market_id=(
            "fixture_oversized_market"
        ),
        access_route_id=(
            "fixture_oversized_access"
        ),
        label="OVERSIZED FIXTURE",
        current_value_eur=5_500_000,
    )

    try:
        build_treasury_state(
            state_id=(
                "fixture_invalid_oversized"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(
                oversized_position,
            ),
        )

    except ValueError as exc:
        print(
            "State rejected by gate:       True"
        )

        print(
            f"Reason:                       "
            f"{exc}"
        )

    else:
        raise AssertionError(
            "Oversized treasury state unexpectedly "
            "passed validation."
        )

    print()
    print("-" * 100)
    print()

    print("INTERPRETATION")
    print()

    print(
        "Case 1 proves that a treasury may be modeled "
        "with no investment positions and all capital "
        "remaining unallocated."
    )

    print(
        "Case 2 proves that current positions and "
        "unallocated treasury capital can coexist."
    )

    print(
        "Case 3 proves that the full treasury may be "
        "represented by existing positions with no "
        "unallocated capital."
    )

    print(
        "Case 4 proves that modeled current positions "
        "cannot exceed the treasury capital defined by "
        "the mandate."
    )

    print(
        "No rebalance decision is made by this layer."
    )


if __name__ == "__main__":
    main()