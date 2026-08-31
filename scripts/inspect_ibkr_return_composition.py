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


from treasury_intelligence.analytics.ibkr_returns import (
    build_ibkr_return_components,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
)

from treasury_intelligence.sources.ibkr import (
    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE,
    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_INSTRUMENT,
    XEON_MARKET,
    build_xeon_snapshot,
)


ESTR_RATE_PCT = 2.188
ESTR_REFERENCE_DATE = "2026-08-27"

POSITION_SIZES_EUR = (
    100_000,
    500_000,
    1_000_000,
    2_000_000,
    5_000_000,
)

HOLDING_PERIOD_DAYS = 365


def main() -> None:
    snapshot = build_xeon_snapshot(
        estr_rate_pct=ESTR_RATE_PCT,
        estr_reference_date=ESTR_REFERENCE_DATE,
    )

    print("IBKR RETURN COMPOSITION")
    print("=" * 72)

    for position_size_eur in POSITION_SIZES_EUR:
        components = (
            build_ibkr_return_components(
                instrument=XEON_INSTRUMENT,
                market=XEON_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
                access_cost_evidence=(
                    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE
                ),
                trading_cost_evidence=(
                    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE
                ),
            )
        )

        analysis = build_return_analysis(
            analysis_id=(
                f"ibkr_composition_"
                f"{int(position_size_eur)}"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            access_route_id=(
                snapshot.access_route_id
            ),
            position_size_eur=(
                position_size_eur
            ),
            holding_period_days=(
                HOLDING_PERIOD_DAYS
            ),
            components=components,
        )

        access_component = next(
            component
            for component in components
            if component.component_type
            == "access_fee"
        )

        entry_component = next(
            component
            for component in components
            if component.component_type
            == "entry_execution_cost"
        )

        exit_component = next(
            component
            for component in components
            if component.component_type
            == "exit_execution_cost"
        )

        slippage_component = next(
            component
            for component in components
            if component.component_type
            == "slippage_price_impact"
        )

        assert access_component.status == "published"
        assert access_component.value == 0.0

        assert entry_component.status == "published"
        assert entry_component.value == 5.0

        assert exit_component.status == "published"
        assert exit_component.value == 5.0

        assert slippage_component.status == "unknown"
        assert slippage_component.value is None

        assert (
            analysis.unknown_cost_component_count
            == 1
        )

        assert (
            abs(
                analysis.known_one_time_cost_bps
                - 10.0
            )
            < 0.000001
        )

        assert (
            analysis.economics_complete
            is False
        )

        assert (
            analysis.realistic_expected_return_pct
            is None
        )

        expected_after_known_costs = (
            snapshot.yield_value_pct
            - 0.10
        )

        assert (
            analysis.return_after_known_costs_pct
            is not None
        )

        assert (
            abs(
                analysis.return_after_known_costs_pct
                - expected_after_known_costs
            )
            < 0.000001
        )

        print()
        print(
            f"EUR {position_size_eur:,.0f}"
        )

        print(
            "  reference yield:",
            f"{analysis.reference_yield_pct:.3f}%",
        )

        print(
            "  recurring access cost:",
            (
                f"{analysis.known_recurring_annualized_cost_pct:.3f}%"
            ),
        )

        print(
            "  roundtrip broker commission:",
            (
                f"{analysis.known_one_time_cost_bps:.3f} bps"
            ),
        )

        print(
            "  roundtrip broker commission EUR:",
            (
                f"EUR "
                f"{analysis.known_one_time_cost_eur:,.2f}"
            ),
        )

        print(
            "  return after known costs:",
            (
                f"{analysis.return_after_known_costs_pct:.3f}%"
            ),
        )

        print(
            "  remaining unknown costs:",
            analysis.unknown_cost_component_count,
        )

        print(
            "  slippage:",
            slippage_component.status,
        )

        print(
            "  economics complete:",
            analysis.economics_complete,
        )

    print()
    print(
        "PASS: IBKR route evidence composes recurring "
        "access cost and published broker commissions "
        "without assuming spread or slippage."
    )


if __name__ == "__main__":
    main()
