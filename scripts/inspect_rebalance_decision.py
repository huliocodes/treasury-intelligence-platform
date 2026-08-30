from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.rebalance import (
    build_rebalance_decision,
)

from treasury_intelligence.models.allocation_deltas import (
    AllocationDeltaLine,
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.economic_comparisons import (
    TreasuryEconomicComparison,
)

from treasury_intelligence.models.rebalance import (
    RebalancePolicy,
)

from treasury_intelligence.models.switching_friction import (
    SwitchingFrictionAssessment,
    SwitchingFrictionLine,
)


MANDATE_ID = "si_model_company_v1"
TREASURY_CAPITAL_EUR = 5_000_000


POLICY = RebalancePolicy(
    policy_id="fixture_rebalance_policy",
    minimum_first_year_net_improvement_bps_of_treasury=5.0,
    notes=(
        "Deterministic test policy. Five basis points "
        "is a fixture threshold, not yet a production "
        "treasury policy."
    ),
)


def build_delta(
    delta_id: str,
    change_required: bool,
) -> TreasuryAllocationDelta:
    if not change_required:
        return TreasuryAllocationDelta(
            delta_id=delta_id,
            mandate_id=MANDATE_ID,
            state_id=f"{delta_id}_state",
            proposal_id=f"{delta_id}_proposal",
            treasury_capital_eur=(
                TREASURY_CAPITAL_EUR
            ),
            current_invested_capital_eur=500_000,
            proposed_invested_capital_eur=500_000,
            current_unallocated_capital_eur=4_500_000,
            proposed_unallocated_capital_eur=4_500_000,
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

    return TreasuryAllocationDelta(
        delta_id=delta_id,
        mandate_id=MANDATE_ID,
        state_id=f"{delta_id}_state",
        proposal_id=f"{delta_id}_proposal",
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        current_invested_capital_eur=500_000,
        proposed_invested_capital_eur=500_000,
        current_unallocated_capital_eur=4_500_000,
        proposed_unallocated_capital_eur=4_500_000,
        gross_position_movement_eur=1_000_000,
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


def build_complete_comparison(
    delta: TreasuryAllocationDelta,
    incremental_benefit_eur: float,
) -> TreasuryEconomicComparison:
    return TreasuryEconomicComparison(
        comparison_id=(
            f"{delta.delta_id}_comparison"
        ),
        mandate_id=MANDATE_ID,
        state_id=delta.state_id,
        proposal_id=delta.proposal_id,
        delta_id=delta.delta_id,
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


def build_incomplete_comparison(
    delta: TreasuryAllocationDelta,
) -> TreasuryEconomicComparison:
    return TreasuryEconomicComparison(
        comparison_id=(
            f"{delta.delta_id}_comparison"
        ),
        mandate_id=MANDATE_ID,
        state_id=delta.state_id,
        proposal_id=delta.proposal_id,
        delta_id=delta.delta_id,
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        comparison_status="incomplete",
        current_annual_return_eur=None,
        proposed_annual_return_eur=60_000,
        incremental_annual_benefit_eur=None,
        incremental_annual_benefit_pct_of_treasury=None,
        current_lines=(),
        proposed_lines=(),
        missing_evidence=(
            "current return evidence unavailable for "
            "POSITION A.",
        ),
    )


def build_complete_friction(
    delta: TreasuryAllocationDelta,
    comparison: TreasuryEconomicComparison,
    switching_cost_eur: float,
) -> SwitchingFrictionAssessment:
    incremental_benefit = (
        comparison.incremental_annual_benefit_eur
    )

    if incremental_benefit is None:
        raise ValueError(
            "Complete friction fixture requires "
            "complete economics."
        )

    first_year_net_benefit = (
        incremental_benefit
        - switching_cost_eur
    )

    if (
        delta.gross_position_movement_eur
        <= 0.01
    ):
        friction_lines = ()

    else:
        half_movement = (
            delta.gross_position_movement_eur
            / 2.0
        )

        friction_bps = (
            switching_cost_eur
            / delta.gross_position_movement_eur
            * 10_000.0
        )

        friction_lines = (
            SwitchingFrictionLine(
                instrument_id="instrument_a",
                market_id="market_a",
                access_route_id="access_a",
                label="POSITION A",
                action="close",
                movement_eur=half_movement,
                friction_bps=friction_bps,
                fixed_cost_eur=0,
                switching_cost_eur=(
                    switching_cost_eur / 2.0
                ),
                evidence_available=True,
            ),
            SwitchingFrictionLine(
                instrument_id="instrument_b",
                market_id="market_b",
                access_route_id="access_b",
                label="POSITION B",
                action="open",
                movement_eur=half_movement,
                friction_bps=friction_bps,
                fixed_cost_eur=0,
                switching_cost_eur=(
                    switching_cost_eur / 2.0
                ),
                evidence_available=True,
            ),
        )

    return SwitchingFrictionAssessment(
        assessment_id=(
            f"{delta.delta_id}_friction"
        ),
        mandate_id=MANDATE_ID,
        delta_id=delta.delta_id,
        economic_comparison_id=(
            comparison.comparison_id
        ),
        gross_position_movement_eur=(
            delta.gross_position_movement_eur
        ),
        friction_status="complete",
        known_switching_cost_eur=(
            switching_cost_eur
        ),
        total_switching_cost_eur=(
            switching_cost_eur
        ),
        incremental_annual_benefit_eur=(
            incremental_benefit
        ),
        first_year_net_benefit_eur=(
            first_year_net_benefit
        ),
        payback_days=(
            (
                switching_cost_eur
                / incremental_benefit
                * 365.0
            )
            if incremental_benefit > 0
            else None
        ),
        net_benefit_available=True,
        friction_lines=friction_lines,
        missing_evidence=(),
    )


def build_incomplete_friction(
    delta: TreasuryAllocationDelta,
    comparison: TreasuryEconomicComparison,
) -> SwitchingFrictionAssessment:
    friction_lines = (
        SwitchingFrictionLine(
            instrument_id="instrument_a",
            market_id="market_a",
            access_route_id="access_a",
            label="POSITION A",
            action="close",
            movement_eur=500_000,
            friction_bps=5.0,
            fixed_cost_eur=0,
            switching_cost_eur=250,
            evidence_available=True,
            notes=(
                "Deterministic known exit-cost fixture."
            ),
        ),
        SwitchingFrictionLine(
            instrument_id="instrument_b",
            market_id="market_b",
            access_route_id="access_b",
            label="POSITION B",
            action="open",
            movement_eur=500_000,
            friction_bps=None,
            fixed_cost_eur=None,
            switching_cost_eur=None,
            evidence_available=False,
            notes=(
                "Executable entry spread and slippage "
                "remain unknown."
            ),
        ),
    )

    return SwitchingFrictionAssessment(
        assessment_id=(
            f"{delta.delta_id}_friction"
        ),
        mandate_id=MANDATE_ID,
        delta_id=delta.delta_id,
        economic_comparison_id=(
            comparison.comparison_id
        ),
        gross_position_movement_eur=(
            delta.gross_position_movement_eur
        ),
        friction_status="incomplete",
        known_switching_cost_eur=250,
        total_switching_cost_eur=None,
        incremental_annual_benefit_eur=(
            comparison.incremental_annual_benefit_eur
        ),
        first_year_net_benefit_eur=None,
        payback_days=None,
        net_benefit_available=False,
        friction_lines=(
            friction_lines
        ),
        missing_evidence=(
            "switching friction evidence unavailable "
            "for POSITION B (open).",
        ),
    )


def print_decision(
    label: str,
    decision,
) -> None:
    print(label)
    print()

    print(
        f"Decision status:              "
        f"{decision.decision_status}"
    )

    print(
        f"Decision:                     "
        f"{decision.decision}"
    )

    print(
        f"Allocation change required:   "
        f"{decision.allocation_change_required}"
    )

    if (
        decision.first_year_net_benefit_eur
        is None
    ):
        net_benefit = "UNKNOWN"
    else:
        net_benefit = (
            "EUR "
            f"{decision.first_year_net_benefit_eur:,.0f}"
        )

    print(
        f"First-year net benefit:       "
        f"{net_benefit}"
    )

    if (
        decision.first_year_net_improvement_bps_of_treasury
        is None
    ):
        improvement_bps = "UNKNOWN"
    else:
        improvement_bps = (
            f"{decision.first_year_net_improvement_bps_of_treasury:.2f} bps"
        )

    print(
        f"Net improvement:              "
        f"{improvement_bps}"
    )

    print(
        f"Required improvement:         "
        f"{decision.minimum_required_improvement_bps:.2f} bps"
    )

    if decision.threshold_met is None:
        threshold_met = "UNKNOWN"
    else:
        threshold_met = str(
            decision.threshold_met
        )

    print(
        f"Threshold met:                "
        f"{threshold_met}"
    )

    print()
    print(
        f"Rationale: {decision.rationale}"
    )

    if decision.evidence_requirements:
        print()
        print("EVIDENCE REQUIRED")
        print()

        for item in decision.evidence_requirements:
            print(
                f"  - {item}"
            )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print("REBALANCE DECISION")
    print()

    print(
        "The rebalance layer converts current-vs-proposed "
        "economics and switching friction into an explicit "
        "treasury decision using an auditable threshold."
    )

    print()

    print(
        "Fixture policy threshold: "
        f"{POLICY.minimum_first_year_net_improvement_bps_of_treasury:.2f} "
        "bps of total treasury."
    )

    print()
    print("-" * 100)
    print()

    unchanged_delta = build_delta(
        delta_id="fixture_unchanged",
        change_required=False,
    )

    unchanged_comparison = (
        build_complete_comparison(
            delta=unchanged_delta,
            incremental_benefit_eur=0,
        )
    )

    unchanged_friction = (
        build_complete_friction(
            delta=unchanged_delta,
            comparison=unchanged_comparison,
            switching_cost_eur=0,
        )
    )

    unchanged_decision = (
        build_rebalance_decision(
            decision_id=(
                "decision_unchanged"
            ),
            policy=POLICY,
            delta=unchanged_delta,
            economic_comparison=(
                unchanged_comparison
            ),
            switching_friction=(
                unchanged_friction
            ),
        )
    )

    print_decision(
        label=(
            "CASE 1 — NO ALLOCATION CHANGE"
        ),
        decision=unchanged_decision,
    )

    incomplete_economics_delta = (
        build_delta(
            delta_id="fixture_incomplete_economics",
            change_required=True,
        )
    )

    incomplete_economics_comparison = (
        build_incomplete_comparison(
            delta=incomplete_economics_delta,
        )
    )

    incomplete_economics_friction = (
        build_incomplete_friction(
            delta=incomplete_economics_delta,
            comparison=(
                incomplete_economics_comparison
            ),
        )
    )

    incomplete_economics_decision = (
        build_rebalance_decision(
            decision_id=(
                "decision_incomplete_economics"
            ),
            policy=POLICY,
            delta=(
                incomplete_economics_delta
            ),
            economic_comparison=(
                incomplete_economics_comparison
            ),
            switching_friction=(
                incomplete_economics_friction
            ),
        )
    )

    print_decision(
        label=(
            "CASE 2 — INCOMPLETE EVIDENCE"
        ),
        decision=(
            incomplete_economics_decision
        ),
    )

    negative_delta = build_delta(
        delta_id="fixture_negative",
        change_required=True,
    )

    negative_comparison = (
        build_complete_comparison(
            delta=negative_delta,
            incremental_benefit_eur=-2_500,
        )
    )

    negative_friction = (
        build_complete_friction(
            delta=negative_delta,
            comparison=negative_comparison,
            switching_cost_eur=500,
        )
    )

    negative_decision = (
        build_rebalance_decision(
            decision_id="decision_negative",
            policy=POLICY,
            delta=negative_delta,
            economic_comparison=(
                negative_comparison
            ),
            switching_friction=(
                negative_friction
            ),
        )
    )

    print_decision(
        label=(
            "CASE 3 — NEGATIVE NET ECONOMICS"
        ),
        decision=negative_decision,
    )

    below_threshold_delta = (
        build_delta(
            delta_id="fixture_below_threshold",
            change_required=True,
        )
    )

    below_threshold_comparison = (
        build_complete_comparison(
            delta=below_threshold_delta,
            incremental_benefit_eur=2_500,
        )
    )

    below_threshold_friction = (
        build_complete_friction(
            delta=below_threshold_delta,
            comparison=(
                below_threshold_comparison
            ),
            switching_cost_eur=500,
        )
    )

    below_threshold_decision = (
        build_rebalance_decision(
            decision_id=(
                "decision_below_threshold"
            ),
            policy=POLICY,
            delta=below_threshold_delta,
            economic_comparison=(
                below_threshold_comparison
            ),
            switching_friction=(
                below_threshold_friction
            ),
        )
    )

    print_decision(
        label=(
            "CASE 4 — POSITIVE BUT BELOW THRESHOLD"
        ),
        decision=(
            below_threshold_decision
        ),
    )

    above_threshold_delta = (
        build_delta(
            delta_id="fixture_above_threshold",
            change_required=True,
        )
    )

    above_threshold_comparison = (
        build_complete_comparison(
            delta=above_threshold_delta,
            incremental_benefit_eur=5_000,
        )
    )

    above_threshold_friction = (
        build_complete_friction(
            delta=above_threshold_delta,
            comparison=(
                above_threshold_comparison
            ),
            switching_cost_eur=500,
        )
    )

    above_threshold_decision = (
        build_rebalance_decision(
            decision_id=(
                "decision_above_threshold"
            ),
            policy=POLICY,
            delta=above_threshold_delta,
            economic_comparison=(
                above_threshold_comparison
            ),
            switching_friction=(
                above_threshold_friction
            ),
        )
    )

    print_decision(
        label=(
            "CASE 5 — NET BENEFIT ABOVE THRESHOLD"
        ),
        decision=(
            above_threshold_decision
        ),
    )

    print("INTERPRETATION")
    print()

    print(
        "Case 1 keeps the current portfolio because "
        "there is no allocation change to make."
    )

    print(
        "Case 2 requires review because the evidence "
        "needed to calculate defensible net economics "
        "is incomplete."
    )

    print(
        "Case 3 keeps the current portfolio because "
        "the proposed allocation has negative first-year "
        "net economics."
    )

    print(
        "Case 4 keeps the current portfolio even though "
        "the proposed allocation is better, because the "
        "improvement is too small to clear the explicit "
        "rebalance threshold."
    )

    print(
        "Case 5 recommends rebalance because the "
        "first-year net improvement is positive and "
        "clears the policy threshold."
    )

    print(
        "The five-basis-point threshold used here is "
        "only a deterministic test policy and should "
        "not yet be treated as the production treasury "
        "policy."
    )


if __name__ == "__main__":
    main()