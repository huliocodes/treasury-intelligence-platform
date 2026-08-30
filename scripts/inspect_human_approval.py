from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.approvals import (
    approve_recommendation,
    create_pending_approval,
    execution_authorized,
    reject_recommendation,
)

from treasury_intelligence.analytics.portfolio_construction import (
    build_portfolio_construction,
)

from treasury_intelligence.analytics.portfolio_proposals import (
    build_portfolio_proposal,
)

from treasury_intelligence.analytics.recommendations import (
    build_recommendation_decision,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.portfolio_construction import (
    AllocationInstruction,
)


DECIDED_AT = "2026-08-30T14:53:00+02:00"


def build_ready_candidate(
) -> PortfolioCandidateAssessment:
    return PortfolioCandidateAssessment(
        assessment_id=(
            "fixture_ready_500k_approval"
        ),
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        instrument_id="fixture_instrument",
        market_id="fixture_market",
        access_route_id="fixture_access",
        label="READY FIXTURE",
        position_size_eur=500_000,
        eligibility_status="eligible",
        liquidity_position_status="supported",
        economics_status="complete",
        base_risk_unknown_dimension_count=0,
        defensible_return_pct=2.500,
        defensible_return_measure=(
            "Deterministic 7B approval fixture."
        ),
        candidate_status=(
            "recommendation_ready"
        ),
        blocking_reasons=(),
        evidence_requirements=(),
        recommendation_ready=True,
        notes=(
            "Deterministic recommendation-ready fixture "
            "used only to validate the approval layer."
        ),
    )


def build_hold_candidate(
) -> PortfolioCandidateAssessment:
    return PortfolioCandidateAssessment(
        assessment_id=(
            "fixture_non_ready_500k_approval"
        ),
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        instrument_id="fixture_non_ready",
        market_id="fixture_non_ready_market",
        access_route_id="fixture_non_ready_access",
        label="NON-READY FIXTURE",
        position_size_eur=500_000,
        eligibility_status="needs_evidence",
        liquidity_position_status="unknown",
        economics_status="incomplete",
        base_risk_unknown_dimension_count=4,
        defensible_return_pct=2.000,
        defensible_return_measure=(
            "Deterministic 7B non-ready fixture."
        ),
        candidate_status="needs_evidence",
        blocking_reasons=(),
        evidence_requirements=(
            "Additional evidence required.",
        ),
        recommendation_ready=False,
        notes=(
            "Deterministic non-ready fixture used "
            "to prove that HOLD recommendations cannot "
            "enter the approval layer."
        ),
    )


def build_allocation_recommendation():
    candidate = build_ready_candidate()

    construction = (
        build_portfolio_construction(
            construction_id=(
                "approval_fixture_construction"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            candidates=(
                candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        candidate.assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    proposal = (
        build_portfolio_proposal(
            proposal_id=(
                "approval_fixture_proposal"
            ),
            construction=construction,
            candidates=(
                candidate,
            ),
        )
    )

    recommendation = (
        build_recommendation_decision(
            recommendation_id=(
                "approval_fixture_recommendation"
            ),
            proposal=proposal,
        )
    )

    return recommendation


def build_hold_recommendation():
    candidate = build_hold_candidate()

    construction = (
        build_portfolio_construction(
            construction_id=(
                "hold_fixture_construction"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            candidates=(
                candidate,
            ),
            instructions=(),
        )
    )

    proposal = (
        build_portfolio_proposal(
            proposal_id=(
                "hold_fixture_proposal"
            ),
            construction=construction,
            candidates=(
                candidate,
            ),
        )
    )

    return build_recommendation_decision(
        recommendation_id=(
            "hold_fixture_recommendation"
        ),
        proposal=proposal,
    )


def print_approval(
    label: str,
    approval,
) -> None:
    print(label)
    print()

    print(
        f"Approval status:              "
        f"{approval.approval_status}"
    )

    print(
        f"Recommendation ID:            "
        f"{approval.recommendation_id}"
    )

    print(
        f"Proposed allocation:          "
        f"EUR {approval.proposed_allocation_eur:,.0f}"
    )

    print(
        f"Authorized allocation:        "
        f"EUR {approval.authorized_allocation_eur:,.0f}"
    )

    print(
        f"Execution authorized:         "
        f"{execution_authorized(approval)}"
    )

    print(
        f"Decided by:                   "
        f"{approval.decided_by}"
    )

    print(
        f"Decided at:                   "
        f"{approval.decided_at}"
    )

    if approval.rationale:
        print()
        print("RATIONALE")
        print()
        print(
            approval.rationale
        )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print("HUMAN APPROVAL RECORD")
    print()

    print(
        "The approval layer records human authorization "
        "for an exact recommendation. It does not execute "
        "the allocation."
    )

    print()

    print("-" * 100)
    print()

    recommendation = (
        build_allocation_recommendation()
    )

    print("UPSTREAM RECOMMENDATION")
    print()

    print(
        f"Recommended action:           "
        f"{recommendation.recommended_action}"
    )

    print(
        f"Recommendation status:        "
        f"{recommendation.recommendation_status}"
    )

    print(
        f"Proposed allocation:          "
        f"EUR {recommendation.allocated_capital_eur:,.0f}"
    )

    print(
        f"Human approval required:      "
        f"{recommendation.requires_human_approval}"
    )

    print()
    print("-" * 100)
    print()

    pending = (
        create_pending_approval(
            approval_id=(
                "approval_fixture_pending"
            ),
            recommendation=recommendation,
            notes=(
                "Awaiting human treasury decision."
            ),
        )
    )

    print_approval(
        label="CASE 1 — PENDING",
        approval=pending,
    )

    approved = (
        approve_recommendation(
            approval_id=(
                "approval_fixture_approved"
            ),
            recommendation=recommendation,
            decided_by="authorized_treasury_approver",
            decided_at=DECIDED_AT,
            rationale=(
                "Approved exactly as proposed."
            ),
        )
    )

    print_approval(
        label="CASE 2 — APPROVED",
        approval=approved,
    )

    rejected = (
        reject_recommendation(
            approval_id=(
                "approval_fixture_rejected"
            ),
            recommendation=recommendation,
            decided_by="authorized_treasury_approver",
            decided_at=DECIDED_AT,
            rationale=(
                "Recommendation rejected. No capital "
                "is authorized for execution."
            ),
        )
    )

    print_approval(
        label="CASE 3 — REJECTED",
        approval=rejected,
    )

    print(
        "CASE 4 — HOLD RECOMMENDATION "
        "CANNOT ENTER APPROVAL"
    )
    print()

    hold_recommendation = (
        build_hold_recommendation()
    )

    print(
        f"Hold recommended action:      "
        f"{hold_recommendation.recommended_action}"
    )

    try:
        create_pending_approval(
            approval_id=(
                "invalid_hold_approval"
            ),
            recommendation=(
                hold_recommendation
            ),
        )

    except ValueError as exc:
        print(
            "Approval rejected by gate:    True"
        )

        print(
            f"Reason:                       "
            f"{exc}"
        )

    else:
        raise AssertionError(
            "Hold recommendation unexpectedly "
            "entered the approval layer."
        )

    print()
    print("-" * 100)
    print()

    print("INTERPRETATION")
    print()

    print(
        "Pending approval authorizes no capital."
    )

    print(
        "Approved authorization matches the exact "
        "EUR 500,000 recommendation."
    )

    print(
        "Rejected approval authorizes no capital."
    )

    print(
        "A HOLD UNALLOCATED recommendation cannot "
        "enter an allocation-approval workflow."
    )

    print(
        "The next execution-planning layer may therefore "
        "use approval status as a hard authorization gate "
        "without treating recommendation as approval."
    )


if __name__ == "__main__":
    main()