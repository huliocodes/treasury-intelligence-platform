from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.ishares import (
    ERNX_ACCESSIBILITY,
    ERNX_IBKR_ACCESS,
    ERNX_INSTRUMENT,
    ERNX_MARKET,
    get_ernx_snapshot,
)


POSITION_SIZE_EUR = 5_000_000


def main() -> None:
    snapshot = get_ernx_snapshot()

    print("NORMALIZED OPPORTUNITY")
    print()

    print("INSTRUMENT")
    print(f"ID:                   {ERNX_INSTRUMENT.instrument_id}")
    print(f"Name:                 {ERNX_INSTRUMENT.name}")
    print(f"ISIN:                 {ERNX_INSTRUMENT.isin}")
    print(f"Type:                 {ERNX_INSTRUMENT.instrument_type}")
    print(f"Yield source:         {ERNX_INSTRUMENT.yield_source}")

    print()
    print("MARKET")
    print(f"Venue:                {ERNX_MARKET.venue}")
    print(f"Ticker:               {ERNX_MARKET.ticker}")
    print(f"Currency:             {ERNX_MARKET.trading_currency}")

    print()
    print("ACCESS ROUTE")
    print(f"Provider:             {ERNX_IBKR_ACCESS.provider}")
    print(f"Route:                {ERNX_IBKR_ACCESS.route_type}")

    print()
    print("ACCESSIBILITY")
    print(f"Entity:               {ERNX_ACCESSIBILITY.entity_type}")
    print(f"Status:               {ERNX_ACCESSIBILITY.status}")
    print(
        f"Technical access:     "
        f"{ERNX_ACCESSIBILITY.technical_access}"
    )
    print(
        f"Corporate access:     "
        f"{ERNX_ACCESSIBILITY.corporate_operational_access}"
    )

    print()
    print("OPPORTUNITY SNAPSHOT")
    print(f"Observed:             {snapshot.observed_date}")
    print(f"Yield measure:        {snapshot.yield_measure}")
    print(f"Yield value:          {snapshot.yield_value_pct:.2f}%")
    print(f"Annual fee:           {snapshot.annual_fee_pct:.2f}%")
    print(f"Duration:             {snapshot.duration_years:.2f} years")
    print(
        f"Average maturity:     "
        f"{snapshot.average_maturity_years:.2f} years"
    )
    print(f"Holdings:             {snapshot.holdings_count}")

    print()
    print("POSITION CONTEXT")
    print(
        f"Model position:       "
        f"EUR {POSITION_SIZE_EUR:,.0f}"
    )

    if snapshot.share_class_aum_eur:
        position_pct = (
            POSITION_SIZE_EUR
            / snapshot.share_class_aum_eur
            * 100
        )

        print(
            f"Position / class AUM: "
            f"{position_pct:.4f}%"
        )


if __name__ == "__main__":
    main()