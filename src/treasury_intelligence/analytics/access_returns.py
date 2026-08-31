from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.models.returns import (
    ReturnComponent,
)
from treasury_intelligence.sources.ibkr import (
    BrokerRecurringAccessCostEvidence,
)


def apply_access_cost_evidence(
    components: tuple[ReturnComponent, ...],
    access_cost_evidence: BrokerRecurringAccessCostEvidence,
    component_id: str,
    label: str | None = None,
) -> tuple[ReturnComponent, ...]:
    if not components:
        raise ValueError(
            "Return components are required."
        )

    if not component_id:
        raise ValueError(
            "component_id is required."
        )

    matching_components = tuple(
        component
        for component in components
        if component.component_id == component_id
    )

    if len(matching_components) != 1:
        raise ValueError(
            "Exactly one matching access-fee "
            "component is required."
        )

    access_fee_component = matching_components[0]

    if access_fee_component.component_type != "access_fee":
        raise ValueError(
            "The matching return component must "
            "have component_type='access_fee'."
        )

    if (
        access_cost_evidence
        .generic_custody_fee_identified
    ):
        raise ValueError(
            "Cannot apply recurring access-cost "
            "evidence when a generic custody fee "
            "has been identified but is not "
            "included in the modeled recurring "
            "access cost."
        )

    source_reference = None

    if access_cost_evidence.source_references:
        source_reference = (
            access_cost_evidence
            .source_references[0]
        )

    enriched_label = label

    if enriched_label is None:
        enriched_label = (
            "Published recurring access cost for "
            f"{access_cost_evidence.product_scope}"
        )

    evidence_notes = (
        access_cost_evidence.notes
        or (
            "Recurring access-cost evidence is "
            "applied only to the modeled access "
            "route and product scope. Specific "
            "future account terms may still "
            "require execution-stage confirmation."
        )
    )

    enriched_components: list[ReturnComponent] = []

    for component in components:
        if component.component_id != component_id:
            enriched_components.append(
                component
            )
            continue

        enriched_components.append(
            replace(
                component,
                label=enriched_label,
                status="published",
                basis="annualized_pct",
                value=(
                    access_cost_evidence
                    .recurring_access_cost_pct
                ),
                source=access_cost_evidence.broker,
                source_url=source_reference,
                notes=evidence_notes,
            )
        )

    return tuple(enriched_components)