from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.addiko import (
    get_addiko_corporate_eur_deposit_rates,
)


def main() -> None:
    rates = get_addiko_corporate_eur_deposit_rates()

    if not rates:
        raise ValueError(
            "No Addiko corporate deposit rates available"
        )

    first = rates[0]

    print(
        f"{first.bank} / "
        f"Corporate EUR deposits"
    )

    print(
        f"Effective: {first.effective_date}"
    )

    print(
        f"Minimum:   EUR {first.minimum_amount_eur:,.2f}"
    )

    print()

    for rate in rates:
        print(
            f"{rate.term_label:<20}"
            f"{rate.annual_rate_pct:>5.2f}%"
            f"  "
            f"{rate.price_status} / "
            f"{rate.quote_firmness}"
        )

    print()
    print("Pricing status")
    print()

    print(
        "Published rates are informational and "
        "non-binding."
    )

    print(
        "Actual pricing may depend on deposit size, "
        "money-market conditions,"
    )

    print(
        "bank liquidity needs and the client "
        "relationship."
    )

    print()
    print(
        f"Source: {first.source_url}"
    )


if __name__ == "__main__":
    main()