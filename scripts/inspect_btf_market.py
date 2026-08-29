from datetime import date
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.bonds import (
    zero_coupon_annualized_yield,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    get_btf_2027_03_10_market_observation,
)


def main() -> None:
    observation = (
        get_btf_2027_03_10_market_observation()
    )

    settlement_date = date(2026, 8, 31)
    maturity_date = date.fromisoformat(
        BTF_2027_03_10.maturity_date
    )

    derived_yield = zero_coupon_annualized_yield(
        price_pct_of_par=observation.price_pct_of_par,
        settlement_date=settlement_date,
        maturity_date=maturity_date,
    )

    print("MARKET OBSERVATION")
    print()

    print(f"Instrument:           {BTF_2027_03_10.name}")
    print(f"ISIN:                 {BTF_2027_03_10.isin}")

    print()
    print(f"Observed:             {observation.observed_at}")
    print(
        f"Observation type:     "
        f"{observation.observation_type}"
    )

    print(
        f"Price:                "
        f"{observation.price_pct_of_par:.2f}% of par"
    )

    print(
        f"Bid:                  "
        f"{observation.bid_price or 'UNKNOWN'}"
    )

    print(
        f"Ask:                  "
        f"{observation.ask_price or 'UNKNOWN'}"
    )

    print(
        f"Bid size:             "
        f"{observation.bid_size or 'UNKNOWN'}"
    )

    print(
        f"Ask size:             "
        f"{observation.ask_size or 'UNKNOWN'}"
    )

    print()
    print(
        f"Settlement assumption:"
        f" {settlement_date.isoformat()}"
    )

    print(
        f"Maturity:             "
        f"{maturity_date.isoformat()}"
    )

    print(
        f"Derived yield:        "
        f"{derived_yield:.3f}%"
    )

    print(
        "Yield measure:        "
        "model_derived_zero_coupon_annualized"
    )

    print()
    print("ACTIONABILITY")
    print("Market observed:      yes")
    print("Firm executable quote:no")

    print()
    print(
        "The derived yield is analytical context, "
        "not a broker quote."
    )


if __name__ == "__main__":
    main()