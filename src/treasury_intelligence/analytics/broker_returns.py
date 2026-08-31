from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.models.returns import (
    ReturnComponent,
)

from treasury_intelligence.sources.ibkr import (
    BrokerTradingCostEvidence,
)


EXECUTION_COMPONENT_TYPES = (
    "entry_execution_cost",
    "exit_execution_cost",
)


def apply_broker_trading_cost_evidence(
    components: tuple[ReturnComponent, ...],
    trading_cost_evidence: BrokerTradingCostEvidence,
    entry_component_id: str,
    exit_component_id: str,
    entry_label: str | None = None,
    exit_label: str | None = None,
) -> tuple[ReturnComponent, ...]:
    if not components:
        raise ValueError(
            "Return components are required."
        )

    if not entry_component_id:
        raise ValueError(
            "entry_component_id is required."
        )

    if not exit_component_id:
        raise ValueError(
            "exit_component_id is required."
        )

    if entry_component_id == exit_component_id:
        raise ValueError(
            "Entry and exit component IDs must differ."
        )

    matching_entry = tuple(
        component
        for component in components
        if component.component_id
        == entry_component_id
    )

    matching_exit = tuple(
        component
        for component in components
        if component.component_id
        == exit_component_id
    )

    if len(matching_entry) != 1:
        raise ValueError(
            "Exactly one matching entry execution "
            "component is required."
        )

    if len(matching_exit) != 1:
        raise ValueError(
            "Exactly one matching exit execution "
            "component is required."
        )

    entry_component = matching_entry[0]
    exit_component = matching_exit[0]

    if (
        entry_component.component_type
        != "entry_execution_cost"
    ):
        raise ValueError(
            "The entry component must have "
            "component_type='entry_execution_cost'."
        )

    if (
        exit_component.component_type
        != "exit_execution_cost"
    ):
        raise ValueError(
            "The exit component must have "
            "component_type='exit_execution_cost'."
        )

    source_reference = None

    if trading_cost_evidence.source_references:
        source_reference = (
            trading_cost_evidence
            .source_references[0]
        )

    default_entry_label = (
        f"Published {trading_cost_evidence.broker} "
        f"{trading_cost_evidence.market_country} "
        "entry commission"
    )

    default_exit_label = (
        f"Published {trading_cost_evidence.broker} "
        f"{trading_cost_evidence.market_country} "
        "exit commission"
    )

    evidence_notes = (
        trading_cost_evidence.notes
        or (
            "Published broker commission evidence is "
            "applied to the modeled access route. "
            "This covers the broker commission only "
            "and does not establish bid-ask spread, "
            "slippage, market impact, liquidity, taxes, "
            "or account-specific execution terms."
        )
    )

    enriched_components: list[
        ReturnComponent
    ] = []

    for component in components:
        if (
            component.component_id
            == entry_component_id
        ):
            enriched_components.append(
                replace(
                    component,
                    label=(
                        entry_label
                        or default_entry_label
                    ),
                    status="published",
                    basis="position_bps",
                    value=(
                        trading_cost_evidence
                        .commission_bps
                    ),
                    source=(
                        trading_cost_evidence
                        .broker
                    ),
                    source_url=source_reference,
                    notes=evidence_notes,
                )
            )
            continue

        if (
            component.component_id
            == exit_component_id
        ):
            enriched_components.append(
                replace(
                    component,
                    label=(
                        exit_label
                        or default_exit_label
                    ),
                    status="published",
                    basis="position_bps",
                    value=(
                        trading_cost_evidence
                        .commission_bps
                    ),
                    source=(
                        trading_cost_evidence
                        .broker
                    ),
                    source_url=source_reference,
                    notes=evidence_notes,
                )
            )
            continue

        enriched_components.append(
            component
        )

    return tuple(enriched_components)
