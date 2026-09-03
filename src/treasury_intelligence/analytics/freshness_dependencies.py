from __future__ import annotations

from treasury_intelligence.models.freshness_dependencies import (
    EvidenceFreshnessDependency,
    OpportunityFreshnessDependencies,
)

from treasury_intelligence.models.opportunities import (
    Accessibility,
    MarketObservation,
    OpportunitySnapshot,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)

from treasury_intelligence.analytics.freshness import (
    assess_evidence_freshness,
)

from treasury_intelligence.models.freshness import (
    EvidenceFreshnessRequirement,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)


def _validate_alignment(
    *,
    snapshot: OpportunitySnapshot,
    market_observation: MarketObservation,
    accessibility: Accessibility,
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
) -> None:
    if (
        market_observation.instrument_id
        != snapshot.instrument_id
    ):
        raise ValueError(
            "Market observation instrument does not "
            "match snapshot."
        )

    if (
        market_observation.market_id
        != snapshot.market_id
    ):
        raise ValueError(
            "Market observation market does not "
            "match snapshot."
        )

    if (
        accessibility.access_route_id
        != snapshot.access_route_id
    ):
        raise ValueError(
            "Accessibility route does not match "
            "snapshot."
        )

    if not risk_assessments:
        raise ValueError(
            "Risk assessments are required."
        )

    for assessment in risk_assessments:
        if (
            assessment.instrument_id
            != snapshot.instrument_id
        ):
            raise ValueError(
                "Risk assessment instrument does not "
                "match snapshot."
            )

        if (
            assessment.market_id
            != snapshot.market_id
        ):
            raise ValueError(
                "Risk assessment market does not "
                "match snapshot."
            )


def _conservative_risk_assessment_date(
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
) -> str:
    dated_required_assessments = tuple(
        assessment
        for assessment in risk_assessments
        if (
            assessment.risk_dimension
            != "liquidity"
            and assessment.evidence_sufficient
            and assessment.assessed_at
        )
    )

    if not dated_required_assessments:
        raise ValueError(
            "At least one dated sufficient non-liquidity "
            "risk assessment is required."
        )

    return min(
        assessment.assessed_at
        for assessment
        in dated_required_assessments
    )


