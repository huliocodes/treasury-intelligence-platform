from __future__ import annotations

from treasury_intelligence.models.economic_comparisons import (
    AllocationReturnInput,
)

from treasury_intelligence.models.economics import (
    EconomicsEvidenceAssessment,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.models.returns import (
    ReturnAnalysis,
)

from treasury_intelligence.models.switching_friction import (
    SwitchingFrictionInput,
)


def build_allocation_return_input(
    label: str,
    return_analysis: ReturnAnalysis,
    economics: EconomicsEvidenceAssessment,
    notes: str | None = None,
) -> AllocationReturnInput:
    if (
        economics.return_analysis_id
        != return_analysis.analysis_id
    ):
        raise ValueError(
            "Economics evidence assessment does not "
            "belong to the supplied return analysis."
        )

    if (
        economics.instrument_id
        != return_analysis.instrument_id
    ):
        raise ValueError(
            "Economics evidence assessment and return "
            "analysis use different instruments."
        )

    if (
        economics.market_id
        != return_analysis.market_id
    ):
        raise ValueError(
            "Economics evidence assessment and return "
            "analysis use different markets."
        )

    if (
        economics.access_route_id
        != return_analysis.access_route_id
    ):
        raise ValueError(
            "Economics evidence assessment and return "
            "analysis use different access routes."
        )

    if (
        abs(
            economics.position_size_eur
            - return_analysis.position_size_eur
        )
        > 0.01
    ):
        raise ValueError(
            "Economics evidence assessment and return "
            "analysis use different position sizes."
        )

    if (
        economics.holding_period_days
        != return_analysis.holding_period_days
    ):
        raise ValueError(
            "Economics evidence assessment and return "
            "analysis use different holding periods."
        )

    evidence_available = (
        economics.economics_status == "complete"
        and economics.realistic_expected_return_available
        and return_analysis.economics_complete
        and return_analysis.realistic_expected_return_pct
        is not None
    )

    if evidence_available:
        annual_return_pct = (
            return_analysis.realistic_expected_return_pct
        )

        source_reference = (
            return_analysis.analysis_id
        )

    else:
        annual_return_pct = None

        source_reference = (
            economics.assessment_id
        )

    return AllocationReturnInput(
        instrument_id=(
            return_analysis.instrument_id
        ),
        market_id=(
            return_analysis.market_id
        ),
        access_route_id=(
            return_analysis.access_route_id
        ),
        label=label,
        annual_return_pct=annual_return_pct,
        evidence_available=evidence_available,
        source_reference=source_reference,
        notes=notes,
    )


def build_candidate_allocation_return_input(
    candidate: PortfolioCandidateAssessment,
    notes: str | None = None,
) -> AllocationReturnInput:
    evidence_available = (
        candidate.recommendation_ready
        and candidate.candidate_status
        == "recommendation_ready"
        and candidate.economics_status
        == "complete"
        and candidate.defensible_return_pct
        is not None
    )

    if evidence_available:
        annual_return_pct = (
            candidate.defensible_return_pct
        )
    else:
        annual_return_pct = None

    return AllocationReturnInput(
        instrument_id=candidate.instrument_id,
        market_id=candidate.market_id,
        access_route_id=candidate.access_route_id,
        label=candidate.label,
        annual_return_pct=annual_return_pct,
        evidence_available=evidence_available,
        source_reference=(
            candidate.assessment_id
        ),
        notes=(
            notes
            or (
                "Review-return input derived from the "
                "production portfolio candidate's "
                "defensible return assessment."
            )
        ),
    )


def build_candidate_embedded_switching_friction_input(
    candidate: PortfolioCandidateAssessment,
    action: str,
    notes: str | None = None,
) -> SwitchingFrictionInput:
    if action not in (
        "open",
        "increase",
    ):
        raise ValueError(
            "Candidate-embedded switching friction "
            "can only support open or increase actions."
        )

    entry_cost_embedded = (
        "entry_execution_cost"
        in candidate.embedded_one_time_cost_component_types
    )

    evidence_available = (
        candidate.recommendation_ready
        and candidate.candidate_status
        == "recommendation_ready"
        and candidate.economics_status
        == "complete"
        and candidate.defensible_return_pct
        is not None
        and entry_cost_embedded
    )

    if evidence_available:
        friction_bps = 0.0
        fixed_cost_eur = 0.0

        default_notes = (
            "Additional switching friction is zero "
            "because the recommendation-ready "
            "candidate return already embeds its "
            "entry execution economics. Embedded "
            "one-time cost component types: "
            + ", ".join(
                candidate
                .embedded_one_time_cost_component_types
            )
            + ". Any separately evidenced transition "
            "cost not represented in candidate return "
            "economics must be supplied separately "
            "rather than double-counted here."
        )

    else:
        friction_bps = None
        fixed_cost_eur = None

        default_notes = (
            "Zero additional switching friction cannot "
            "be established from candidate return "
            "provenance. Recommendation-ready complete "
            "economics with an embedded "
            "entry_execution_cost are required."
        )

    return SwitchingFrictionInput(
        instrument_id=candidate.instrument_id,
        market_id=candidate.market_id,
        access_route_id=candidate.access_route_id,
        label=candidate.label,
        action=action,
        friction_bps=friction_bps,
        fixed_cost_eur=fixed_cost_eur,
        evidence_available=evidence_available,
        source_reference=(
            candidate.assessment_id
        ),
        notes=(
            notes
            or default_notes
        ),
    )
