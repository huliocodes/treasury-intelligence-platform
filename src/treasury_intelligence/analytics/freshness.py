from __future__ import annotations

from datetime import date

from treasury_intelligence.models.freshness import (
    EvidenceFreshnessAssessment,
    EvidenceFreshnessRequirement,
)


def _parse_iso_date(
    value: str,
    *,
    field_name: str,
) -> date:
    if not value:
        raise ValueError(
            f"{field_name} is required."
        )

    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(
            f"{field_name} must use YYYY-MM-DD format."
        ) from exc


def assess_evidence_freshness(
    *,
    requirement: EvidenceFreshnessRequirement,
    observed_date: str,
    as_of: str,
) -> EvidenceFreshnessAssessment:
    observed = _parse_iso_date(
        observed_date,
        field_name="observed_date",
    )
    review_date = _parse_iso_date(
        as_of,
        field_name="as_of",
    )

    age_days = (
        review_date - observed
    ).days

    if age_days < 0:
        status = "future_dated"
    elif age_days <= requirement.maximum_age_days:
        status = "fresh"
    else:
        status = "stale"

    return EvidenceFreshnessAssessment(
        evidence_type=requirement.evidence_type,
        observed_date=observed_date,
        as_of=as_of,
        age_days=age_days,
        maximum_age_days=(
            requirement.maximum_age_days
        ),
        status=status,
    )
