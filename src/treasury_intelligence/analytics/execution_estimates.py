from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.models.returns import (
    ReturnComponent,
)


ETF_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS = 10.0

SOVEREIGN_BILL_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS = 5.0


def apply_estimated_roundtrip_slippage(
    components: tuple[ReturnComponent, ...],
    component_id: str,
    roundtrip_bps: float,
    estimate_basis: str,
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

    if roundtrip_bps < 0:
        raise ValueError(
            "roundtrip_bps cannot be negative."
        )

    if not estimate_basis:
        raise ValueError(
            "estimate_basis is required."
        )

    matches = tuple(
        component
        for component in components
        if component.component_id == component_id
    )

    if len(matches) != 1:
        raise ValueError(
            "Exactly one matching slippage component "
            "is required."
        )

    component = matches[0]

    if (
        component.component_type
        != "slippage_price_impact"
    ):
        raise ValueError(
            "The target component must have "
            "component_type='slippage_price_impact'."
        )

    estimate_notes = (
        notes
        or (
            "Conservative modeled round-trip execution "
            "friction. This is an estimate rather than "
            "an executable quote. Direct position-sized "
            "execution evidence should override the "
            "estimate when available."
        )
    )

    enriched_components: list[
        ReturnComponent
    ] = []

    for existing in components:
        if existing.component_id == component_id:
            enriched_components.append(
                replace(
                    existing,
                    label=(
                        "Estimated round-trip spread, "
                        "slippage, and market impact"
                    ),
                    status="estimated",
                    basis="position_bps",
                    value=roundtrip_bps,
                    source="Treasury Intelligence model",
                    source_url=None,
                    notes=(
                        f"{estimate_basis}. "
                        f"{estimate_notes}"
                    ),
                )
            )
            continue

        enriched_components.append(
            existing
        )

    return tuple(enriched_components)
