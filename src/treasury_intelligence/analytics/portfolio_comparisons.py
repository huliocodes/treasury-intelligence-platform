from __future__ import annotations

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.portfolio_comparisons import (
    PortfolioAlternativeComparison,
    PortfolioComparisonSide,
)

from treasury_intelligence.models.portfolio_construction import (
    PortfolioConstructionAssessment,
)


CAPITAL_TOLERANCE_EUR = 0.01


def _index_candidates(
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> dict[
    str,
    PortfolioCandidateAssessment,
]:
    indexed = {}

    for candidate in candidates:
        if candidate.assessment_id in indexed:
            raise ValueError(
                "Duplicate portfolio candidate assessment ID: "
                f"{candidate.assessment_id}"
            )

        indexed[
            candidate.assessment_id
        ] = candidate

    return indexed


def _validate_construction(
    construction: PortfolioConstructionAssessment,
) -> None:
    if (
        construction.construction_status
        != "valid_allocation"
    ):
        raise ValueError(
            "Portfolio comparison requires a valid "
            "portfolio construction."
        )

    if construction.allocated_capital_eur <= 0:
        raise ValueError(
            "Portfolio comparison requires positive "
            "allocated capital."
        )

    if not construction.allocation_lines:
        raise ValueError(
            "Portfolio comparison requires at least one "
            "allocation line."
        )


def _build_comparison_side(
    construction: PortfolioConstructionAssessment,
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> PortfolioComparisonSide:
    _validate_construction(
        construction
    )

    indexed_candidates = (
        _index_candidates(
            candidates
        )
    )

    annual_return_eur = 0.0

    for line in construction.allocation_lines:
        candidate = indexed_candidates.get(
            line.candidate_assessment_id
        )

        if candidate is None:
            raise ValueError(
                "Portfolio allocation line references "
                "a candidate not supplied to the "
                "comparison."
            )

        if (
            candidate.mandate_id
            != construction.mandate_id
        ):
            raise ValueError(
                "Portfolio candidate mandate does not "
                "match portfolio construction mandate."
            )

        if not candidate.recommendation_ready:
            raise ValueError(
                f"{candidate.label}: comparison cannot "
                "use a candidate that is not "
                "recommendation-ready."
            )

        if candidate.defensible_return_pct is None:
            raise ValueError(
                f"{candidate.label}: comparison requires "
                "a defensible return."
            )

        if (
            abs(
                candidate.position_size_eur
                - line.allocation_eur
            )
            > CAPITAL_TOLERANCE_EUR
        ):
            raise ValueError(
                f"{candidate.label}: allocation does not "
                "match the candidate's analyzed position "
                "size."
            )

        annual_return_eur += (
            line.allocation_eur
            * candidate.defensible_return_pct
            / 100.0
        )

    annual_return_pct = (
        annual_return_eur
        / construction.allocated_capital_eur
        * 100.0
    )

    largest_position_pct = max(
        line.allocation_pct_of_treasury
        for line in construction.allocation_lines
    )

    return PortfolioComparisonSide(
        construction_id=(
            construction.construction_id
        ),
        allocated_capital_eur=(
            construction.allocated_capital_eur
        ),
        unallocated_capital_eur=(
            construction.unallocated_capital_eur
        ),
        position_count=len(
            construction.allocation_lines
        ),
        largest_position_pct=(
            largest_position_pct
        ),
        annual_return_pct=(
            annual_return_pct
        ),
        annual_return_eur=(
            annual_return_eur
        ),
    )


def build_portfolio_alternative_comparison(
    *,
    comparison_id: str,
    selected_construction: (
        PortfolioConstructionAssessment
    ),
    selected_candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
    alternative_construction: (
        PortfolioConstructionAssessment
    ),
    alternative_candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
    notes: str | None = None,
) -> PortfolioAlternativeComparison:
    if not comparison_id:
        raise ValueError(
            "comparison_id is required."
        )

    if (
        selected_construction.mandate_id
        != alternative_construction.mandate_id
    ):
        raise ValueError(
            "Selected and alternative constructions must "
            "use the same mandate."
        )

    if (
        abs(
            selected_construction.treasury_capital_eur
            - alternative_construction.treasury_capital_eur
        )
        > CAPITAL_TOLERANCE_EUR
    ):
        raise ValueError(
            "Selected and alternative constructions must "
            "use the same treasury capital."
        )

    selected = _build_comparison_side(
        construction=selected_construction,
        candidates=selected_candidates,
    )

    alternative = _build_comparison_side(
        construction=alternative_construction,
        candidates=alternative_candidates,
    )

    return_difference_pct = (
        selected.annual_return_pct
        - alternative.annual_return_pct
    )

    return PortfolioAlternativeComparison(
        comparison_id=comparison_id,
        mandate_id=(
            selected_construction.mandate_id
        ),
        treasury_capital_eur=(
            selected_construction.treasury_capital_eur
        ),
        selected=selected,
        alternative=alternative,
        return_difference_bps=(
            return_difference_pct * 100.0
        ),
        annual_return_difference_eur=(
            selected.annual_return_eur
            - alternative.annual_return_eur
        ),
        position_count_difference=(
            selected.position_count
            - alternative.position_count
        ),
        largest_position_pct_difference=(
            selected.largest_position_pct
            - alternative.largest_position_pct
        ),
        notes=notes,
    )