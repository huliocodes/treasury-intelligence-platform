from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.models.execution_evidence import (
    PositionExecutionEvidence,
)
from treasury_intelligence.models.returns import (
    ReturnComponent,
)


def apply_position_execution_evidence(
    components: tuple[ReturnComponent, ...],
    execution_evidence: PositionExecutionEvidence,
    component_id: str,
    label: str | None = None,
    source: str | None = None,
    notes: str | None = None,
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
            "Exactly one matching execution-cost "
            "component is required."
        )

    execution_component = matching_components[0]

    if execution_component.component_type not in (
        "entry_execution_cost",
        "exit_execution_cost",
        "slippage_price_impact",
        "liquidity_cost",
        "other_cost",
    ):
        raise ValueError(
            "The matching return component must "
            "represent an execution-related cost."
        )

    if (
        execution_evidence.position_sized_cost_supported
        and execution_evidence.observed_roundtrip_cost_bps
        is None
    ):
        raise ValueError(
            "Supported position-sized execution "
            "evidence requires an observed "
            "roundtrip cost."
        )

    if (
        execution_evidence.position_sized_cost_supported
        and execution_evidence.execution_evidence_status
        != "supported"
    ):
        raise ValueError(
            "Position-sized execution cost cannot "
            "be applied when execution evidence "
            "status is not supported."
        )

    if (
        not execution_evidence
        .position_sized_cost_supported
    ):
        return components

    source_reference = None

    if execution_evidence.source_references:
        source_reference = (
            execution_evidence
            .source_references[0]
        )

    enriched_label = (
        label
        or (
            "Position-sized implicit "
            "execution cost"
        )
    )

    enriched_notes = (
        notes
        or execution_evidence.notes
        or (
            "Position-sized execution-cost "
            "evidence is applied only to the "
            "requested position size supported "
            "by the evidence. The observed "
            "roundtrip cost must not be "
            "extrapolated to unsupported "
            "position sizes."
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
                basis="position_bps",
                value=(
                    execution_evidence
                    .observed_roundtrip_cost_bps
                ),
                source=source,
                source_url=source_reference,
                notes=enriched_notes,
            )
        )

    return tuple(enriched_components)


XEON_SPREAD_SLIPPAGE_COMPONENT_ID = (
    "xeon_spread_slippage"
)


def apply_xeon_execution_evidence(
    components: tuple[ReturnComponent, ...],
    execution_evidence: PositionExecutionEvidence,
) -> tuple[ReturnComponent, ...]:
    """
    Temporary compatibility wrapper.

    XEON callers will be migrated to the generic
    apply_position_execution_evidence() interface
    during architecture consolidation. New
    analytics code should not use this wrapper.
    """

    return apply_position_execution_evidence(
        components=components,
        execution_evidence=execution_evidence,
        component_id=(
            XEON_SPREAD_SLIPPAGE_COMPONENT_ID
        ),
        label=(
            "XEON position-sized Xetra "
            "implicit execution cost"
        ),
        source="Deutsche Boerse Xetra",
        notes=(
            "Published Xetra Liquidity Measure "
            "is applied only because the "
            "treasury position exactly matches "
            "the order size for which the XLM "
            "was measured. The observed "
            "roundtrip implicit transaction "
            "cost includes market impact for "
            "that measured order size. This "
            "value must not be extrapolated to "
            "larger positions."
        ),
    )