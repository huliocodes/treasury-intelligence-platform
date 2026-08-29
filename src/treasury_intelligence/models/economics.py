from __future__ import annotations

from dataclasses import dataclass


ECONOMICS_STATUSES = (
    "complete",
    "incomplete",
)


ECONOMICS_GAP_PRIORITIES = (
    "low",
    "medium",
    "high",
    "critical",
)


@dataclass(frozen=True)
class EconomicsEvidenceGap:
    evidence_gap_id: str

    return_analysis_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float
    holding_period_days: int

    component_id: str
    component_type: str
    component_label: str
    component_basis: str

    current_status: str

    priority: str
    blocking: bool

    required_evidence: str
    resolution_action: str

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.position_size_eur <= 0:
            raise ValueError(
                "position_size_eur must be greater than zero."
            )

        if self.holding_period_days <= 0:
            raise ValueError(
                "holding_period_days must be greater than zero."
            )

        if (
            self.priority
            not in ECONOMICS_GAP_PRIORITIES
        ):
            raise ValueError(
                "Unsupported economics gap priority: "
                f"{self.priority}"
            )

        if self.current_status != "unknown":
            raise ValueError(
                "Economics evidence gaps must originate "
                "from unknown return components."
            )


@dataclass(frozen=True)
class EconomicsEvidenceAssessment:
    assessment_id: str

    return_analysis_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float
    holding_period_days: int

    economics_status: str

    realistic_expected_return_available: bool

    blocking_gap_count: int

    evidence_gaps: tuple[
        EconomicsEvidenceGap,
        ...
    ]

    strongest_supported_claim: str

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.position_size_eur <= 0:
            raise ValueError(
                "position_size_eur must be greater than zero."
            )

        if self.holding_period_days <= 0:
            raise ValueError(
                "holding_period_days must be greater than zero."
            )

        if (
            self.economics_status
            not in ECONOMICS_STATUSES
        ):
            raise ValueError(
                "Unsupported economics status: "
                f"{self.economics_status}"
            )

        if self.blocking_gap_count < 0:
            raise ValueError(
                "blocking_gap_count cannot be negative."
            )

        actual_blocking_count = sum(
            1
            for gap in self.evidence_gaps
            if gap.blocking
        )

        if (
            self.blocking_gap_count
            != actual_blocking_count
        ):
            raise ValueError(
                "blocking_gap_count does not match "
                "the evidence gap collection."
            )

        if (
            self.economics_status == "complete"
            and self.blocking_gap_count != 0
        ):
            raise ValueError(
                "Complete economics cannot contain "
                "blocking evidence gaps."
            )

        if (
            self.economics_status == "complete"
            and not self.realistic_expected_return_available
        ):
            raise ValueError(
                "Complete economics must provide a "
                "realistic expected return."
            )

        if (
            self.economics_status == "incomplete"
            and self.realistic_expected_return_available
        ):
            raise ValueError(
                "Incomplete economics must not claim "
                "a realistic expected return."
            )