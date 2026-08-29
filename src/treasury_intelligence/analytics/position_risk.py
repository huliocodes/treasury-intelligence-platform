from __future__ import annotations

from treasury_intelligence.models.liquidity import (
    LiquidityEvidenceAssessment,
)

from treasury_intelligence.models.opportunities import (
    PositionAnalysis,
)

from treasury_intelligence.models.position_risk import (
    PositionRiskAssessment,
)

from treasury_intelligence.models.risk import (
    RISK_DIMENSIONS,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


def _index_risk_assessments(
    risk_assessments: tuple[RiskAssessment, ...],
) -> dict[str, RiskAssessment]:
    indexed = {}

    for assessment in risk_assessments:
        if assessment.risk_dimension in indexed:
            raise ValueError(
                "Duplicate risk assessment for dimension: "
                f"{assessment.risk_dimension}"
            )

        indexed[
            assessment.risk_dimension
        ] = assessment

    missing_dimensions = (
        set(RISK_DIMENSIONS)
        - set(indexed)
    )

    if missing_dimensions:
        raise ValueError(
            "Missing risk assessments for dimensions: "
            + ", ".join(
                sorted(missing_dimensions)
            )
        )

    return indexed


def _validate_entity_alignment(
    risk_assessments: tuple[RiskAssessment, ...],
    position: PositionAnalysis,
    liquidity_assessment: LiquidityEvidenceAssessment,
) -> None:
    for risk_assessment in risk_assessments:
        if (
            risk_assessment.instrument_id
            != position.instrument_id
        ):
            raise ValueError(
                "Risk assessment instrument does not match "
                "position analysis."
            )

        if (
            risk_assessment.market_id
            != position.market_id
        ):
            raise ValueError(
                "Risk assessment market does not match "
                "position analysis."
            )

    if (
        liquidity_assessment.instrument_id
        != position.instrument_id
    ):
        raise ValueError(
            "Liquidity assessment instrument does not match "
            "position analysis."
        )

    if (
        liquidity_assessment.market_id
        != position.market_id
    ):
        raise ValueError(
            "Liquidity assessment market does not match "
            "position analysis."
        )

    if (
        liquidity_assessment.access_route_id
        != position.access_route_id
    ):
        raise ValueError(
            "Liquidity assessment access route does not "
            "match position analysis."
        )

    if (
        liquidity_assessment.position_size_eur
        != position.position_size_eur
    ):
        raise ValueError(
            "Liquidity assessment position size does not "
            "match position analysis."
        )


def _build_non_position_sensitive_assessment(
    base_assessment: RiskAssessment,
    position: PositionAnalysis,
) -> PositionRiskAssessment:
    return PositionRiskAssessment(
        assessment_id=(
            f"{position.analysis_id}_"
            f"{base_assessment.risk_dimension}_risk"
        ),
        instrument_id=position.instrument_id,
        market_id=position.market_id,
        access_route_id=position.access_route_id,
        position_size_eur=position.position_size_eur,
        risk_dimension=(
            base_assessment.risk_dimension
        ),
        base_risk_level=(
            base_assessment.risk_level
        ),
        position_sensitive=False,
        position_risk_status=(
            "not_position_sensitive"
        ),
        evidence_sufficient=(
            base_assessment.evidence_sufficient
        ),
        rationale=(
            "No position-size-specific modifier is currently "
            "modeled for this risk dimension. The instrument-"
            "level qualitative assessment is preserved without "
            "changing it solely because of position size."
        ),
        supporting_risk_assessment_id=(
            base_assessment.assessment_id
        ),
        supporting_position_analysis_id=(
            position.analysis_id
        ),
        notes=(
            "Future evidence may make this dimension position-"
            "sensitive. No such rule is assumed in 4C."
        ),
    )


def _build_liquidity_position_assessment(
    base_assessment: RiskAssessment,
    position: PositionAnalysis,
    liquidity_assessment: LiquidityEvidenceAssessment,
) -> PositionRiskAssessment:
    if (
        not liquidity_assessment
        .sufficient_for_immediate_liquidity
    ):
        return PositionRiskAssessment(
            assessment_id=(
                f"{position.analysis_id}_liquidity_risk"
            ),
            instrument_id=position.instrument_id,
            market_id=position.market_id,
            access_route_id=position.access_route_id,
            position_size_eur=position.position_size_eur,
            risk_dimension="liquidity",
            base_risk_level=(
                base_assessment.risk_level
            ),
            position_sensitive=True,
            position_risk_status="unknown",
            evidence_sufficient=False,
            rationale=(
                "Position-size liquidity evidence is not strong "
                "enough to determine whether the full position "
                "can be exited immediately. Market activity, "
                "fund size, or displayed trading activity alone "
                "does not establish position-size executable "
                "depth."
            ),
            supporting_risk_assessment_id=(
                base_assessment.assessment_id
            ),
            supporting_position_analysis_id=(
                position.analysis_id
            ),
            supporting_liquidity_assessment_id=(
                liquidity_assessment.assessment_id
            ),
        )

    if (
        liquidity_assessment
        .immediate_liquidity_supported
        is True
    ):
        coverage = (
            position.immediate_exit_coverage_pct
        )

        coverage_text = (
            f"{coverage:.2f}%"
            if coverage is not None
            else "at least full position coverage"
        )

        return PositionRiskAssessment(
            assessment_id=(
                f"{position.analysis_id}_liquidity_risk"
            ),
            instrument_id=position.instrument_id,
            market_id=position.market_id,
            access_route_id=position.access_route_id,
            position_size_eur=position.position_size_eur,
            risk_dimension="liquidity",
            base_risk_level=(
                base_assessment.risk_level
            ),
            position_sensitive=True,
            position_risk_status="supported",
            evidence_sufficient=True,
            rationale=(
                "Direct position-size liquidity evidence "
                "supports immediate exit of the modeled "
                f"position. Observed coverage: {coverage_text}."
            ),
            supporting_risk_assessment_id=(
                base_assessment.assessment_id
            ),
            supporting_position_analysis_id=(
                position.analysis_id
            ),
            supporting_liquidity_assessment_id=(
                liquidity_assessment.assessment_id
            ),
            notes=(
                "Supported describes the observed position-size "
                "liquidity condition. It does not convert the "
                "instrument-level qualitative liquidity risk "
                "assessment into low risk."
            ),
        )

    if (
        liquidity_assessment
        .immediate_liquidity_supported
        is False
    ):
        coverage = (
            position.immediate_exit_coverage_pct
        )

        coverage_text = (
            f"{coverage:.2f}%"
            if coverage is not None
            else "less than full position coverage"
        )

        return PositionRiskAssessment(
            assessment_id=(
                f"{position.analysis_id}_liquidity_risk"
            ),
            instrument_id=position.instrument_id,
            market_id=position.market_id,
            access_route_id=position.access_route_id,
            position_size_eur=position.position_size_eur,
            risk_dimension="liquidity",
            base_risk_level=(
                base_assessment.risk_level
            ),
            position_sensitive=True,
            position_risk_status="not_supported",
            evidence_sufficient=True,
            rationale=(
                "Direct position-size liquidity evidence shows "
                "that the modeled position cannot currently be "
                "fully exited immediately. Observed coverage: "
                f"{coverage_text}."
            ),
            supporting_risk_assessment_id=(
                base_assessment.assessment_id
            ),
            supporting_position_analysis_id=(
                position.analysis_id
            ),
            supporting_liquidity_assessment_id=(
                liquidity_assessment.assessment_id
            ),
            notes=(
                "Not supported is a position-specific observed "
                "liquidity conclusion. It is not an arbitrary "
                "conversion into a high or very-high qualitative "
                "risk score."
            ),
        )

    return PositionRiskAssessment(
        assessment_id=(
            f"{position.analysis_id}_liquidity_risk"
        ),
        instrument_id=position.instrument_id,
        market_id=position.market_id,
        access_route_id=position.access_route_id,
        position_size_eur=position.position_size_eur,
        risk_dimension="liquidity",
        base_risk_level=(
            base_assessment.risk_level
        ),
        position_sensitive=True,
        position_risk_status="unknown",
        evidence_sufficient=False,
        rationale=(
            "The liquidity evidence layer did not produce a "
            "position-size immediate-liquidity conclusion."
        ),
        supporting_risk_assessment_id=(
            base_assessment.assessment_id
        ),
        supporting_position_analysis_id=(
            position.analysis_id
        ),
        supporting_liquidity_assessment_id=(
            liquidity_assessment.assessment_id
        ),
    )


def build_position_risk_assessments(
    risk_assessments: tuple[RiskAssessment, ...],
    position: PositionAnalysis,
    liquidity_assessment: LiquidityEvidenceAssessment,
) -> tuple[PositionRiskAssessment, ...]:
    _validate_entity_alignment(
        risk_assessments=risk_assessments,
        position=position,
        liquidity_assessment=liquidity_assessment,
    )

    indexed = _index_risk_assessments(
        risk_assessments
    )

    results = []

    for risk_dimension in RISK_DIMENSIONS:
        base_assessment = indexed[
            risk_dimension
        ]

        if risk_dimension == "liquidity":
            result = (
                _build_liquidity_position_assessment(
                    base_assessment=base_assessment,
                    position=position,
                    liquidity_assessment=(
                        liquidity_assessment
                    ),
                )
            )
        else:
            result = (
                _build_non_position_sensitive_assessment(
                    base_assessment=base_assessment,
                    position=position,
                )
            )

        results.append(result)

    return tuple(results)


def get_liquidity_position_risk(
    assessments: tuple[
        PositionRiskAssessment,
        ...
    ],
) -> PositionRiskAssessment:
    matches = tuple(
        assessment
        for assessment in assessments
        if assessment.risk_dimension == "liquidity"
    )

    if len(matches) != 1:
        raise ValueError(
            "Expected exactly one liquidity position-risk "
            "assessment."
        )

    return matches[0]