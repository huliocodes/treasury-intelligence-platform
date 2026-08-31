from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.analytics.allocation_selection import (
    AllocationOpportunity,
    build_return_priority_portfolio_construction,
)

from treasury_intelligence.analytics.portfolio_comparisons import (
    build_portfolio_alternative_comparison,
)

from treasury_intelligence.analytics.recommendation_candidates import (
    build_btf_recommendation_candidate,
    build_bubill_recommendation_candidate,
    build_ernx_recommendation_candidate,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
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


def build_construction(
    *,
    construction_id: str,
    maximum_single_position_pct: float,
):
    mandate = replace(
        MODEL_COMPANY_MANDATE,
        maximum_single_position_pct=(
            maximum_single_position_pct
        ),
    )

    return (
        build_return_priority_portfolio_construction(
            construction_id=construction_id,
            mandate=mandate,
            opportunities=OPPORTUNITIES,
        )
    )


def print_side(
    label: str,
    side,
) -> None:
    print(label)
    print(
        "  Construction:",
        side.construction_id,
    )
    print(
        "  Positions:",
        side.position_count,
    )
    print(
        "  Largest position:",
        f"{side.largest_position_pct:.2f}%",
    )
    print(
        "  Annual return:",
        f"{side.annual_return_pct:.3f}%",
    )
    print(
        "  Annual return EUR:",
        f"EUR {side.annual_return_eur:,.0f}",
    )


selected_construction, selected_candidates = (
    build_construction(
        construction_id="selected_100pct",
        maximum_single_position_pct=100.0,
    )
)

alternative_50_construction, alternative_50_candidates = (
    build_construction(
        construction_id="alternative_50pct",
        maximum_single_position_pct=50.0,
    )
)

alternative_40_construction, alternative_40_candidates = (
    build_construction(
        construction_id="alternative_40pct",
        maximum_single_position_pct=40.0,
    )
)


comparison_50 = (
    build_portfolio_alternative_comparison(
        comparison_id="selected_vs_50pct",
        selected_construction=(
            selected_construction
        ),
        selected_candidates=(
            selected_candidates
        ),
        alternative_construction=(
            alternative_50_construction
        ),
        alternative_candidates=(
            alternative_50_candidates
        ),
        notes=(
            "Diagnostic comparison only. A 50% "
            "single-position limit is not asserted to "
            "be the correct production treasury policy."
        ),
    )
)

comparison_40 = (
    build_portfolio_alternative_comparison(
        comparison_id="selected_vs_40pct",
        selected_construction=(
            selected_construction
        ),
        selected_candidates=(
            selected_candidates
        ),
        alternative_construction=(
            alternative_40_construction
        ),
        alternative_candidates=(
            alternative_40_candidates
        ),
        notes=(
            "Diagnostic comparison only. A 40% "
            "single-position limit is not asserted to "
            "be the correct production treasury policy."
        ),
    )
)


print("===== SELECTED VS 50% ALTERNATIVE =====")
print()

print_side(
    "SELECTED",
    comparison_50.selected,
)

print()

print_side(
    "ALTERNATIVE",
    comparison_50.alternative,
)

print()

print(
    "Selected return advantage:",
    f"{comparison_50.return_difference_bps:.2f} bps",
)

print(
    "Selected annual EUR advantage:",
    (
        "EUR "
        f"{comparison_50.annual_return_difference_eur:,.0f}"
    ),
)

print(
    "Position-count difference:",
    comparison_50.position_count_difference,
)

print(
    "Largest-position difference:",
    (
        f"{comparison_50.largest_position_pct_difference:.2f}"
        " percentage points"
    ),
)

print()
print("===== SELECTED VS 40% ALTERNATIVE =====")
print()

print_side(
    "SELECTED",
    comparison_40.selected,
)

print()

print_side(
    "ALTERNATIVE",
    comparison_40.alternative,
)

print()

print(
    "Selected return advantage:",
    f"{comparison_40.return_difference_bps:.2f} bps",
)

print(
    "Selected annual EUR advantage:",
    (
        "EUR "
        f"{comparison_40.annual_return_difference_eur:,.0f}"
    ),
)

print(
    "Position-count difference:",
    comparison_40.position_count_difference,
)

print(
    "Largest-position difference:",
    (
        f"{comparison_40.largest_position_pct_difference:.2f}"
        " percentage points"
    ),
)