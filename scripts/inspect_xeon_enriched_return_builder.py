from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.access_returns import (
    apply_access_cost_evidence,
)

from treasury_intelligence.analytics.economics import (
    build_economics_evidence_assessment,
)

from treasury_intelligence.analytics.execution_evidence import (
    assess_xetra_position_execution_evidence,
)

from treasury_intelligence.analytics.execution_returns import (
    apply_position_execution_evidence,
)

from treasury_intelligence.analytics.frictions import (
    build_xeon_return_components,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
)

from treasury_intelligence.sources.ibkr import (
    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE,
)

from treasury_intelligence.sources.xetra import (
    XEON_XETRA_2024_TURNOVER,
    XEON_XETRA_XLM_100K,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
    get_xeon_market_observation,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
)

REFERENCE_YIELD_PCT = 2.273
HOLDING_PERIOD_DAYS = 365

SPREAD_SLIPPAGE_COMPONENT_ID = (
    "xeon_spread_slippage"
)

ACCESS_FEE_COMPONENT_ID = (
    "xeon_access_fee"
)


def find_component(
    components: tuple,
    component_id: str,
):
    matches = tuple(
        component
        for component in components
        if component.component_id == component_id
    )

    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one component "
            f"with ID {component_id}."
        )

    return matches[0]


def format_pct(
    value: float | None,
) -> str:
    if value is None:
        return "UNKNOWN"

    return f"{value:.3f}%"


def format_bps(
    value: float | None,
) -> str:
    if value is None:
        return "UNKNOWN"

    return f"{value:.1f} bps"


