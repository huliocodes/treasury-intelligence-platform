from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.access_returns import (
    apply_xeon_access_cost_evidence,
)

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


def find_component(
    components: tuple,
    component_id: str,
):
    matches = tuple(
        component
        for component in components
        if component.component_id
        == component_id
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


def print_evidence_gaps(
    economics,
) -> None:
    if not economics.evidence_gaps:
        print(
            "Blocking evidence gaps:        NONE"
        )
        return

    print(
        "BLOCKING EVIDENCE GAPS"
    )
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

        print(
            "   Required evidence:"
        )

        print(
            f"   {gap.required_evidence}"
        )

        print()

        print(
            "   Resolution:"
        )

        print(
            f"   {gap.resolution_action}"
        )

        print()


def inspect_position(
    position_size_eur: float,
) -> None:
    market_observation = (
        get_xeon_market_observation()
    )

    execution_evidence = (
        assess_xetra_position_execution_evidence(
            assessment_id=(
                "xeon_access_cost_execution_"
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
                "XEON access-cost integration "
                "validation."
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

    execution_enriched_components = (
        apply_xeon_execution_evidence(
            components=(
                base_components
            ),
            execution_evidence=(
                execution_evidence
            ),
        )
    )

    fully_enriched_components = (
        apply_xeon_access_cost_evidence(
            components=(
                execution_enriched_components
            ),
            access_cost_evidence=(
                IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE
            ),
        )
    )

    spread_component = (
        find_component(
            components=(
                fully_enriched_components
            ),
            component_id=(
                "xeon_spread_slippage"
            ),
        )
    )

    access_fee_component = (
        find_component(
            components=(
                fully_enriched_components
            ),
            component_id=(
                "xeon_access_fee"
            ),
        )
    )

    return_analysis = (
        build_return_analysis(
            analysis_id=(
                "xeon_access_cost_integrated_"
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
                fully_enriched_components
            ),
            notes=(
                "XEON return analysis with "
                "position-sized Xetra execution "
                "evidence and route-specific IBKR "
                "recurring access-cost evidence."
            ),
        )
    )

    economics = (
        build_economics_evidence_assessment(
            return_analysis
        )
    )

    access_evidence = (
        IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE
    )

    print(
        f"EUR {position_size_eur:,.0f} POSITION"
    )
    print()

    print(
        "IBKR ROUTE-SPECIFIC ACCESS EVIDENCE"
    )
    print()

    print(
        f"Account minimum:               "
        f"USD {access_evidence.account_minimum_usd:.2f}"
    )

    print(
        f"Inactivity fee:                "
        f"USD {access_evidence.inactivity_fee_usd:.2f}"
    )

    print(
        f"Platform fee:                  "
        f"{access_evidence.platform_fee_pct:.3f}%"
    )

    print(
        f"Generic custody fee found:     "
        f"{access_evidence.generic_custody_fee_identified}"
    )

    print(
        f"Recurring access cost:         "
        f"{access_evidence.recurring_access_cost_pct:.3f}%"
    )

    print(
        f"Specific account verified:     "
        f"{access_evidence.specific_account_terms_verified}"
    )

    print()

    print(
        "POSITION-SIZED EXECUTION EVIDENCE"
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

    print(
        f"Xetra implicit roundtrip cost: "
        f"{format_bps(spread_component.value)}"
    )

    print()

    print(
        "RETURN COMPONENTS"
    )
    print()

    print(
        f"Spread/slippage status:        "
        f"{spread_component.status}"
    )

    print(
        f"Spread/slippage value:         "
        f"{format_bps(spread_component.value)}"
    )

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
        f"Realistic return available:    "
        f"{economics.realistic_expected_return_available}"
    )

    print(
        f"Blocking gaps:                 "
        f"{economics.blocking_gap_count}"
    )

    print()

    print_evidence_gaps(
        economics=(
            economics
        ),
    )

    print()

    print(
        "Strongest supported claim:"
    )

    print(
        economics.strongest_supported_claim
    )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print(
        "XEON ROUTE-SPECIFIC ACCESS-COST INTEGRATION"
    )
    print()

    print(
        "This inspection applies published IBKR "
        "organization-account and Germany/Xetra "
        "ETF fee evidence without treating "
        "execution-stage account confirmation as "
        "an unresolved economic cost."
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
        "  Broker commissions are known."
    )

    print(
        "  Position-sized Xetra implicit "
        "execution cost is known."
    )

    print(
        "  Route-specific recurring IBKR "
        "access cost is modeled as zero from "
        "published public pricing."
    )

    print(
        "  Economics should therefore become "
        "complete."
    )

    print()

    print(
        "EUR 500,000:"
    )

    print(
        "  Broker commissions are known."
    )

    print(
        "  Route-specific recurring IBKR access "
        "cost is known."
    )

    print(
        "  Position-sized Xetra execution cost "
        "remains unknown."
    )

    print(
        "  Economics should therefore remain "
        "incomplete with one blocking gap."
    )

    print()

    print(
        "Specific future corporate-account terms "
        "remain an execution-stage confirmation "
        "and are not represented as a fabricated "
        "economic cost."
    )


if __name__ == "__main__":
    main()