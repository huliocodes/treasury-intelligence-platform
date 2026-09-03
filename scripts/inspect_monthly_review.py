from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.allocation_deltas import (
    build_treasury_allocation_delta,
)

from treasury_intelligence.analytics.allocation_opportunities import (
    ALLOCATION_OPPORTUNITIES,
)

from treasury_intelligence.analytics.allocation_selection import (
    build_return_priority_portfolio_construction,
)

from treasury_intelligence.analytics.cash_returns import (
    build_freshness_aware_cash_baseline_return_assessment,
    build_unallocated_return_input,
)

from treasury_intelligence.analytics.economic_comparisons import (
    build_treasury_economic_comparison,
)

from treasury_intelligence.analytics.mandate_surveillance import (
    build_treasury_mandate_surveillance,
)

from treasury_intelligence.analytics.monthly_reviews import (
    build_monthly_review_report,
)

from treasury_intelligence.analytics.portfolio_proposals import (
    build_portfolio_proposal,
)

from treasury_intelligence.analytics.rebalance import (
    build_rebalance_decision,
)

from treasury_intelligence.analytics.review_returns import (
    build_candidate_allocation_return_input,
    build_candidate_embedded_switching_friction_input,
)

from treasury_intelligence.analytics.switching_friction import (
    build_switching_friction_assessment,
)

from treasury_intelligence.current_treasury import (
    build_model_company_current_treasury,
)

from treasury_intelligence.analytics.universe_candidates import (
    analyze_opportunity_universe_at_position_size,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)


from treasury_intelligence.models.economic_comparisons import (
    UnallocatedReturnInput,
)

from treasury_intelligence.policies.model_company import (
    MODEL_COMPANY_REBALANCE_POLICY,
)


AS_OF = "2026-09-03"


