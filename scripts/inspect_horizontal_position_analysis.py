from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.positions import (
    build_etf_position_analysis,
    build_sovereign_bill_position_analysis,
)

from treasury_intelligence.sources.amundi import (
    build_amundi_smart_overnight_snapshot,
)

from treasury_intelligence.sources.germany import (
    get_bubill_2027_07_14_market_observation,
    get_bubill_2027_07_14_snapshot,
)


def main() -> None:
    position_sizes = (
        100_000.0,
        500_000.0,
        2_000_000.0,
    )

    amundi_snapshot = (
        build_amundi_smart_overnight_snapshot(
            estr_rate_pct=2.188,
            estr_reference_date="2026-08-27",
        )
    )

    bubill_snapshot = (
        get_bubill_2027_07_14_snapshot()
    )

    bubill_market_observation = (
        get_bubill_2027_07_14_market_observation()
    )

    print("AMUNDI ETF")
    print("=" * 60)

    for position_size_eur in position_sizes:
        analysis = build_etf_position_analysis(
            snapshot=amundi_snapshot,
            position_size_eur=position_size_eur,
            position_scale_eur=(
                amundi_snapshot.fund_aum_eur
            ),
            position_scale_reference="fund_aum",
        )

        print(
            "Position:",
            f"EUR {analysis.position_size_eur:,.0f}",
        )

        print(
            "Position / fund AUM:",
            (
                f"{analysis.position_pct_of_market:.4f}%"
                if analysis.position_pct_of_market
                is not None
                else "UNKNOWN"
            ),
        )

        print(
            "Daily turnover:",
            analysis.observed_daily_turnover_eur,
        )

        print(
            "Liquidity evidence:",
            analysis.liquidity_evidence_level,
        )

        print(
            "Immediate exit supported:",
            analysis.immediate_exit_supported,
        )

        print(
            "Reference yield:",
            (
                f"{analysis.reference_yield_pct:.3f}%"
                if analysis.reference_yield_pct
                is not None
                else "UNKNOWN"
            ),
        )

        print()

    print("BUBILL")
    print("=" * 60)

    for position_size_eur in position_sizes:
        analysis = (
            build_sovereign_bill_position_analysis(
                snapshot=bubill_snapshot,
                market_observation=(
                    bubill_market_observation
                ),
                position_size_eur=position_size_eur,
            )
        )

        print(
            "Position:",
            f"EUR {analysis.position_size_eur:,.0f}",
        )

        print(
            "Position / issue outstanding:",
            (
                f"{analysis.position_pct_of_market:.4f}%"
                if analysis.position_pct_of_market
                is not None
                else "UNKNOWN"
            ),
        )

        print(
            "Reference yield:",
            (
                f"{analysis.reference_yield_pct:.3f}%"
                if analysis.reference_yield_pct
                is not None
                else "UNKNOWN"
            ),
        )

        print(
            "Executable economics known:",
            analysis.executable_economics_known,
        )

        print(
            "Immediate exit supported:",
            analysis.immediate_exit_supported,
        )

        print()


if __name__ == "__main__":
    main()