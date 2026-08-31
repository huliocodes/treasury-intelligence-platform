from __future__ import annotations

from collections.abc import Callable

from treasury_intelligence.analytics.economics import (
    build_economics_evidence_assessment,
)

from treasury_intelligence.analytics.eligibility import (
    evaluate_eligibility,
)

from treasury_intelligence.analytics.liquidity import (
    assess_liquidity_evidence,
)

from treasury_intelligence.analytics.portfolio import (
    build_integrated_portfolio_candidate,
)

from treasury_intelligence.analytics.position_risk import (
    build_position_risk_assessments,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
)

from treasury_intelligence.models.opportunities import (
    Accessibility,
    Instrument,
    Market,
    MarketObservation,
    OpportunitySnapshot,
    PositionAnalysis,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.returns import (
    ReturnComponent,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


PositionBuilder = Callable[
    [float],
    PositionAnalysis,
]

ReturnComponentBuilder = Callable[
    [float],
    tuple[ReturnComponent, ...],
]


def _validate_normalized_opportunity(
    instrument: Instrument,
    market: Market,
    accessibility: Accessibility,
    snapshot: OpportunitySnapshot,
) -> None:
    if (
        market.instrument_id
        != instrument.instrument_id
    ):
        raise ValueError(
            "Market instrument does not match instrument."
        )

    if (
        snapshot.instrument_id
        != instrument.instrument_id
    ):
        raise ValueError(
            "Snapshot instrument does not match instrument."
        )

    if snapshot.market_id != market.market_id:
        raise ValueError(
            "Snapshot market does not match market."
        )

    if (
        accessibility.access_route_id
        != snapshot.access_route_id
    ):
        raise ValueError(
            "Accessibility route does not match "
            "snapshot access route."
        )


def _validate_position_alignment(
    position: PositionAnalysis,
    instrument: Instrument,
    market: Market,
    snapshot: OpportunitySnapshot,
    position_size_eur: float,
) -> None:
    if (
        position.instrument_id
        != instrument.instrument_id
    ):
        raise ValueError(
            "Position instrument does not match "
            "normalized opportunity."
        )

    if position.market_id != market.market_id:
        raise ValueError(
            "Position market does not match "
            "normalized opportunity."
        )

    if (
        position.access_route_id
        != snapshot.access_route_id
    ):
        raise ValueError(
            "Position access route does not match "
            "normalized opportunity."
        )

    if (
        position.position_size_eur
        != position_size_eur
    ):
        raise ValueError(
            "Position builder returned a different "
            "position size than requested."
        )


def _validate_risk_alignment(
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
    instrument: Instrument,
    market: Market,
) -> None:
    if not risk_assessments:
        raise ValueError(
            "Risk assessments are required."
        )

    for assessment in risk_assessments:
        if (
            assessment.instrument_id
            != instrument.instrument_id
        ):
            raise ValueError(
                "Risk assessment instrument does not "
                "match normalized opportunity."
            )

        if (
            assessment.market_id
            != market.market_id
        ):
            raise ValueError(
                "Risk assessment market does not "
                "match normalized opportunity."
            )


def analyze_opportunity_position(
    *,
    assessment_id: str,
    label: str,
    mandate,
    instrument: Instrument,
    market: Market,
    accessibility: Accessibility,
    snapshot: OpportunitySnapshot,
    position_size_eur: float,
    holding_period_days: int,
    position_builder: PositionBuilder,
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
    return_component_builder: ReturnComponentBuilder,
    market_observation: MarketObservation | None = None,
    notes: str | None = None,
) -> PortfolioCandidateAssessment:
    if not assessment_id:
        raise ValueError(
            "assessment_id is required."
        )

    if not label:
        raise ValueError(
            "label is required."
        )

    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    if holding_period_days <= 0:
        raise ValueError(
            "holding_period_days must be greater than zero."
        )

    _validate_normalized_opportunity(
        instrument=instrument,
        market=market,
        accessibility=accessibility,
        snapshot=snapshot,
    )

    _validate_risk_alignment(
        risk_assessments=risk_assessments,
        instrument=instrument,
        market=market,
    )

    position = position_builder(
        position_size_eur
    )

    _validate_position_alignment(
        position=position,
        instrument=instrument,
        market=market,
        snapshot=snapshot,
        position_size_eur=position_size_eur,
    )

    liquidity = assess_liquidity_evidence(
        market_observation=market_observation,
        position=position,
    )

    eligibility = evaluate_eligibility(
        mandate=mandate,
        instrument=instrument,
        market=market,
        accessibility=accessibility,
        position=position,
    )

    position_risk = (
        build_position_risk_assessments(
            risk_assessments=(
                risk_assessments
            ),
            position=position,
            liquidity_assessment=liquidity,
        )
    )

    return_components = (
        return_component_builder(
            position_size_eur
        )
    )

    return_analysis = build_return_analysis(
        analysis_id=(
            f"{assessment_id}_return"
        ),
        instrument_id=(
            instrument.instrument_id
        ),
        market_id=market.market_id,
        access_route_id=(
            snapshot.access_route_id
        ),
        position_size_eur=(
            position_size_eur
        ),
        holding_period_days=(
            holding_period_days
        ),
        components=return_components,
        notes=(
            "Return analysis generated through the "
            "generic universe orchestration path."
        ),
    )

    economics = (
        build_economics_evidence_assessment(
            return_analysis
        )
    )

    return (
        build_integrated_portfolio_candidate(
            assessment_id=assessment_id,
            label=label,
            eligibility=eligibility,
            risk_assessments=(
                risk_assessments
            ),
            position_risk_assessments=(
                position_risk
            ),
            economics=economics,
            return_analysis=return_analysis,
            notes=notes,
        )
    )