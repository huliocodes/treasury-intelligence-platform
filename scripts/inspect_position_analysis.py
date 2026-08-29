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
    get_ernx_market_observation,
    get_ernx_snapshot,
)

from treasury_intelligence.sources.xtrackers import (
    build_xeon_snapshot,
    get_xeon_market_observation,
)


POSITION_SIZES_EUR = [
    50_000,
    100_000,
    500_000,
    1_000_000,
    5_000_000,
]


def format_optional_bool(
    value: bool | None,
) -> str:
    if value is True:
        return "yes"

    if value is False:
        return "no"

    return "unknown"


def format_optional_pct(
    value: float | None,
) -> str:
    if value is None:
        return "unknown"

    return f"{value:.2f}%"


def main() -> None:
    aave_observation = fetch_aave_v3_base_eurc()

    estr = fetch_recent_estr(limit=1)[-1]

    xeon_snapshot = build_xeon_snapshot(
        estr_rate_pct=estr.rate_pct,
        estr_reference_date=estr.reference_date,
    )

    xeon_market_observation = (
        get_xeon_market_observation()
    )

    ernx_snapshot = get_ernx_snapshot()

    ernx_market_observation = (
        get_ernx_market_observation()
    )

    btf_snapshot = get_btf_2027_03_10_snapshot()

    btf_market_observation = (
        get_btf_2027_03_10_market_observation()
    )

    settlement_date = date(2026, 8, 31)

    maturity_date = date.fromisoformat(
        BTF_2027_03_10.maturity_date
    )

    btf_market_yield = zero_coupon_annualized_yield(
        price_pct_of_par=(
            btf_market_observation.price_pct_of_par
        ),
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
            f"{format_optional_bool(analysis.entry_supported):<7} | "
            f"immediate exit: "
            f"{format_optional_bool(analysis.immediate_exit_supported):<7} | "
            f"exit coverage: "
            f"{format_optional_pct(analysis.immediate_exit_coverage_pct):>8}"
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
            market_observation=btf_market_observation,
            position_size_eur=position_size,
            market_derived_yield_pct=(
                btf_market_yield
            ),
        )

        market_pct = (
            "unknown"
            if analysis.position_pct_of_market is None
            else (
                f"{analysis.position_pct_of_market:.4f}%"
            )
        )

        executable = (
            "yes"
            if analysis.executable_economics_known
            else "no"
        )

        print(
            f"EUR {position_size:>10,.0f} | "
            f"entry: "
            f"{format_optional_bool(analysis.entry_supported):<7} | "
            f"immediate exit: "
            f"{format_optional_bool(analysis.immediate_exit_supported):<7} | "
            f"issue: {market_pct:>8} | "
            f"executable: {executable}"
        )

    print()
    print("XEON")
    print(
        f"Benchmark estimate:   "
        f"{xeon_snapshot.yield_value_pct:.3f}%"
    )
    print(
        f"Observed turnover:    "
        f"EUR "
        f"{xeon_market_observation.daily_turnover_eur:,.0f}"
    )
    print()

    for position_size in POSITION_SIZES_EUR:
        analysis = build_xeon_position_analysis(
            snapshot=xeon_snapshot,
            position_size_eur=position_size,
            market_observation=(
                xeon_market_observation
            ),
        )

        market_pct = (
            "unknown"
            if analysis.position_pct_of_market is None
            else (
                f"{analysis.position_pct_of_market:.4f}%"
            )
        )

        turnover_pct = (
            "unknown"
            if (
                analysis.position_pct_of_daily_turnover
                is None
            )
            else (
                f"{analysis.position_pct_of_daily_turnover:.2f}%"
            )
        )

        executable = (
            "yes"
            if analysis.executable_economics_known
            else "no"
        )

        print(
            f"EUR {position_size:>10,.0f} | "
            f"entry: "
            f"{format_optional_bool(analysis.entry_supported):<7} | "
            f"immediate exit: "
            f"{format_optional_bool(analysis.immediate_exit_supported):<7} | "
            f"market ref: {market_pct:>8} | "
            f"daily turnover: {turnover_pct:>8} | "
            f"executable: {executable}"
        )

    print()
    print("ERNX")
    print(
        f"Portfolio YTM:        "
        f"{ernx_snapshot.yield_value_pct:.3f}%"
    )
    print(
        f"Observed turnover:    "
        f"EUR "
        f"{ernx_market_observation.daily_turnover_eur:,.0f}"
    )
    print()

    for position_size in POSITION_SIZES_EUR:
        analysis = build_ernx_position_analysis(
            snapshot=ernx_snapshot,
            position_size_eur=position_size,
            market_observation=(
                ernx_market_observation
            ),
        )

        market_pct = (
            "unknown"
            if analysis.position_pct_of_market is None
            else (
                f"{analysis.position_pct_of_market:.4f}%"
            )
        )

        turnover_pct = (
            "unknown"
            if (
                analysis.position_pct_of_daily_turnover
                is None
            )
            else (
                f"{analysis.position_pct_of_daily_turnover:.2f}%"
            )
        )

        executable = (
            "yes"
            if analysis.executable_economics_known
            else "no"
        )

        print(
            f"EUR {position_size:>10,.0f} | "
            f"entry: "
            f"{format_optional_bool(analysis.entry_supported):<7} | "
            f"immediate exit: "
            f"{format_optional_bool(analysis.immediate_exit_supported):<7} | "
            f"market ref: {market_pct:>8} | "
            f"daily turnover: {turnover_pct:>8} | "
            f"executable: {executable}"
        )


if __name__ == "__main__":
    main()