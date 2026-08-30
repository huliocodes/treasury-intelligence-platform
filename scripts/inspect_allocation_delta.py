from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.allocation_deltas import (
    build_treasury_allocation_delta,
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
        defensible_return_pct=2.500,
        defensible_return_measure=(
            "Deterministic 7C.2 fixture."
        ),
        candidate_status=(
            "recommendation_ready"
        ),
        blocking_reasons=(),
        evidence_requirements=(),
        recommendation_ready=True,
        notes=(
            "Deterministic recommendation-ready "
            "candidate used to validate allocation "
            "delta mechanics."
        ),
    )


def build_non_ready_candidate(
) -> PortfolioCandidateAssessment:
    return PortfolioCandidateAssessment(
        assessment_id=(
            "fixture_non_ready_delta"
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
            "Deterministic 7C.2 fixture."
        ),
        candidate_status="needs_evidence",
        blocking_reasons=(),
        evidence_requirements=(
            "Additional evidence required.",
        ),
        recommendation_ready=False,
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


def print_delta(
    label: str,
    delta,
) -> None:
    print(label)
    print()

    print(
        f"Current invested:             "
        f"EUR "
        f"{delta.current_invested_capital_eur:,.0f}"
    )

    print(
        f"Proposed invested:            "
        f"EUR "
        f"{delta.proposed_invested_capital_eur:,.0f}"
    )

    print(
        f"Current unallocated:          "
        f"EUR "
        f"{delta.current_unallocated_capital_eur:,.0f}"
    )

    print(
        f"Proposed unallocated:         "
        f"EUR "
        f"{delta.proposed_unallocated_capital_eur:,.0f}"
    )

    print(
        f"Gross position movement:      "
        f"EUR "
        f"{delta.gross_position_movement_eur:,.0f}"
    )

    print(
        f"Change required:              "
        f"{delta.change_required}"
    )

    if delta.delta_lines:
        print()
        print("POSITION DELTAS")
        print()

        for line in delta.delta_lines:
            print(
                f"  {line.label:<20} "
                f"{line.action:<10} | "
                f"current EUR "
                f"{line.current_value_eur:>10,.0f} | "
                f"proposed EUR "
                f"{line.proposed_value_eur:>10,.0f} | "
                f"delta EUR "
                f"{line.delta_eur:>+10,.0f}"
            )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print("CURRENT VS PROPOSED ALLOCATION DELTA")
    print()

    print(
        "The allocation-delta layer compares the "
        "current treasury state with an explicit "
        "portfolio proposal. It calculates capital "
        "movement but makes no rebalance decision."
    )

    print()
    print("-" * 100)
    print()

    current_position = TreasuryPosition(
        position_id=(
            "fixture_existing_hold"
        ),
        instrument_id="instrument_a",
        market_id="market_a",
        access_route_id="access_a",
        label="POSITION A",
        current_value_eur=1_000_000,
    )

    current_state = (
        build_treasury_state(
            state_id=(
                "fixture_existing_state"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(
                current_position,
            ),
        )
    )

    non_ready_candidate = (
        build_non_ready_candidate()
    )

    no_actionable_proposal = (
        build_proposal(
            case_id="no_actionable",
            candidates=(
                non_ready_candidate,
            ),
            instructions=(),
        )
    )

    no_action_delta = (
        build_treasury_allocation_delta(
            delta_id=(
                "delta_no_actionable"
            ),
            state=current_state,
            proposal=(
                no_actionable_proposal
            ),
        )
    )

    print_delta(
        label=(
            "CASE 1 — NO ACTIONABLE PROPOSAL "
            "RETAINS CURRENT STATE"
        ),
        delta=no_action_delta,
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

    new_candidate = (
        build_ready_candidate(
            assessment_id=(
                "fixture_new_500k"
            ),
            instrument_id="instrument_b",
            market_id="market_b",
            access_route_id="access_b",
            label="POSITION B",
            position_size_eur=500_000,
        )
    )

    new_proposal = (
        build_proposal(
            case_id="new_position",
            candidates=(
                new_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        new_candidate.assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    open_delta = (
        build_treasury_allocation_delta(
            delta_id=(
                "delta_open_position"
            ),
            state=(
                fully_unallocated_state
            ),
            proposal=new_proposal,
        )
    )

    print_delta(
        label=(
            "CASE 2 — OPEN NEW EUR 500K POSITION"
        ),
        delta=open_delta,
    )

    current_a = TreasuryPosition(
        position_id=(
            "fixture_current_a_1m"
        ),
        instrument_id="instrument_a",
        market_id="market_a",
        access_route_id="access_a",
        label="POSITION A",
        current_value_eur=1_000_000,
    )

    state_a_1m = (
        build_treasury_state(
            state_id=(
                "fixture_state_a_1m"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(
                current_a,
            ),
        )
    )

    reduced_a_candidate = (
        build_ready_candidate(
            assessment_id=(
                "fixture_a_target_500k"
            ),
            instrument_id="instrument_a",
            market_id="market_a",
            access_route_id="access_a",
            label="POSITION A",
            position_size_eur=500_000,
        )
    )

    reduced_a_proposal = (
        build_proposal(
            case_id="reduce_a",
            candidates=(
                reduced_a_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        reduced_a_candidate.assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    decrease_delta = (
        build_treasury_allocation_delta(
            delta_id=(
                "delta_decrease_a"
            ),
            state=state_a_1m,
            proposal=reduced_a_proposal,
        )
    )

    print_delta(
        label=(
            "CASE 3 — REDUCE EXISTING POSITION"
        ),
        delta=decrease_delta,
    )

    current_rotation_position = TreasuryPosition(
        position_id=(
            "fixture_rotation_a"
        ),
        instrument_id="instrument_a",
        market_id="market_a",
        access_route_id="access_a",
        label="POSITION A",
        current_value_eur=500_000,
    )

    rotation_state = (
        build_treasury_state(
            state_id=(
                "fixture_rotation_state"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
            positions=(
                current_rotation_position,
            ),
        )
    )

    rotation_candidate = (
        build_ready_candidate(
            assessment_id=(
                "fixture_rotation_b"
            ),
            instrument_id="instrument_b",
            market_id="market_b",
            access_route_id="access_b",
            label="POSITION B",
            position_size_eur=500_000,
        )
    )

    rotation_proposal = (
        build_proposal(
            case_id="rotate_a_to_b",
            candidates=(
                rotation_candidate,
            ),
            instructions=(
                AllocationInstruction(
                    candidate_assessment_id=(
                        rotation_candidate.assessment_id
                    ),
                    allocation_eur=500_000,
                ),
            ),
        )
    )

    rotation_delta = (
        build_treasury_allocation_delta(
            delta_id=(
                "delta_rotate_a_to_b"
            ),
            state=rotation_state,
            proposal=rotation_proposal,
        )
    )

    print_delta(
        label=(
            "CASE 4 — ROTATE EUR 500K "
            "FROM POSITION A TO POSITION B"
        ),
        delta=rotation_delta,
    )

    print("INTERPRETATION")
    print()

    print(
        "Case 1 proves that the absence of an "
        "actionable proposal does not liquidate "
        "existing treasury positions."
    )

    print(
        "Case 2 identifies a EUR 500,000 new position "
        "funded from currently unallocated treasury "
        "capital."
    )

    print(
        "Case 3 identifies a EUR 500,000 reduction "
        "in an existing position."
    )

    print(
        "Case 4 identifies both sides of a rotation: "
        "EUR 500,000 must leave Position A and "
        "EUR 500,000 must enter Position B."
    )

    print(
        "Gross position movement is transaction notional "
        "across investment positions. The EUR 500,000 "
        "rotation therefore creates EUR 1,000,000 of "
        "gross position movement."
    )

    print(
        "No judgment has yet been made about whether "
        "any of these changes are economically worth "
        "executing."
    )


if __name__ == "__main__":
    main()