from __future__ import annotations

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.portfolio_construction import (
    PortfolioConstructionAssessment,
)

from treasury_intelligence.models.portfolio_proposals import (
    PortfolioProposal,
)


def _validate_alignment(
    construction: PortfolioConstructionAssessment,
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> None:
    if (
        construction.construction_status
        == "invalid_allocation"
    ):
        raise ValueError(
            "Cannot assemble a portfolio proposal from "
            "an invalid portfolio construction."
        )

    if construction.candidate_count != len(candidates):
        raise ValueError(
            "Portfolio construction candidate count does "
            "not match supplied candidates."
        )

    recommendation_ready_count = sum(
        1
        for candidate in candidates
        if candidate.recommendation_ready
    )

    if (
        construction
        .recommendation_ready_candidate_count
        != recommendation_ready_count
    ):
        raise ValueError(
            "Portfolio construction recommendation-ready "
            "count does not match supplied candidates."
        )

    for candidate in candidates:
        if (
            candidate.mandate_id
            != construction.mandate_id
        ):
            raise ValueError(
                "Portfolio candidate mandate does not match "
                "portfolio construction mandate."
            )


def _evidence_blocked_labels(
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> tuple[str, ...]:
    return tuple(
        candidate.label
        for candidate in candidates
        if (
            not candidate.recommendation_ready
            and candidate.candidate_status
            == "needs_evidence"
        )
    )


def _proposal_state(
    construction: PortfolioConstructionAssessment,
) -> tuple[
    str,
    str,
    str,
]:
    if (
        construction.construction_status
        == "no_actionable_allocation"
    ):
        return (
            "no_actionable_allocation",
            "hold_unallocated",
            (
                "No candidate is recommendation-ready. "
                "The treasury should not be forced into "
                "an allocation while required evidence "
                "remains unresolved."
            ),
        )

    if (
        construction.construction_status
        == "valid_allocation"
        and construction.allocated_capital_eur == 0
    ):
        return (
            "no_allocation_proposed",
            "hold_unallocated",
            (
                "Recommendation-ready candidates exist, "
                "but no validated allocation instructions "
                "were supplied."
            ),
        )

    if (
        construction.construction_status
        == "valid_allocation"
        and construction.allocated_capital_eur > 0
    ):
        return (
            "allocation_proposed",
            "propose_allocation",
            (
                "The proposed allocation passed the "
                "portfolio construction policy and may "
                "proceed to the approval layer."
            ),
        )

    raise ValueError(
        "Unsupported portfolio construction state."
    )


def build_portfolio_proposal(
    proposal_id: str,
    construction: PortfolioConstructionAssessment,
    candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
    notes: str | None = None,
) -> PortfolioProposal:
    _validate_alignment(
        construction=construction,
        candidates=candidates,
    )

    (
        proposal_status,
        decision,
        rationale,
    ) = _proposal_state(
        construction
    )

    return PortfolioProposal(
        proposal_id=proposal_id,
        mandate_id=construction.mandate_id,
        construction_id=(
            construction.construction_id
        ),
        treasury_capital_eur=(
            construction.treasury_capital_eur
        ),
        candidate_count=(
            construction.candidate_count
        ),
        recommendation_ready_candidate_count=(
            construction
            .recommendation_ready_candidate_count
        ),
        allocated_capital_eur=(
            construction.allocated_capital_eur
        ),
        unallocated_capital_eur=(
            construction.unallocated_capital_eur
        ),
        proposal_status=proposal_status,
        decision=decision,
        allocation_lines=(
            construction.allocation_lines
        ),
        evidence_blocked_candidate_labels=(
            _evidence_blocked_labels(
                candidates
            )
        ),
        rationale=rationale,
        notes=notes,
    )