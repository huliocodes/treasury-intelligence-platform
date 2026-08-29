from __future__ import annotations

from dataclasses import dataclass


POSITION_RISK_STATUSES = (
    "supported",
    "not_supported",
    "unknown",
    "not_position_sensitive",
)


@dataclass(frozen=True)
class PositionRiskAssessment:
    assessment_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float

    risk_dimension: str

    base_risk_level: str

    position_sensitive: bool
    position_risk_status: str

    evidence_sufficient: bool

    rationale: str

    supporting_risk_assessment_id: str

    supporting_position_analysis_id: str

    supporting_liquidity_assessment_id: str | None = None

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.position_size_eur <= 0:
            raise ValueError(
                "position_size_eur must be greater than zero."
            )

        if (
            self.position_risk_status
            not in POSITION_RISK_STATUSES
        ):
            raise ValueError(
                "Unsupported position risk status: "
                f"{self.position_risk_status}"
            )

        if (
            self.position_risk_status
            == "not_position_sensitive"
            and self.position_sensitive
        ):
            raise ValueError(
                "A position-sensitive assessment cannot use "
                "not_position_sensitive status."
            )

        if (
            self.position_risk_status
            in ("supported", "not_supported")
            and not self.evidence_sufficient
        ):
            raise ValueError(
                "A supported or not_supported conclusion "
                "requires sufficient evidence."
            )

        if (
            self.position_risk_status == "unknown"
            and self.evidence_sufficient
        ):
            raise ValueError(
                "An unknown position-risk conclusion cannot "
                "have evidence_sufficient=True."
            )