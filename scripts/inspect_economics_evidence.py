from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.economics import (
    build_economics_evidence_assessment,
)

from treasury_intelligence.analytics.frictions import (
    build_xeon_return_components,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
)


POSITION_SIZE_EUR = 500_000

REFERENCE_YIELD_PCT = 2.273


def build_xeon_analysis(
    holding_period_days: int,
):
    return build_return_analysis(
        analysis_id=(
            f"xeon_500k_{holding_period_days}d_"
            "economics"
        ),
        instrument_id=(
            XEON_INSTRUMENT.instrument_id
        ),
        market_id=(
            XEON_MARKET.market_id
        ),
        access_route_id=(
            XEON_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=(
            POSITION_SIZE_EUR
        ),
        holding_period_days=(
            holding_period_days
        ),
        components=(
            build_xeon_return_components(
                position_size_eur=(
                    POSITION_SIZE_EUR
                ),
                reference_yield_pct=(
                    REFERENCE_YIELD_PCT
                ),
            )
        ),
        notes=(
            "XEON economics evidence validation."
        ),
    )


def print_assessment(
    holding_period_days: int,
) -> None:
    analysis = build_xeon_analysis(
        holding_period_days
    )

    assessment = (
        build_economics_evidence_assessment(
            analysis
        )
    )

    print(
        f"XEON EUR {POSITION_SIZE_EUR:,.0f} "
        f"- {holding_period_days}-DAY SCENARIO"
    )

    print()

    print(
        f"Economics status:              "
        f"{assessment.economics_status}"
    )

    print(
        f"Blocking economics gaps:       "
        f"{assessment.blocking_gap_count}"
    )

    print(
        f"Realistic return available:    "
        f"{assessment.realistic_expected_return_available}"
    )

    print(
        f"Reference yield:               "
        f"{analysis.reference_yield_pct:.3f}%"
    )

    print(
        f"Return after known costs:      "
        f"{analysis.return_after_known_costs_pct:.3f}%"
    )

    if (
        analysis.realistic_expected_return_pct
        is None
    ):
        print(
            "Realistic expected return:     UNKNOWN"
        )
    else:
        print(
            f"Realistic expected return:     "
            f"{analysis.realistic_expected_return_pct:.3f}%"
        )

    print()

    print("STRONGEST SUPPORTED CLAIM")
    print()

    print(
        assessment.strongest_supported_claim
    )

    print()

    print("BLOCKING GAPS")
    print()

    for index, gap in enumerate(
        assessment.evidence_gaps,
        start=1,
    ):
        print(
            f"{index}. {gap.component_label}"
        )

        print(
            f"   Component type:      "
            f"{gap.component_type}"
        )

        print(
            f"   Current status:      "
            f"{gap.current_status}"
        )

        print(
            f"   Basis:               "
            f"{gap.component_basis}"
        )

        print(
            f"   Priority:            "
            f"{gap.priority}"
        )

        print(
            f"   Blocking:            "
            f"{gap.blocking}"
        )

        print(
            f"   Required evidence:   "
            f"{gap.required_evidence}"
        )

        print(
            f"   Resolution action:   "
            f"{gap.resolution_action}"
        )

        print()

    print("-" * 100)
    print()


def main() -> None:
    print("ECONOMICS EVIDENCE SUFFICIENCY")
    print()

    print(
        "Unknown return components are converted into "
        "explicit evidence gaps rather than silently "
        "treated as zero."
    )

    print()

    print("-" * 100)
    print()

    print_assessment(
        holding_period_days=30
    )

    print_assessment(
        holding_period_days=365
    )

    print("INTERPRETATION")
    print()

    print(
        "Both scenarios use the same currently known "
        "economic evidence."
    )

    print(
        "Holding period changes the annualized impact "
        "of known one-time costs but does not resolve "
        "missing execution evidence."
    )

    print(
        "A realistic expected return should appear only "
        "after every modeled blocking cost component has "
        "sufficient evidence."
    )


if __name__ == "__main__":
    main()