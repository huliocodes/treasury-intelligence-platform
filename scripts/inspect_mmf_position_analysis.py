from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.positions import (
    build_money_market_fund_position_analysis,
)

from treasury_intelligence.sources.blackrock import (
    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MINIMUM_EUR,
    get_blackrock_ics_euro_liquidity_core_t0_snapshot,
)

from treasury_intelligence.sources.spiko import (
    SPIKO_EU_TBILLS_MINIMUM_EUR,
    get_spiko_eu_tbills_snapshot,
)


def print_analysis(
    label: str,
    snapshot,
    minimum_initial_investment_eur: float,
    position_sizes: tuple[float, ...],
) -> None:
    print(label)
    print("=" * 60)

    for position_size_eur in position_sizes:
        analysis = (
            build_money_market_fund_position_analysis(
                snapshot=snapshot,
                position_size_eur=position_size_eur,
                minimum_initial_investment_eur=(
                    minimum_initial_investment_eur
                ),
            )
        )

        print(
            "Position:",
            f"EUR {analysis.position_size_eur:,.0f}",
        )

        print(
            "Published minimum:",
            f"EUR {minimum_initial_investment_eur:,.0f}",
        )

        print(
            "Entry supported by product minimum:",
            analysis.entry_supported,
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
                f"{analysis.reference_yield_pct:.2f}%"
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
            "Rejection reason:",
            analysis.rejection_reason,
        )

        print()


def main() -> None:
    position_sizes = (
        100_000.0,
        500_000.0,
        1_000_000.0,
        2_000_000.0,
    )

    blackrock = (
        get_blackrock_ics_euro_liquidity_core_t0_snapshot()
    )

    spiko = get_spiko_eu_tbills_snapshot()

    print_analysis(
        label="BLACKROCK TRADITIONAL MMF",
        snapshot=blackrock,
        minimum_initial_investment_eur=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MINIMUM_EUR
        ),
        position_sizes=position_sizes,
    )

    print_analysis(
        label="SPIKO TOKENIZED MMF",
        snapshot=spiko,
        minimum_initial_investment_eur=(
            SPIKO_EU_TBILLS_MINIMUM_EUR
        ),
        position_sizes=position_sizes,
    )


if __name__ == "__main__":
    main()