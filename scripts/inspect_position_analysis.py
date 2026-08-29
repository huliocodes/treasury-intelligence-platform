from datetime import date
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.bonds import (
    zero_coupon_annualized_yield,
)

from treasury_intelligence.analytics.positions import (
    build_aave_position_analysis,
    build_btf_position_analysis,
    build_ernx_position_analysis,
    build_xeon_position_analysis,
)

from treasury_intelligence.sources.aave import (
    fetch_aave_v3_base_eurc,
)

from treasury_intelligence.sources.ecb import (
    fetch_recent_estr,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    get_btf_2027_03_10_market_observation,
    get_btf_2027_03_10_snapshot,
)

from treasury_intelligence.sources.ishares import (
    get_ernx_snapshot,
)

from treasury_intelligence.sources.xtrackers import (
    build_xeon_snapshot,
)


POSITION_SIZES_EUR = [
    50_000,
    100_000,
    500_000,
    1_000_000,
    5_000_000,
]


def yes_no_unknown(
    value: bool | None,
) -> str:
    if value is True:
        return "yes"

    if value is False:
        return "no"

    return "unknown"


def print_market_scale_analysis(
    label: str,
    snapshot_yield_pct: float,
    yield_label: str,
    builder,
) -> None:
    print(label)
    print(
        f"{yield_label:<22}"
        f"{snapshot_yield_pct:.3f}%"
    )

    print()

    for position_size in POSITION_SIZES_EUR:
        analysis = builder(position_size)

        position_pct = (
            analysis.position_pct_of_market
            if analysis.position_pct_of_market is not None
            else 0
        )

        print(
            f"EUR {position_size:>10,.0f} | "
            f"entry: "
            f"{yes_no_unknown(analysis.entry_supported):<7} | "
            f"immediate exit: "
            f"{yes_no_unknown(
                analysis.immediate_exit_supported
            ):<7} | "
            f"market ref: "
            f"{position_pct:>7.4f}% | "
            f"executable: "
            f"{yes_no_unknown(
                analysis.executable_economics_known
            )}"
        )


def main() -> None:
    aave_observation = fetch_aave_v3_base_eurc()

    estr = fetch_recent_estr(limit=1)[-1]

    xeon_snapshot = build_xeon_snapshot(
        estr_rate_pct=estr.rate_pct,
        estr_reference_date=estr.reference_date,
    )

    ernx_snapshot = get_ernx_snapshot()

    btf_snapshot = get_btf_2027_03_10_snapshot()

    btf_market = (
        get_btf_2027_03_10_market_observation()
    )

    settlement_date = date(2026, 8, 31)

    maturity_date = date.fromisoformat(
        BTF_2027_03_10.maturity_date
    )

    btf_market_yield = zero_coupon_annualized_yield(
        price_pct_of_par=btf_market.price_pct_of_par,
        settlement_date=settlement_date,
        maturity_date=maturity_date,
    )

    print("POSITION-SIZE ANALYSIS")
    print()

    print("AAVE V3 BASE EURC")

    print(
        f"Current supply APY:   "
        f"{aave_observation.supply_apy_pct:.3f}%"
    )

    print()

    for position_size in POSITION_SIZES_EUR:
        analysis = build_aave_position_analysis(
            observation=aave_observation,
            position_size_eur=position_size,
        )

        print(
            f"EUR {position_size:>10,.0f} | "
            f"entry: "
            f"{yes_no_unknown(analysis.entry_supported):<7} | "
            f"immediate exit: "
            f"{yes_no_unknown(
                analysis.immediate_exit_supported
            ):<7} | "
            f"exit coverage: "
            f"{analysis.immediate_exit_coverage_pct:>6.2f}%"
        )

    print()
    print("FRENCH BTF")

    print(
        f"Public derived yield: "
        f"{btf_market_yield:.3f}%"
    )

    print()

    for position_size in POSITION_SIZES_EUR:
        analysis = build_btf_position_analysis(
            snapshot=btf_snapshot,
            market_observation=btf_market,
            position_size_eur=position_size,
            market_derived_yield_pct=btf_market_yield,
        )

        position_pct = (
            analysis.position_pct_of_market
            if analysis.position_pct_of_market is not None
            else 0
        )

        executable = yes_no_unknown(
            analysis.executable_economics_known
        )

        print(
            f"EUR {position_size:>10,.0f} | "
            f"entry: "
            f"{yes_no_unknown(analysis.entry_supported):<7} | "
            f"immediate exit: "
            f"{yes_no_unknown(
                analysis.immediate_exit_supported
            ):<7} | "
            f"issue: "
            f"{position_pct:>7.4f}% | "
            f"executable: {executable}"
        )

    print()

    print_market_scale_analysis(
        label="XEON",
        snapshot_yield_pct=xeon_snapshot.yield_value_pct,
        yield_label="Benchmark estimate:",
        builder=lambda position_size: (
            build_xeon_position_analysis(
                snapshot=xeon_snapshot,
                position_size_eur=position_size,
            )
        ),
    )

    print()

    print_market_scale_analysis(
        label="ERNX",
        snapshot_yield_pct=ernx_snapshot.yield_value_pct,
        yield_label="Portfolio YTM:",
        builder=lambda position_size: (
            build_ernx_position_analysis(
                snapshot=ernx_snapshot,
                position_size_eur=position_size,
            )
        ),
    )


if __name__ == "__main__":
    main()