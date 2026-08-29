from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.addiko import (
    get_addiko_corporate_eur_deposit_rates,
)

from treasury_intelligence.sources.banks import (
    interpret_bank_deposit_position,
)


POSITION_SIZE_EUR = 5_000_000

TARGET_TERM_LABEL = "271 days–1 year"


def main() -> None:
    rates = get_addiko_corporate_eur_deposit_rates()

    rate = next(
        (
            item
            for item in rates
            if item.term_label == TARGET_TERM_LABEL
        ),
        None,
    )

    if rate is None:
        raise ValueError(
            f"Could not find term: {TARGET_TERM_LABEL}"
        )

    interpretation = interpret_bank_deposit_position(
        rate,
        POSITION_SIZE_EUR,
    )

    print(
        f"{rate.bank} / {rate.product}"
    )

    print()
    print(
        f"Position size:        "
        f"EUR {interpretation.position_size_eur:,.2f}"
    )

    print(
        f"Term:                 "
        f"{rate.term_label}"
    )

    print(
        f"Published rate:       "
        f"{interpretation.published_rate_pct:.2f}%"
    )

    print(
        f"Pricing status:       "
        f"{rate.price_status} / "
        f"{rate.quote_firmness}"
    )

    print()

    minimum_text = (
        "yes"
        if interpretation.minimum_amount_supported
        else "no"
    )

    print(
        f"Minimum supported:    "
        f"{minimum_text}"
    )

    if interpretation.maximum_amount_supported is None:
        maximum_text = "unknown"
    else:
        maximum_text = (
            "yes"
            if interpretation.maximum_amount_supported
            else "no"
        )

    print(
        f"Maximum supported:    "
        f"{maximum_text}"
    )

    executable_text = (
        "yes"
        if interpretation.published_rate_is_executable
        else "no"
    )

    print(
        f"Published executable: "
        f"{executable_text}"
    )

    quote_text = (
        "yes"
        if interpretation.quote_required
        else "no"
    )

    print(
        f"Quote required:       "
        f"{quote_text}"
    )

    if interpretation.executable_rate_pct is None:
        executable_rate_text = "UNKNOWN"
    else:
        executable_rate_text = (
            f"{interpretation.executable_rate_pct:.2f}%"
        )

    print(
        f"Executable rate:      "
        f"{executable_rate_text}"
    )


if __name__ == "__main__":
    main()