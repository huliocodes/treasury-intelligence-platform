from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.ecb import (
    fetch_recent_estr,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_ACCESSIBILITY,
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
    build_xeon_snapshot,
)


POSITION_SIZE_EUR = 5_000_000


def main() -> None:
    estr = fetch_recent_estr(limit=1)[-1]

    snapshot = build_xeon_snapshot(
        estr_rate_pct=estr.rate_pct,
        estr_reference_date=estr.reference_date,
    )

    print("NORMALIZED OPPORTUNITY")
    print()

    print("INSTRUMENT")
    print(f"ID:                   {XEON_INSTRUMENT.instrument_id}")
    print(f"Name:                 {XEON_INSTRUMENT.name}")
    print(f"ISIN:                 {XEON_INSTRUMENT.isin}")
    print(f"Type:                 {XEON_INSTRUMENT.instrument_type}")
    print(f"Yield source:         {XEON_INSTRUMENT.yield_source}")

    print()
    print("MARKET")
    print(f"Venue:                {XEON_MARKET.venue}")
    print(f"Ticker:               {XEON_MARKET.ticker}")
    print(f"Currency:             {XEON_MARKET.trading_currency}")

    print()
    print("ACCESS ROUTE")
    print(f"Provider:             {XEON_IBKR_ACCESS.provider}")
    print(f"Route:                {XEON_IBKR_ACCESS.route_type}")

    print()
    print("ACCESSIBILITY")
    print(f"Entity:               {XEON_ACCESSIBILITY.entity_type}")
    print(f"Status:               {XEON_ACCESSIBILITY.status}")
    print(
        f"Technical access:     "
        f"{XEON_ACCESSIBILITY.technical_access}"
    )
    print(
        f"Corporate access:     "
        f"{XEON_ACCESSIBILITY.corporate_operational_access}"
    )

    print()
    print("OPPORTUNITY SNAPSHOT")
    print(f"Observed:             {snapshot.observed_date}")
    print(f"Yield measure:        {snapshot.yield_measure}")
    print(f"Yield value:          {snapshot.yield_value_pct:.3f}%")
    print(f"Benchmark:            {snapshot.benchmark_id}")
    print(
        f"Benchmark spread:     "
        f"{snapshot.benchmark_spread_bps:.1f} bps"
    )

    print()
    print("POSITION CONTEXT")
    print(
        f"Model position:       "
        f"EUR {POSITION_SIZE_EUR:,.0f}"
    )

    if snapshot.fund_aum_eur:
        position_pct = (
            POSITION_SIZE_EUR
            / snapshot.fund_aum_eur
            * 100
        )

        print(
            f"Position / fund AUM:  "
            f"{position_pct:.4f}%"
        )


if __name__ == "__main__":
    main()