from __future__ import annotations

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.portfolio_construction import (
    AllocationInstruction,
    PortfolioAllocationLine,
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


def _count_recommendation_ready(
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> int:
    return sum(
        1
        for candidate in candidates
        if candidate.recommendation_ready
    )


def _validate_instruction_candidate(
    mandate: TreasuryMandate,
    candidate: PortfolioCandidateAssessment,
    instruction: AllocationInstruction,
) -> tuple[str, ...]:
    issues = []

    if not candidate.recommendation_ready:
        issues.append(
            (
                f"{candidate.label}: candidate "
                "is not recommendation-ready and "
                "cannot receive an allocation."
            )
        )

    if (
        abs(
            instruction.allocation_eur
            - candidate.position_size_eur
        )
        > CAPITAL_TOLERANCE_EUR
    ):
        issues.append(
            (
                f"{candidate.label}: requested allocation "
                f"EUR {instruction.allocation_eur:,.2f} "
                "does not match the analyzed candidate "
                f"position size of "
                f"EUR {candidate.position_size_eur:,.2f}. "
                "A different position size requires a new "
                "upstream position analysis."
            )
        )

    if (
        instruction.allocation_eur
        < mandate.minimum_useful_allocation_eur
    ):
        issues.append(
            (
                f"{candidate.label}: allocation "
                f"EUR {instruction.allocation_eur:,.2f} "
                "is below the mandate minimum useful "
                f"allocation of "
                f"EUR "
                f"{mandate.minimum_useful_allocation_eur:,.2f}."
            )
        )

    allocation_pct = (
        instruction.allocation_eur
        / mandate.treasury_capital_eur
        * 100
    )

    if (
        allocation_pct
        > mandate.maximum_single_position_pct
    ):
        issues.append(
            (
                f"{candidate.label}: allocation represents "
                f"{allocation_pct:.2f}% of treasury capital, "
                "above the mandate maximum single-position "
                f"allocation of "
                f"{mandate.maximum_single_position_pct:.2f}%."
            )
        )

    return tuple(issues)


def _build_allocation_line(
    mandate: TreasuryMandate,
    candidate: PortfolioCandidateAssessment,
    instruction: AllocationInstruction,
) -> PortfolioAllocationLine:
    allocation_pct = (
        instruction.allocation_eur
        / mandate.treasury_capital_eur
        * 100
    )

    return PortfolioAllocationLine(
        candidate_assessment_id=(
            candidate.assessment_id
        ),
        instrument_id=(
            candidate.instrument_id
        ),
        market_id=(
            candidate.market_id
        ),
        access_route_id=(
            candidate.access_route_id
        ),
        label=candidate.label,
        allocation_eur=(
            instruction.allocation_eur
        ),
        allocation_pct_of_treasury=(
            allocation_pct
        ),
        candidate_position_size_eur=(
            candidate.position_size_eur
        ),
    )


def build_portfolio_construction(
    construction_id: str,
    mandate: TreasuryMandate,
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
    instructions: tuple[
        AllocationInstruction,
        ...
    ] = (),
    notes: str | None = None,
) -> PortfolioConstructionAssessment:
    indexed_candidates = (
        _index_candidates(
            candidates
        )
    )

    recommendation_ready_count = (
        _count_recommendation_ready(
            candidates
        )
    )

    if not instructions:
        if recommendation_ready_count == 0:
            return PortfolioConstructionAssessment(
                construction_id=construction_id,
                mandate_id=mandate.mandate_id,
                treasury_capital_eur=(
                    mandate.treasury_capital_eur
                ),
                candidate_count=len(candidates),
                recommendation_ready_candidate_count=0,
                allocated_capital_eur=0.0,
                unallocated_capital_eur=(
                    mandate.treasury_capital_eur
                ),
                allocation_lines=(),
                construction_status=(
                    "no_actionable_allocation"
                ),
                validation_issues=(),
                notes=(
                    notes
                    or (
                        "No recommendation-ready candidates "
                        "exist. Treasury capital remains "
                        "unallocated by this construction "
                        "layer rather than being forced into "
                        "an unsupported investment."
                    )
                ),
            )

        return PortfolioConstructionAssessment(
            construction_id=construction_id,
            mandate_id=mandate.mandate_id,
            treasury_capital_eur=(
                mandate.treasury_capital_eur
            ),
            candidate_count=len(candidates),
            recommendation_ready_candidate_count=(
                recommendation_ready_count
            ),
            allocated_capital_eur=0.0,
            unallocated_capital_eur=(
                mandate.treasury_capital_eur
            ),
            allocation_lines=(),
            construction_status=(
                "valid_allocation"
            ),
            validation_issues=(),
            notes=(
                notes
                or (
                    "Recommendation-ready candidates exist, "
                    "but no allocation instructions were "
                    "supplied. Capital therefore remains "
                    "unallocated."
                )
            ),
        )

    issues = []
    lines = []

    seen_candidate_ids = set()

    for instruction in instructions:
        candidate_id = (
            instruction.candidate_assessment_id
        )

        if candidate_id in seen_candidate_ids:
            issues.append(
                (
                    "Duplicate allocation instruction for "
                    f"candidate {candidate_id}."
                )
            )
            continue

        seen_candidate_ids.add(
            candidate_id
        )

        candidate = indexed_candidates.get(
            candidate_id
        )

        if candidate is None:
            issues.append(
                (
                    "Allocation instruction references "
                    "unknown candidate assessment "
                    f"{candidate_id}."
                )
            )
            continue

        issues.extend(
            _validate_instruction_candidate(
                mandate=mandate,
                candidate=candidate,
                instruction=instruction,
            )
        )

        lines.append(
            _build_allocation_line(
                mandate=mandate,
                candidate=candidate,
                instruction=instruction,
            )
        )

    allocated_capital_eur = sum(
        line.allocation_eur
        for line in lines
    )

    if (
        allocated_capital_eur
        > mandate.treasury_capital_eur
        + CAPITAL_TOLERANCE_EUR
    ):
        issues.append(
            (
                "Total proposed allocation of "
                f"EUR {allocated_capital_eur:,.2f} "
                "exceeds treasury capital of "
                f"EUR "
                f"{mandate.treasury_capital_eur:,.2f}."
            )
        )

    unallocated_capital_eur = max(
        mandate.treasury_capital_eur
        - allocated_capital_eur,
        0.0,
    )

    construction_status = (
        "invalid_allocation"
        if issues
        else "valid_allocation"
    )

    return PortfolioConstructionAssessment(
        construction_id=construction_id,
        mandate_id=mandate.mandate_id,
        treasury_capital_eur=(
            mandate.treasury_capital_eur
        ),
        candidate_count=len(candidates),
        recommendation_ready_candidate_count=(
            recommendation_ready_count
        ),
        allocated_capital_eur=(
            allocated_capital_eur
        ),
        unallocated_capital_eur=(
            unallocated_capital_eur
        ),
        allocation_lines=tuple(
            lines
        ),
        construction_status=(
            construction_status
        ),
        validation_issues=tuple(
            dict.fromkeys(
                issues
            )
        ),
        notes=notes,
    )