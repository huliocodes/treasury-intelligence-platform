from __future__ import annotations

import os
from datetime import datetime, time, timezone

import psycopg

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

from treasury_intelligence.persistence.opportunity_snapshots import (
    load_latest_opportunity_snapshot,
)

from treasury_intelligence.sources.aave import (
    load_latest_aave_reserve_observation,
)

from treasury_intelligence.sources.ecb import (
    load_latest_estr_observation,
)

from treasury_intelligence.sources.france import (
    get_btf_2027_03_10_snapshot,
)

from treasury_intelligence.sources.ishares import (
    get_ernx_snapshot,
)


AS_OF = "2026-09-08"


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is required for the canonical "
            "production recommendation."
        )

    warehouse_as_of = datetime.combine(
        datetime.fromisoformat(AS_OF).date(),
        time.max,
        tzinfo=timezone.utc,
    )

    with psycopg.connect(database_url) as connection:
        btf_2027_03_10_snapshot = (
            load_latest_opportunity_snapshot(
                connection=connection,
                structural_snapshot=(
                    get_btf_2027_03_10_snapshot()
                ),
            )
        )

        ernx_snapshot = (
            load_latest_opportunity_snapshot(
                connection=connection,
                structural_snapshot=(
                    get_ernx_snapshot()
                ),
            )
        )

        estr_observation = (
            load_latest_estr_observation(
                connection=connection,
                as_of=warehouse_as_of,
            )
        )

        aave_observation = (
            load_latest_aave_reserve_observation(
                connection=connection,
                as_of=warehouse_as_of,
            )
        )

    universe_candidates = (
        analyze_opportunity_universe_at_position_size(
            position_size_eur=(
                MODEL_COMPANY_MANDATE.treasury_capital_eur
            ),
            mandate=MODEL_COMPANY_MANDATE,
            estr_observation=estr_observation,
            ernx_snapshot=ernx_snapshot,
            btf_2027_03_10_snapshot=(
                btf_2027_03_10_snapshot
            ),
            aave_observation=aave_observation,
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

    assert (
        len(ready)
        + len(needs_evidence)
        + len(blocked)
        == len(universe_candidates)
    )

    assert len(allocation_candidates) == 14
    assert allocation_candidates == universe_candidates

    ready_with_returns = tuple(
        candidate
        for candidate in ready
        if candidate.defensible_return_pct is not None
    )

    assert len(ready_with_returns) == len(ready)

    assert construction.candidate_count == 14

    assert (
        construction.recommendation_ready_candidate_count
        == len(ready)
    )

    selected = None

    if ready_with_returns:
        assert len(construction.allocation_lines) == 1

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

        assert selected.recommendation_ready
        assert selected.defensible_return_pct is not None

        assert selected is max(
            ready_with_returns,
            key=lambda candidate: (
                candidate.defensible_return_pct,
                candidate.assessment_id,
            ),
        )

        assert abs(
            construction.allocated_capital_eur
            - MODEL_COMPANY_MANDATE.treasury_capital_eur
        ) <= 0.01

        assert abs(
            construction.unallocated_capital_eur
        ) <= 0.01

    else:
        assert len(construction.allocation_lines) == 0

        assert abs(
            construction.allocated_capital_eur
        ) <= 0.01

        assert abs(
            construction.unallocated_capital_eur
            - MODEL_COMPANY_MANDATE.treasury_capital_eur
        ) <= 0.01

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

    approval = None

    if (
        recommendation.recommended_action
        == "submit_for_approval"
    ):
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

    explanation = None

    if selected is not None:
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
        == len(ready)
    )

    assert (
        report.universe.needs_evidence_count
        == len(needs_evidence)
    )

    assert (
        report.universe.blocked_count
        == len(blocked)
    )

    assert (
        len(ready)
        + len(needs_evidence)
        + len(blocked)
        == 14
    )

    assert report.authorized_allocation_eur == 0.0
    assert not report.execution_authorized

    if selected is not None:
        assert explanation is not None

        assert (
            explanation.selected_label
            == selected.label
        )

        assert abs(
            explanation.selected_allocation_eur
            - selected.position_size_eur
        ) <= 0.01

        assert abs(
            explanation.selected_allocation_pct
            - 100.0
        ) < 0.001

        assert selected.defensible_return_pct is not None

        assert abs(
            explanation.selected_return_pct
            - selected.defensible_return_pct
        ) < 1e-9

        expected_annual_return_eur = (
            selected.position_size_eur
            * selected.defensible_return_pct
            / 100.0
        )

        assert abs(
            explanation.selected_annual_return_eur
            - expected_annual_return_eur
        ) <= 0.01

        assert explanation.target_yield_pct == 3.0

        assert (
            recommendation.recommended_action
            == "submit_for_approval"
        )

        assert (
            recommendation.recommendation_status
            == "decision_ready"
        )

        assert recommendation.requires_human_approval
        assert not recommendation.requires_review

        assert approval is not None
        assert approval.approval_status == "pending"

        assert (
            explanation.authorized_allocation_eur
            == 0.0
        )

        assert not explanation.execution_authorized

    else:
        assert explanation is None
        assert approval is None

        assert (
            recommendation.recommended_action
            == "hold_unallocated"
        )

        assert (
            recommendation.recommendation_status
            == "decision_ready"
        )

        assert not recommendation.requires_human_approval
        assert not recommendation.requires_review

        assert abs(
            report.allocated_capital_eur
        ) <= 0.01

        assert abs(
            report.unallocated_capital_eur
            - MODEL_COMPANY_MANDATE.treasury_capital_eur
        ) <= 0.01

        assert (
            report.portfolio_defensible_return_pct
            is None
        )

        assert (
            report.portfolio_annual_return_eur
            is None
        )

        assert report.approval_status is None

    print(
        "MILESTONE 16C.4 - WAREHOUSE-BACKED "
        "PRODUCTION DECISION"
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

    if selected is not None:
        assert explanation is not None

        print(
            "Decision state: actionable allocation"
        )

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

    else:
        print(
            "Decision state: hold unallocated"
        )

        print(
            "Selected: none"
        )

        print(
            "Allocation:",
            f"EUR {report.allocated_capital_eur:,.0f}",
        )

        print(
            "Unallocated:",
            f"EUR {report.unallocated_capital_eur:,.0f}",
        )

        print(
            "Reason: no recommendation-ready opportunity "
            "currently satisfies the production evidence "
            "and freshness gates."
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
        (
            selected in universe_candidates
            if selected is not None
            else "not applicable"
        ),
    )

    print()

    print(
        "All Milestone 16C.4 warehouse-backed "
        "production-decision assertions passed."
    )


if __name__ == "__main__":
    main()
