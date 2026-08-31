from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from treasury_intelligence.analytics.portfolio_construction import (
    build_portfolio_construction,
)

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.portfolio_construction import (
    AllocationInstruction,
    PortfolioConstructionAssessment,
)


CandidateBuilder = Callable[
    [
        float,
        TreasuryMandate,
    ],
    PortfolioCandidateAssessment,
]


@dataclass(frozen=True)
class AllocationOpportunity:
    key: str
    label: str
    candidate_builder: CandidateBuilder

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError(
                "Allocation opportunity key is required."
            )

        if not self.label:
            raise ValueError(
                "Allocation opportunity label is required."
            )


def _validate_opportunities(
    opportunities: tuple[
        AllocationOpportunity,
        ...
    ],
) -> None:
    seen_keys = set()

    for opportunity in opportunities:
        if opportunity.key in seen_keys:
            raise ValueError(
                "Duplicate allocation opportunity key: "
                f"{opportunity.key}"
            )

        seen_keys.add(
            opportunity.key
        )


def _maximum_position_eur(
    mandate: TreasuryMandate,
) -> float:
    if (
        mandate.maximum_single_position_pct
        <= 0
    ):
        raise ValueError(
            "maximum_single_position_pct must be "
            "greater than zero."
        )

    if (
        mandate.maximum_single_position_pct
        > 100
    ):
        raise ValueError(
            "maximum_single_position_pct cannot "
            "exceed 100."
        )

    return (
        mandate.treasury_capital_eur
        * mandate.maximum_single_position_pct
        / 100
    )


def _build_candidates_for_size(
    opportunities: tuple[
        AllocationOpportunity,
        ...
    ],
    position_size_eur: float,
    mandate: TreasuryMandate,
) -> tuple[
    tuple[
        AllocationOpportunity,
        PortfolioCandidateAssessment,
    ],
    ...
]:
    results = []

    for opportunity in opportunities:
        candidate = (
            opportunity.candidate_builder(
                position_size_eur,
                mandate,
            )
        )

        if (
            abs(
                candidate.position_size_eur
                - position_size_eur
            )
            > 0.01
        ):
            raise ValueError(
                f"{opportunity.label}: candidate builder "
                "returned a different position size than "
                "the allocator requested."
            )

        if (
            candidate.mandate_id
            != mandate.mandate_id
        ):
            raise ValueError(
                f"{opportunity.label}: candidate mandate "
                "does not match allocation mandate."
            )

        results.append(
            (
                opportunity,
                candidate,
            )
        )

    return tuple(
        results
    )


def _select_best_candidate(
    candidates: tuple[
        tuple[
            AllocationOpportunity,
            PortfolioCandidateAssessment,
        ],
        ...
    ],
) -> tuple[
    AllocationOpportunity,
    PortfolioCandidateAssessment,
] | None:
    eligible = tuple(
        (
            opportunity,
            candidate,
        )
        for opportunity, candidate in candidates
        if (
            candidate.recommendation_ready
            and candidate.defensible_return_pct
            is not None
        )
    )

    if not eligible:
        return None

    return max(
        eligible,
        key=lambda item: (
            item[1].defensible_return_pct,
            item[0].key,
        ),
    )


def build_return_priority_portfolio_construction(
    *,
    construction_id: str,
    mandate: TreasuryMandate,
    opportunities: tuple[
        AllocationOpportunity,
        ...
    ],
    notes: str | None = None,
) -> tuple[
    PortfolioConstructionAssessment,
    tuple[
        PortfolioCandidateAssessment,
        ...
    ],
]:
    if not construction_id:
        raise ValueError(
            "construction_id is required."
        )

    if mandate.treasury_capital_eur <= 0:
        raise ValueError(
            "Treasury capital must be greater than zero."
        )

    _validate_opportunities(
        opportunities
    )

    if not opportunities:
        construction = (
            build_portfolio_construction(
                construction_id=construction_id,
                mandate=mandate,
                candidates=(),
                instructions=(),
                notes=(
                    notes
                    or (
                        "No allocation opportunities were "
                        "supplied."
                    )
                ),
            )
        )

        return (
            construction,
            (),
        )

    maximum_position_eur = (
        _maximum_position_eur(
            mandate
        )
    )

    remaining_capital_eur = (
        mandate.treasury_capital_eur
    )

    remaining_opportunities = list(
        opportunities
    )

    selected_candidates = []
    instructions = []

    while (
        remaining_capital_eur
        >= mandate.minimum_useful_allocation_eur
        and remaining_opportunities
    ):
        requested_position_eur = min(
            maximum_position_eur,
            remaining_capital_eur,
        )

        if (
            requested_position_eur
            < mandate.minimum_useful_allocation_eur
        ):
            break

        analyzed = (
            _build_candidates_for_size(
                opportunities=tuple(
                    remaining_opportunities
                ),
                position_size_eur=(
                    requested_position_eur
                ),
                mandate=mandate,
            )
        )

        selected = (
            _select_best_candidate(
                analyzed
            )
        )

        if selected is None:
            break

        (
            selected_opportunity,
            selected_candidate,
        ) = selected

        selected_candidates.append(
            selected_candidate
        )

        instructions.append(
            AllocationInstruction(
                candidate_assessment_id=(
                    selected_candidate.assessment_id
                ),
                allocation_eur=(
                    selected_candidate.position_size_eur
                ),
            )
        )

        remaining_capital_eur -= (
            selected_candidate.position_size_eur
        )

        remaining_opportunities = [
            opportunity
            for opportunity
            in remaining_opportunities
            if (
                opportunity.key
                != selected_opportunity.key
            )
        ]

    construction = (
        build_portfolio_construction(
            construction_id=construction_id,
            mandate=mandate,
            candidates=tuple(
                selected_candidates
            ),
            instructions=tuple(
                instructions
            ),
            notes=(
                notes
                or (
                    "Capital is allocated only to "
                    "recommendation-ready candidates at "
                    "their exact analyzed position sizes. "
                    "Among candidates satisfying upstream "
                    "constraints, allocation priority is "
                    "highest defensible return. No "
                    "diversification constraint is imposed "
                    "beyond the treasury mandate's explicit "
                    "maximum single-position limit."
                )
            ),
        )
    )

    return (
        construction,
        tuple(
            selected_candidates
        ),
    )