from __future__ import annotations

from treasury_intelligence.models.risk import (
    RISK_DIMENSIONS,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


def build_unknown_risk_assessments(
    instrument_id: str,
    market_id: str,
    assessed_at: str,
    rationale_by_dimension: dict[str, str] | None = None,
    notes: str | None = None,
) -> tuple[RiskAssessment, ...]:
    if not instrument_id:
        raise ValueError(
            "instrument_id must not be empty."
        )

    if not market_id:
        raise ValueError(
            "market_id must not be empty."
        )

    if not assessed_at:
        raise ValueError(
            "assessed_at must not be empty."
        )

    rationales = rationale_by_dimension or {}

    unknown_dimensions = (
        set(rationales)
        - set(RISK_DIMENSIONS)
    )

    if unknown_dimensions:
        raise ValueError(
            "Unsupported risk dimensions in "
            "rationale_by_dimension: "
            + ", ".join(
                sorted(unknown_dimensions)
            )
        )

    assessments = []

    for risk_dimension in RISK_DIMENSIONS:
        rationale = rationales.get(
            risk_dimension,
            (
                "Sufficient evidence has not yet been "
                "incorporated to assign a defensible "
                "qualitative risk level for this dimension."
            ),
        )

        assessments.append(
            RiskAssessment(
                assessment_id=(
                    f"{instrument_id}_"
                    f"{risk_dimension}_risk"
                ),
                instrument_id=instrument_id,
                market_id=market_id,
                risk_dimension=risk_dimension,
                risk_level="unknown",
                rationale=rationale,
                supporting_observation_ids=(),
                assessed_at=assessed_at,
                evidence_sufficient=False,
                notes=notes,
            )
        )

    return tuple(assessments)