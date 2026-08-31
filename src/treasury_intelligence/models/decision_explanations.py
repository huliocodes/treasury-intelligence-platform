from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadyOpportunityComparison:
    label: str
    defensible_return_pct: float
    annual_return_eur_at_position: float
    return_difference_vs_selected_bps: float
    annual_return_difference_vs_selected_eur: float

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError(
                "Ready opportunity label is required."
            )


@dataclass(frozen=True)
class NonReadyOpportunityExplanation:
    label: str
    candidate_status: str
    defensible_return_pct: float | None
    blocking_reasons: tuple[str, ...]
    evidence_requirements: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError(
                "Non-ready opportunity label is required."
            )

        if self.candidate_status not in (
            "blocked",
            "needs_evidence",
        ):
            raise ValueError(
                "Non-ready opportunity must be blocked "
                "or needs_evidence."
            )

        if (
            not self.blocking_reasons
            and not self.evidence_requirements
        ):
            raise ValueError(
                "Non-ready opportunity must contain at "
                "least one blocker or evidence "
                "requirement."
            )


@dataclass(frozen=True)
class ConcentrationAlternativeExplanation:
    label: str
    maximum_single_position_pct: float
    position_count: int
    largest_position_pct: float
    annual_return_pct: float
    annual_return_eur: float
    return_cost_bps: float
    annual_return_cost_eur: float

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError(
                "Concentration alternative label is "
                "required."
            )

        if (
            self.maximum_single_position_pct <= 0
            or self.maximum_single_position_pct > 100
        ):
            raise ValueError(
                "maximum_single_position_pct must be "
                "greater than zero and no more than 100."
            )

        if self.position_count <= 0:
            raise ValueError(
                "position_count must be greater than zero."
            )

        if (
            self.largest_position_pct <= 0
            or self.largest_position_pct > 100
        ):
            raise ValueError(
                "largest_position_pct must be greater "
                "than zero and no more than 100."
            )


@dataclass(frozen=True)
class TreasuryDecisionExplanation:
    explanation_id: str
    report_id: str
    mandate_id: str

    selected_label: str
    selected_allocation_eur: float
    selected_allocation_pct: float

    selected_return_pct: float
    selected_annual_return_eur: float

    target_yield_pct: float | None
    target_yield_gap_pct: float | None
    target_yield_gap_eur: float | None

    ready_opportunities: tuple[
        ReadyOpportunityComparison,
        ...
    ]

    non_ready_opportunities: tuple[
        NonReadyOpportunityExplanation,
        ...
    ]

    concentration_alternatives: tuple[
        ConcentrationAlternativeExplanation,
        ...
    ]

    concentration_policy_interpretation: str

    approval_status: str | None
    authorized_allocation_eur: float
    execution_authorized: bool

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.explanation_id:
            raise ValueError(
                "explanation_id is required."
            )

        if not self.report_id:
            raise ValueError(
                "report_id is required."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id is required."
            )

        if not self.selected_label:
            raise ValueError(
                "selected_label is required."
            )

        if self.selected_allocation_eur <= 0:
            raise ValueError(
                "selected_allocation_eur must be greater "
                "than zero."
            )

        if (
            self.selected_allocation_pct <= 0
            or self.selected_allocation_pct > 100
        ):
            raise ValueError(
                "selected_allocation_pct must be greater "
                "than zero and no more than 100."
            )

        if not self.ready_opportunities:
            raise ValueError(
                "At least one recommendation-ready "
                "opportunity is required."
            )

        selected_matches = tuple(
            opportunity
            for opportunity in self.ready_opportunities
            if opportunity.label == self.selected_label
        )

        if len(selected_matches) != 1:
            raise ValueError(
                "Selected opportunity must appear exactly "
                "once in ready_opportunities."
            )

        if not self.concentration_policy_interpretation:
            raise ValueError(
                "concentration_policy_interpretation is "
                "required."
            )

        if self.authorized_allocation_eur < 0:
            raise ValueError(
                "authorized_allocation_eur cannot be "
                "negative."
            )

        if (
            self.execution_authorized
            and self.approval_status != "approved"
        ):
            raise ValueError(
                "Execution cannot be authorized without "
                "approved status."
            )