from __future__ import annotations

from treasury_intelligence.models.decision_explanations import (
    ConcentrationAlternativeExplanation,
    NonReadyOpportunityExplanation,
    ReadyOpportunityComparison,
    TreasuryDecisionExplanation,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.portfolio_comparisons import (
    PortfolioAlternativeComparison,
)

from treasury_intelligence.models.treasury_decision_reports import (
    TreasuryDecisionReport,
)


CAPITAL_TOLERANCE_EUR = 0.01


def _selected_allocation(
    report: TreasuryDecisionReport,
):
    if len(report.allocation_lines) != 1:
        raise ValueError(
            "V1 decision explanation currently requires "
            "exactly one selected allocation line."
        )

    return report.allocation_lines[0]


def _build_ready_comparisons(
    *,
    report: TreasuryDecisionReport,
    universe_candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> tuple[
    ReadyOpportunityComparison,
    ...
]:
    selected_line = _selected_allocation(
        report
    )

    ready_candidates = tuple(
        candidate
        for candidate in universe_candidates
        if candidate.recommendation_ready
    )

    if not ready_candidates:
        raise ValueError(
            "Decision explanation requires at least one "
            "recommendation-ready opportunity."
        )

    selected_candidates = tuple(
        candidate
        for candidate in ready_candidates
        if (
            candidate.instrument_id
            == selected_line.instrument_id
        )
    )

    if len(selected_candidates) != 1:
        raise ValueError(
            "Selected allocation must match exactly one "
            "recommendation-ready universe candidate."
        )

    selected_candidate = (
        selected_candidates[0]
    )

    if selected_candidate.defensible_return_pct is None:
        raise ValueError(
            "Selected candidate requires a defensible "
            "return."
        )

    if (
        abs(
            selected_candidate.position_size_eur
            - selected_line.allocation_eur
        )
        > CAPITAL_TOLERANCE_EUR
    ):
        raise ValueError(
            "Selected universe candidate position size "
            "must match selected allocation."
        )

    selected_return_pct = (
        selected_candidate.defensible_return_pct
    )

    comparisons = []

    for candidate in ready_candidates:
        if candidate.defensible_return_pct is None:
            raise ValueError(
                f"{candidate.label}: recommendation-ready "
                "candidate requires a defensible return."
            )

        annual_return_eur = (
            candidate.position_size_eur
            * candidate.defensible_return_pct
            / 100.0
        )

        return_difference_pct = (
            selected_return_pct
            - candidate.defensible_return_pct
        )

        annual_return_difference_eur = (
            selected_candidate.position_size_eur
            * return_difference_pct
            / 100.0
        )

        comparisons.append(
            ReadyOpportunityComparison(
                label=candidate.label,
                defensible_return_pct=(
                    candidate.defensible_return_pct
                ),
                annual_return_eur_at_position=(
                    annual_return_eur
                ),
                return_difference_vs_selected_bps=(
                    return_difference_pct * 100.0
                ),
                annual_return_difference_vs_selected_eur=(
                    annual_return_difference_eur
                ),
            )
        )

    return tuple(
        sorted(
            comparisons,
            key=lambda comparison: (
                -comparison.defensible_return_pct,
                comparison.label,
            ),
        )
    )


def _build_non_ready_explanations(
    universe_candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
) -> tuple[
    NonReadyOpportunityExplanation,
    ...
]:
    explanations = []

    for candidate in universe_candidates:
        if candidate.recommendation_ready:
            continue

        explanations.append(
            NonReadyOpportunityExplanation(
                label=candidate.label,
                candidate_status=(
                    candidate.candidate_status
                ),
                defensible_return_pct=(
                    candidate.defensible_return_pct
                ),
                blocking_reasons=(
                    candidate.blocking_reasons
                ),
                evidence_requirements=(
                    candidate.evidence_requirements
                ),
            )
        )

    return tuple(
        explanations
    )


def _build_concentration_alternative(
    *,
    label: str,
    maximum_single_position_pct: float,
    comparison: PortfolioAlternativeComparison,
) -> ConcentrationAlternativeExplanation:
    if comparison.return_difference_bps < -1e-9:
        raise ValueError(
            "Concentration alternative unexpectedly "
            "outperforms the selected construction. "
            "Review comparison orientation before "
            "describing the difference as a cost."
        )

    if (
        comparison.annual_return_difference_eur
        < -CAPITAL_TOLERANCE_EUR
    ):
        raise ValueError(
            "Concentration alternative unexpectedly "
            "produces greater annual return than the "
            "selected construction."
        )

    return ConcentrationAlternativeExplanation(
        label=label,
        maximum_single_position_pct=(
            maximum_single_position_pct
        ),
        position_count=(
            comparison.alternative.position_count
        ),
        largest_position_pct=(
            comparison.alternative.largest_position_pct
        ),
        annual_return_pct=(
            comparison.alternative.annual_return_pct
        ),
        annual_return_eur=(
            comparison.alternative.annual_return_eur
        ),
        return_cost_bps=(
            comparison.return_difference_bps
        ),
        annual_return_cost_eur=(
            comparison.annual_return_difference_eur
        ),
    )


def build_treasury_decision_explanation(
    *,
    explanation_id: str,
    report: TreasuryDecisionReport,
    universe_candidates: tuple[
        PortfolioCandidateAssessment,
        ...
    ],
    concentration_comparisons: tuple[
        tuple[
            str,
            float,
            PortfolioAlternativeComparison,
        ],
        ...
    ] = (),
    notes: str | None = None,
) -> TreasuryDecisionExplanation:
    if not explanation_id:
        raise ValueError(
            "explanation_id is required."
        )

    selected_line = _selected_allocation(
        report
    )

    if (
        report.portfolio_defensible_return_pct
        is None
    ):
        raise ValueError(
            "Decision explanation requires a defensible "
            "portfolio return."
        )

    if (
        report.portfolio_annual_return_eur
        is None
    ):
        raise ValueError(
            "Decision explanation requires an annual "
            "portfolio return."
        )

    ready_opportunities = (
        _build_ready_comparisons(
            report=report,
            universe_candidates=universe_candidates,
        )
    )

    non_ready_opportunities = (
        _build_non_ready_explanations(
            universe_candidates
        )
    )

    concentration_alternatives = tuple(
        _build_concentration_alternative(
            label=label,
            maximum_single_position_pct=(
                maximum_single_position_pct
            ),
            comparison=comparison,
        )
        for (
            label,
            maximum_single_position_pct,
            comparison,
        ) in concentration_comparisons
    )

    concentration_policy_interpretation = (
        "The current mandate permits the selected "
        "single-position allocation. The alternative "
        "maximum-position scenarios are counterfactual "
        "diagnostics only. Their lower concentration "
        "does not by itself establish that they are "
        "safer or optimal, and no 40% or 50% production "
        "concentration policy is asserted."
    )

    return TreasuryDecisionExplanation(
        explanation_id=explanation_id,
        report_id=report.report_id,
        mandate_id=report.mandate_id,
        selected_label=selected_line.label,
        selected_allocation_eur=(
            selected_line.allocation_eur
        ),
        selected_allocation_pct=(
            selected_line.allocation_pct_of_treasury
        ),
        selected_return_pct=(
            report.portfolio_defensible_return_pct
        ),
        selected_annual_return_eur=(
            report.portfolio_annual_return_eur
        ),
        target_yield_pct=(
            report.target_yield_pct
        ),
        target_yield_gap_pct=(
            report.target_yield_gap_pct
        ),
        target_yield_gap_eur=(
            report.target_yield_gap_eur
        ),
        ready_opportunities=(
            ready_opportunities
        ),
        non_ready_opportunities=(
            non_ready_opportunities
        ),
        concentration_alternatives=(
            concentration_alternatives
        ),
        concentration_policy_interpretation=(
            concentration_policy_interpretation
        ),
        approval_status=(
            report.approval_status
        ),
        authorized_allocation_eur=(
            report.authorized_allocation_eur
        ),
        execution_authorized=(
            report.execution_authorized
        ),
        notes=notes,
    )