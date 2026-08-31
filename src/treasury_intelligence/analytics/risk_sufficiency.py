from __future__ import annotations

from dataclasses import dataclass

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.risk import (
    RISK_DIMENSIONS,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


VERY_HIGH_CAPITAL_PRESERVATION_REQUIRED_DIMENSIONS = (
    "principal_credit",
    "market",
    "currency_asset",
    "structural_counterparty",
    "technical",
    "operational_regulatory",
)

VERY_HIGH_CAPITAL_PRESERVATION_ACCEPTABLE_LEVELS = (
    "very_low",
    "low",
    "not_applicable",
)


@dataclass(frozen=True)
class RiskEvidenceSufficiencyAssessment:
    mandate_id: str

    instrument_id: str
    market_id: str

    required_dimensions: tuple[str, ...]

    insufficient_dimensions: tuple[str, ...]
    unacceptable_dimensions: tuple[str, ...]

    evidence_requirements: tuple[str, ...]
    risk_blocking_reasons: tuple[str, ...]

    evidence_sufficient: bool
    risk_acceptable: bool
    sufficient_for_recommendation: bool

    notes: str | None = None


def _index_risk_assessments(
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
) -> dict[str, RiskAssessment]:
    if not risk_assessments:
        raise ValueError(
            "Risk assessments are required."
        )

    indexed: dict[str, RiskAssessment] = {}

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
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
) -> tuple[str, str]:
    first_assessment = risk_assessments[0]

    instrument_id = (
        first_assessment.instrument_id
    )

    market_id = first_assessment.market_id

    for assessment in risk_assessments:
        if (
            assessment.instrument_id
            != instrument_id
        ):
            raise ValueError(
                "Risk assessments must reference "
                "one instrument."
            )

        if assessment.market_id != market_id:
            raise ValueError(
                "Risk assessments must reference "
                "one market."
            )

    return (
        instrument_id,
        market_id,
    )


def _required_dimensions(
    mandate: TreasuryMandate,
) -> tuple[str, ...]:
    if (
        mandate.capital_preservation_priority
        == "very_high"
    ):
        return (
            VERY_HIGH_CAPITAL_PRESERVATION_REQUIRED_DIMENSIONS
        )

    return ()


def _acceptable_risk_levels(
    mandate: TreasuryMandate,
) -> tuple[str, ...]:
    if (
        mandate.capital_preservation_priority
        == "very_high"
    ):
        return (
            VERY_HIGH_CAPITAL_PRESERVATION_ACCEPTABLE_LEVELS
        )

    return (
        "very_low",
        "low",
        "moderate",
        "high",
        "very_high",
        "not_applicable",
    )


def _risk_evidence_requirement(
    assessment: RiskAssessment,
) -> str:
    return (
        "Sufficient risk evidence is required for "
        f"'{assessment.risk_dimension}' before this "
        "opportunity can be recommendation-ready under "
        "the very-high-capital-preservation mandate. "
        f"Current assessment: {assessment.rationale}"
    )


def _risk_blocking_reason(
    assessment: RiskAssessment,
) -> str:
    return (
        "Known risk level is not acceptable for "
        f"'{assessment.risk_dimension}' under the "
        "very-high-capital-preservation mandate. "
        f"Current risk level: {assessment.risk_level}. "
        f"Assessment rationale: {assessment.rationale}"
    )


def assess_risk_evidence_sufficiency(
    *,
    mandate: TreasuryMandate,
    risk_assessments: tuple[
        RiskAssessment,
        ...
    ],
) -> RiskEvidenceSufficiencyAssessment:
    indexed = _index_risk_assessments(
        risk_assessments
    )

    (
        instrument_id,
        market_id,
    ) = _validate_entity_alignment(
        risk_assessments
    )

    required_dimensions = _required_dimensions(
        mandate
    )

    acceptable_levels = _acceptable_risk_levels(
        mandate
    )

    insufficient_dimensions = tuple(
        dimension
        for dimension in required_dimensions
        if not indexed[
            dimension
        ].evidence_sufficient
    )

    unacceptable_dimensions = tuple(
        dimension
        for dimension in required_dimensions
        if (
            indexed[dimension].evidence_sufficient
            and indexed[dimension].risk_level
            not in acceptable_levels
        )
    )

    evidence_requirements = tuple(
        _risk_evidence_requirement(
            indexed[dimension]
        )
        for dimension in insufficient_dimensions
    )

    risk_blocking_reasons = tuple(
        _risk_blocking_reason(
            indexed[dimension]
        )
        for dimension in unacceptable_dimensions
    )

    evidence_sufficient = (
        len(insufficient_dimensions) == 0
    )

    risk_acceptable = (
        len(unacceptable_dimensions) == 0
    )

    return RiskEvidenceSufficiencyAssessment(
        mandate_id=mandate.mandate_id,
        instrument_id=instrument_id,
        market_id=market_id,
        required_dimensions=required_dimensions,
        insufficient_dimensions=(
            insufficient_dimensions
        ),
        unacceptable_dimensions=(
            unacceptable_dimensions
        ),
        evidence_requirements=(
            evidence_requirements
        ),
        risk_blocking_reasons=(
            risk_blocking_reasons
        ),
        evidence_sufficient=(
            evidence_sufficient
        ),
        risk_acceptable=(
            risk_acceptable
        ),
        sufficient_for_recommendation=(
            evidence_sufficient
            and risk_acceptable
        ),
        notes=(
            "Liquidity is deliberately excluded from "
            "this base-risk gate. Treasury liquidity "
            "requirements are evaluated separately using "
            "position-size-aware liquidity evidence and "
            "position risk. Unknown required risks create "
            "evidence requirements. Known required risks "
            "outside mandate tolerance create blockers."
        ),
    )