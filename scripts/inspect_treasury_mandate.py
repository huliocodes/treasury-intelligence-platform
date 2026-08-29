from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def main() -> None:
    mandate = MODEL_COMPANY_MANDATE

    print("TREASURY MANDATE")
    print()

    print(f"ID:                         {mandate.mandate_id}")
    print(f"Name:                       {mandate.name}")

    print()
    print("CAPITAL")

    print(
        f"Base currency:              "
        f"{mandate.base_currency}"
    )

    print(
        f"Treasury capital:           "
        f"EUR {mandate.treasury_capital_eur:,.0f}"
    )

    print(
        f"Minimum useful allocation:  "
        f"EUR {mandate.minimum_useful_allocation_eur:,.0f}"
    )

    print(
        f"Maximum single position:    "
        f"{mandate.maximum_single_position_pct:.1f}%"
    )

    print()
    print("RETURN")

    if mandate.target_yield_pct is not None:
        print(
            f"Target yield:               "
            f"{mandate.target_yield_pct:.2f}%"
        )
    else:
        print("Target yield:               none")

    print(
        f"Hard yield constraint:      "
        f"{yes_no(mandate.target_yield_is_hard_constraint)}"
    )

    print()
    print("RISK / LIQUIDITY")

    print(
        f"Capital preservation:       "
        f"{mandate.capital_preservation_priority}"
    )

    print(
        f"Liquidity requirement:      "
        f"{mandate.liquidity_requirement}"
    )

    print(
        f"Allowed currencies:         "
        f"{', '.join(mandate.allowed_currencies)}"
    )

    print(
        f"Maximum unhedged FX:         "
        f"{mandate.maximum_unhedged_fx_exposure_pct:.1f}%"
    )

    if (
        mandate.minimum_immediate_liquidity_coverage_pct
        is not None
    ):
        print(
            f"Immediate liquidity cover:  "
            f"{mandate.minimum_immediate_liquidity_coverage_pct:.1f}%"
        )

    if mandate.maximum_settlement_days is not None:
        print(
            f"Maximum settlement:         "
            f"T+{mandate.maximum_settlement_days}"
        )

    print()
    print("ACCESS")

    print(
        f"Verified corporate access:  "
        f"{yes_no(mandate.require_verified_corporate_access)}"
    )

    print(
        f"Allowed access statuses:    "
        f"{', '.join(mandate.allowed_accessibility_statuses)}"
    )

    print()
    print("OPERATING CADENCE")

    print(
        f"Review frequency:           "
        f"{mandate.review_frequency_days} days"
    )

    print()
    print("POLICY STATE")

    if mandate.allowed_instrument_types is None:
        print(
            "Instrument-type whitelist:  "
            "not yet restricted"
        )
    else:
        print(
            "Instrument-type whitelist:  "
            f"{', '.join(mandate.allowed_instrument_types)}"
        )

    print(
        "Diversification limits:      "
        "not yet defined beyond single-position maximum"
    )


if __name__ == "__main__":
    main()