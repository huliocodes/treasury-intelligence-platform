from __future__ import annotations

from treasury_intelligence.analytics.mandate_surveillance import (
    build_treasury_mandate_surveillance,
)

from treasury_intelligence.analytics.monthly_reviews import (
    build_monthly_review_report,
)

from treasury_intelligence.analytics.treasury_state import (
    build_treasury_state,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.allocation_deltas import (
    AllocationDeltaLine,
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.economic_comparisons import (
    TreasuryEconomicComparison,
)

from treasury_intelligence.models.mandate_surveillance import (
    CurrentHoldingMandateAssessment,
)

from treasury_intelligence.models.portfolio_construction import (
    PortfolioAllocationLine,
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
    TreasuryPosition,
)


AS_OF = "2026-09-02T22:00:00Z"

TREASURY_CAPITAL_EUR = 5_000_000.0

POSITION_ID = "current_position"
CANDIDATE_ID = "current_candidate"
INSTRUMENT_ID = "current_instrument"
MARKET_ID = "current_market"
ACCESS_ROUTE_ID = "current_access"
LABEL = "CURRENT HOLDING"


def build_components():
    position = TreasuryPosition(
        position_id=POSITION_ID,
        instrument_id=INSTRUMENT_ID,
        market_id=MARKET_ID,
        access_route_id=ACCESS_ROUTE_ID,
        label=LABEL,
        current_value_eur=TREASURY_CAPITAL_EUR,
    )

    state = build_treasury_state(
        state_id="surveillance_review_state",
        mandate=MODEL_COMPANY_MANDATE,
        as_of=AS_OF,
        positions=(position,),
    )

    allocation_line = PortfolioAllocationLine(
        candidate_assessment_id=CANDIDATE_ID,
        instrument_id=INSTRUMENT_ID,
        market_id=MARKET_ID,
        access_route_id=ACCESS_ROUTE_ID,
        label=LABEL,
        allocation_eur=TREASURY_CAPITAL_EUR,
        allocation_pct_of_treasury=100.0,
        candidate_position_size_eur=(
            TREASURY_CAPITAL_EUR
        ),
    )

    proposal = PortfolioProposal(
        proposal_id="surveillance_review_proposal",
        mandate_id=state.mandate_id,
        construction_id="fixture_construction",
        treasury_capital_eur=TREASURY_CAPITAL_EUR,
        candidate_count=1,
        recommendation_ready_candidate_count=1,
        allocated_capital_eur=TREASURY_CAPITAL_EUR,
        unallocated_capital_eur=0.0,
        proposal_status="allocation_proposed",
        decision="propose_allocation",
        allocation_lines=(allocation_line,),
        evidence_blocked_candidate_labels=(),
        rationale=(
            "Deterministic fixture proposes retaining "
            "the current allocation."
        ),
    )

    delta_line = AllocationDeltaLine(
        instrument_id=INSTRUMENT_ID,
        market_id=MARKET_ID,
        access_route_id=ACCESS_ROUTE_ID,
        label=LABEL,
        current_value_eur=TREASURY_CAPITAL_EUR,
        proposed_value_eur=TREASURY_CAPITAL_EUR,
        delta_eur=0.0,
        action="unchanged",
    )

    delta = TreasuryAllocationDelta(
        delta_id="surveillance_review_delta",
        mandate_id=state.mandate_id,
        state_id=state.state_id,
        proposal_id=proposal.proposal_id,
        treasury_capital_eur=TREASURY_CAPITAL_EUR,
        current_invested_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        proposed_invested_capital_eur=(
            TREASURY_CAPITAL_EUR
        ),
        current_unallocated_capital_eur=0.0,
        proposed_unallocated_capital_eur=0.0,
        gross_position_movement_eur=0.0,
        change_required=False,
        delta_lines=(delta_line,),
        notes=(
            "Deterministic unchanged-allocation fixture."
        ),
    )

    comparison = TreasuryEconomicComparison(
        comparison_id="surveillance_review_economics",
        mandate_id=state.mandate_id,
        state_id=state.state_id,
        proposal_id=proposal.proposal_id,
        delta_id=delta.delta_id,
        treasury_capital_eur=TREASURY_CAPITAL_EUR,
        comparison_status="complete",
        current_annual_return_eur=100_000.0,
        proposed_annual_return_eur=100_000.0,
        incremental_annual_benefit_eur=0.0,
        incremental_annual_benefit_pct_of_treasury=0.0,
        current_lines=(),
        proposed_lines=(),
        missing_evidence=(),
        notes=(
            "Deterministic unchanged-return fixture."
        ),
    )

    friction = SwitchingFrictionAssessment(
        assessment_id="surveillance_review_friction",
        mandate_id=state.mandate_id,
        delta_id=delta.delta_id,
        economic_comparison_id=(
            comparison.comparison_id
        ),
        gross_position_movement_eur=0.0,
        friction_status="complete",
        known_switching_cost_eur=0.0,
        total_switching_cost_eur=0.0,
        incremental_annual_benefit_eur=0.0,
        first_year_net_benefit_eur=0.0,
        payback_days=None,
        net_benefit_available=True,
        friction_lines=(),
        missing_evidence=(),
        notes=(
            "No allocation movement means zero "
            "switching friction."
        ),
    )

    decision = RebalanceDecision(
        decision_id="surveillance_review_decision",
        mandate_id=state.mandate_id,
        policy_id="fixture_policy",
        delta_id=delta.delta_id,
        economic_comparison_id=(
            comparison.comparison_id
        ),
        switching_friction_assessment_id=(
            friction.assessment_id
        ),
        treasury_capital_eur=TREASURY_CAPITAL_EUR,
        allocation_change_required=False,
        economic_comparison_status="complete",
        friction_status="complete",
        incremental_annual_benefit_eur=0.0,
        total_switching_cost_eur=0.0,
        first_year_net_benefit_eur=0.0,
        first_year_net_improvement_bps_of_treasury=0.0,
        minimum_required_improvement_bps=5.0,
        decision="keep_current",
        decision_status="decision_ready",
        threshold_met=False,
        rationale=(
            "No economic reason to switch."
        ),
        evidence_requirements=(),
    )

    return (
        position,
        state,
        proposal,
        delta,
        comparison,
        friction,
        decision,
    )


def build_surveillance(
    *,
    position: TreasuryPosition,
    state,
    status: str,
):
    if status == "compliant":
        assessment = (
            CurrentHoldingMandateAssessment(
                assessment_id=(
                    "holding_compliant"
                ),
                mandate_id=state.mandate_id,
                position_id=position.position_id,
                instrument_id=position.instrument_id,
                market_id=position.market_id,
                access_route_id=(
                    position.access_route_id
                ),
                position_size_eur=(
                    position.current_value_eur
                ),
                status="compliant",
                blocking_reasons=(),
                evidence_requirements=(),
            )
        )

    elif status == "breach":
        assessment = (
            CurrentHoldingMandateAssessment(
                assessment_id="holding_breach",
                mandate_id=state.mandate_id,
                position_id=position.position_id,
                instrument_id=position.instrument_id,
                market_id=position.market_id,
                access_route_id=(
                    position.access_route_id
                ),
                position_size_eur=(
                    position.current_value_eur
                ),
                status="breach",
                blocking_reasons=(
                    "Current holding no longer satisfies "
                    "the immediate-liquidity requirement.",
                ),
                evidence_requirements=(),
            )
        )

    elif status == "evidence_required":
        assessment = (
            CurrentHoldingMandateAssessment(
                assessment_id="holding_evidence",
                mandate_id=state.mandate_id,
                position_id=position.position_id,
                instrument_id=position.instrument_id,
                market_id=position.market_id,
                access_route_id=(
                    position.access_route_id
                ),
                position_size_eur=(
                    position.current_value_eur
                ),
                status="evidence_required",
                blocking_reasons=(),
                evidence_requirements=(
                    "Current holding liquidity evidence "
                    "must be refreshed.",
                ),
            )
        )

    else:
        raise ValueError(
            f"Unsupported fixture status: {status}"
        )

    return build_treasury_mandate_surveillance(
        surveillance_id=(
            f"surveillance_{status}"
        ),
        state=state,
        holding_assessments=(assessment,),
    )


def print_review(
    *,
    label: str,
    review,
) -> None:
    print(label)
    print()

    print(
        f"Surveillance:                 "
        f"{review.mandate_surveillance_status}"
    )

    print(
        f"Economic decision:            "
        f"{review.rebalance_decision}"
    )

    print(
        f"Final action:                 "
        f"{review.review_action}"
    )

    print(
        f"Review status:                "
        f"{review.review_status}"
    )

    print(
        f"Mandate blocking reasons:     "
        f"{len(review.mandate_blocking_reasons)}"
    )

    print(
        f"Evidence requirements:        "
        f"{len(review.evidence_requirements)}"
    )

    print()
    print(
        f"Summary: {review.summary}"
    )

    print()
    print("-" * 100)
    print()


def main() -> None:
    (
        position,
        state,
        proposal,
        delta,
        comparison,
        friction,
        decision,
    ) = build_components()

    compliant = build_surveillance(
        position=position,
        state=state,
        status="compliant",
    )

    compliant_review = (
        build_monthly_review_report(
            review_id="review_compliant",
            state=state,
            proposal=proposal,
            delta=delta,
            economic_comparison=comparison,
            switching_friction=friction,
            rebalance_decision=decision,
            mandate_surveillance=compliant,
        )
    )

    print_review(
        label=(
            "CASE 1 — COMPLIANT + KEEP CURRENT"
        ),
        review=compliant_review,
    )

    breach = build_surveillance(
        position=position,
        state=state,
        status="breach",
    )

    breach_review = (
        build_monthly_review_report(
            review_id="review_breach",
            state=state,
            proposal=proposal,
            delta=delta,
            economic_comparison=comparison,
            switching_friction=friction,
            rebalance_decision=decision,
            mandate_surveillance=breach,
        )
    )

    print_review(
        label=(
            "CASE 2 — BREACH + ECONOMIC "
            "KEEP CURRENT"
        ),
        review=breach_review,
    )

    evidence = build_surveillance(
        position=position,
        state=state,
        status="evidence_required",
    )

    evidence_review = (
        build_monthly_review_report(
            review_id="review_evidence",
            state=state,
            proposal=proposal,
            delta=delta,
            economic_comparison=comparison,
            switching_friction=friction,
            rebalance_decision=decision,
            mandate_surveillance=evidence,
        )
    )

    print_review(
        label=(
            "CASE 3 — HOLDING EVIDENCE REQUIRED"
        ),
        review=evidence_review,
    )

    assert (
        compliant_review.review_action
        == "hold"
    )

    assert (
        compliant_review.review_status
        == "complete"
    )

    assert (
        breach_review.review_action
        == "review_for_rebalance"
    )

    assert (
        breach_review.mandate_blocking_reasons
    )

    assert (
        evidence_review.review_action
        == "evidence_required"
    )

    assert (
        evidence_review.review_status
        == "follow_up_required"
    )

    assert (
        evidence_review.evidence_requirements
    )

    print(
        "All Milestone 14C surveillance-aware "
        "monthly-review assertions passed."
    )


if __name__ == "__main__":
    main()
