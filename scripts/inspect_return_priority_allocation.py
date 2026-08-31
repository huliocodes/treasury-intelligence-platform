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


from treasury_intelligence.analytics.allocation_selection import (
    AllocationOpportunity,
    build_return_priority_portfolio_construction,
)

from treasury_intelligence.analytics.recommendation_candidates import (
    build_btf_recommendation_candidate,
    build_bubill_recommendation_candidate,
    build_ernx_recommendation_candidate,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)


def main() -> None:
    opportunities = (
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

    (
        construction,
        selected_candidates,
    ) = (
        build_return_priority_portfolio_construction(
            construction_id=(
                "model_company_return_priority_v1"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            opportunities=opportunities,
        )
    )

    candidate_by_id = {
        candidate.assessment_id: candidate
        for candidate in selected_candidates
    }

    print()
    print(
        "RETURN-PRIORITY PORTFOLIO CONSTRUCTION"
    )
    print("=" * 90)
    print()

    print(
        "Treasury capital:",
        f"EUR "
        f"{construction.treasury_capital_eur:,.0f}",
    )

    print(
        "Mandate max single position:",
        f"{MODEL_COMPANY_MANDATE.maximum_single_position_pct:.2f}%",
    )

    print(
        "Minimum useful allocation:",
        f"EUR "
        f"{MODEL_COMPANY_MANDATE.minimum_useful_allocation_eur:,.0f}",
    )

    print(
        "Target yield:",
        (
            f"{MODEL_COMPANY_MANDATE.target_yield_pct:.3f}%"
            if MODEL_COMPANY_MANDATE.target_yield_pct
            is not None
            else None
        ),
    )

    print(
        "Target is hard constraint:",
        MODEL_COMPANY_MANDATE.target_yield_is_hard_constraint,
    )

    print()

    print(
        "Construction status:",
        construction.construction_status,
    )

    print(
        "Allocated capital:",
        f"EUR "
        f"{construction.allocated_capital_eur:,.0f}",
    )

    print(
        "Unallocated capital:",
        f"EUR "
        f"{construction.unallocated_capital_eur:,.0f}",
    )

    print()

    print("ALLOCATIONS")
    print("-" * 90)

    weighted_return_numerator = 0.0

    for line in construction.allocation_lines:
        candidate = candidate_by_id[
            line.candidate_assessment_id
        ]

        return_pct = (
            candidate.defensible_return_pct
        )

        if return_pct is None:
            raise ValueError(
                "Selected allocation has no "
                "defensible return."
            )

        weighted_return_numerator += (
            line.allocation_eur
            * return_pct
        )

        print(
            f"{line.label:<20}"
            f"EUR {line.allocation_eur:>14,.0f}"
            f"  "
            f"{line.allocation_pct_of_treasury:>7.2f}%"
            f"  "
            f"{return_pct:>7.3f}%"
        )

    print()

    if construction.allocated_capital_eur > 0:
        portfolio_return_pct = (
            weighted_return_numerator
            / construction.allocated_capital_eur
        )
    else:
        portfolio_return_pct = None

    print(
        "Portfolio defensible return:",
        (
            f"{portfolio_return_pct:.3f}%"
            if portfolio_return_pct is not None
            else None
        ),
    )

    if (
        portfolio_return_pct is not None
        and MODEL_COMPANY_MANDATE.target_yield_pct
        is not None
    ):
        target_gap_pct = (
            MODEL_COMPANY_MANDATE.target_yield_pct
            - portfolio_return_pct
        )

        print(
            "Target yield gap:",
            f"{target_gap_pct:.3f} percentage points",
        )

    print()

    print("SELECTED CANDIDATE CHECK")
    print("-" * 90)

    for candidate in selected_candidates:
        print(
            f"{candidate.label:<20}"
            f"EUR {candidate.position_size_eur:>14,.0f}"
            f"  "
            f"{candidate.candidate_status:<22}"
            f"  "
            f"{candidate.defensible_return_pct:.3f}%"
        )

    print()
    print("INTERPRETATION")
    print("-" * 90)
    print()

    print(
        "This construction does not invent a "
        "diversification requirement."
    )

    print(
        "It applies the explicit treasury mandate, "
        "requires exact position-size upstream analysis, "
        "and prioritizes the highest defensible return "
        "among recommendation-ready opportunities."
    )

    print()

    if len(construction.allocation_lines) == 1:
        print(
            "The current mandate permits the resulting "
            "single-position portfolio. A diversified "
            "portfolio would require an explicit "
            "concentration or diversification policy "
            "rather than a hidden allocator preference."
        )


if __name__ == "__main__":
    main()