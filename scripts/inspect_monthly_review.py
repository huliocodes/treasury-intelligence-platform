from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.monthly_reviews import (
    build_monthly_review_report,
)

from treasury_intelligence.models.allocation_deltas import (
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.economic_comparisons import (
    TreasuryEconomicComparison,
)

from treasury_intelligence.models.portfolio_proposals import (
    PortfolioProposal,
)

from treasury_intelligence.models.rebalance import (
    RebalanceDecision,
)

from treasury_intelligence.models.switching_friction import (
    SwitchingFrictionAssessment,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryState,
)


MANDATE_ID = "si_model_company_v1"
TREASURY_CAPITAL_EUR = 5_000_000


def build_current_state() -> TreasuryState:
    return TreasuryState(
        state_id="monthly_review_state_2026_08_30",
        mandate_id=MANDATE_ID,
        as_of="2026-08-30",
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        positions=(),
        invested_capital_eur=0,
        unallocated_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        notes=(
            "Model-company monthly-review fixture: "
            "treasury currently fully unallocated."
        ),
    )


def build_current_proposal() -> PortfolioProposal:
    return PortfolioProposal(
        proposal_id=(
            "monthly_review_proposal_2026_08_30"
        ),
        mandate_id=MANDATE_ID,
        construction_id=(
            "monthly_review_construction_2026_08_30"
        ),
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        candidate_count=1,
        recommendation_ready_candidate_count=0,
        allocated_capital_eur=0,
        unallocated_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        proposal_status=(
            "no_actionable_allocation"
        ),
        decision="hold_unallocated",
        allocation_lines=(),
        evidence_blocked_candidate_labels=(
            "XEON",
        ),
        rationale=(
            "No researched candidate is currently "
            "recommendation-ready under the model-company "
            "mandate. XEON remains blocked by unresolved "
            "position-size liquidity and executable "
            "economics evidence."
        ),
        notes=(
            "This assembly fixture reflects the current "
            "validated project evidence. It does not "
            "recompute the XEON candidate inside this "
            "script."
        ),
    )


def build_current_delta(
    state: TreasuryState,
    proposal: PortfolioProposal,
) -> TreasuryAllocationDelta:
    return TreasuryAllocationDelta(
        delta_id=(
            "monthly_review_delta_2026_08_30"
        ),
        mandate_id=MANDATE_ID,
        state_id=state.state_id,
        proposal_id=proposal.proposal_id,
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        current_invested_capital_eur=0,
        proposed_invested_capital_eur=0,
        current_unallocated_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        proposed_unallocated_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        gross_position_movement_eur=0,
        change_required=False,
        delta_lines=(),
    )


def build_current_economic_comparison(
    state: TreasuryState,
    proposal: PortfolioProposal,
    delta: TreasuryAllocationDelta,
) -> TreasuryEconomicComparison:
    return TreasuryEconomicComparison(
        comparison_id=(
            "monthly_review_economics_2026_08_30"
        ),
        mandate_id=MANDATE_ID,
        state_id=state.state_id,
        proposal_id=proposal.proposal_id,
        delta_id=delta.delta_id,
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        comparison_status="incomplete",
        current_annual_return_eur=None,
        proposed_annual_return_eur=None,
        incremental_annual_benefit_eur=None,
        incremental_annual_benefit_pct_of_treasury=None,
        current_lines=(),
        proposed_lines=(),
        missing_evidence=(
            "Current unallocated treasury return "
            "evidence is not yet modeled as a "
            "defensible blended cash return.",
        ),
        notes=(
            "No allocation change is proposed, so "
            "economic incompleteness does not create "
            "transaction movement but remains relevant "
            "to treasury intelligence."
        ),
    )


def build_current_switching_friction(
    delta: TreasuryAllocationDelta,
    comparison: TreasuryEconomicComparison,
) -> SwitchingFrictionAssessment:
    return SwitchingFrictionAssessment(
        assessment_id=(
            "monthly_review_friction_2026_08_30"
        ),
        mandate_id=MANDATE_ID,
        delta_id=delta.delta_id,
        economic_comparison_id=(
            comparison.comparison_id
        ),
        gross_position_movement_eur=0,
        friction_status="complete",
        known_switching_cost_eur=0,
        total_switching_cost_eur=0,
        incremental_annual_benefit_eur=None,
        first_year_net_benefit_eur=None,
        payback_days=None,
        net_benefit_available=False,
        friction_lines=(),
        missing_evidence=(),
        notes=(
            "No portfolio movement is proposed, so "
            "no switching friction is incurred."
        ),
    )


def build_current_rebalance_decision(
    delta: TreasuryAllocationDelta,
    comparison: TreasuryEconomicComparison,
    friction: SwitchingFrictionAssessment,
) -> RebalanceDecision:
    return RebalanceDecision(
        decision_id=(
            "monthly_review_decision_2026_08_30"
        ),
        mandate_id=MANDATE_ID,
        policy_id="fixture_rebalance_policy",
        delta_id=delta.delta_id,
        economic_comparison_id=(
            comparison.comparison_id
        ),
        switching_friction_assessment_id=(
            friction.assessment_id
        ),
        treasury_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        allocation_change_required=False,
        economic_comparison_status=(
            comparison.comparison_status
        ),
        friction_status=(
            friction.friction_status
        ),
        incremental_annual_benefit_eur=None,
        total_switching_cost_eur=0,
        first_year_net_benefit_eur=None,
        first_year_net_improvement_bps_of_treasury=0,
        minimum_required_improvement_bps=5,
        decision="keep_current",
        decision_status="decision_ready",
        threshold_met=False,
        rationale=(
            "No portfolio allocation change is currently "
            "proposed, so the current treasury state is "
            "retained."
        ),
        evidence_requirements=(),
        notes=(
            "A keep-current rebalance decision does not "
            "mean all market research is complete."
        ),
    )


def main() -> None:
    print("INTEGRATED MONTHLY TREASURY REVIEW")
    print()

    state = build_current_state()

    proposal = build_current_proposal()

    delta = build_current_delta(
        state=state,
        proposal=proposal,
    )

    comparison = (
        build_current_economic_comparison(
            state=state,
            proposal=proposal,
            delta=delta,
        )
    )

    friction = (
        build_current_switching_friction(
            delta=delta,
            comparison=comparison,
        )
    )

    decision = (
        build_current_rebalance_decision(
            delta=delta,
            comparison=comparison,
            friction=friction,
        )
    )

    review = build_monthly_review_report(
        review_id=(
            "monthly_review_2026_08_30"
        ),
        state=state,
        proposal=proposal,
        delta=delta,
        economic_comparison=comparison,
        switching_friction=friction,
        rebalance_decision=decision,
        notes=(
            "First integrated monthly-review assembly."
        ),
    )

    print(
        f"As of:                         "
        f"{review.as_of}"
    )

    print(
        f"Treasury capital:              "
        f"EUR {review.treasury_capital_eur:,.0f}"
    )

    print(
        f"Current invested:              "
        f"EUR "
        f"{review.current_invested_capital_eur:,.0f}"
    )

    print(
        f"Current unallocated:           "
        f"EUR "
        f"{review.current_unallocated_capital_eur:,.0f}"
    )

    print(
        f"Proposed allocated:            "
        f"EUR "
        f"{review.proposed_allocated_capital_eur:,.0f}"
    )

    print(
        f"Proposed unallocated:          "
        f"EUR "
        f"{review.proposed_unallocated_capital_eur:,.0f}"
    )

    print(
        f"Gross position movement:       "
        f"EUR "
        f"{review.gross_position_movement_eur:,.0f}"
    )

    print()

    print(
        f"Rebalance decision:            "
        f"{review.rebalance_decision}"
    )

    print(
        f"Decision status:               "
        f"{review.rebalance_decision_status}"
    )

    print(
        f"Monthly review status:         "
        f"{review.review_status}"
    )

    print()

    print("SUMMARY")
    print()

    print(
        review.summary
    )

    if (
        review.evidence_blocked_candidate_labels
    ):
        print()
        print("EVIDENCE-BLOCKED CANDIDATES")
        print()

        for label in (
            review
            .evidence_blocked_candidate_labels
        ):
            print(
                f"  - {label}"
            )

    if review.evidence_requirements:
        print()
        print("EVIDENCE REQUIREMENTS")
        print()

        for item in (
            review.evidence_requirements
        ):
            print(
                f"  - {item}"
            )

    print()
    print("-" * 100)
    print()

    print("INTERPRETATION")
    print()

    print(
        "The treasury action and the research status "
        "are intentionally separate."
    )

    print(
        "The system can correctly keep the current "
        "allocation while still requiring evidence "
        "follow-up on researched opportunities."
    )

    print(
        "This prevents keep_current from being "
        "misinterpreted as all opportunities having "
        "been fully resolved."
    )

    print(
        "The next integration step should replace "
        "manual assembly of these intermediate objects "
        "with calls into the existing analytical "
        "pipeline."
    )


if __name__ == "__main__":
    main()