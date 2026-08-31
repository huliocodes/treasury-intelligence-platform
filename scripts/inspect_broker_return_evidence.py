from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_DIR),
    )


from treasury_intelligence.analytics.broker_returns import (
    apply_broker_trading_cost_evidence,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
)

from treasury_intelligence.models.returns import (
    ReturnComponent,
)

from treasury_intelligence.sources.ibkr import (
    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
    1_000_000,
    2_000_000,
    5_000_000,
)

HOLDING_PERIOD_DAYS = 365

REFERENCE_YIELD_PCT = 2.173


def build_base_components(
    position_size_eur: float,
) -> tuple[ReturnComponent, ...]:
    return (
        ReturnComponent(
            component_id="test_reference_yield",
            component_type="reference_yield",
            label="Test reference yield",
            status="published",
            basis="annualized_pct",
            value=REFERENCE_YIELD_PCT,
        ),
        ReturnComponent(
            component_id="test_access_fee",
            component_type="access_fee",
            label="Recurring access cost",
            status="known_zero",
            basis="annualized_pct",
            value=0.0,
        ),
        ReturnComponent(
            component_id="test_entry_execution",
            component_type="entry_execution_cost",
            label="Entry execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="test_exit_execution",
            component_type="exit_execution_cost",
            label="Exit execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="test_slippage",
            component_type="slippage_price_impact",
            label=(
                "Round-trip spread, slippage, "
                "or market impact"
            ),
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="test_fx_cost",
            component_type="fx_hedging_cost",
            label="FX conversion or hedging cost",
            status="known_zero",
            basis="annualized_pct",
            value=0.0,
        ),
    )


def main() -> None:
    evidence = (
        IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE
    )

    print(
        "Broker:",
        evidence.broker,
    )
    print(
        "Market country:",
        evidence.market_country,
    )
    print(
        "Pricing plan:",
        evidence.pricing_plan,
    )
    print(
        "Routing method:",
        evidence.routing_method,
    )
    print(
        "Published commission bps:",
        evidence.commission_bps,
    )
    print()

    for position_size_eur in POSITION_SIZES_EUR:
        components = build_base_components(
            position_size_eur
        )

        enriched_components = (
            apply_broker_trading_cost_evidence(
                components=components,
                trading_cost_evidence=evidence,
                entry_component_id=(
                    "test_entry_execution"
                ),
                exit_component_id=(
                    "test_exit_execution"
                ),
            )
        )

        analysis = build_return_analysis(
            analysis_id=(
                "broker_return_evidence_"
                f"{int(position_size_eur)}"
            ),
            instrument_id="test_instrument",
            market_id="test_market",
            access_route_id="test_access_route",
            position_size_eur=(
                position_size_eur
            ),
            holding_period_days=(
                HOLDING_PERIOD_DAYS
            ),
            components=enriched_components,
            notes=(
                "Validation of generic published "
                "broker commission enrichment."
            ),
        )

        entry_component = next(
            component
            for component in enriched_components
            if component.component_id
            == "test_entry_execution"
        )

        exit_component = next(
            component
            for component in enriched_components
            if component.component_id
            == "test_exit_execution"
        )

        slippage_component = next(
            component
            for component in enriched_components
            if component.component_id
            == "test_slippage"
        )

        expected_one_way_cost_eur = (
            position_size_eur
            * evidence.commission_bps
            / 10_000
        )

        expected_roundtrip_cost_eur = (
            expected_one_way_cost_eur
            * 2
        )

        assert (
            entry_component.status
            == "published"
        )

        assert (
            exit_component.status
            == "published"
        )

        assert (
            entry_component.value
            == evidence.commission_bps
        )

        assert (
            exit_component.value
            == evidence.commission_bps
        )

        assert (
            slippage_component.status
            == "unknown"
        )

        assert (
            slippage_component.value
            is None
        )

        assert (
            abs(
                analysis.known_one_time_cost_bps
                - 10.0
            )
            < 0.000001
        )

        assert (
            abs(
                analysis.known_one_time_cost_eur
                - expected_roundtrip_cost_eur
            )
            < 0.000001
        )

        assert (
            analysis.unknown_cost_component_count
            == 1
        )

        assert (
            analysis.economics_complete
            is False
        )

        assert (
            analysis.realistic_expected_return_pct
            is None
        )

        print(
            f"EUR {position_size_eur:,.0f}"
        )
        print(
            "  entry commission:",
            f"{entry_component.value:.3f} bps",
        )
        print(
            "  exit commission:",
            f"{exit_component.value:.3f} bps",
        )
        print(
            "  roundtrip broker commission:",
            (
                f"EUR "
                f"{analysis.known_one_time_cost_eur:,.2f}"
            ),
        )
        print(
            "  known roundtrip cost:",
            (
                f"{analysis.known_one_time_cost_bps:.3f} "
                "bps"
            ),
        )
        print(
            "  slippage status:",
            slippage_component.status,
        )
        print(
            "  economics complete:",
            analysis.economics_complete,
        )
        print(
            "  realistic expected return:",
            (
                analysis
                .realistic_expected_return_pct
            ),
        )
        print()

    print(
        "PASS: published broker commissions are "
        "modeled independently from position-sized "
        "spread/slippage evidence."
    )


if __name__ == "__main__":
    main()
