from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.allocation_deltas import (
    build_treasury_allocation_delta,
)

from treasury_intelligence.analytics.economic_comparisons import (
    build_treasury_economic_comparison,
)

from treasury_intelligence.analytics.portfolio_construction import (
    build_portfolio_construction,
)

from treasury_intelligence.analytics.portfolio_proposals import (
    build_portfolio_proposal,
)

from treasury_intelligence.analytics.treasury_state import (
    build_treasury_state,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.economic_comparisons import (
    AllocationReturnInput,
    UnallocatedReturnInput,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.portfolio_construction import (
    AllocationInstruction,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryPosition,
)


AS_OF = "2026-08-30T15:00:00+02:00"


def build_ready_candidate(
    assessment_id: str,
    instrument_id: str,
    market_id: str,
    access_route_id: str,
    label: str,
    position_size_eur: float,
    defensible_return_pct: float,
) -> PortfolioCandidateAssessment:
    return PortfolioCandidateAssessment(
        assessment_id=assessment_id,
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        instrument_id=instrument_id,
        market_id=market_id,
        access_route_id=access_route_id,
        label=label,
        position_size_eur=(
            position_size_eur
        ),
        eligibility_status="eligible",
        liquidity_position_status="supported",
        economics_status="complete",
        base_risk_unknown_dimension_count=0,
        defensible_return_pct=(
            defensible_return_pct
        ),
        defensible_return_measure=(
            "Deterministic 7C.3 fixture."
        ),
        candidate_status=(
            "recommendation_ready"
        ),
        blocking_reasons=(),
        evidence_requirements=(),
        recommendation_ready=True,
    )


def build_proposal(
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

    return build_portfolio_proposal(
        proposal_id=(
            f"{case_id}_proposal"
        ),
        construction=construction,
        candidates=candidates,
    )


def print_comparison(
    label: str,
    comparison,
) -> None:
    print(label)
    print()

    print(
        f"Comparison status:            "
        f"{comparison.comparison_status}"
    )

    if (
        comparison.current_annual_return_eur
        is None
    ):
        current_return = "UNKNOWN"
    else:
        current_return = (
            "EUR "
            f"{comparison.current_annual_return_eur:,.0f}"
        )

    if (
        comparison.proposed_annual_return_eur
        is None
    ):
        proposed_return = "UNKNOWN"
    else:
        proposed_return = (
            "EUR "
            f"{comparison.proposed_annual_return_eur:,.0f}"
        )

    if (
        comparison.incremental_annual_benefit_eur
        is None
    ):
        incremental_benefit = "UNKNOWN"
    else:
        incremental_benefit = (
            "EUR "
            f"{comparison.incremental_annual_benefit_eur:,.0f}"
        )

    print(
        f"Current annual return:        "
        f"{current_return}"
    )

    print(
        f"Proposed annual return:       "
        f"{proposed_return}"
    )

    print(
        f"Incremental annual benefit:   "
        f"{incremental_benefit}"
    )

    if (
        comparison.incremental_annual_benefit_pct_of_treasury
        is None
    ):
        benefit_pct = "UNKNOWN"
    else:
        benefit_pct = (
            f"{comparison.incremental_annual_benefit_pct_of_treasury:.4f}%"
        )

    print(
        f"Benefit % of treasury:        "
        f"{benefit_pct}"
    )

    if comparison.missing_evidence:
        print()
        print("MISSING EVIDENCE")
        print()

        for item in (
            comparison.missing_evidence
        ):
            print(
                f"  - {item}"
            )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print("INCREMENTAL ECONOMIC BENEFIT")
    print()

    print(
        "The economic-comparison layer measures the "
        "expected annual return difference between "
        "current and proposed treasury allocations "
        "before switching costs."
    )

    print()
    print("-" * 100)
    print()

    unallocated_1pct = (
        UnallocatedReturnInput(
            annual_return_pct=1.0,
            evidence_available=True,
            source_reference=(
                "fixture_unallocated_1pct"
            ),
        )
    )

    fully_unallocated_state = (
        build_treasury_state(
            state_id=(
                "fixture_unallocated_state"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(),
        )
    )

    position_b_candidate = (
        build_ready_candidate(
            assessment_id=(
                "fixture_b_500k"
            ),
            instrument_id="instrument_b",
            market_id="market_b",
            access_route_id="access_b",
            label="POSITION B",
            position_size_eur=500_000,
            defensible_return_pct=3.0,
        )
    )

    open_b_proposal = (
        build_proposal(
            case_id="open_b",
            candidates=(
                position_b_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        position_b_candidate.assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    open_b_delta = (
        build_treasury_allocation_delta(
            delta_id="delta_open_b",
            state=fully_unallocated_state,
            proposal=open_b_proposal,
        )
    )

    open_b_comparison = (
        build_treasury_economic_comparison(
            comparison_id=(
                "comparison_open_b"
            ),
            state=fully_unallocated_state,
            proposal=open_b_proposal,
            delta=open_b_delta,
            current_position_returns=(),
            proposed_position_returns=(
                AllocationReturnInput(
                    instrument_id="instrument_b",
                    market_id="market_b",
                    access_route_id="access_b",
                    label="POSITION B",
                    annual_return_pct=3.0,
                    evidence_available=True,
                    source_reference=(
                        "fixture_b_return"
                    ),
                ),
            ),
            current_unallocated_return=(
                unallocated_1pct
            ),
            proposed_unallocated_return=(
                unallocated_1pct
            ),
        )
    )

    print_comparison(
        label=(
            "CASE 1 — ALLOCATE EUR 500K "
            "FROM 1% CASH TO 3% POSITION"
        ),
        comparison=open_b_comparison,
    )

    current_a_position = TreasuryPosition(
        position_id="fixture_a_position",
        instrument_id="instrument_a",
        market_id="market_a",
        access_route_id="access_a",
        label="POSITION A",
        current_value_eur=500_000,
    )

    rotation_state = (
        build_treasury_state(
            state_id="fixture_rotation_state",
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(
                current_a_position,
            ),
        )
    )

    rotation_b_candidate = (
        build_ready_candidate(
            assessment_id=(
                "fixture_rotation_b"
            ),
            instrument_id="instrument_b",
            market_id="market_b",
            access_route_id="access_b",
            label="POSITION B",
            position_size_eur=500_000,
            defensible_return_pct=3.0,
        )
    )

    rotation_proposal = (
        build_proposal(
            case_id="rotation",
            candidates=(
                rotation_b_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        rotation_b_candidate.assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    rotation_delta = (
        build_treasury_allocation_delta(
            delta_id="delta_rotation",
            state=rotation_state,
            proposal=rotation_proposal,
        )
    )

    rotation_comparison = (
        build_treasury_economic_comparison(
            comparison_id=(
                "comparison_rotation"
            ),
            state=rotation_state,
            proposal=rotation_proposal,
            delta=rotation_delta,
            current_position_returns=(
                AllocationReturnInput(
                    instrument_id="instrument_a",
                    market_id="market_a",
                    access_route_id="access_a",
                    label="POSITION A",
                    annual_return_pct=2.0,
                    evidence_available=True,
                    source_reference=(
                        "fixture_a_return"
                    ),
                ),
            ),
            proposed_position_returns=(
                AllocationReturnInput(
                    instrument_id="instrument_b",
                    market_id="market_b",
                    access_route_id="access_b",
                    label="POSITION B",
                    annual_return_pct=3.0,
                    evidence_available=True,
                    source_reference=(
                        "fixture_b_return"
                    ),
                ),
            ),
            current_unallocated_return=(
                unallocated_1pct
            ),
            proposed_unallocated_return=(
                unallocated_1pct
            ),
        )
    )

    print_comparison(
        label=(
            "CASE 2 — ROTATE EUR 500K "
            "FROM 2% POSITION TO 3% POSITION"
        ),
        comparison=rotation_comparison,
    )

    unknown_current_comparison = (
        build_treasury_economic_comparison(
            comparison_id=(
                "comparison_unknown_current"
            ),
            state=rotation_state,
            proposal=rotation_proposal,
            delta=rotation_delta,
            current_position_returns=(
                AllocationReturnInput(
                    instrument_id="instrument_a",
                    market_id="market_a",
                    access_route_id="access_a",
                    label="POSITION A",
                    annual_return_pct=None,
                    evidence_available=False,
                    notes=(
                        "Current defensible return "
                        "has not been established."
                    ),
                ),
            ),
            proposed_position_returns=(
                AllocationReturnInput(
                    instrument_id="instrument_b",
                    market_id="market_b",
                    access_route_id="access_b",
                    label="POSITION B",
                    annual_return_pct=3.0,
                    evidence_available=True,
                ),
            ),
            current_unallocated_return=(
                unallocated_1pct
            ),
            proposed_unallocated_return=(
                unallocated_1pct
            ),
        )
    )

    print_comparison(
        label=(
            "CASE 3 — UNKNOWN CURRENT ECONOMICS"
        ),
        comparison=(
            unknown_current_comparison
        ),
    )

    unchanged_a_candidate = (
        build_ready_candidate(
            assessment_id=(
                "fixture_unchanged_a"
            ),
            instrument_id="instrument_a",
            market_id="market_a",
            access_route_id="access_a",
            label="POSITION A",
            position_size_eur=500_000,
            defensible_return_pct=2.0,
        )
    )

    unchanged_proposal = (
        build_proposal(
            case_id="unchanged",
            candidates=(
                unchanged_a_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        unchanged_a_candidate.assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    unchanged_delta = (
        build_treasury_allocation_delta(
            delta_id="delta_unchanged",
            state=rotation_state,
            proposal=unchanged_proposal,
        )
    )

    unchanged_comparison = (
        build_treasury_economic_comparison(
            comparison_id=(
                "comparison_unchanged"
            ),
            state=rotation_state,
            proposal=unchanged_proposal,
            delta=unchanged_delta,
            current_position_returns=(
                AllocationReturnInput(
                    instrument_id="instrument_a",
                    market_id="market_a",
                    access_route_id="access_a",
                    label="POSITION A",
                    annual_return_pct=2.0,
                    evidence_available=True,
                ),
            ),
            proposed_position_returns=(
                AllocationReturnInput(
                    instrument_id="instrument_a",
                    market_id="market_a",
                    access_route_id="access_a",
                    label="POSITION A",
                    annual_return_pct=2.0,
                    evidence_available=True,
                ),
            ),
            current_unallocated_return=(
                unallocated_1pct
            ),
            proposed_unallocated_return=(
                unallocated_1pct
            ),
        )
    )

    print_comparison(
        label=(
            "CASE 4 — UNCHANGED PORTFOLIO"
        ),
        comparison=unchanged_comparison,
    )

    print("INTERPRETATION")
    print()

    print(
        "Case 1 measures the opportunity cost of moving "
        "EUR 500,000 from treasury capital earning 1% "
        "into a position expected to earn 3%."
    )

    print(
        "Case 2 measures the benefit of rotating "
        "EUR 500,000 from a 2% position into a 3% "
        "position."
    )

    print(
        "Case 3 proves that unknown current economics "
        "cannot be silently replaced with a zero return."
    )

    print(
        "Case 4 proves that an economically unchanged "
        "portfolio produces zero incremental benefit."
    )

    print(
        "Switching costs have not yet been deducted. "
        "No rebalance recommendation is made by this "
        "layer."
    )


if __name__ == "__main__":
    main()