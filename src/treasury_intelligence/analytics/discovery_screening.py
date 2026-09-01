from __future__ import annotations

from treasury_intelligence.models.discovery_screening import (
    DiscoveryOpportunity,
    DiscoveryScreeningContext,
    DiscoveryScreeningResult,
)


def screen_discovery_opportunity(
    opportunity: DiscoveryOpportunity,
    context: DiscoveryScreeningContext,
) -> DiscoveryScreeningResult:
    screening_reasons: list[str] = []
    evidence_requirements: list[str] = []

    if opportunity.mandate_relevance == "none":
        screening_reasons.append(
            "Opportunity is explicitly outside the current treasury mandate."
        )

        return _build_result(
            opportunity=opportunity,
            status="screened_out",
            screening_reasons=screening_reasons,
            evidence_requirements=evidence_requirements,
        )

    if opportunity.known_hard_mandate_conflict:
        screening_reasons.append(
            opportunity.known_hard_mandate_conflict_reason
            or "Opportunity has a known hard mandate conflict."
        )

        return _build_result(
            opportunity=opportunity,
            status="screened_out",
            screening_reasons=screening_reasons,
            evidence_requirements=evidence_requirements,
        )

    if (
        opportunity.minimum_investment_eur is not None
        and opportunity.minimum_investment_eur
        > context.treasury_capital_eur
    ):
        screening_reasons.append(
            "Minimum investment exceeds total treasury capital: "
            f"€{opportunity.minimum_investment_eur:,.0f} minimum "
            f"vs €{context.treasury_capital_eur:,.0f} treasury."
        )

        return _build_result(
            opportunity=opportunity,
            status="screened_out",
            screening_reasons=screening_reasons,
            evidence_requirements=evidence_requirements,
        )

    if (
        opportunity.maximum_plausible_allocation_eur is not None
        and opportunity.maximum_plausible_allocation_eur
        < context.minimum_useful_allocation_eur
    ):
        screening_reasons.append(
            "Maximum plausible allocation is below the mandate's "
            "minimum useful allocation: "
            f"€{opportunity.maximum_plausible_allocation_eur:,.0f} "
            f"capacity vs "
            f"€{context.minimum_useful_allocation_eur:,.0f} minimum."
        )

        return _build_result(
            opportunity=opportunity,
            status="screened_out",
            screening_reasons=screening_reasons,
            evidence_requirements=evidence_requirements,
        )

    if opportunity.currency is None:
        evidence_requirements.append(
            "Verify instrument or economic exposure currency."
        )
    elif opportunity.currency not in context.allowed_currencies:
        screening_reasons.append(
            f"Currency {opportunity.currency} is not allowed by the "
            "current treasury screening context."
        )

        return _build_result(
            opportunity=opportunity,
            status="screened_out",
            screening_reasons=screening_reasons,
            evidence_requirements=evidence_requirements,
        )

    if opportunity.slovenian_doo_access_status == "blocked":
        screening_reasons.append(
            "Known Slovenian d.o.o. corporate access route is blocked."
        )

        return _build_result(
            opportunity=opportunity,
            status="access_blocked",
            screening_reasons=screening_reasons,
            evidence_requirements=evidence_requirements,
        )

    if opportunity.possible_access_route is None:
        evidence_requirements.append(
            "Identify a plausible Slovenian d.o.o. access route."
        )

    if opportunity.slovenian_doo_access_status == "unknown":
        evidence_requirements.append(
            "Verify whether a Slovenian d.o.o. can access the opportunity."
        )

    if (
        opportunity.slovenian_doo_access_status == "plausible"
        and not opportunity.access_evidence_sufficient
    ):
        evidence_requirements.append(
            "Upgrade plausible corporate access to sufficiently "
            "verified evidence."
        )

    if (
        context.require_verified_corporate_access
        and (
            opportunity.slovenian_doo_access_status != "verified"
            or not opportunity.access_evidence_sufficient
        )
    ):
        return _build_result(
            opportunity=opportunity,
            status="access_unknown",
            screening_reasons=screening_reasons,
            evidence_requirements=_deduplicate(
                evidence_requirements
            ),
        )

    if evidence_requirements:
        return _build_result(
            opportunity=opportunity,
            status="access_unknown",
            screening_reasons=screening_reasons,
            evidence_requirements=_deduplicate(
                evidence_requirements
            ),
        )

    screening_reasons.append(
        "No discovery-level hard mandate conflict was identified."
    )
    screening_reasons.append(
        "Corporate access is sufficiently verified for discovery screening."
    )
    screening_reasons.append(
        "Opportunity is large enough for at least the minimum useful "
        "allocation where capacity evidence is available."
    )

    return _build_result(
        opportunity=opportunity,
        status="research_candidate",
        screening_reasons=screening_reasons,
        evidence_requirements=(),
    )


def screen_discovery_universe(
    opportunities: tuple[DiscoveryOpportunity, ...],
    context: DiscoveryScreeningContext,
) -> tuple[DiscoveryScreeningResult, ...]:
    opportunity_ids: set[str] = set()
    results: list[DiscoveryScreeningResult] = []

    for opportunity in opportunities:
        if opportunity.opportunity_id in opportunity_ids:
            raise ValueError(
                "Duplicate discovery opportunity_id: "
                f"{opportunity.opportunity_id}"
            )

        opportunity_ids.add(opportunity.opportunity_id)

        results.append(
            screen_discovery_opportunity(
                opportunity=opportunity,
                context=context,
            )
        )

    return tuple(results)


def _build_result(
    opportunity: DiscoveryOpportunity,
    status: str,
    screening_reasons: list[str] | tuple[str, ...],
    evidence_requirements: list[str] | tuple[str, ...],
) -> DiscoveryScreeningResult:
    valid_statuses = {
        "discovered",
        "screened_out",
        "research_candidate",
        "access_unknown",
        "access_blocked",
    }

    if status not in valid_statuses:
        raise ValueError(f"Unsupported discovery status: {status}")

    return DiscoveryScreeningResult(
        opportunity_id=opportunity.opportunity_id,
        display_name=opportunity.display_name,
        category=opportunity.category,
        status=status,
        research_priority=opportunity.discovery_priority,
        screening_reasons=tuple(screening_reasons),
        evidence_requirements=tuple(evidence_requirements),
        corporate_access_status=(
            opportunity.slovenian_doo_access_status
        ),
        access_evidence_sufficient=(
            opportunity.access_evidence_sufficient
        ),
        suitable_for_full_research=(
            status == "research_candidate"
        ),
    )


def _deduplicate(
    values: list[str] | tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))