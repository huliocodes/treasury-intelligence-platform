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
    cost_source_reference: str,
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
            observed_date=None,
            required_for_recommendation=True,
            notes=(
                "Current normalized Accessibility objects "
                "do not carry an evidence observation "
                "date. V1 must preserve this as undated "
                "rather than borrowing a market or "
                "snapshot date."
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
            observed_date=None,
            required_for_recommendation=True,
            notes=(
                "Current production access/trading-cost "
                "evidence used by these candidates does "
                "not expose a generic evidence date at "
                "the candidate boundary. V1 therefore "
                "classifies cost freshness as undated "
                "until dated provenance is promoted."
            ),
        ),
    )

    return OpportunityFreshnessDependencies(
        instrument_id=instrument_id,
        market_id=market_id,
        access_route_id=access_route_id,
        dependencies=dependencies,
    )
