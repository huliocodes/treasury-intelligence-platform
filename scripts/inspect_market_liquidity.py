from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.positions import (
    build_ernx_position_analysis,
    build_xeon_position_analysis,
)

from treasury_intelligence.sources.ecb import (
    fetch_recent_estr,
)

from treasury_intelligence.sources.ishares import (
    get_ernx_market_observation,
    get_ernx_snapshot,
)

from treasury_intelligence.sources.xtrackers import (
    build_xeon_snapshot,
    get_xeon_market_observation,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
    1_000_000,
    5_000_000,
)


def print_observation(
    label: str,
    observation,
) -> None:
    print(label)
    print(
        f"Observed:             "
        f"{observation.observed_at}"
    )

    print(
        f"Observation type:     "
        f"{observation.observation_type}"
    )

    print(
        f"Last price:           "
        f"EUR {observation.last_price:,.3f}"
    )

    print(
        f"Daily volume:         "
        f"{observation.daily_volume_units:,.0f} units"
    )

    print(
        f"Derived turnover:     "
        f"EUR {observation.daily_turnover_eur:,.0f}"
    )

    print()


def print_positions(
    label: str,
    snapshot,
    observation,
    builder,
) -> None:
    print(label)

    for position_size in POSITION_SIZES_EUR:
        analysis = builder(
            snapshot=snapshot,
            position_size_eur=position_size,
            market_observation=observation,
        )

        turnover_pct = (
            "UNKNOWN"
            if analysis.position_pct_of_daily_turnover
            is None
            else (
                f"{analysis.position_pct_of_daily_turnover:.2f}%"
            )
        )

        immediate_exit = (
            "unknown"
            if analysis.immediate_exit_supported is None
            else (
                "yes"
                if analysis.immediate_exit_supported
                else "no"
            )
        )

        print(
            f"EUR {position_size:>10,.0f} | "
            f"daily turnover: {turnover_pct:>9} | "
            f"immediate exit: {immediate_exit}"
        )

    print()


def main() -> None:
    estr = fetch_recent_estr(limit=1)[-1]

    xeon_snapshot = build_xeon_snapshot(
        estr_rate_pct=estr.rate_pct,
        estr_reference_date=estr.reference_date,
    )

    xeon_market = get_xeon_market_observation()

    ernx_snapshot = get_ernx_snapshot()

    ernx_market = get_ernx_market_observation()

    print("PUBLIC MARKET LIQUIDITY EVIDENCE")
    print()

    print_observation(
        "XEON XETRA",
        xeon_market,
    )

    print_positions(
        "XEON POSITION CONTEXT",
        xeon_snapshot,
        xeon_market,
        build_xeon_position_analysis,
    )

    print_observation(
        "ERNX XETRA",
        ernx_market,
    )

    print_positions(
        "ERNX POSITION CONTEXT",
        ernx_snapshot,
        ernx_market,
        build_ernx_position_analysis,
    )

    print("INTERPRETATION")
    print()
    print(
        "Observed daily turnover is market-activity evidence."
    )

    print(
        "It is not equivalent to immediate executable depth."
    )

    print(
        "Therefore immediate exit remains UNKNOWN until "
        "position-size-specific bid/ask depth or equivalent "
        "execution evidence is available."
    )


if __name__ == "__main__":
    main()