from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.analytics.allocation_opportunities import (
    ALLOCATION_OPPORTUNITIES,
)

from treasury_intelligence.analytics.allocation_selection import (
    build_return_priority_portfolio_construction,
)

from treasury_intelligence.analytics.approvals import (
    create_pending_approval,
)

from treasury_intelligence.analytics.decision_explanations import (
    build_treasury_decision_explanation,
)

from treasury_intelligence.analytics.portfolio_comparisons import (
    build_portfolio_alternative_comparison,
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



def build_construction(
    *,
    construction_id: str,
    maximum_single_position_pct: float,
):
    mandate = replace(
        MODEL_COMPANY_MANDATE,
        maximum_single_position_pct=(
            maximum_single_position_pct
        ),
    )

    return (
        mandate,
        *build_return_priority_portfolio_construction(
            construction_id=construction_id,
            mandate=mandate,
            opportunities=ALLOCATION_OPPORTUNITIES,
            notes=(
                "Counterfactual concentration scenario "
                "for decision explanation."
            ),
        ),
    )


AS_OF = "2026-09-03"


universe_candidates = (
    analyze_opportunity_universe_at_position_size(
        position_size_eur=(
            MODEL_COMPANY_MANDATE.treasury_capital_eur
        ),
        mandate=MODEL_COMPANY_MANDATE,
        as_of=AS_OF,
    )
)


construction, selected_candidates = (
    build_return_priority_portfolio_construction(
        construction_id=(
            "model_company_5m_return_priority"
        ),
        mandate=MODEL_COMPANY_MANDATE,
        opportunities=ALLOCATION_OPPORTUNITIES,
        notes=(
            "Return-priority V1 construction using the "
            "currently recommendation-ready opportunity "
            "set."
        ),
    )
)


proposal = build_portfolio_proposal(
    proposal_id="model_company_5m_proposal",
    construction=construction,
    candidates=selected_candidates,
)


recommendation = build_recommendation_decision(
    recommendation_id=(
        "model_company_5m_recommendation"
    ),
    proposal=proposal,
)


approval = create_pending_approval(
    approval_id="model_company_5m_approval",
    recommendation=recommendation,
    notes=(
        "Pending human approval. No execution is "
        "authorized."
    ),
)


report = build_treasury_decision_report(
    report_id="model_company_5m_report",
    mandate=MODEL_COMPANY_MANDATE,
    universe_candidates=universe_candidates,
    construction=construction,
    allocation_candidates=selected_candidates,
    recommendation=recommendation,
    approval=approval,
    notes=(
        "Expanded treasury decision report using "
        "real production universe assessments. "
        "Execution and operational implementation "
        "remain outside the current project scope."
    ),
)


(
    mandate_50,
    construction_50,
    candidates_50,
) = build_construction(
    construction_id=(
        "model_company_5m_50pct_diagnostic"
    ),
    maximum_single_position_pct=50.0,
)


(
    mandate_40,
    construction_40,
    candidates_40,
) = build_construction(
    construction_id=(
        "model_company_5m_40pct_diagnostic"
    ),
    maximum_single_position_pct=40.0,
)


comparison_50 = (
    build_portfolio_alternative_comparison(
        comparison_id=(
            "selected_vs_50pct_diagnostic"
        ),
        selected_construction=construction,
        selected_candidates=selected_candidates,
        alternative_construction=construction_50,
        alternative_candidates=candidates_50,
        notes=(
            "50% maximum-position diagnostic only."
        ),
    )
)


comparison_40 = (
    build_portfolio_alternative_comparison(
        comparison_id=(
            "selected_vs_40pct_diagnostic"
        ),
        selected_construction=construction,
        selected_candidates=selected_candidates,
        alternative_construction=construction_40,
        alternative_candidates=candidates_40,
        notes=(
            "40% maximum-position diagnostic only."
        ),
    )
)


explanation = (
    build_treasury_decision_explanation(
        explanation_id=(
            "model_company_5m_explanation"
        ),
        report=report,
        universe_candidates=universe_candidates,
        concentration_comparisons=(
            (
                "50% maximum-position diagnostic",
                mandate_50.maximum_single_position_pct,
                comparison_50,
            ),
            (
                "40% maximum-position diagnostic",
                mandate_40.maximum_single_position_pct,
                comparison_40,
            ),
        ),
        notes=(
            "Decision explanation reports existing "
            "analytical outputs and does not introduce "
            "a diversification policy."
        ),
    )
)


print("===== TREASURY DECISION =====")
print()

print(
    "Mandate:",
    report.mandate_name,
)

print(
    "Treasury capital:",
    f"EUR {report.treasury_capital_eur:,.0f}",
)

print(
    "Target yield:",
    (
        f"{report.target_yield_pct:.3f}%"
        if report.target_yield_pct is not None
        else "None"
    ),
)

print(
    "Target is hard constraint:",
    report.target_yield_is_hard_constraint,
)

print()

print("===== REAL EUR 5M UNIVERSE =====")

print(
    "Opportunities:",
    report.universe.opportunity_count,
)

print(
    "Recommendation-ready:",
    report.universe.recommendation_ready_count,
)

print(
    "Needs evidence:",
    report.universe.needs_evidence_count,
)

print(
    "Blocked:",
    report.universe.blocked_count,
)

print()

print("===== RECOMMENDATION =====")

print(
    "Selected:",
    explanation.selected_label,
)

print(
    "Allocation:",
    f"EUR {explanation.selected_allocation_eur:,.0f}",
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
    f"EUR {explanation.selected_annual_return_eur:,.0f}",
)

print()

print("===== WHY THIS OPPORTUNITY =====")

for opportunity in explanation.ready_opportunities:
    print(
        f"{opportunity.label:<20}"
        f"{opportunity.defensible_return_pct:>8.3f}%"
        f"  annual="
        f"EUR {opportunity.annual_return_eur_at_position:>10,.0f}"
        f"  selected advantage="
        f"{opportunity.return_difference_vs_selected_bps:>6.2f} bps"
        f" / EUR "
        f"{opportunity.annual_return_difference_vs_selected_eur:,.0f}"
    )

print()

print("===== TARGET =====")

print(
    "Target:",
    (
        f"{explanation.target_yield_pct:.3f}%"
        if explanation.target_yield_pct is not None
        else "None"
    ),
)

print(
    "Achieved:",
    f"{explanation.selected_return_pct:.3f}%",
)

print(
    "Yield gap:",
    (
        f"{explanation.target_yield_gap_pct:.3f} "
        "percentage points"
        if explanation.target_yield_gap_pct is not None
        else "None"
    ),
)

print(
    "Annual EUR gap:",
    (
        f"EUR {explanation.target_yield_gap_eur:,.0f}"
        if explanation.target_yield_gap_eur is not None
        else "None"
    ),
)

print()

print("===== CONCENTRATION DIAGNOSTICS =====")

print(
    f"{'Scenario':<34}"
    f"{'Positions':>10}"
    f"{'Largest':>12}"
    f"{'Return':>12}"
    f"{'Annual EUR':>16}"
    f"{'Cost':>12}"
)

for alternative in (
    explanation.concentration_alternatives
):
    print(
        f"{alternative.label:<34}"
        f"{alternative.position_count:>10}"
        f"{alternative.largest_position_pct:>11.2f}%"
        f"{alternative.annual_return_pct:>11.3f}%"
        f"  EUR {alternative.annual_return_eur:>10,.0f}"
        f"{alternative.return_cost_bps:>9.2f} bps"
    )

print()

print(
    explanation.concentration_policy_interpretation
)

print()

print("===== NON-READY OPPORTUNITIES =====")

for opportunity in (
    explanation.non_ready_opportunities
):
    return_text = (
        f"{opportunity.defensible_return_pct:.3f}%"
        if opportunity.defensible_return_pct is not None
        else "unknown"
    )

    print()
    print(
        f"{opportunity.label} "
        f"[{opportunity.candidate_status}] "
        f"return={return_text}"
    )

    print(
        "  Blockers:",
        len(opportunity.blocking_reasons),
    )

    for blocker in opportunity.blocking_reasons:
        print(
            f"    - {blocker}"
        )

    print(
        "  Evidence requirements:",
        len(opportunity.evidence_requirements),
    )

    for requirement in (
        opportunity.evidence_requirements
    ):
        print(
            f"    - {requirement}"
        )

print()

print("===== APPROVAL / EXECUTION =====")

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
    explanation.approval_status,
)

print(
    "Authorized allocation:",
    f"EUR {explanation.authorized_allocation_eur:,.0f}",
)

print(
    "Execution authorized:",
    explanation.execution_authorized,
)

print(
    "Report status:",
    report.report_status,
)
