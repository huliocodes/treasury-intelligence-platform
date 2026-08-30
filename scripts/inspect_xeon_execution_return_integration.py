from dataclasses import fields, is_dataclass
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.economics import (
    build_economics_evidence_assessment,
)

from treasury_intelligence.analytics.execution_evidence import (
    assess_xetra_position_execution_evidence,
)

from treasury_intelligence.analytics.execution_returns import (
    apply_xeon_execution_evidence,
)

from treasury_intelligence.analytics.frictions import (
    build_xeon_return_components,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
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


def print_economics_schema(
    economics,
) -> None:
    print(
        "ECONOMICS OBJECT FIELDS"
    )
    print()

    if not is_dataclass(economics):
        print(
            "Economics assessment is not a dataclass."
        )
        return

    for field in fields(economics):
        value = getattr(
            economics,
            field.name,
        )

        print(
            f"  {field.name:<30}"
            f"{repr(value)}"
        )


def inspect_position(
    position_size_eur: float,
) -> None:
    market_observation = (
        get_xeon_market_observation()
    )

    execution_evidence = (
        assess_xetra_position_execution_evidence(
            assessment_id=(
                "xeon_execution_return_"
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
                market_observation
                .daily_turnover_eur
            ),
            notes=(
                "XEON execution-return "
                "integration validation."
            ),
        )
    )

    base_components = (
        build_xeon_return_components(
            position_size_eur=(
                position_size_eur
            ),
            reference_yield_pct=(
                REFERENCE_YIELD_PCT
            ),
        )
    )

    enriched_components = (
        apply_xeon_execution_evidence(
            components=(
                base_components
            ),
            execution_evidence=(
                execution_evidence
            ),
        )
    )

    base_spread_component = (
        find_component(
            components=(
                base_components
            ),
            component_id=(
                "xeon_spread_slippage"
            ),
        )
    )

    enriched_spread_component = (
        find_component(
            components=(
                enriched_components
            ),
            component_id=(
                "xeon_spread_slippage"
            ),
        )
    )

    access_fee_component = (
        find_component(
            components=(
                enriched_components
            ),
            component_id=(
                "xeon_access_fee"
            ),
        )
    )

    return_analysis = (
        build_return_analysis(
            analysis_id=(
                "xeon_execution_integrated_"
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
            components=(
                enriched_components
            ),
            notes=(
                "XEON return analysis with "
                "position-sized public Xetra "
                "execution evidence where "
                "supported."
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
        f"Execution evidence:            "
        f"{execution_evidence.execution_evidence_status}"
    )

    print(
        f"Position-sized cost supported: "
        f"{execution_evidence.position_sized_cost_supported}"
    )

    print()

    print(
        "SPREAD / SLIPPAGE COMPONENT"
    )
    print()

    print(
        f"Before status:                 "
        f"{base_spread_component.status}"
    )

    print(
        f"Before value:                  "
        f"{format_bps(base_spread_component.value)}"
    )

    print(
        f"After status:                  "
        f"{enriched_spread_component.status}"
    )

    print(
        f"After value:                   "
        f"{format_bps(enriched_spread_component.value)}"
    )

    print(
        f"After source:                  "
        f"{enriched_spread_component.source}"
    )

    print()

    print(
        "RESIDUAL ACCESS COST"
    )
    print()

    print(
        f"Access-fee status:             "
        f"{access_fee_component.status}"
    )

    print(
        f"Access-fee value:              "
        f"{format_pct(access_fee_component.value)}"
    )

    print()

    print(
        "RETURN ANALYSIS"
    )
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

    print(
        "ECONOMICS EVIDENCE"
    )
    print()

    print(
        f"Economics status:              "
        f"{economics.economics_status}"
    )

    print(
        f"Blocking gaps:                 "
        f"{economics.blocking_gap_count}"
    )

    print()

    print_economics_schema(
        economics=(
            economics
        ),
    )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print(
        "XEON EXECUTION EVIDENCE → RETURN INTEGRATION"
    )
    print()

    print(
        "Position-sized public Xetra execution "
        "evidence is applied to the existing "
        "XEON return-component model without "
        "extrapolation."
    )
    print()

    print(
        "The comparison demonstrates whether "
        "economics evidence improves differently "
        "at EUR 100,000 and EUR 500,000."
    )
    print()

    print("=" * 100)
    print()

    for position_size_eur in POSITION_SIZES_EUR:
        inspect_position(
            position_size_eur=(
                position_size_eur
            ),
        )

    print(
        "EXPECTED INTERPRETATION"
    )
    print()

    print(
        "EUR 100,000:"
    )

    print(
        "  Xetra execution-cost gap closes."
    )

    print(
        "  Residual corporate access cost remains "
        "unknown."
    )

    print(
        "  Economics therefore improves from two "
        "blocking gaps to one."
    )

    print()

    print(
        "EUR 500,000:"
    )

    print(
        "  Position-sized Xetra execution cost "
        "remains unknown."
    )

    print(
        "  Residual corporate access cost also "
        "remains unknown."
    )

    print(
        "  Economics therefore remains incomplete "
        "with two blocking gaps."
    )

    print()

    print(
        "No XLM value is extrapolated beyond its "
        "published EUR 100,000 measurement size."
    )


if __name__ == "__main__":
    main()