def build_opportunity_freshness_dependencies(
    *,
    snapshot: OpportunitySnapshot,
    market_observation: MarketObservation,
    accessibility: Accessibility,
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
    accessibility_source_reference: str,
    accessibility_observed_date: str | None,
    cost_source_reference: str,
    cost_observed_date: str | None,
) -> OpportunityFreshnessDependencies:
    _validate_alignment(
        snapshot=snapshot,
        market_observation=market_observation,
        accessibility=accessibility,
        risk_assessments=risk_assessments,
    )

    instrument_id = snapshot.instrument_id
    market_id = snapshot.market_id
    access_route_id = snapshot.access_route_id

    risk_assessment_date = (
        _conservative_risk_assessment_date(
            risk_assessments
        )
    )

    dependencies = (
        EvidenceFreshnessDependency(
            dependency_id=(
                f"{instrument_id}_market_return"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            access_route_id=access_route_id,
            evidence_type="market_return",
            source_reference=snapshot.snapshot_id,
            observed_date=snapshot.observed_date,
            required_for_recommendation=True,
            notes=(
                "Reference return economics come from "
                "the normalized opportunity snapshot. "
                "Freshness therefore follows the "
                "snapshot observation date."
            ),
        ),
        EvidenceFreshnessDependency(
            dependency_id=(
                f"{instrument_id}_market_liquidity"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            access_route_id=access_route_id,
            evidence_type="market_liquidity",
            source_reference=(
                market_observation.observation_id
            ),
            observed_date=(
                market_observation.observed_at
            ),
            required_for_recommendation=True,
            notes=(
                "Position-size liquidity analysis uses "
                "the supplied market observation together "
                "with product or issue scale. The market "
                "observation is therefore treated as a "
                "dated liquidity dependency."
            ),
        ),
        EvidenceFreshnessDependency(
            dependency_id=(
                f"{instrument_id}_risk"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            access_route_id=access_route_id,
            evidence_type="risk",
            source_reference=(
                f"{instrument_id}_risk_assessment_set"
            ),
            observed_date=risk_assessment_date,
            required_for_recommendation=True,
            notes=(
                "V1 freshness follows the oldest dated "
                "sufficient non-liquidity risk assessment "
                "used by the recommendation gate. This "
                "is deliberately conservative and does "
                "not substitute for the underlying risk "
                "observation provenance."
            ),
        ),
        EvidenceFreshnessDependency(
            dependency_id=(
                f"{instrument_id}_accessibility"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            access_route_id=access_route_id,
            evidence_type="accessibility",
            source_reference=(
                accessibility_source_reference
            ),
            observed_date=(
                accessibility_observed_date
            ),
            required_for_recommendation=True,
            notes=(
                "Accessibility freshness follows the "
                "dated provenance supporting the "
                "normalized corporate-access conclusion. "
                "If that provenance has no date, the "
                "dependency remains explicitly undated."
            ),
        ),
        EvidenceFreshnessDependency(
            dependency_id=(
                f"{instrument_id}_cost"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            access_route_id=access_route_id,
            evidence_type="cost",
            source_reference=cost_source_reference,
            observed_date=cost_observed_date,
            required_for_recommendation=True,
            notes=(
                "Cost freshness follows the dated "
                "broker or route evidence actually used "
                "by the return analysis. If the source "
                "does not expose a date, the dependency "
                "remains explicitly undated."
            ),
        ),
    )

    return OpportunityFreshnessDependencies(
        instrument_id=instrument_id,
        market_id=market_id,
        access_route_id=access_route_id,
        dependencies=dependencies,
    )



def build_freshness_evidence_requirements(
    *,
    dependencies: OpportunityFreshnessDependencies,
    requirements: tuple[
        EvidenceFreshnessRequirement,
        ...
    ],
    as_of: str,
) -> tuple[str, ...]:
    requirement_map = {
        requirement.evidence_type: requirement
        for requirement in requirements
    }

    evidence_requirements = []

    for dependency in dependencies.required_dependencies:
        requirement = requirement_map.get(
            dependency.evidence_type
        )

        if requirement is None:
            raise ValueError(
                "No freshness requirement supplied for "
                f"evidence type '{dependency.evidence_type}'."
            )

        if dependency.observed_date is None:
            evidence_requirements.append(
                "Refresh required: "
                f"{dependency.evidence_type} evidence "
                f"for {dependency.instrument_id} is "
                "required for recommendation but has "
                "no dated provenance."
            )
            continue

        assessment = assess_evidence_freshness(
            requirement=requirement,
            observed_date=dependency.observed_date,
            as_of=as_of,
        )

        if assessment.usable:
            continue

        if assessment.status == "stale":
            evidence_requirements.append(
                "Refresh required: "
                f"{dependency.evidence_type} evidence "
                f"for {dependency.instrument_id} was "
                f"observed {dependency.observed_date}, "
                f"is {assessment.age_days} days old as "
                f"of {as_of}, and exceeds the "
                f"{assessment.maximum_age_days}-day "
                "freshness limit."
            )
        elif assessment.status == "future_dated":
            evidence_requirements.append(
                "Refresh required: "
                f"{dependency.evidence_type} evidence "
                f"for {dependency.instrument_id} is "
                f"future-dated {dependency.observed_date} "
                f"relative to review date {as_of}."
            )
        else:
            raise ValueError(
                "Unsupported freshness status: "
                f"{assessment.status}"
            )

    return tuple(
        dict.fromkeys(
            evidence_requirements
        )
    )



def apply_freshness_evidence_requirements(
    *,
    candidate: PortfolioCandidateAssessment,
    freshness_evidence_requirements: tuple[
        str,
        ...
    ],
) -> PortfolioCandidateAssessment:
    if not freshness_evidence_requirements:
        return candidate

    evidence_requirements = tuple(
        dict.fromkeys(
            (
                *candidate.evidence_requirements,
                *freshness_evidence_requirements,
            )
        )
    )

    if candidate.blocking_reasons:
        candidate_status = "blocked"
        recommendation_ready = False

    elif evidence_requirements:
        candidate_status = "needs_evidence"
        recommendation_ready = False

    else:
        candidate_status = (
            "recommendation_ready"
        )
        recommendation_ready = True

    return PortfolioCandidateAssessment(
        assessment_id=candidate.assessment_id,
        mandate_id=candidate.mandate_id,
        instrument_id=candidate.instrument_id,
        market_id=candidate.market_id,
        access_route_id=candidate.access_route_id,
        label=candidate.label,
        position_size_eur=(
            candidate.position_size_eur
        ),
        eligibility_status=(
            candidate.eligibility_status
        ),
        liquidity_position_status=(
            candidate.liquidity_position_status
        ),
        economics_status=(
            candidate.economics_status
        ),
        base_risk_unknown_dimension_count=(
            candidate.base_risk_unknown_dimension_count
        ),
        defensible_return_pct=(
            candidate.defensible_return_pct
        ),
        defensible_return_measure=(
            candidate.defensible_return_measure
        ),
        candidate_status=candidate_status,
        blocking_reasons=(
            candidate.blocking_reasons
        ),
        evidence_requirements=(
            evidence_requirements
        ),
        recommendation_ready=(
            recommendation_ready
        ),
        embedded_one_time_cost_component_types=(
            candidate
            .embedded_one_time_cost_component_types
        ),
        notes=candidate.notes,
    )
