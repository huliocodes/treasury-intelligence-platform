from __future__ import annotations

from treasury_intelligence.models.discovery_screening import (
    DiscoveryOpportunity,
    DiscoveryScreeningResult,
)
from treasury_intelligence.models.research_triage import (
    EvidenceDimension,
    ResearchAction,
    ResearchEvidenceState,
    ResearchTriageResult,
)


_EVIDENCE_DIMENSIONS: tuple[
    tuple[EvidenceDimension, str],
    ...,
] = (
    ("identity", "identity_evidence_sufficient"),
    (
        "corporate_access",
        "corporate_access_evidence_sufficient",
    ),
    (
        "current_market_return",
        "current_market_return_evidence_sufficient",
    ),
    (
        "realistic_net_return",
        "realistic_net_return_evidence_sufficient",
    ),
    (
        "position_liquidity",
        "position_liquidity_evidence_sufficient",
    ),
    (
        "execution_cost",
        "execution_cost_evidence_sufficient",
    ),
    (
        "risk_evidence",
        "risk_evidence_sufficient",
    ),
)


def build_research_triage(
    opportunities: tuple[DiscoveryOpportunity, ...],
    screening_results: tuple[DiscoveryScreeningResult, ...],
    evidence_states: tuple[ResearchEvidenceState, ...],
) -> tuple[ResearchTriageResult, ...]:
    opportunity_by_id = _index_opportunities(opportunities)
    screening_by_id = _index_screening_results(screening_results)
    evidence_by_id = _index_evidence_states(evidence_states)

    research_candidate_ids = {
        result.opportunity_id
        for result in screening_results
        if result.suitable_for_full_research
    }

    missing_evidence_state_ids = (
        research_candidate_ids - evidence_by_id.keys()
    )

    if missing_evidence_state_ids:
        raise ValueError(
            "Missing ResearchEvidenceState entries for research candidates: "
            + ", ".join(sorted(missing_evidence_state_ids))
        )

    unexpected_evidence_state_ids = (
        evidence_by_id.keys() - research_candidate_ids
    )

    if unexpected_evidence_state_ids:
        raise ValueError(
            "ResearchEvidenceState entries must only describe current "
            "research candidates. Unexpected opportunity_ids: "
            + ", ".join(sorted(unexpected_evidence_state_ids))
        )

    preliminary_results: list[
        tuple[
            DiscoveryOpportunity,
            ResearchEvidenceState,
            ResearchAction,
            tuple[EvidenceDimension, ...],
            tuple[EvidenceDimension, ...],
            tuple[str, ...],
        ]
    ] = []

    for opportunity_id in research_candidate_ids:
        opportunity = opportunity_by_id[opportunity_id]
        screening_result = screening_by_id[opportunity_id]
        evidence_state = evidence_by_id[opportunity_id]

        if not screening_result.suitable_for_full_research:
            raise ValueError(
                "Research triage may only contain opportunities that passed "
                "discovery screening."
            )

        missing_evidence = _missing_evidence(evidence_state)
        reusable_evidence = _reusable_evidence(evidence_state)

        action = _select_action(
            evidence_state=evidence_state,
            missing_evidence=missing_evidence,
        )

        rationale = _build_rationale(
            evidence_state=evidence_state,
            action=action,
            missing_evidence=missing_evidence,
        )

        preliminary_results.append(
            (
                opportunity,
                evidence_state,
                action,
                missing_evidence,
                reusable_evidence,
                rationale,
            )
        )

    research_required = [
        item
        for item in preliminary_results
        if item[2] != "reuse_existing_analysis"
    ]

    research_required.sort(
        key=lambda item: _research_sort_key(
            opportunity=item[0],
            action=item[2],
            missing_evidence=item[3],
        )
    )

    rank_by_opportunity_id = {
        item[0].opportunity_id: index
        for index, item in enumerate(
            research_required,
            start=1,
        )
    }

    final_results = [
        ResearchTriageResult(
            opportunity_id=opportunity.opportunity_id,
            display_name=opportunity.display_name,
            discovery_priority=opportunity.discovery_priority,
            action=action,
            missing_evidence=missing_evidence,
            reusable_evidence=reusable_evidence,
            research_required=(
                action != "reuse_existing_analysis"
            ),
            research_rank=rank_by_opportunity_id.get(
                opportunity.opportunity_id
            ),
            rationale=rationale,
        )
        for (
            opportunity,
            _,
            action,
            missing_evidence,
            reusable_evidence,
            rationale,
        ) in preliminary_results
    ]

    return tuple(
        sorted(
            final_results,
            key=_final_result_sort_key,
        )
    )


