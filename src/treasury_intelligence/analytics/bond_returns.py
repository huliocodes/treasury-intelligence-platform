from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.analytics.execution_estimates import (
    apply_estimated_roundtrip_slippage,
)

from treasury_intelligence.analytics.generic_returns import (
    build_conservative_return_components,
)

from treasury_intelligence.models.opportunities import (
    Instrument,
    Market,
    OpportunitySnapshot,
)

from treasury_intelligence.models.returns import (
    ReturnComponent,
)

from treasury_intelligence.sources.ibkr_fixed_income import (
    EuropeOtcBondCommissionEvidence,
)


def calculate_tiered_otc_bond_commission_eur(
    position_size_eur: float,
    evidence: EuropeOtcBondCommissionEvidence,
) -> float:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    first_tier_value_eur = min(
        position_size_eur,
        evidence.first_tier_limit_eur,
    )

    additional_value_eur = max(
        position_size_eur
        - evidence.first_tier_limit_eur,
        0.0,
    )

    first_tier_cost_eur = (
        first_tier_value_eur
        * evidence.first_tier_commission_bps
        / 10_000
    )

    additional_cost_eur = (
        additional_value_eur
        * evidence.additional_commission_bps
        / 10_000
    )

    return (
        first_tier_cost_eur
        + additional_cost_eur
    )


def calculate_tiered_otc_bond_commission_bps(
    position_size_eur: float,
    evidence: EuropeOtcBondCommissionEvidence,
) -> float:
    commission_eur = (
        calculate_tiered_otc_bond_commission_eur(
            position_size_eur=position_size_eur,
            evidence=evidence,
        )
    )

    return (
        commission_eur
        / position_size_eur
        * 10_000
    )


def build_ibkr_europe_otc_bond_return_components(
    *,
    instrument: Instrument,
    market: Market,
    snapshot: OpportunitySnapshot,
    position_size_eur: float,
    reference_yield_includes_product_fee: bool | None,
    trading_cost_evidence: EuropeOtcBondCommissionEvidence,
    estimated_roundtrip_slippage_bps: float,
) -> tuple[ReturnComponent, ...]:
    components = (
        build_conservative_return_components(
            instrument=instrument,
            market=market,
            snapshot=snapshot,
            reference_yield_includes_product_fee=(
                reference_yield_includes_product_fee
            ),
        )
    )

    access_component_id = (
        f"{snapshot.snapshot_id}_access_fee"
    )

    entry_component_id = (
        f"{snapshot.snapshot_id}_entry_execution"
    )

    exit_component_id = (
        f"{snapshot.snapshot_id}_exit_execution"
    )

    slippage_component_id = (
        f"{snapshot.snapshot_id}_slippage"
    )

    source_reference = (
        trading_cost_evidence.source_references[0]
        if trading_cost_evidence.source_references
        else None
    )

    one_way_commission_bps = (
        calculate_tiered_otc_bond_commission_bps(
            position_size_eur=position_size_eur,
            evidence=trading_cost_evidence,
        )
    )

    enriched_components: list[
        ReturnComponent
    ] = []

    for component in components:
        if component.component_id == access_component_id:
            enriched_components.append(
                replace(
                    component,
                    label=(
                        "Published IBKR recurring "
                        "organization-account cost"
                    ),
                    status="published",
                    basis="annualized_pct",
                    value=(
                        trading_cost_evidence
                        .recurring_access_cost_pct
                    ),
                    source=(
                        trading_cost_evidence.broker
                    ),
                    source_url=source_reference,
                    notes=(
                        "IBKR publishes zero account "
                        "minimums and inactivity fees for "
                        "organization accounts. Optional "
                        "services and transaction-specific "
                        "charges are treated separately."
                    ),
                )
            )
            continue

        if component.component_id == entry_component_id:
            enriched_components.append(
                replace(
                    component,
                    label=(
                        "Published IBKR Europe OTC "
                        "bond entry commission"
                    ),
                    status="published",
                    basis="position_bps",
                    value=one_way_commission_bps,
                    source=(
                        trading_cost_evidence.broker
                    ),
                    source_url=source_reference,
                    notes=(
                        trading_cost_evidence.notes
                    ),
                )
            )
            continue

        if component.component_id == exit_component_id:
            enriched_components.append(
                replace(
                    component,
                    label=(
                        "Published IBKR Europe OTC "
                        "bond exit commission"
                    ),
                    status="published",
                    basis="position_bps",
                    value=one_way_commission_bps,
                    source=(
                        trading_cost_evidence.broker
                    ),
                    source_url=source_reference,
                    notes=(
                        "Modeled using the same published "
                        "IBKR Europe OTC commission tiers "
                        "as the entry transaction."
                    ),
                )
            )
            continue

        enriched_components.append(
            component
        )

    return apply_estimated_roundtrip_slippage(
        components=tuple(enriched_components),
        component_id=slippage_component_id,
        roundtrip_bps=(
            estimated_roundtrip_slippage_bps
        ),
        estimate_basis=(
            "Conservative estimate for a strongly "
            "inferred liquid sovereign-bill position "
            "relative to issue scale and market structure"
        ),
    )