def build_evidence_enriched_components(
    position_size_eur: float,
    current_daily_turnover_eur: float | None,
) -> tuple:
    base_components = (
        build_xeon_return_components(
            position_size_eur=position_size_eur,
            reference_yield_pct=(
                REFERENCE_YIELD_PCT
            ),
        )
    )

    execution_evidence = (
        assess_xetra_position_execution_evidence(
            assessment_id=(
                "xeon_enriched_execution_"
                f"{int(position_size_eur)}"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=(
                XEON_MARKET.market_id
            ),
            position_size_eur=(
                position_size_eur
            ),
            xlm_evidence=(
                XEON_XETRA_XLM_100K
            ),
            annual_turnover_evidence=(
                XEON_XETRA_2024_TURNOVER
            ),
            current_daily_turnover_eur=(
                current_daily_turnover_eur
            ),
            notes=(
                "Public Xetra execution evidence "
                "used by the XEON inspection fixture."
            ),
        )
    )

    execution_enriched_components = (
        apply_position_execution_evidence(
            components=base_components,
            execution_evidence=execution_evidence,
            component_id=(
                SPREAD_SLIPPAGE_COMPONENT_ID
            ),
            label=(
                "XEON position-sized Xetra "
                "implicit execution cost"
            ),
            source="Deutsche Boerse Xetra",
            notes=(
                "Published Xetra Liquidity Measure "
                "is applied only when the requested "
                "position matches the measured order "
                "size. No XLM execution-cost value "
                "is extrapolated to larger positions."
            ),
        )
    )

    return apply_access_cost_evidence(
        components=execution_enriched_components,
        access_cost_evidence=(
            IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE
        ),
        component_id=ACCESS_FEE_COMPONENT_ID,
        label=(
            "Published recurring IBKR access "
            "cost for Germany/Xetra ETF route"
        ),
    )


def print_evidence_gaps(
    economics,
) -> None:
    if not economics.evidence_gaps:
        print(
            "Blocking evidence gaps:        NONE"
        )
        return

    print("BLOCKING EVIDENCE GAPS")
    print()

    for index, gap in enumerate(
        economics.evidence_gaps,
        start=1,
    ):
        print(
            f"{index}. {gap.component_label}"
        )

        print(
            f"   Component:                  "
            f"{gap.component_id}"
        )

        print(
            f"   Status:                     "
            f"{gap.current_status}"
        )

        print(
            f"   Priority:                   "
            f"{gap.priority}"
        )

        print(
            f"   Blocking:                   "
            f"{gap.blocking}"
        )

        print()


def inspect_position(
    position_size_eur: float,
) -> None:
    market_observation = (
        get_xeon_market_observation()
    )

    components = (
        build_evidence_enriched_components(
            position_size_eur=(
                position_size_eur
            ),
            current_daily_turnover_eur=(
                market_observation
                .daily_turnover_eur
            ),
        )
    )

    spread_component = find_component(
        components=components,
        component_id=(
            SPREAD_SLIPPAGE_COMPONENT_ID
        ),
    )

    access_component = find_component(
        components=components,
        component_id=(
            ACCESS_FEE_COMPONENT_ID
        ),
    )

    return_analysis = (
        build_return_analysis(
            analysis_id=(
                "xeon_enriched_return_analysis_"
                f"{int(position_size_eur)}"
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
                position_size_eur
            ),
            holding_period_days=(
                HOLDING_PERIOD_DAYS
            ),
            components=components,
            notes=(
                "XEON inspection using generic "
                "return-evidence enrichment "
                "primitives."
            ),
        )
    )

    economics = (
        build_economics_evidence_assessment(
            return_analysis
        )
    )

    print(
        f"EUR {position_size_eur:,.0f} POSITION"
    )
    print()

    print(
        f"Component count:               "
        f"{len(components)}"
    )
    print()

    print("EXECUTION COST")
    print()

    print(
        f"Status:                        "
        f"{spread_component.status}"
    )

    print(
        f"Roundtrip cost:                "
        f"{format_bps(spread_component.value)}"
    )

    print(
        f"Source:                        "
        f"{spread_component.source}"
    )
    print()

    print("ACCESS COST")
    print()

    print(
        f"Status:                        "
        f"{access_component.status}"
    )

    print(
        f"Annual cost:                   "
        f"{format_pct(access_component.value)}"
    )

    print(
        f"Source:                        "
        f"{access_component.source}"
    )
    print()

    print("RETURN ANALYSIS")
    print()

    print(
        f"Return after known costs:      "
        f"{format_pct(return_analysis.return_after_known_costs_pct)}"
    )

    print(
        f"Realistic expected return:     "
        f"{format_pct(return_analysis.realistic_expected_return_pct)}"
    )
    print()

    print("ECONOMICS")
    print()

    print(
        f"Status:                        "
        f"{economics.economics_status}"
    )

    print(
        f"Realistic return available:    "
        f"{economics.realistic_expected_return_available}"
    )

    print(
        f"Blocking gaps:                 "
        f"{economics.blocking_gap_count}"
    )
    print()

    print_evidence_gaps(
        economics=economics,
    )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print(
        "XEON GENERIC EVIDENCE-ENRICHMENT INSPECTION"
    )
    print()

    print(
        "This inspection validates that XEON can "
        "be assembled from generic production "
        "return-evidence enrichment primitives."
    )
    print()

    print(
        "There is no XEON-specific production "
        "return orchestrator."
    )
    print()

    print("=" * 100)
    print()

    for position_size_eur in POSITION_SIZES_EUR:
        inspect_position(
            position_size_eur=position_size_eur,
        )

    print("EXPECTED RESULT")
    print()

    print("EUR 100,000")
    print(
        "  Xetra execution cost:        2.4 bps"
    )
    print(
        "  IBKR recurring access cost:  0.000%"
    )
    print(
        "  Realistic expected return:   2.049%"
    )
    print(
        "  Economics:                   complete"
    )
    print(
        "  Blocking gaps:               0"
    )
    print()

    print("EUR 500,000")
    print(
        "  Xetra execution cost:        UNKNOWN"
    )
    print(
        "  IBKR recurring access cost:  0.000%"
    )
    print(
        "  Realistic expected return:   UNKNOWN"
    )
    print(
        "  Economics:                   incomplete"
    )
    print(
        "  Blocking gaps:               1"
    )


if __name__ == "__main__":
    main()