def _select_action(
    evidence_state: ResearchEvidenceState,
    missing_evidence: tuple[EvidenceDimension, ...],
) -> ResearchAction:
    if evidence_state.prior_analysis_status == "complete":
        if missing_evidence:
            raise ValueError(
                "Complete prior analysis cannot contain missing evidence."
            )

        return "reuse_existing_analysis"

    if evidence_state.prior_analysis_status == "partial":
        if not missing_evidence:
            raise ValueError(
                "Partial prior analysis must identify evidence that remains "
                "incomplete."
            )

        return "refresh_existing_analysis"

    if not missing_evidence:
        raise ValueError(
            "An opportunity with no prior analysis must identify missing "
            "evidence before it can enter research triage."
        )

    return "complete_missing_analysis"


def _missing_evidence(
    evidence_state: ResearchEvidenceState,
) -> tuple[EvidenceDimension, ...]:
    return tuple(
        dimension
        for dimension, attribute_name in _EVIDENCE_DIMENSIONS
        if not getattr(evidence_state, attribute_name)
    )


def _reusable_evidence(
    evidence_state: ResearchEvidenceState,
) -> tuple[EvidenceDimension, ...]:
    return tuple(
        dimension
        for dimension, attribute_name in _EVIDENCE_DIMENSIONS
        if getattr(evidence_state, attribute_name)
    )


def _build_rationale(
    evidence_state: ResearchEvidenceState,
    action: ResearchAction,
    missing_evidence: tuple[EvidenceDimension, ...],
) -> tuple[str, ...]:
    rationale: list[str] = []

    if action == "reuse_existing_analysis":
        rationale.append(
            "Existing V1 analysis is already complete across the required "
            "research dimensions."
        )

    elif action == "refresh_existing_analysis":
        rationale.append(
            "A prior candidate analysis exists and should be reused where "
            "possible rather than rebuilt from scratch."
        )

        rationale.append(
            "Remaining evidence gaps: "
            + ", ".join(missing_evidence)
            + "."
        )

    else:
        rationale.append(
            "The opportunity passed discovery screening but does not yet "
            "have a complete downstream candidate analysis."
        )

        rationale.append(
            "Required evidence: "
            + ", ".join(missing_evidence)
            + "."
        )

    if evidence_state.reusable_analysis_summary:
        rationale.append(
            evidence_state.reusable_analysis_summary
        )

    rationale.extend(evidence_state.evidence_notes)

    return tuple(rationale)


def _research_sort_key(
    opportunity: DiscoveryOpportunity,
    action: ResearchAction,
    missing_evidence: tuple[EvidenceDimension, ...],
) -> tuple[int, int, int, str]:
    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    action_order = {
        "refresh_existing_analysis": 0,
        "complete_missing_analysis": 1,
        "reuse_existing_analysis": 2,
    }

    return (
        priority_order[opportunity.discovery_priority],
        action_order[action],
        len(missing_evidence),
        opportunity.opportunity_id,
    )


def _final_result_sort_key(
    result: ResearchTriageResult,
) -> tuple[int, int, str]:
    if result.research_required:
        return (
            0,
            result.research_rank or 0,
            result.opportunity_id,
        )

    return (
        1,
        0,
        result.opportunity_id,
    )


def _index_opportunities(
    opportunities: tuple[DiscoveryOpportunity, ...],
) -> dict[str, DiscoveryOpportunity]:
    indexed: dict[str, DiscoveryOpportunity] = {}

    for opportunity in opportunities:
        if opportunity.opportunity_id in indexed:
            raise ValueError(
                "Duplicate DiscoveryOpportunity opportunity_id: "
                f"{opportunity.opportunity_id}"
            )

        indexed[opportunity.opportunity_id] = opportunity

    return indexed


def _index_screening_results(
    screening_results: tuple[DiscoveryScreeningResult, ...],
) -> dict[str, DiscoveryScreeningResult]:
    indexed: dict[str, DiscoveryScreeningResult] = {}

    for result in screening_results:
        if result.opportunity_id in indexed:
            raise ValueError(
                "Duplicate DiscoveryScreeningResult opportunity_id: "
                f"{result.opportunity_id}"
            )

        indexed[result.opportunity_id] = result

    return indexed


def _index_evidence_states(
    evidence_states: tuple[ResearchEvidenceState, ...],
) -> dict[str, ResearchEvidenceState]:
    indexed: dict[str, ResearchEvidenceState] = {}

    for state in evidence_states:
        if state.opportunity_id in indexed:
            raise ValueError(
                "Duplicate ResearchEvidenceState opportunity_id: "
                f"{state.opportunity_id}"
            )

        indexed[state.opportunity_id] = state

    return indexed