def main() -> None:
    print(
        "FULL-UNIVERSE MONTHLY TREASURY REVIEW"
    )
    print()

    treasury_capital_eur = (
        MODEL_COMPANY_MANDATE.treasury_capital_eur
    )

    universe_candidates = (
        analyze_opportunity_universe_at_position_size(
            position_size_eur=(
                treasury_capital_eur
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
        )
    )

    construction, selected_candidates = (
        build_return_priority_portfolio_construction(
            construction_id=(
                "monthly_review_construction_"
                "2026_09_03"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            opportunities=ALLOCATION_OPPORTUNITIES,
            notes=(
                "Monthly review uses the production "
                "return-priority allocation opportunity "
                "registry."
            ),
        )
    )

    proposal = (
        build_portfolio_proposal(
            proposal_id=(
                "monthly_review_proposal_"
                "2026_09_03"
            ),
            construction=construction,
            candidates=selected_candidates,
            notes=(
                "Monthly-review proposal generated "
                "from the production allocation "
                "opportunity set."
            ),
        )
    )

    current_treasury = (
        build_model_company_current_treasury(
            as_of=AS_OF,
            positions=(),
            notes=(
                "Production current-treasury input "
                "currently represents the model company "
                "as fully unallocated because verified "
                "real holdings have not yet been supplied."
            ),
        )
    )

    state = current_treasury.state

    delta = (
        build_treasury_allocation_delta(
            delta_id=(
                "monthly_review_delta_"
                "2026_09_03"
            ),
            state=state,
            proposal=proposal,
            notes=(
                "Allocation delta compares the current "
                "treasury state with the production "
                "portfolio proposal."
            ),
        )
    )

    cash_baseline = (
        current_treasury.cash_baseline
    )

    cash_return_assessment = (
        build_freshness_aware_cash_baseline_return_assessment(
            assessment_id=(
                "model_company_cash_return_"
                "2026_09_03"
            ),
            baseline=cash_baseline,
            as_of="2026-09-03",
            notes=(
                "Current model-company cash return "
                "assessment derived from the explicit "
                "cash baseline."
            ),
        )
    )

    current_unallocated_return = (
        build_unallocated_return_input(
            assessment=cash_return_assessment,
            notes=(
                "Current unallocated treasury return "
                "derived from the unresolved current "
                "cash baseline."
            ),
        )
    )

    proposed_unallocated_return = (
        UnallocatedReturnInput(
            annual_return_pct=None,
            evidence_available=False,
            source_reference=(
                "monthly_review_proposed_unallocated_"
                "2026_09_03"
            ),
            notes=(
                "No proposed unallocated-return "
                "assumption is required when the "
                "production proposal allocates all "
                "treasury capital. If proposed "
                "unallocated capital becomes positive, "
                "its return evidence must be supplied."
            ),
        )
    )

    proposed_position_returns = tuple(
        build_candidate_allocation_return_input(
            candidate=candidate,
            notes=(
                "Production candidate return used "
                "for recurring treasury review."
            ),
        )
        for candidate in selected_candidates
    )

    comparison = (
        build_treasury_economic_comparison(
            comparison_id=(
                "monthly_review_economics_"
                "2026_09_03"
            ),
            state=state,
            proposal=proposal,
            delta=delta,
            current_position_returns=(),
            proposed_position_returns=(
                proposed_position_returns
            ),
            current_unallocated_return=(
                current_unallocated_return
            ),
            proposed_unallocated_return=(
                proposed_unallocated_return
            ),
            notes=(
                "Recurring economic comparison between "
                "the current treasury state and the "
                "current production portfolio proposal. "
                "Unknown current cash economics remain "
                "explicit."
            ),
        )
    )

    selected_candidate_map = {
        (
            candidate.instrument_id,
            candidate.market_id,
            candidate.access_route_id,
        ): candidate
        for candidate in selected_candidates
    }

    switching_friction_inputs = tuple(
        build_candidate_embedded_switching_friction_input(
            candidate=selected_candidate_map[
                (
                    line.instrument_id,
                    line.market_id,
                    line.access_route_id,
                )
            ],
            action=line.action,
            notes=(
                "No additional switching cost is "
                "charged where the selected production "
                "candidate's defensible return already "
                "embeds entry execution economics."
            ),
        )
        for line in delta.delta_lines
        if (
            abs(line.delta_eur) > 0.01
            and line.action
            in (
                "open",
                "increase",
            )
            and (
                line.instrument_id,
                line.market_id,
                line.access_route_id,
            )
            in selected_candidate_map
        )
    )

    switching_friction = (
        build_switching_friction_assessment(
            assessment_id=(
                "monthly_review_switching_"
                "friction_2026_09_03"
            ),
            delta=delta,
            economic_comparison=comparison,
            friction_inputs=(
                switching_friction_inputs
            ),
            notes=(
                "Switching friction contains only "
                "additional transition costs not already "
                "embedded in the compared candidate "
                "return. Missing provenance or separate "
                "transition costs remain explicit."
            ),
        )
    )

    policy = MODEL_COMPANY_REBALANCE_POLICY

    decision = (
        build_rebalance_decision(
            decision_id=(
                "monthly_review_decision_"
                "2026_09_03"
            ),
            policy=policy,
            delta=delta,
            economic_comparison=comparison,
            switching_friction=(
                switching_friction
            ),
            notes=(
                "Rebalance decision derived from the "
                "production recurring-review pipeline."
            ),
        )
    )

    mandate_surveillance = (
        build_treasury_mandate_surveillance(
            surveillance_id=(
                "monthly_review_mandate_"
                "surveillance_2026_09_03"
            ),
            state=state,
            holding_assessments=(),
            notes=(
                "The current modeled treasury state "
                "contains no invested positions. "
                "Therefore there are no current "
                "holdings to assess for mandate "
                "deterioration."
            ),
        )
    )

    review = (
        build_monthly_review_report(
            review_id=(
                "monthly_review_2026_09_03"
            ),
            state=state,
            proposal=proposal,
            delta=delta,
            economic_comparison=comparison,
            switching_friction=(
                switching_friction
            ),
            rebalance_decision=decision,
            mandate_surveillance=(
                mandate_surveillance
            ),
            notes=(
                "Milestone 15D full-universe recurring "
                "treasury review with transaction-cost "
                "double-counting protection."
            ),
        )
    )

    recommendation_ready_count = sum(
        1
        for candidate in universe_candidates
        if candidate.recommendation_ready
    )

    needs_evidence_count = sum(
        1
        for candidate in universe_candidates
        if candidate.candidate_status
        == "needs_evidence"
    )

    blocked_count = sum(
        1
        for candidate in universe_candidates
        if candidate.candidate_status
        == "blocked"
    )

    print("PRODUCTION UNIVERSE")
    print()

    print(
        f"Opportunities:                 "
        f"{len(universe_candidates)}"
    )

    print(
        f"Recommendation-ready:          "
        f"{recommendation_ready_count}"
    )

    print(
        f"Needs evidence:                "
        f"{needs_evidence_count}"
    )

    print(
        f"Blocked:                       "
        f"{blocked_count}"
    )

    print()
    print("PRODUCTION PORTFOLIO PROPOSAL")
    print()

    print(
        f"Construction status:           "
        f"{construction.construction_status}"
    )

    print(
        f"Proposal status:               "
        f"{proposal.proposal_status}"
    )

    print(
        f"Proposal decision:             "
        f"{proposal.decision}"
    )

    print(
        f"Selected positions:            "
        f"{len(selected_candidates)}"
    )

    for candidate in selected_candidates:
        if candidate.defensible_return_pct is None:
            return_text = "UNKNOWN"
        else:
            return_text = (
                f"{candidate.defensible_return_pct:.3f}%"
            )

        print(
            f"  - {candidate.label}: "
            f"EUR {candidate.position_size_eur:,.0f} "
            f"at {return_text}"
        )

        print(
            "    embedded one-time costs: "
            + (
                ", ".join(
                    candidate
                    .embedded_one_time_cost_component_types
                )
                or "none"
            )
        )

    print()
    print("CURRENT TREASURY STATE")
    print()

    print(
        f"Treasury capital:              "
        f"EUR {state.treasury_capital_eur:,.0f}"
    )

    print(
        f"Current invested:              "
        f"EUR {state.invested_capital_eur:,.0f}"
    )

    print(
        f"Current unallocated:           "
        f"EUR {state.unallocated_capital_eur:,.0f}"
    )

    print(
        f"Current cash evidence:         "
        f"{cash_return_assessment.assessment_status}"
    )

    if (
        cash_return_assessment
        .blended_annual_return_pct
        is None
    ):
        cash_return_text = "UNKNOWN"
    else:
        cash_return_text = (
            f"{cash_return_assessment.blended_annual_return_pct:.3f}%"
        )

    print(
        f"Current cash return:           "
        f"{cash_return_text}"
    )

    print()
    print("ALLOCATION DELTA")
    print()

    print(
        f"Proposed allocated:            "
        f"EUR {proposal.allocated_capital_eur:,.0f}"
    )

    print(
        f"Proposed unallocated:          "
        f"EUR {proposal.unallocated_capital_eur:,.0f}"
    )

    print(
        f"Gross position movement:       "
        f"EUR {delta.gross_position_movement_eur:,.0f}"
    )

    print()
    print("ECONOMIC REVIEW")
    print()

    print(
        f"Economic comparison:           "
        f"{comparison.comparison_status}"
    )

    if comparison.current_annual_return_eur is None:
        current_return_text = "UNKNOWN"
    else:
        current_return_text = (
            f"EUR {comparison.current_annual_return_eur:,.0f}"
        )

    if comparison.proposed_annual_return_eur is None:
        proposed_return_text = "UNKNOWN"
    else:
        proposed_return_text = (
            f"EUR {comparison.proposed_annual_return_eur:,.0f}"
        )

    print(
        f"Current annual return:         "
        f"{current_return_text}"
    )

    print(
        f"Proposed annual return:        "
        f"{proposed_return_text}"
    )

    print(
        f"Switching friction:            "
        f"{switching_friction.friction_status}"
    )

    if switching_friction.total_switching_cost_eur is None:
        switching_cost_text = "UNKNOWN"
    else:
        switching_cost_text = (
            f"EUR "
            f"{switching_friction.total_switching_cost_eur:,.2f}"
        )

    print(
        f"Additional switching cost:     "
        f"{switching_cost_text}"
    )

    print()
    print("MONTHLY REVIEW")
    print()

    print(
        f"Mandate surveillance:          "
        f"{review.mandate_surveillance_status}"
    )

    print(
        f"Rebalance decision:            "
        f"{review.rebalance_decision}"
    )

    print(
        f"Decision status:               "
        f"{review.rebalance_decision_status}"
    )

    print(
        f"Final review action:           "
        f"{review.review_action}"
    )

    print(
        f"Monthly review status:         "
        f"{review.review_status}"
    )

    print()
    print("SUMMARY")
    print()
    print(review.summary)

    if comparison.missing_evidence:
        print()
        print("ECONOMIC EVIDENCE REQUIREMENTS")
        print()

        for requirement in comparison.missing_evidence:
            print(
                f"  - {requirement}"
            )

    if switching_friction.missing_evidence:
        print()
        print("SWITCHING EVIDENCE REQUIREMENTS")
        print()

        for requirement in (
            switching_friction.missing_evidence
        ):
            print(
                f"  - {requirement}"
            )

    print()
    print("-" * 100)
    print()
    print("MILESTONE 15D ASSERTIONS")
    print()

    assert len(universe_candidates) == 14

    assert recommendation_ready_count > 0

    assert construction.construction_status == (
        "valid_allocation"
    )

    assert proposal.proposal_status == (
        "allocation_proposed"
    )

    assert proposal.allocated_capital_eur > 0

    assert selected_candidates

    assert all(
        candidate.recommendation_ready
        for candidate in selected_candidates
    )

    assert all(
        return_input.evidence_available
        for return_input in proposed_position_returns
    )

    assert state.invested_capital_eur == 0

    assert (
        state.unallocated_capital_eur
        == treasury_capital_eur
    )

    assert delta.change_required

    assert delta.gross_position_movement_eur > 0

    assert (
        cash_return_assessment.assessment_status
        == "incomplete"
    )

    assert (
        current_unallocated_return
        .evidence_available
        is False
    )

    assert comparison.comparison_status == (
        "incomplete"
    )

    assert comparison.current_annual_return_eur is None

    assert comparison.proposed_annual_return_eur is not None

    assert switching_friction_inputs

    assert all(
        friction_input.evidence_available
        for friction_input in switching_friction_inputs
    )

    assert all(
        friction_input.friction_bps == 0.0
        and friction_input.fixed_cost_eur == 0.0
        for friction_input in switching_friction_inputs
    )

    assert (
        switching_friction.friction_status
        == "complete"
    )

    assert (
        switching_friction.total_switching_cost_eur
        == 0.0
    )

    assert not switching_friction.missing_evidence

    assert (
        mandate_surveillance.status
        == "compliant"
    )

    assert decision.decision == "needs_review"

    assert (
        decision.decision_status
        == "review_required"
    )

    assert review.review_action == (
        "evidence_required"
    )

    assert review.review_status == (
        "follow_up_required"
    )

    print(
        "Production universe connected:         yes"
    )

    print(
        "Production portfolio proposal created: yes"
    )

    print(
        "Current treasury state connected:      yes"
    )

    print(
        "Allocation delta connected:            yes"
    )

    print(
        "Production returns connected:          yes"
    )

    print(
        "Return-cost provenance preserved:      yes"
    )

    print(
        "Double-counting protection active:     yes"
    )

    print(
        "Additional switching friction known:   yes"
    )

    print(
        "Unknown cash economics preserved:      yes"
    )

    print(
        "Mandate surveillance connected:        yes"
    )

    print(
        "Rebalance decision connected:          yes"
    )

    print(
        "Monthly review connected:              yes"
    )

    print()

    print(
        "All Milestone 15D cost-inclusion "
        "provenance assertions passed."
    )


if __name__ == "__main__":
    main()
