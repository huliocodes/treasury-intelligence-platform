from __future__ import annotations

from treasury_intelligence.analytics.allocation_selection import (
    AllocationOpportunity,
    build_return_priority_portfolio_construction,
)

from treasury_intelligence.analytics.approvals import (
    create_pending_approval,
)

from treasury_intelligence.analytics.portfolio_proposals import (
    build_portfolio_proposal,
)

from treasury_intelligence.analytics.recommendation_candidates import (
    build_btf_recommendation_candidate,
    build_bubill_recommendation_candidate,
    build_ernx_recommendation_candidate,
)

from treasury_intelligence.analytics.recommendations import (
    build_recommendation_decision,
)

from treasury_intelligence.analytics.treasury_decision_reports import (
    build_treasury_decision_report,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)


OPPORTUNITIES = (
    AllocationOpportunity(
        key="ernx",
        label="ERNX",
        candidate_builder=(
            build_ernx_recommendation_candidate
        ),
    ),
    AllocationOpportunity(
        key="btf",
        label="French BTF",
        candidate_builder=(
            build_btf_recommendation_candidate
        ),
    ),
    AllocationOpportunity(
        key="bubill",
        label="German Bubill",
        candidate_builder=(
            build_bubill_recommendation_candidate
        ),
    ),
)


def build_summary_candidate(
    *,
    assessment_id: str,
    label: str,
    candidate_status: str,
) -> PortfolioCandidateAssessment:
    recommendation_ready = (
        candidate_status == "recommendation_ready"
    )

    blocking_reasons = (
        ("Blocked by current mandate or evidence.",)
        if candidate_status == "blocked"
        else ()
    )

    evidence_requirements = (
        ("Additional evidence required.",)
        if candidate_status == "needs_evidence"
        else ()
    )

    return PortfolioCandidateAssessment(
        assessment_id=assessment_id,
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        instrument_id=(
            f"{assessment_id}_instrument"
        ),
        market_id=f"{assessment_id}_market",
        access_route_id=(
            f"{assessment_id}_access"
        ),
        label=label,
        position_size_eur=100_000.0,
        eligibility_status=(
            "eligible"
            if recommendation_ready
            else "not_ready"
        ),
        liquidity_position_status=(
            "supported"
            if recommendation_ready
            else "unknown"
        ),
        economics_status=(
            "sufficient"
            if recommendation_ready
            else "incomplete"
        ),
        base_risk_unknown_dimension_count=(
            0 if recommendation_ready else 1
        ),
        defensible_return_pct=(
            0.0
            if recommendation_ready
            else None
        ),
        defensible_return_measure=(
            "diagnostic"
            if recommendation_ready
            else None
        ),
        candidate_status=candidate_status,
        blocking_reasons=blocking_reasons,
        evidence_requirements=(
            evidence_requirements
        ),
        recommendation_ready=(
            recommendation_ready
        ),
        notes=(
            "Universe-summary fixture only. Actual "
            "opportunity status is regression-tested by "
            "inspect_universe_position_matrix.py."
        ),
    )


universe_candidates = (
    build_summary_candidate(
        assessment_id="summary_ernx",
        label="ERNX",
        candidate_status="recommendation_ready",
    ),
    build_summary_candidate(
        assessment_id="summary_btf",
        label="French BTF",
        candidate_status="recommendation_ready",
    ),
    build_summary_candidate(
        assessment_id="summary_bubill",
        label="German Bubill",
        candidate_status="recommendation_ready",
    ),
    build_summary_candidate(
        assessment_id="summary_amundi",
        label="Amundi Overnight",
        candidate_status="needs_evidence",
    ),
    build_summary_candidate(
        assessment_id="summary_xeon",
        label="XEON",
        candidate_status="blocked",
    ),
    build_summary_candidate(
        assessment_id="summary_aave",
        label="Aave V3 Base EURC",
        candidate_status="blocked",
    ),
    build_summary_candidate(
        assessment_id="summary_addiko",
        label="Addiko Deposit",
        candidate_status="blocked",
    ),
    build_summary_candidate(
        assessment_id="summary_blackrock",
        label="BlackRock MMF",
        candidate_status="blocked",
    ),
    build_summary_candidate(
        assessment_id="summary_spiko",
        label="Spiko",
        candidate_status="blocked",
    ),
)


construction, selected_candidates = (
    build_return_priority_portfolio_construction(
        construction_id=(
            "model_company_5m_return_priority"
        ),
        mandate=MODEL_COMPANY_MANDATE,
        opportunities=OPPORTUNITIES,
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
        "Initial V1 treasury decision report. Execution "
        "and operational implementation remain outside "
        "the current project scope."
    ),
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

print("===== UNIVERSE =====")

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

print(
    "Ready:",
    ", ".join(
        report.universe.recommendation_ready_labels
    ),
)

print(
    "Needs evidence:",
    ", ".join(
        report.universe.needs_evidence_labels
    ),
)

print(
    "Blocked:",
    ", ".join(
        report.universe.blocked_labels
    ),
)

print()

print("===== ALLOCATION =====")

for line in report.allocation_lines:
    print(
        f"{line.label:<20}",
        f"EUR {line.allocation_eur:>12,.0f}",
        f"{line.allocation_pct_of_treasury:>7.2f}%",
    )

print()

print(
    "Allocated:",
    f"EUR {report.allocated_capital_eur:,.0f}",
)

print(
    "Unallocated:",
    f"EUR {report.unallocated_capital_eur:,.0f}",
)

print()

print("===== RETURN =====")

print(
    "Portfolio defensible return:",
    (
        f"{report.portfolio_defensible_return_pct:.3f}%"
        if report.portfolio_defensible_return_pct
        is not None
        else "Unknown"
    ),
)

print(
    "Portfolio annual return:",
    (
        f"EUR {report.portfolio_annual_return_eur:,.0f}"
        if report.portfolio_annual_return_eur
        is not None
        else "Unknown"
    ),
)

print(
    "Target yield gap:",
    (
        f"{report.target_yield_gap_pct:.3f} "
        "percentage points"
        if report.target_yield_gap_pct
        is not None
        else "Unknown"
    ),
)

print(
    "Target annual EUR gap:",
    (
        f"EUR {report.target_yield_gap_eur:,.0f}"
        if report.target_yield_gap_eur
        is not None
        else "Unknown"
    ),
)

print()

print("===== DECISION / APPROVAL =====")

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
    f"EUR {report.authorized_allocation_eur:,.0f}",
)

print(
    "Execution authorized:",
    report.execution_authorized,
)

print(
    "Report status:",
    report.report_status,
)

print()

print("Rationale:")
print(report.rationale)