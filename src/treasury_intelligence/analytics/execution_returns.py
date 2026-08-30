from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.models.execution_evidence import (
    PositionExecutionEvidence,
)


XEON_SPREAD_SLIPPAGE_COMPONENT_ID = (
    "xeon_spread_slippage"
)


def apply_xeon_execution_evidence(
    components: tuple,
    execution_evidence: PositionExecutionEvidence,
) -> tuple:
    if not components:
        raise ValueError(
            "Return components are required."
        )

    matching_components = tuple(
        component
        for component in components
        if getattr(
            component,
            "component_id",
            None,
        )
        == XEON_SPREAD_SLIPPAGE_COMPONENT_ID
    )

    if len(matching_components) != 1:
        raise ValueError(
            "Exactly one XEON spread/slippage "
            "component is required."
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

    enriched_components = []

    for component in components:
        if (
            component.component_id
            != XEON_SPREAD_SLIPPAGE_COMPONENT_ID
        ):
            enriched_components.append(
                component
            )
            continue

        if (
            not execution_evidence
            .position_sized_cost_supported
        ):
            enriched_components.append(
                component
            )
            continue

        source_reference = None

        if execution_evidence.source_references:
            source_reference = (
                execution_evidence
                .source_references[0]
            )

        enriched_component = replace(
            component,
            label=(
                "XEON position-sized Xetra "
                "implicit execution cost"
            ),
            status="published",
            basis="position_bps",
            value=(
                execution_evidence
                .observed_roundtrip_cost_bps
            ),
            source="Deutsche Boerse Xetra",
            source_url=source_reference,
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

        enriched_components.append(
            enriched_component
        )

    return tuple(
        enriched_components
    )