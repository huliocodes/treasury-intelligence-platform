from __future__ import annotations

from dataclasses import dataclass


RISK_LEVELS = (
    "very_low",
    "low",
    "moderate",
    "high",
    "very_high",
    "unknown",
    "not_applicable",
)


@dataclass(frozen=True)
class RiskAssessment:
    assessment_id: str

    instrument_id: str
    market_id: str

    risk_dimension: str
    risk_level: str

    rationale: str

    supporting_observation_ids: tuple[str, ...]

    assessed_at: str

    position_size_eur: float | None = None

    evidence_sufficient: bool = False

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(
                f"Unsupported risk level: {self.risk_level}"
            )

        if (
            self.risk_level == "unknown"
            and self.evidence_sufficient
        ):
            raise ValueError(
                "An unknown risk assessment cannot have "
                "evidence_sufficient=True."
            )

        if (
            self.risk_level
            not in ("unknown", "not_applicable")
            and not self.supporting_observation_ids
        ):
            raise ValueError(
                "A qualitative risk assessment requires at "
                "least one supporting observation."
            )