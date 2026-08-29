from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.portfolio_construction import (
    build_portfolio_construction,
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
            "fixture_xeon_500k_candidate"
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
            "Deterministic 6C policy fixture."
        ),
        candidate_status="needs_evidence",
        blocking_reasons=(),
        evidence_requirements=(
            "Position-size executable liquidity required.",
        ),
        recommendation_ready=False,
        notes=(
            "Deterministic fixture used only to validate "
            "portfolio-construction policy behavior."
        ),
    )


def build_ready_candidate(
) -> PortfolioCandidateAssessment:
    return PortfolioCandidateAssessment(
        assessment_id=(
            "fixture_ready_500k_candidate"
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
            "Deterministic 6C policy fixture."
        ),
        candidate_status=(
            "recommendation_ready"
        ),
        blocking_reasons=(),
        evidence_requirements=(),
        recommendation_ready=True,
        notes=(
            "Deterministic recommendation-ready fixture "
            "used only to validate construction rules."
        ),
    )


def print_assessment(
    label: str,
    assessment,
) -> None:
    print(label)
    print()

    print(
        f"Construction status:          "
        f"{assessment.construction_status}"
    )

    print(
        f"Treasury capital:             "
        f"EUR {assessment.treasury_capital_eur:,.0f}"
    )

    print(
        f"Candidates:                   "
        f"{assessment.candidate_count}"
    )

    print(
        f"Recommendation ready:         "
        f"{assessment.recommendation_ready_candidate_count}"
    )

    print(
        f"Allocated capital:            "
        f"EUR {assessment.allocated_capital_eur:,.0f}"
    )

    print(
        f"Unallocated capital:          "
        f"EUR {assessment.unallocated_capital_eur:,.0f}"
    )

    if assessment.allocation_lines:
        print()
        print("ALLOCATION LINES")

        for line in assessment.allocation_lines:
            print(
                f"  {line.label:<20} "
                f"EUR {line.allocation_eur:>12,.0f} | "
                f"{line.allocation_pct_of_treasury:>6.2f}%"
            )

    if assessment.validation_issues:
        print()
        print("VALIDATION ISSUES")

        for issue in assessment.validation_issues:
            print(
                f"  - {issue}"
            )

    if assessment.notes:
        print()
        print(
            f"Notes: {assessment.notes}"
        )

    print()
    print("-" * 100)
    print()


def main() -> None:
    mandate = MODEL_COMPANY_MANDATE

    print("PORTFOLIO CONSTRUCTION POLICY")
    print()

    print(
        "Portfolio construction does not force capital "
        "into candidates that are not recommendation-ready."
    )

    print()

    print("-" * 100)
    print()

    no_action = (
        build_portfolio_construction(
            construction_id=(
                "model_company_no_action"
            ),
            mandate=mandate,
            candidates=(),
            instructions=(),
        )
    )

    print_assessment(
        label=(
            "CASE 1 — NO ACTIONABLE CANDIDATES"
        ),
        assessment=no_action,
    )

    non_ready_candidate = (
        build_non_ready_candidate()
    )

    blocked_attempt = (
        build_portfolio_construction(
            construction_id=(
                "model_company_blocked_attempt"
            ),
            mandate=mandate,
            candidates=(
                non_ready_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        non_ready_candidate
                        .assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    print_assessment(
        label=(
            "CASE 2 — ATTEMPT TO ALLOCATE "
            "TO NON-READY CANDIDATE"
        ),
        assessment=blocked_attempt,
    )

    ready_candidate = (
        build_ready_candidate()
    )

    mismatched_size = (
        build_portfolio_construction(
            construction_id=(
                "model_company_size_mismatch"
            ),
            mandate=mandate,
            candidates=(
                ready_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        ready_candidate
                        .assessment_id
                    ),
                    allocation_eur=750_000,
                ),
            ),
        )
    )

    print_assessment(
        label=(
            "CASE 3 — POSITION-SIZE MISMATCH"
        ),
        assessment=mismatched_size,
    )

    valid_allocation = (
        build_portfolio_construction(
            construction_id=(
                "model_company_valid_fixture"
            ),
            mandate=mandate,
            candidates=(
                ready_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        ready_candidate
                        .assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    print_assessment(
        label=(
            "CASE 4 — VALID POLICY-COMPLIANT "
            "ALLOCATION"
        ),
        assessment=valid_allocation,
    )

    print("INTERPRETATION")
    print()

    print(
        "Case 1 is the current production-relevant "
        "portfolio behavior: if no candidate is "
        "recommendation-ready, no capital is deployed."
    )

    print(
        "Case 2 proves that portfolio construction "
        "cannot override upstream recommendation readiness."
    )

    print(
        "Case 3 proves that a candidate assessment is "
        "position-size specific. A different allocation "
        "requires a new upstream analysis."
    )

    print(
        "Case 4 proves that a recommendation-ready "
        "candidate at its analyzed position size can pass "
        "the mechanical construction policy."
    )
    

if __name__ == "__main__":
    main()