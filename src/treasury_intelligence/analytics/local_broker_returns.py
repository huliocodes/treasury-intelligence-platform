from __future__ import annotations

from dataclasses import replace

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


def build_local_broker_return_components(
    *,
    instrument: Instrument,
    market: Market,
    snapshot: OpportunitySnapshot,
    reference_yield_includes_product_fee: bool | None,
) -> tuple[ReturnComponent, ...]:
    components = build_conservative_return_components(
        instrument=instrument,
        market=market,
        snapshot=snapshot,
        reference_yield_includes_product_fee=(
            reference_yield_includes_product_fee
        ),
    )

    enriched: list[ReturnComponent] = []

    for component in components:
        if component.component_type == "access_fee":
            enriched.append(
                replace(
                    component,
                    label=(
                        "Slovenian corporate brokerage "
                        "recurring access cost"
                    ),
                    status="unknown",
                    basis="annualized_pct",
                    value=None,
                    notes=(
                        "A Slovenian corporate brokerage route "
                        "to LJSE is supported, but a sufficiently "
                        "specific published recurring custody or "
                        "account-cost schedule has not yet been "
                        "normalized for the modeled legal entity. "
                        "No zero cost is assumed."
                    ),
                )
            )
            continue

        if (
            component.component_type
            == "entry_execution_cost"
        ):
            enriched.append(
                replace(
                    component,
                    label=(
                        "LJSE corporate broker entry commission"
                    ),
                    status="unknown",
                    basis="position_bps",
                    value=None,
                    notes=(
                        "No sufficiently specific published "
                        "corporate commission schedule has yet "
                        "been normalized for the modeled "
                        "Slovenian brokerage route."
                    ),
                )
            )
            continue

        if (
            component.component_type
            == "exit_execution_cost"
        ):
            enriched.append(
                replace(
                    component,
                    label=(
                        "LJSE corporate broker exit commission"
                    ),
                    status="unknown",
                    basis="position_bps",
                    value=None,
                    notes=(
                        "No sufficiently specific published "
                        "corporate commission schedule has yet "
                        "been normalized for the modeled "
                        "Slovenian brokerage route."
                    ),
                )
            )
            continue

        if (
            component.component_type
            == "slippage_price_impact"
        ):
            enriched.append(
                replace(
                    component,
                    label=(
                        "ICASH round-trip spread, slippage "
                        "or market impact"
                    ),
                    status="unknown",
                    basis="position_bps",
                    value=None,
                    notes=(
                        "LJSE verifies a market maker, but the "
                        "published minimum quote obligation is "
                        "too small to support a treasury-size "
                        "execution-cost assumption. No generic "
                        "Xetra ETF slippage estimate is reused."
                    ),
                )
            )
            continue

        enriched.append(component)

    return tuple(enriched)
