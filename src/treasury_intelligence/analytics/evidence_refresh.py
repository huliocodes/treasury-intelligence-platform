from __future__ import annotations

from treasury_intelligence.analytics.freshness import (
    assess_evidence_freshness,
)

from treasury_intelligence.models.evidence_refresh import (
    EvidenceRefreshItem,
    EvidenceRefreshPlan,
)

from treasury_intelligence.models.freshness import (
    EvidenceFreshnessRequirement,
)

from treasury_intelligence.models.freshness_dependencies import (
    OpportunityFreshnessDependencies,
)


def build_evidence_refresh_plan(
    *,
    plan_id: str,
    dependency_sets: tuple[
        OpportunityFreshnessDependencies,
        ...
    ],
    requirements: tuple[
        EvidenceFreshnessRequirement,
        ...
    ],
    as_of: str,
    notes: str | None = None,
) -> EvidenceRefreshPlan:
    if not plan_id:
        raise ValueError(
            "plan_id is required."
        )

    if not as_of:
        raise ValueError(
            "as_of is required."
        )

    requirement_map = {
        requirement.evidence_type: requirement
        for requirement in requirements
    }

    if len(requirement_map) != len(requirements):
        raise ValueError(
            "Freshness requirements must have "
            "unique evidence types."
        )

    refresh_items = []

    for dependency_set in dependency_sets:
        for dependency in (
            dependency_set.required_dependencies
        ):
            requirement = requirement_map.get(
                dependency.evidence_type
            )

            if requirement is None:
                raise ValueError(
                    "No freshness requirement supplied "
                    "for evidence type "
                    f"'{dependency.evidence_type}'."
                )

            if dependency.observed_date is None:
                refresh_items.append(
                    EvidenceRefreshItem(
                        refresh_item_id=(
                            f"{dependency.dependency_id}"
                            "_establish_provenance"
                        ),
                        dependency_id=(
                            dependency.dependency_id
                        ),
                        instrument_id=(
                            dependency.instrument_id
                        ),
                        market_id=(
                            dependency.market_id
                        ),
                        access_route_id=(
                            dependency.access_route_id
                        ),
                        evidence_type=(
                            dependency.evidence_type
                        ),
                        source_reference=(
                            dependency.source_reference
                        ),
                        observed_date=None,
                        maximum_age_days=(
                            requirement.maximum_age_days
                        ),
                        action=(
                            "establish_provenance"
                        ),
                        reason="undated",
                        age_days=None,
                        notes=(
                            "Required recommendation "
                            "evidence exists without "
                            "dated provenance."
                        ),
                    )
                )

                continue

            assessment = assess_evidence_freshness(
                requirement=requirement,
                observed_date=(
                    dependency.observed_date
                ),
                as_of=as_of,
            )

            if assessment.usable:
                continue

            if assessment.status not in (
                "stale",
                "future_dated",
            ):
                raise ValueError(
                    "Unsupported freshness status: "
                    f"{assessment.status}"
                )

            refresh_items.append(
                EvidenceRefreshItem(
                    refresh_item_id=(
                        f"{dependency.dependency_id}"
                        "_refresh"
                    ),
                    dependency_id=(
                        dependency.dependency_id
                    ),
                    instrument_id=(
                        dependency.instrument_id
                    ),
                    market_id=(
                        dependency.market_id
                    ),
                    access_route_id=(
                        dependency.access_route_id
                    ),
                    evidence_type=(
                        dependency.evidence_type
                    ),
                    source_reference=(
                        dependency.source_reference
                    ),
                    observed_date=(
                        dependency.observed_date
                    ),
                    maximum_age_days=(
                        assessment.maximum_age_days
                    ),
                    action="refresh",
                    reason=assessment.status,
                    age_days=assessment.age_days,
                    notes=(
                        "Required recommendation "
                        "evidence is outside the "
                        "production freshness contract."
                    ),
                )
            )

    refresh_items = sorted(
        refresh_items,
        key=lambda item: (
            item.instrument_id,
            item.evidence_type,
            item.dependency_id,
        ),
    )

    return EvidenceRefreshPlan(
        plan_id=plan_id,
        as_of=as_of,
        items=tuple(refresh_items),
        notes=notes,
    )
