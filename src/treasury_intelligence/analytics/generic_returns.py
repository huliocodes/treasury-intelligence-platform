from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    Instrument,
    Market,
    OpportunitySnapshot,
)

from treasury_intelligence.models.returns import (
    ReturnComponent,
)


def build_conservative_return_components(
    instrument: Instrument,
    market: Market,
    snapshot: OpportunitySnapshot,
    reference_yield_includes_product_fee: bool | None,
) -> tuple[ReturnComponent, ...]:
    if (
        snapshot.instrument_id
        != instrument.instrument_id
    ):
        raise ValueError(
            "Snapshot instrument does not match instrument."
        )

    if snapshot.market_id != market.market_id:
        raise ValueError(
            "Snapshot market does not match market."
        )

    reference_status = "published"

    if (
        snapshot.yield_measure
        == "benchmark_linked_estimate"
    ):
        reference_status = "model_derived"

    components: list[ReturnComponent] = [
        ReturnComponent(
            component_id=(
                f"{snapshot.snapshot_id}_reference_yield"
            ),
            component_type="reference_yield",
            label=(
                f"{instrument.name} reference yield"
            ),
            status=reference_status,
            basis="annualized_pct",
            value=snapshot.yield_value_pct,
            source=snapshot.source,
            source_url=snapshot.source_url,
            notes=(
                "Uses the normalized opportunity snapshot's "
                "reference yield exactly as stored. This is "
                "not automatically treated as an executable "
                "or realistic expected return."
            ),
        )
    ]

    if snapshot.annual_fee_pct is None:
        components.append(
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_product_fee"
                ),
                component_type="product_fee",
                label="Product fee",
                status="not_applicable",
                basis="annualized_pct",
                value=None,
                notes=(
                    "No separate annual product fee is "
                    "recorded in the normalized snapshot."
                ),
            )
        )

    elif reference_yield_includes_product_fee is True:
        components.append(
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_product_fee"
                ),
                component_type="product_fee",
                label=(
                    "Product fee already reflected in "
                    "reference yield"
                ),
                status="not_applicable",
                basis="annualized_pct",
                value=None,
                source=snapshot.source,
                source_url=snapshot.source_url,
                notes=(
                    "The normalized reference-yield evidence "
                    "already reflects the published product fee. "
                    "The fee is therefore not deducted again."
                ),
            )
        )

    elif reference_yield_includes_product_fee is False:
        components.append(
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_product_fee"
                ),
                component_type="product_fee",
                label="Published annual product fee",
                status="published",
                basis="annualized_pct",
                value=snapshot.annual_fee_pct,
                source=snapshot.source,
                source_url=snapshot.source_url,
                notes=(
                    "The product fee is deducted separately "
                    "because the supplied reference yield is "
                    "modeled as being before this fee."
                ),
            )
        )

    else:
        components.append(
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_product_fee"
                ),
                component_type="product_fee",
                label="Product-fee treatment",
                status="unknown",
                basis="annualized_pct",
                value=None,
                source=snapshot.source,
                source_url=snapshot.source_url,
                notes=(
                    "A published annual product fee exists, "
                    "but current evidence does not establish "
                    "whether the normalized reference yield "
                    "already includes that fee. No deduction "
                    "is guessed."
                ),
            )
        )

    components.extend(
        (
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_access_fee"
                ),
                component_type="access_fee",
                label="Recurring access cost",
                status="unknown",
                basis="annualized_pct",
                value=None,
                notes=(
                    "Exact recurring access, custody, platform, "
                    "or corporate-account cost for the modeled "
                    "route has not yet been applied. Generic "
                    "access-cost evidence may enrich this "
                    "component later."
                ),
            ),
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_entry_execution"
                ),
                component_type="entry_execution_cost",
                label="Entry execution cost",
                status="unknown",
                basis="position_bps",
                value=None,
                notes=(
                    "Position-specific entry execution cost has "
                    "not yet been established for this analysis."
                ),
            ),
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_exit_execution"
                ),
                component_type="exit_execution_cost",
                label="Exit execution cost",
                status="unknown",
                basis="position_bps",
                value=None,
                notes=(
                    "Position-specific exit execution cost has "
                    "not yet been established for this analysis."
                ),
            ),
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_slippage"
                ),
                component_type="slippage_price_impact",
                label=(
                    "Round-trip spread, slippage, or "
                    "market impact"
                ),
                status="unknown",
                basis="position_bps",
                value=None,
                notes=(
                    "No position-size execution-quality value "
                    "is guessed from AUM, issue size, turnover, "
                    "dealing terms, or non-executable pricing."
                ),
            ),
        )
    )

    if market.venue_type == "defi_protocol":
        components.append(
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_network_cost"
                ),
                component_type="network_cost",
                label="Blockchain network transaction cost",
                status="unknown",
                basis="fixed_eur",
                value=None,
                notes=(
                    "The opportunity uses a DeFi protocol. "
                    "Position-specific blockchain transaction "
                    "costs have not yet been established and "
                    "are therefore not assumed to be zero."
                ),
            )
        )

    if (
        instrument.currency == "EUR"
        and market.trading_currency == "EUR"
    ):
        components.append(
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_fx_cost"
                ),
                component_type="fx_hedging_cost",
                label="FX conversion or hedging cost",
                status="known_zero",
                basis="annualized_pct",
                value=0.0,
                notes=(
                    "The normalized instrument currency and "
                    "market trading currency are EUR, matching "
                    "the modeled EUR treasury exposure."
                ),
            )
        )

    else:
        components.append(
            ReturnComponent(
                component_id=(
                    f"{snapshot.snapshot_id}_fx_cost"
                ),
                component_type="fx_hedging_cost",
                label="FX conversion or hedging cost",
                status="unknown",
                basis="annualized_pct",
                value=None,
                notes=(
                    "The normalized currency information does "
                    "not establish a zero-FX-cost EUR treasury "
                    "path."
                ),
            )
        )

    return tuple(components)