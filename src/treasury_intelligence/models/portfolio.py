from __future__ import annotations

from dataclasses import dataclass


PORTFOLIO_CANDIDATE_STATUSES = (
    "blocked",
    "needs_evidence",
    "recommendation_ready",
)


@dataclass(frozen=True)
class PortfolioCandidateAssessment:
    assessment_id: str

    mandate_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    label: str

    position_size_eur: float

    eligibility_status: str
    liquidity_position_status: str

    economics_status: str

    base_risk_unknown_dimension_count: int

    defensible_return_pct: float | None
    defensible_return_measure: str | None

    candidate_status: str

    blocking_reasons: tuple[str, ...]
    evidence_requirements: tuple[str, ...]

    recommendation_ready: bool

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.position_size_eur <= 0:
            raise ValueError(
                "position_size_eur must be greater than zero."
            )

        if (
            self.candidate_status
            not in PORTFOLIO_CANDIDATE_STATUSES
        ):
            raise ValueError(
                "Unsupported portfolio candidate status: "
                f"{self.candidate_status}"
            )

        if self.base_risk_unknown_dimension_count < 0:
            raise ValueError(
                "base_risk_unknown_dimension_count "
                "cannot be negative."
            )

        if (
            self.recommendation_ready
            and self.candidate_status
            != "recommendation_ready"
        ):
            raise ValueError(
                "recommendation_ready=True requires "
                "candidate_status='recommendation_ready'."
            )

        if (
            self.candidate_status
            == "recommendation_ready"
            and not self.recommendation_ready
        ):
            raise ValueError(
                "A recommendation_ready candidate must "
                "set recommendation_ready=True."
            )

        if (
            self.candidate_status == "blocked"
            and not self.blocking_reasons
        ):
            raise ValueError(
                "Blocked candidates require at least one "
                "blocking reason."
            )

        if (
            self.candidate_status == "needs_evidence"
            and not self.evidence_requirements
        ):
            raise ValueError(
                "needs_evidence candidates require at least "
                "one evidence requirement."
            )