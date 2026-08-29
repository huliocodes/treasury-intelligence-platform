from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.ecb import (
    fetch_recent_estr,
)

from treasury_intelligence.sources.xtrackers import (
    XEON,
    estimate_xeon_rate,
)


POSITION_SIZE_EUR = 5_000_000


def main() -> None:
    estr_observations = fetch_recent_estr(limit=1)
    estr = estr_observations[-1]

    estimate = estimate_xeon_rate(
        estr.rate_pct
    )

    print(
        f"{XEON.provider} / {XEON.ticker}"
    )

    print()
    print(f"Name:                 {XEON.name}")
    print(f"ISIN:                 {XEON.isin}")
    print(f"Instrument type:      {XEON.instrument_type}")
    print(f"Structure:            {XEON.legal_structure}")
    print(f"Replication:          {XEON.replication}")

    print()
    print(f"Exchange:             {XEON.exchange}")
    print(f"Trading currency:     {XEON.trading_currency}")
    print(f"Access route:         {XEON.access_route}")
    print(f"Access status:        {XEON.access_status}")

    print()
    print(
        f"Fund AUM:             "
        f"EUR {XEON.fund_aum_eur:,.0f}"
    )

    print(
        f"Model position:       "
        f"EUR {POSITION_SIZE_EUR:,.0f}"
    )

    fund_pct = (
        POSITION_SIZE_EUR
        / XEON.fund_aum_eur
        * 100
    )

    print(
        f"Position / fund AUM:  "
        f"{fund_pct:.4f}%"
    )

    print()
    print(
        f"€STR:                 "
        f"{estimate.benchmark_rate_pct:.3f}%"
    )

    print(
        f"Index adjustment:     "
        f"+{estimate.benchmark_spread_bps:.1f} bps"
    )

    print(
        f"Annual fund fee:      "
        f"-{estimate.annual_fee_pct:.2f}%"
    )

    print(
        f"Implied rate*:        "
        f"{estimate.implied_rate_before_trading_costs_pct:.3f}%"
    )

    print()
    print(
        "*Benchmark-linked estimate before bid/ask spread, "
        "broker commissions,"
    )

    print(
        "slippage, tracking differences, taxes and "
        "other execution costs."
    )

    print(
        "It is not a guaranteed or executable yield."
    )


if __name__ == "__main__":
    main()