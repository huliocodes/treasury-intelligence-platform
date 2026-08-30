from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.switching_friction import (
    build_switching_friction_assessment,
)

from treasury_intelligence.models.allocation_deltas import (
    AllocationDeltaLine,
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.economic_comparisons import (
    TreasuryEconomicComparison,
)

from treasury_intelligence.models.switching_friction import (
    SwitchingFrictionInput,
)


MANDATE_ID = "si_model_company_v1"
TREASURY_CAPITAL_EUR = 5_000_000


def build_rotation_delta(
) -> TreasuryAllocationDelta:
    return TreasuryAllocationDelta(
        delta_id="fixture_rotation_delta",
        mandate_id=MANDATE_ID,
        state_id="fixture_rotation_state",
        proposal_id="fixture_rotation_proposal",
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        current_invested_capital_eur=(
            500_000
        ),
        proposed_invested_capital_eur=(
            500_000
        ),
        current_unallocated_capital_eur=(
            4_500_000
        ),
        proposed_unallocated_capital_eur=(
            4_500_000
        ),
        gross_position_movement_eur=(
            1_000_000
        ),
        change_required=True,
        delta_lines=(
            AllocationDeltaLine(
                instrument_id="instrument_a",
                market_id="market_a",
                access_route_id="access_a",
                label="POSITION A",
                current_value_eur=500_000,
                proposed_value_eur=0,
                delta_eur=-500_000,
                action="close",
            ),
            AllocationDeltaLine(
                instrument_id="instrument_b",
                market_id="market_b",
                access_route_id="access_b",
                label="POSITION B",
                current_value_eur=0,
                proposed_value_eur=500_000,
                delta_eur=500_000,
                action="open",
            ),
        ),
    )


def build_rotation_comparison(
    incremental_benefit_eur: float = 5_000,
) -> TreasuryEconomicComparison:
    return TreasuryEconomicComparison(
        comparison_id=(
            "fixture_rotation_comparison"
        ),
        mandate_id=MANDATE_ID,
        state_id="fixture_rotation_state",
        proposal_id="fixture_rotation_proposal",
        delta_id="fixture_rotation_delta",
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        comparison_status="complete",
        current_annual_return_eur=55_000,
        proposed_annual_return_eur=(
            55_000
            + incremental_benefit_eur
        ),
        incremental_annual_benefit_eur=(
            incremental_benefit_eur
        ),
        incremental_annual_benefit_pct_of_treasury=(
            incremental_benefit_eur
            / TREASURY_CAPITAL_EUR
            * 100.0
        ),
        current_lines=(),
        proposed_lines=(),
        missing_evidence=(),
    )


def build_unchanged_delta(
) -> TreasuryAllocationDelta:
    return TreasuryAllocationDelta(
        delta_id="fixture_unchanged_delta",
        mandate_id=MANDATE_ID,
        state_id="fixture_unchanged_state",
        proposal_id="fixture_unchanged_proposal",
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        current_invested_capital_eur=(
            500_000
        ),
        proposed_invested_capital_eur=(
            500_000
        ),
        current_unallocated_capital_eur=(
            4_500_000
        ),
        proposed_unallocated_capital_eur=(
            4_500_000
        ),
        gross_position_movement_eur=0,
        change_required=False,
        delta_lines=(
            AllocationDeltaLine(
                instrument_id="instrument_a",
                market_id="market_a",
                access_route_id="access_a",
                label="POSITION A",
                current_value_eur=500_000,
                proposed_value_eur=500_000,
                delta_eur=0,
                action="unchanged",
            ),
        ),
    )


def build_unchanged_comparison(
) -> TreasuryEconomicComparison:
    return TreasuryEconomicComparison(
        comparison_id=(
            "fixture_unchanged_comparison"
        ),
        mandate_id=MANDATE_ID,
        state_id="fixture_unchanged_state",
        proposal_id="fixture_unchanged_proposal",
        delta_id="fixture_unchanged_delta",
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        comparison_status="complete",
        current_annual_return_eur=55_000,
        proposed_annual_return_eur=55_000,
        incremental_annual_benefit_eur=0,
        incremental_annual_benefit_pct_of_treasury=0,
        current_lines=(),
        proposed_lines=(),
        missing_evidence=(),
    )


def print_assessment(
    label: str,
    assessment,
) -> None:
    print(label)
    print()

    print(
        f"Friction status:              "
        f"{assessment.friction_status}"
    )

    print(
        f"Gross position movement:      "
        f"EUR "
        f"{assessment.gross_position_movement_eur:,.0f}"
    )

    print(
        f"Known switching cost:         "
        f"EUR "
        f"{assessment.known_switching_cost_eur:,.0f}"
    )

    if assessment.total_switching_cost_eur is None:
        total_cost = "UNKNOWN"
    else:
        total_cost = (
            "EUR "
            f"{assessment.total_switching_cost_eur:,.0f}"
        )

    print(
        f"Total switching cost:         "
        f"{total_cost}"
    )

    if (
        assessment.incremental_annual_benefit_eur
        is None
    ):
        annual_benefit = "UNKNOWN"
    else:
        annual_benefit = (
            "EUR "
            f"{assessment.incremental_annual_benefit_eur:,.0f}"
        )

    print(
        f"Incremental annual benefit:   "
        f"{annual_benefit}"
    )

    if (
        assessment.first_year_net_benefit_eur
        is None
    ):
        net_benefit = "UNKNOWN"
    else:
        net_benefit = (
            "EUR "
            f"{assessment.first_year_net_benefit_eur:,.0f}"
        )

    print(
        f"First-year net benefit:       "
        f"{net_benefit}"
    )

    if assessment.payback_days is None:
        payback = "N/A"
    else:
        payback = (
            f"{assessment.payback_days:.1f} days"
        )

    print(
        f"Switching-cost payback:       "
        f"{payback}"
    )

    print(
        f"Net benefit available:        "
        f"{assessment.net_benefit_available}"
    )

    if assessment.friction_lines:
        print()
        print("FRICTION LINES")
        print()

        for line in assessment.friction_lines:
            if line.friction_bps is None:
                bps = "UNKNOWN"
            else:
                bps = (
                    f"{line.friction_bps:.2f} bps"
                )

            if line.switching_cost_eur is None:
                cost = "UNKNOWN"
            else:
                cost = (
                    "EUR "
                    f"{line.switching_cost_eur:,.0f}"
                )

            print(
                f"  {line.label:<20} "
                f"{line.action:<10} | "
                f"movement EUR "
                f"{line.movement_eur:>10,.0f} | "
                f"{bps:<12} | "
                f"{cost}"
            )

    if assessment.missing_evidence:
        print()
        print("MISSING EVIDENCE")
        print()

        for item in assessment.missing_evidence:
            print(
                f"  - {item}"
            )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print("SWITCHING FRICTION ANALYSIS")
    print()

    print(
        "The switching-friction layer applies "
        "transaction costs only to capital that "
        "actually changes allocation."
    )

    print()
    print("-" * 100)
    print()

    rotation_delta = (
        build_rotation_delta()
    )

    rotation_comparison = (
        build_rotation_comparison()
    )

    complete_rotation = (
        build_switching_friction_assessment(
            assessment_id=(
                "fixture_complete_rotation"
            ),
            delta=rotation_delta,
            economic_comparison=(
                rotation_comparison
            ),
            friction_inputs=(
                SwitchingFrictionInput(
                    instrument_id="instrument_a",
                    market_id="market_a",
                    access_route_id="access_a",
                    label="POSITION A",
                    action="close",
                    friction_bps=5.0,
                    fixed_cost_eur=0,
                    evidence_available=True,
                    source_reference=(
                        "fixture_exit_cost"
                    ),
                ),
                SwitchingFrictionInput(
                    instrument_id="instrument_b",
                    market_id="market_b",
                    access_route_id="access_b",
                    label="POSITION B",
                    action="open",
                    friction_bps=5.0,
                    fixed_cost_eur=0,
                    evidence_available=True,
                    source_reference=(
                        "fixture_entry_cost"
                    ),
                ),
            ),
        )
    )

    print_assessment(
        label=(
            "CASE 1 — COMPLETE EUR 500K ROTATION"
        ),
        assessment=complete_rotation,
    )

    unknown_entry = (
        build_switching_friction_assessment(
            assessment_id=(
                "fixture_unknown_entry"
            ),
            delta=rotation_delta,
            economic_comparison=(
                rotation_comparison
            ),
            friction_inputs=(
                SwitchingFrictionInput(
                    instrument_id="instrument_a",
                    market_id="market_a",
                    access_route_id="access_a",
                    label="POSITION A",
                    action="close",
                    friction_bps=5.0,
                    fixed_cost_eur=0,
                    evidence_available=True,
                ),
                SwitchingFrictionInput(
                    instrument_id="instrument_b",
                    market_id="market_b",
                    access_route_id="access_b",
                    label="POSITION B",
                    action="open",
                    friction_bps=None,
                    fixed_cost_eur=None,
                    evidence_available=False,
                    notes=(
                        "Executable entry spread and "
                        "slippage are unknown."
                    ),
                ),
            ),
        )
    )

    print_assessment(
        label=(
            "CASE 2 — UNKNOWN ENTRY FRICTION"
        ),
        assessment=unknown_entry,
    )

    unchanged_delta = (
        build_unchanged_delta()
    )

    unchanged_comparison = (
        build_unchanged_comparison()
    )

    unchanged_assessment = (
        build_switching_friction_assessment(
            assessment_id=(
                "fixture_unchanged"
            ),
            delta=unchanged_delta,
            economic_comparison=(
                unchanged_comparison
            ),
            friction_inputs=(),
        )
    )

    print_assessment(
        label=(
            "CASE 3 — UNCHANGED PORTFOLIO"
        ),
        assessment=unchanged_assessment,
    )

    negative_comparison = (
        build_rotation_comparison(
            incremental_benefit_eur=-2_500,
        )
    )

    negative_assessment = (
        build_switching_friction_assessment(
            assessment_id=(
                "fixture_negative_benefit"
            ),
            delta=rotation_delta,
            economic_comparison=(
                negative_comparison
            ),
            friction_inputs=(
                SwitchingFrictionInput(
                    instrument_id="instrument_a",
                    market_id="market_a",
                    access_route_id="access_a",
                    label="POSITION A",
                    action="close",
                    friction_bps=5.0,
                    fixed_cost_eur=0,
                    evidence_available=True,
                ),
                SwitchingFrictionInput(
                    instrument_id="instrument_b",
                    market_id="market_b",
                    access_route_id="access_b",
                    label="POSITION B",
                    action="open",
                    friction_bps=5.0,
                    fixed_cost_eur=0,
                    evidence_available=True,
                ),
            ),
        )
    )

    print_assessment(
        label=(
            "CASE 4 — PROPOSED ALLOCATION "
            "HAS WORSE ECONOMICS"
        ),
        assessment=negative_assessment,
    )

    print("INTERPRETATION")
    print()

    print(
        "Case 1 prices both sides of a EUR 500,000 "
        "rotation. EUR 1,000,000 of gross transaction "
        "notional at 5 bps per leg creates EUR 500 of "
        "switching cost."
    )

    print(
        "Case 2 proves that known exit cost does not "
        "allow an unknown entry cost to be treated "
        "as zero."
    )

    print(
        "Case 3 proves that an unchanged portfolio "
        "requires no switching-friction inputs and "
        "has zero switching cost."
    )

    print(
        "Case 4 proves that switching friction can "
        "make already-worse economics even worse; "
        "no payback period is reported when the "
        "annual incremental benefit is non-positive."
    )

    print(
        "This layer still does not decide whether "
        "the treasury should rebalance."
    )


if __name__ == "__main__":
    main()