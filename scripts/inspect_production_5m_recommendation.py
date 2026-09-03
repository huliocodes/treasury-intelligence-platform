from __future__ import annotations

from treasury_intelligence.analytics.allocation_selection import (
    build_single_position_construction_from_analyzed_candidates,
)

from treasury_intelligence.analytics.approvals import (
    create_pending_approval,
)

from treasury_intelligence.analytics.decision_explanations import (
    build_treasury_decision_explanation,
)

from treasury_intelligence.analytics.portfolio_proposals import (
    build_portfolio_proposal,
)

from treasury_intelligence.analytics.recommendations import (
    build_recommendation_decision,
)

from treasury_intelligence.analytics.treasury_decision_reports import (
    build_treasury_decision_report,
)

from treasury_intelligence.analytics.universe_candidates import (
    analyze_opportunity_universe_at_position_size,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)


AS_OF = "2026-09-03"


def main() -> None:
    universe_candidates = (
        analyze_opportunity_universe_at_position_size(
            position_size_eur=(
                MODEL_COMPANY_MANDATE.treasury_capital_eur
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
        )
    )

    (
        construction,
        allocation_candidates,
    ) = (
        build_single_position_construction_from_analyzed_candidates(
            construction_id=(
                "model_company_5m_production"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            candidates=universe_candidates,
        )
    )

    assert len(universe_candidates) == 14

    ready = tuple(
        candidate
        for candidate in universe_candidates
        if candidate.recommendation_ready
    )

    needs_evidence = tuple(
        candidate
        for candidate in universe_candidates
        if candidate.candidate_status == "needs_evidence"
    )

    blocked = tuple(
        candidate
        for candidate in universe_candidates
        if candidate.candidate_status == "blocked"
    )

    assert len(ready) == 2
    assert len(needs_evidence) == 7
    assert len(blocked) == 5

    assert len(allocation_candidates) == 14

    assert allocation_candidates == universe_candidates

    selected_assessment_id = (
        construction.allocation_lines[0]
        .candidate_assessment_id
    )

    selected_matches = tuple(
        candidate
        for candidate in allocation_candidates
        if (
            candidate.assessment_id
            == selected_assessment_id
        )
    )

    assert len(selected_matches) == 1

    selected = selected_matches[0]

    assert selected in universe_candidates

    assert selected.label == "French BTF Aug 2027"

    assert abs(
        selected.position_size_eur
        - 5_000_000.0
    ) <= 0.01

    assert selected.defensible_return_pct is not None

    assert abs(
        selected.defensible_return_pct
        - 2.7597
    ) < 0.001

    ready_with_returns = tuple(
        candidate
        for candidate in ready
        if candidate.defensible_return_pct is not None
    )

    assert len(ready_with_returns) == 2

    assert selected is max(
        ready_with_returns,
        key=lambda candidate: (
            candidate.defensible_return_pct,
            candidate.assessment_id,
        ),
    )

    assert construction.candidate_count == 14

    assert (
        construction.recommendation_ready_candidate_count
        == 2
    )

    assert abs(
        construction.allocated_capital_eur
        - 5_000_000.0
    ) <= 0.01

    assert abs(
        construction.unallocated_capital_eur
    ) <= 0.01

    assert len(construction.allocation_lines) == 1

    assert (
        construction.allocation_lines[0]
        .candidate_assessment_id
        == selected.assessment_id
    )

    proposal = build_portfolio_proposal(
        proposal_id=(
            "model_company_5m_production_proposal"
        ),
        construction=construction,
        candidates=allocation_candidates,
    )

    recommendation = build_recommendation_decision(
        recommendation_id=(
            "model_company_5m_production_recommendation"
        ),
        proposal=proposal,
    )

    approval = create_pending_approval(
        approval_id=(
            "model_company_5m_production_approval"
        ),
        recommendation=recommendation,
        notes=(
            "Pending human approval. No execution is "
            "authorized."
        ),
    )

    report = build_treasury_decision_report(
        report_id=(
            "model_company_5m_production_report"
        ),
        mandate=MODEL_COMPANY_MANDATE,
        universe_candidates=universe_candidates,
        construction=construction,
        allocation_candidates=allocation_candidates,
        recommendation=recommendation,
        approval=approval,
        notes=(
            "Canonical production decision uses one "
            "freshness-gated universe for both universe "
            "reporting and allocation selection."
        ),
    )

    explanation = build_treasury_decision_explanation(
        explanation_id=(
            "model_company_5m_production_explanation"
        ),
        report=report,
        universe_candidates=universe_candidates,
        notes=(
            "Production decision explanation uses the "
            "same candidate assessments that drove "
            "allocation selection."
        ),
    )

    assert report.universe.opportunity_count == 14

    assert (
        report.universe.recommendation_ready_count
        == 2
    )

    assert report.universe.needs_evidence_count == 7
    assert report.universe.blocked_count == 5

    assert (
        explanation.selected_label
        == "French BTF Aug 2027"
    )

    assert abs(
        explanation.selected_allocation_eur
        - 5_000_000.0
    ) <= 0.01

    assert abs(
        explanation.selected_allocation_pct
        - 100.0
    ) < 0.001

    assert abs(
        explanation.selected_return_pct
        - selected.defensible_return_pct
    ) < 1e-9

    expected_annual_return_eur = (
        5_000_000.0
        * selected.defensible_return_pct
        / 100.0
    )

    assert abs(
        explanation.selected_annual_return_eur
        - expected_annual_return_eur
    ) <= 0.01

    assert explanation.target_yield_pct == 3.0

    assert explanation.target_yield_gap_pct is not None
    assert explanation.target_yield_gap_pct > 0

    assert (
        recommendation.recommended_action
        == "submit_for_approval"
    )

    assert (
        recommendation.recommendation_status
        == "decision_ready"
    )

    assert approval.approval_status == "pending"

    assert explanation.authorized_allocation_eur == 0.0
    assert not explanation.execution_authorized

    print(
        "MILESTONE 15K — CANONICAL PRODUCTION "
        "EUR 5M RECOMMENDATION"
    )
    print()

    print(
        "As of:",
        AS_OF,
    )

    print(
        "Treasury capital:",
        f"EUR "
        f"{MODEL_COMPANY_MANDATE.treasury_capital_eur:,.0f}",
    )

    print()

    print(
        "Production universe:",
        len(universe_candidates),
    )

    print(
        "Recommendation-ready:",
        len(ready),
    )

    print(
        "Needs evidence:",
        len(needs_evidence),
    )

    print(
        "Blocked:",
        len(blocked),
    )

    print()

    print(
        "Selected:",
        explanation.selected_label,
    )

    print(
        "Allocation:",
        f"EUR "
        f"{explanation.selected_allocation_eur:,.0f}",
    )

    print(
        "Allocation percentage:",
        f"{explanation.selected_allocation_pct:.2f}%",
    )

    print(
        "Defensible return:",
        f"{explanation.selected_return_pct:.3f}%",
    )

    print(
        "Expected annual return:",
        f"EUR "
        f"{explanation.selected_annual_return_eur:,.0f}",
    )

    print()

    print(
        "Target yield:",
        f"{explanation.target_yield_pct:.3f}%",
    )

    print(
        "Target yield gap:",
        f"{explanation.target_yield_gap_pct:.3f} "
        "percentage points",
    )

    print(
        "Target annual EUR gap:",
        f"EUR "
        f"{explanation.target_yield_gap_eur:,.0f}",
    )

    print()

    print("READY OPPORTUNITIES")

    for opportunity in explanation.ready_opportunities:
        print(
            f"  {opportunity.label:<24}"
            f"{opportunity.defensible_return_pct:>7.3f}%"
            f"  annual="
            f"EUR "
            f"{opportunity.annual_return_eur_at_position:>10,.0f}"
            f"  disadvantage="
            f"{opportunity.return_difference_vs_selected_bps:>6.2f}"
            f" bps"
        )

    print()

    print(
        "Recommended action:",
        report.recommended_action,
    )

    print(
        "Recommendation status:",
        report.recommendation_status,
    )

    print(
        "Approval status:",
        report.approval_status,
    )

    print(
        "Authorized allocation:",
        f"EUR "
        f"{report.authorized_allocation_eur:,.0f}",
    )

    print(
        "Execution authorized:",
        report.execution_authorized,
    )

    print()

    print(
        "Selection candidate count:",
        construction.candidate_count,
    )

    print(
        "Selected assessment originates from "
        "production universe:",
        selected in universe_candidates,
    )

    print()

    print(
        "All Milestone 15K canonical-production-"
        "selection assertions passed."
    )


if __name__ == "__main__":
    main()
