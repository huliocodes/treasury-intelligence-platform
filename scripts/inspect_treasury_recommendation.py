from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


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


def build_non_ready_candidate(
) -> PortfolioCandidateAssessment:
    return PortfolioCandidateAssessment(
        assessment_id=(
            "fixture_xeon_500k_recommendation"
        ),
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        instrument_id="xeon",
        market_id="xeon_xetra",
        access_route_id="xeon_broker",
        label="XEON",
        position_size_eur=500_000,
        eligibility_status="needs_evidence",
        liquidity_position_status="unknown",
        economics_status="incomplete",
        base_risk_unknown_dimension_count=4,
        defensible_return_pct=2.073,
        defensible_return_measure=(
            "Deterministic 7A policy fixture."
        ),
        candidate_status="needs_evidence",
        blocking_reasons=(),
        evidence_requirements=(
            "Position-size executable liquidity required.",
        ),
        recommendation_ready=False,
        notes=(
            "Deterministic non-ready candidate used "
            "to validate the recommendation layer."
        ),
    )


def build_ready_candidate(
) -> PortfolioCandidateAssessment:
    return PortfolioCandidateAssessment(
        assessment_id=(
            "fixture_ready_500k_recommendation"
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
            "Deterministic 7A policy fixture."
        ),
        candidate_status=(
            "recommendation_ready"
        ),
        blocking_reasons=(),
        evidence_requirements=(),
        recommendation_ready=True,
        notes=(
            "Deterministic recommendation-ready "
            "candidate used to validate the "
            "recommendation layer."
        ),
    )


def build_decision(
    case_id: str,
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
    instructions: tuple[
        AllocationInstruction,
        ...
    ],
):
    construction = (
        build_portfolio_construction(
            construction_id=(
                f"{case_id}_construction"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            candidates=candidates,
            instructions=instructions,
        )
    )

    proposal = (
        build_portfolio_proposal(
            proposal_id=(
                f"{case_id}_proposal"
            ),
            construction=construction,
            candidates=candidates,
        )
    )

    recommendation = (
        build_recommendation_decision(
            recommendation_id=(
                f"{case_id}_recommendation"
            ),
            proposal=proposal,
        )
    )

    return (
        construction,
        proposal,
        recommendation,
    )


def print_decision(
    label: str,
    construction,
    proposal,
    recommendation,
) -> None:
    print(label)
    print()

    print(
        f"Construction status:          "
        f"{construction.construction_status}"
    )

    print(
        f"Proposal status:              "
        f"{proposal.proposal_status}"
    )

    print(
        f"Recommendation status:        "
        f"{recommendation.recommendation_status}"
    )

    print(
        f"Recommended action:           "
        f"{recommendation.recommended_action}"
    )

    print(
        f"Allocated capital:            "
        f"EUR {recommendation.allocated_capital_eur:,.0f}"
    )

    print(
        f"Unallocated capital:          "
        f"EUR {recommendation.unallocated_capital_eur:,.0f}"
    )

    print(
        f"Human approval required:      "
        f"{recommendation.requires_human_approval}"
    )

    print(
        f"Review required:              "
        f"{recommendation.requires_review}"
    )

    if recommendation.allocation_lines:
        print()
        print("PROPOSED ALLOCATIONS")

        for line in (
            recommendation.allocation_lines
        ):
            print(
                f"  {line.label:<20} "
                f"EUR {line.allocation_eur:>12,.0f} | "
                f"{line.allocation_pct_of_treasury:>6.2f}%"
            )

    print()
    print("RATIONALE")
    print()

    print(
        recommendation.rationale
    )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print("TREASURY RECOMMENDATION DECISION")
    print()

    print(
        "The recommendation layer converts a validated "
        "portfolio proposal into the next treasury action."
    )

    print()

    print("-" * 100)
    print()

    non_ready_candidate = (
        build_non_ready_candidate()
    )

    (
        construction,
        proposal,
        recommendation,
    ) = build_decision(
        case_id="no_actionable",
        candidates=(
            non_ready_candidate,
        ),
        instructions=(),
    )

    print_decision(
        label=(
            "CASE 1 — NO ACTIONABLE ALLOCATION"
        ),
        construction=construction,
        proposal=proposal,
        recommendation=recommendation,
    )

    ready_candidate = (
        build_ready_candidate()
    )

    (
        construction,
        proposal,
        recommendation,
    ) = build_decision(
        case_id="ready_without_allocation",
        candidates=(
            ready_candidate,
        ),
        instructions=(),
    )

    print_decision(
        label=(
            "CASE 2 — READY CANDIDATE BUT "
            "NO ALLOCATION PROPOSED"
        ),
        construction=construction,
        proposal=proposal,
        recommendation=recommendation,
    )

    (
        construction,
        proposal,
        recommendation,
    ) = build_decision(
        case_id="allocation_proposed",
        candidates=(
            ready_candidate,
        ),
        instructions=(
            AllocationInstruction(
                candidate_assessment_id=(
                    ready_candidate.assessment_id
                ),
                allocation_eur=500_000,
            ),
        ),
    )

    print_decision(
        label=(
            "CASE 3 — VALID ALLOCATION PROPOSED"
        ),
        construction=construction,
        proposal=proposal,
        recommendation=recommendation,
    )

    print("INTERPRETATION")
    print()

    print(
        "Case 1 is the current production-relevant "
        "behavior: unresolved evidence leads to a "
        "decision-ready HOLD UNALLOCATED recommendation."
    )

    print(
        "Case 2 does not silently convert the existence "
        "of recommendation-ready candidates into an "
        "investment decision. It requires review because "
        "no allocation instructions exist."
    )

    print(
        "Case 3 does not approve or execute the proposed "
        "investment. It submits the policy-compliant "
        "proposal to the next human approval layer."
    )


if __name__ == "__main__":
    main()