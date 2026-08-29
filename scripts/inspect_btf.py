from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_ACCESSIBILITY,
    BTF_2027_03_10_IBKR_ACCESS,
    BTF_2027_03_10_MARKET,
    get_btf_2027_03_10_snapshot,
)


POSITION_SIZE_EUR = 5_000_000


def main() -> None:
    snapshot = get_btf_2027_03_10_snapshot()

    print("NORMALIZED OPPORTUNITY")
    print()

    print("INSTRUMENT")
    print(f"ID:                   {BTF_2027_03_10.instrument_id}")
    print(f"Name:                 {BTF_2027_03_10.name}")
    print(f"Issuer:               {BTF_2027_03_10.issuer}")
    print(f"ISIN:                 {BTF_2027_03_10.isin}")
    print(f"Type:                 {BTF_2027_03_10.instrument_type}")
    print(f"Currency:             {BTF_2027_03_10.currency}")
    print(f"Maturity:             {BTF_2027_03_10.maturity_date}")
    print(f"Coupon:               {BTF_2027_03_10.coupon_type}")

    print()
    print("MARKET")
    print(f"Venue:                {BTF_2027_03_10_MARKET.venue}")
    print(
        f"Venue type:           "
        f"{BTF_2027_03_10_MARKET.venue_type}"
    )
    print(
        f"Settlement:           "
        f"{BTF_2027_03_10_MARKET.settlement_cycle}"
    )

    print()
    print("ACCESS ROUTE")
    print(
        f"Provider:             "
        f"{BTF_2027_03_10_IBKR_ACCESS.provider}"
    )
    print(
        f"Route:                "
        f"{BTF_2027_03_10_IBKR_ACCESS.route_type}"
    )

    print()
    print("ACCESSIBILITY")
    print(
        f"Entity:               "
        f"{BTF_2027_03_10_ACCESSIBILITY.entity_type}"
    )
    print(
        f"Status:               "
        f"{BTF_2027_03_10_ACCESSIBILITY.status}"
    )
    print(
        f"Technical access:     "
        f"{BTF_2027_03_10_ACCESSIBILITY.technical_access}"
    )
    print(
        f"Corporate access:     "
        f"{BTF_2027_03_10_ACCESSIBILITY.corporate_operational_access}"
    )

    print()
    print("OPPORTUNITY SNAPSHOT")
    print(f"Observed:             {snapshot.observed_date}")
    print(f"Yield measure:        {snapshot.yield_measure}")
    print(f"Yield value:          {snapshot.yield_value_pct:.3f}%")
    print(f"Price status:         {snapshot.price_status}")
    print(f"Quote firmness:       {snapshot.quote_firmness}")

    print()
    print("POSITION CONTEXT")
    print(
        f"Model position:       "
        f"EUR {POSITION_SIZE_EUR:,.0f}"
    )

    if snapshot.outstanding_amount_eur:
        position_pct = (
            POSITION_SIZE_EUR
            / snapshot.outstanding_amount_eur
            * 100
        )

        print(
            f"Issue outstanding:    "
            f"EUR {snapshot.outstanding_amount_eur:,.0f}"
        )

        print(
            f"Position / issue:     "
            f"{position_pct:.4f}%"
        )

    print(
        f"Early exit possible:  "
        f"{'yes' if snapshot.early_exit_possible else 'no'}"
    )

    print()
    print("ACTIONABILITY")

    executable = (
        snapshot.price_status == "executed"
        or snapshot.quote_firmness == "firm"
    )

    print(
        f"Executable economics: "
        f"{'yes' if executable else 'no'}"
    )

    if not executable:
        print(
            "Reason:               "
            "live IBKR secondary-market quote required"
        )


if __name__ == "__main__":
    main()