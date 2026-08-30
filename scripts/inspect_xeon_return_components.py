from dataclasses import fields, is_dataclass
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.frictions import (
    build_xeon_return_components,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
)

REFERENCE_YIELD_PCT = 2.273


def print_value(
    label: str,
    value,
) -> None:
    print(
        f"{label:<32}"
        f"{value}"
    )


def inspect_component(
    index: int,
    component,
) -> None:
    print(
        f"COMPONENT {index}"
    )
    print()

    print_value(
        "Python type:",
        type(component).__name__,
    )

    print_value(
        "Dataclass:",
        is_dataclass(component),
    )

    print_value(
        "repr:",
        repr(component),
    )

    if is_dataclass(component):
        print()
        print(
            "FIELDS"
        )
        print()

        for field in fields(component):
            value = getattr(
                component,
                field.name,
            )

            print_value(
                f"  {field.name}:",
                repr(value),
            )

    elif hasattr(
        component,
        "__dict__",
    ):
        print()
        print(
            "ATTRIBUTES"
        )
        print()

        for name, value in sorted(
            vars(component).items()
        ):
            print_value(
                f"  {name}:",
                repr(value),
            )

    print()
    print("-" * 100)
    print()


def inspect_position(
    position_size_eur: float,
) -> None:
    components = (
        build_xeon_return_components(
            position_size_eur=(
                position_size_eur
            ),
            reference_yield_pct=(
                REFERENCE_YIELD_PCT
            ),
        )
    )

    print(
        f"EUR {position_size_eur:,.0f} POSITION"
    )
    print()

    print_value(
        "Component container type:",
        type(components).__name__,
    )

    print_value(
        "Component count:",
        len(components),
    )

    print()

    print("=" * 100)
    print()

    for index, component in enumerate(
        components,
        start=1,
    ):
        inspect_component(
            index=index,
            component=component,
        )


def main() -> None:
    print(
        "XEON RETURN COMPONENT STRUCTURE AUDIT"
    )
    print()

    print(
        "This inspection shows the exact existing "
        "return-component schema before Xetra "
        "position-sized execution evidence is "
        "connected to production economics."
    )
    print()

    print(
        "No return assumptions are changed by "
        "this script."
    )
    print()

    print("=" * 100)
    print()

    for position_size_eur in POSITION_SIZES_EUR:
        inspect_position(
            position_size_eur=(
                position_size_eur
            ),
        )

    print(
        "INTERPRETATION"
    )
    print()

    print(
        "The output above is the production "
        "interface that 8B.3C must preserve."
    )
    print()

    print(
        "We specifically need to identify the "
        "existing entry and exit execution-cost "
        "components, their evidence flags, and "
        "how unknown spread/slippage is currently "
        "represented."
    )


if __name__ == "__main__":
    main()