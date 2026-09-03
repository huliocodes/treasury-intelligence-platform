from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.recommendation_candidates import (
    build_btf_2027_08_11_recommendation_candidate,
)

from treasury_intelligence.analytics.review_returns import (
    build_candidate_embedded_switching_friction_input,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)


POSITION_SIZE_EUR = 5_000_000.0


def build_fixture_without_provenance():
    return PortfolioCandidateAssessment(
        assessment_id=(
            "recommendation_ready_without_provenance"
        ),
        mandate_id=MODEL_COMPANY_MANDATE.mandate_id,
        instrument_id="fixture_instrument",
        market_id="fixture_market",
        access_route_id="fixture_access",
        label="FIXTURE WITHOUT PROVENANCE",
        position_size_eur=POSITION_SIZE_EUR,
        eligibility_status="eligible",
        liquidity_position_status="supported",
        economics_status="complete",
        base_risk_unknown_dimension_count=0,
        defensible_return_pct=2.5,
        defensible_return_measure=(
            "Deterministic fixture return."
        ),
        candidate_status="recommendation_ready",
        blocking_reasons=(),
        evidence_requirements=(),
        recommendation_ready=True,
        notes=(
            "Recommendation-ready fixture deliberately "
            "contains no embedded entry-cost provenance."
        ),
    )


def main() -> None:
    print("MILESTONE 15D — COST-INCLUSION PROVENANCE")
    print()

    candidate = (
        build_btf_2027_08_11_recommendation_candidate(
            position_size_eur=POSITION_SIZE_EUR,
        )
    )

    friction_input = (
        build_candidate_embedded_switching_friction_input(
            candidate=candidate,
            action="open",
        )
    )

    print("CASE 1 — PRODUCTION FRENCH BTF AUG 2027")
    print()

    print(
        f"Candidate status:              "
        f"{candidate.candidate_status}"
    )

    print(
        f"Defensible return:             "
        f"{candidate.defensible_return_pct:.3f}%"
    )

    print(
        "Embedded one-time costs:       "
        + ", ".join(
            candidate
            .embedded_one_time_cost_component_types
        )
    )

    print(
        f"Additional friction evidence:  "
        f"{friction_input.evidence_available}"
    )

    print(
        f"Additional friction bps:       "
        f"{friction_input.friction_bps:.3f}"
    )

    print(
        f"Additional fixed cost:         "
        f"EUR {friction_input.fixed_cost_eur:,.2f}"
    )

    assert candidate.recommendation_ready

    assert candidate.economics_status == "complete"

    assert (
        candidate.defensible_return_pct
        is not None
    )

    assert (
        "entry_execution_cost"
        in candidate.embedded_one_time_cost_component_types
    )

    assert (
        "exit_execution_cost"
        in candidate.embedded_one_time_cost_component_types
    )

    assert (
        "slippage_price_impact"
        in candidate.embedded_one_time_cost_component_types
    )

    assert friction_input.evidence_available

    assert friction_input.friction_bps == 0.0

    assert friction_input.fixed_cost_eur == 0.0

    print()
    print("-" * 100)
    print()
    print("CASE 2 — NO EMBEDDED ENTRY-COST PROVENANCE")
    print()

    fixture = build_fixture_without_provenance()

    fixture_friction = (
        build_candidate_embedded_switching_friction_input(
            candidate=fixture,
            action="open",
        )
    )

    print(
        f"Candidate status:              "
        f"{fixture.candidate_status}"
    )

    print(
        f"Embedded one-time costs:       "
        f"{fixture.embedded_one_time_cost_component_types}"
    )

    print(
        f"Additional friction evidence:  "
        f"{fixture_friction.evidence_available}"
    )

    assert fixture.recommendation_ready

    assert (
        fixture.embedded_one_time_cost_component_types
        == ()
    )

    assert (
        fixture_friction.evidence_available
        is False
    )

    assert fixture_friction.friction_bps is None

    assert fixture_friction.fixed_cost_eur is None

    print()
    print("-" * 100)
    print()
    print("CASE 3 — UNSUPPORTED CLOSE ACTION")
    print()

    close_rejected = False

    try:
        build_candidate_embedded_switching_friction_input(
            candidate=candidate,
            action="close",
        )
    except ValueError:
        close_rejected = True

    print(
        f"Close action rejected:         "
        f"{close_rejected}"
    )

    assert close_rejected

    print()
    print(
        "All Milestone 15D cost-inclusion provenance "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
