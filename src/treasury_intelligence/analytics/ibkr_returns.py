from __future__ import annotations

from treasury_intelligence.analytics.access_returns import (
    apply_access_cost_evidence,
)

from treasury_intelligence.analytics.broker_returns import (
    apply_broker_trading_cost_evidence,
)

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

from treasury_intelligence.sources.ibkr import (
    BrokerRecurringAccessCostEvidence,
    BrokerTradingCostEvidence,
)


def build_ibkr_return_components(
    *,
    instrument: Instrument,
    market: Market,
    snapshot: OpportunitySnapshot,
    reference_yield_includes_product_fee: bool | None,
    access_cost_evidence: BrokerRecurringAccessCostEvidence,
    trading_cost_evidence: BrokerTradingCostEvidence,
    estimated_roundtrip_slippage_bps: float | None = None,
    estimated_slippage_basis: str | None = None,
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

    components = apply_access_cost_evidence(
        components=components,
        access_cost_evidence=(
            access_cost_evidence
        ),
        component_id=access_component_id,
    )

    components = (
        apply_broker_trading_cost_evidence(
            components=components,
            trading_cost_evidence=(
                trading_cost_evidence
            ),
            entry_component_id=(
                entry_component_id
            ),
            exit_component_id=(
                exit_component_id
            ),
        )
    )

    if estimated_roundtrip_slippage_bps is None:
        return components

    return apply_estimated_roundtrip_slippage(
        components=components,
        component_id=slippage_component_id,
        roundtrip_bps=(
            estimated_roundtrip_slippage_bps
        ),
        estimate_basis=(
            estimated_slippage_basis
            or (
                "Conservative modeled execution "
                "estimate for the supplied route"
            )
        ),
    )
