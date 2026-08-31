from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_DIR),
    )


from treasury_intelligence.analytics.universe_candidates import (
    build_model_company_opportunity_universe,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)


POSITION_SIZES_EUR = (
    100_000.0,
    500_000.0,
    1_000_000.0,
    2_000_000.0,
    5_000_000.0,
)


def short_status(
    candidate: PortfolioCandidateAssessment,
) -> str:
    if candidate.recommendation_ready:
        return "READY"

    if candidate.candidate_status == "blocked":
        return "BLOCK"

    if candidate.candidate_status == "needs_evidence":
        return "EVID"

    return candidate.candidate_status.upper()


def format_return(
    candidate: PortfolioCandidateAssessment,
) -> str:
    if candidate.defensible_return_pct is None:
        return "-"

    return (
        f"{candidate.defensible_return_pct:.3f}%"
    )


def build_matrix_candidates():
    opportunities = (
        build_model_company_opportunity_universe()
    )

    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ] = {}

    for opportunity in opportunities:
        candidates_by_opportunity[
            opportunity.key
        ] = [
            opportunity.candidate_builder(
                position_size_eur,
                MODEL_COMPANY_MANDATE,
            )
            for position_size_eur in POSITION_SIZES_EUR
        ]

    return (
        opportunities,
        candidates_by_opportunity,
    )


def print_matrix(
    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ],
    opportunities,
) -> None:
    print()
    print("V1 UNIVERSE POSITION MATRIX")
    print("=" * 118)

    header = (
        f"{'Opportunity':<20}"
        f"{'EUR 100k':>18}"
        f"{'EUR 500k':>18}"
        f"{'EUR 1m':>18}"
        f"{'EUR 2m':>18}"
        f"{'EUR 5m':>18}"
    )

    print(header)
    print("-" * 118)

    for opportunity in opportunities:
        candidates = (
            candidates_by_opportunity[
                opportunity.key
            ]
        )

        cells = []

        for candidate in candidates:
            cells.append(
                f"{short_status(candidate)} "
                f"{format_return(candidate)}"
            )

        print(
            f"{opportunity.label:<20}"
            f"{cells[0]:>18}"
            f"{cells[1]:>18}"
            f"{cells[2]:>18}"
            f"{cells[3]:>18}"
            f"{cells[4]:>18}"
        )

    print("=" * 118)


def print_detail(
    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ],
    opportunities,
) -> None:
    print()
    print("POSITION-SIZE DETAIL")
    print("=" * 118)

    for opportunity in opportunities:
        print()
        print(opportunity.label)
        print("-" * 118)

        for candidate in (
            candidates_by_opportunity[
                opportunity.key
            ]
        ):
            print(
                f"EUR {candidate.position_size_eur:>11,.0f}"
                f" | eligibility: "
                f"{candidate.eligibility_status:<14}"
                f" | liquidity: "
                f"{candidate.liquidity_position_status:<13}"
                f" | economics: "
                f"{candidate.economics_status:<10}"
                f" | return: "
                f"{format_return(candidate):>7}"
                f" | status: "
                f"{candidate.candidate_status:<20}"
                f" | ready: "
                f"{candidate.recommendation_ready}"
            )


def print_evidence_summary(
    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ],
    opportunities,
) -> None:
    print()
    print("EVIDENCE / BLOCKER SUMMARY AT EUR 5M")
    print("=" * 118)

    for opportunity in opportunities:
        candidate = (
            candidates_by_opportunity[
                opportunity.key
            ][-1]
        )

        print()
        print(
            f"{opportunity.label} "
            f"- EUR {candidate.position_size_eur:,.0f}"
        )

        print(
            f"Candidate status: "
            f"{candidate.candidate_status}"
        )

        print(
            f"Unknown base risk dimensions: "
            f"{candidate.base_risk_unknown_dimension_count}"
        )

        print(
            f"Evidence requirements: "
            f"{len(candidate.evidence_requirements)}"
        )

        if candidate.evidence_requirements:
            for requirement in (
                candidate.evidence_requirements
            ):
                print(
                    f"  EVIDENCE: {requirement}"
                )

        print(
            f"Blocking reasons: "
            f"{len(candidate.blocking_reasons)}"
        )

        if candidate.blocking_reasons:
            for blocker in candidate.blocking_reasons:
                print(
                    f"  BLOCKER: {blocker}"
                )


def print_summary(
    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ],
    opportunities,
) -> None:
    all_candidates = tuple(
        candidate
        for opportunity in opportunities
        for candidate in (
            candidates_by_opportunity[
                opportunity.key
            ]
        )
    )

    ready = sum(
        1
        for candidate in all_candidates
        if candidate.recommendation_ready
    )

    needs_evidence = sum(
        1
        for candidate in all_candidates
        if (
            candidate.candidate_status
            == "needs_evidence"
        )
    )

    blocked = sum(
        1
        for candidate in all_candidates
        if candidate.candidate_status == "blocked"
    )

    print()
    print("SUMMARY")
    print("=" * 118)

    print(
        "Opportunity count:",
        len(opportunities),
    )

    print(
        "Position analyses:",
        len(all_candidates),
    )

    print(
        "Recommendation-ready:",
        ready,
    )

    print(
        "Needs evidence:",
        needs_evidence,
    )

    print(
        "Blocked:",
        blocked,
    )


def main() -> None:
    (
        opportunities,
        candidates_by_opportunity,
    ) = build_matrix_candidates()

    print_matrix(
        candidates_by_opportunity=(
            candidates_by_opportunity
        ),
        opportunities=opportunities,
    )

    print_detail(
        candidates_by_opportunity=(
            candidates_by_opportunity
        ),
        opportunities=opportunities,
    )

    print_evidence_summary(
        candidates_by_opportunity=(
            candidates_by_opportunity
        ),
        opportunities=opportunities,
    )

    print_summary(
        candidates_by_opportunity=(
            candidates_by_opportunity
        ),
        opportunities=opportunities,
    )


if __name__ == "__main__":
    main()