from __future__ import annotations

from treasury_intelligence.models.frictions import (
    FrictionObservation,
)

from treasury_intelligence.models.returns import (
    ReturnComponent,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
)


XEON_FRICTION_OBSERVED_AT = "2026-08-29"


def get_xeon_friction_observations(
    position_size_eur: float,
) -> tuple[FrictionObservation, ...]:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    return (
        FrictionObservation(
            observation_id=(
                "xeon_dws_all_in_fee_2026_08_29"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            access_route_id=(
                XEON_IBKR_ACCESS.access_route_id
            ),
            observed_at=(
                XEON_FRICTION_OBSERVED_AT
            ),
            friction_type="fund_fee",
            label="XEON all-in fund fee",
            basis="annualized_pct",
            value=0.10,
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=(
                "https://etf.dws.com/"
            ),
            notes=(
                "DWS factsheet publishes an all-in fee "
                "of 0.10% p.a. for LU0290358497."
            ),
        ),
        FrictionObservation(
            observation_id=(
                "xeon_ibkr_entry_commission_"
                "2026_08_29"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            access_route_id=(
                XEON_IBKR_ACCESS.access_route_id
            ),
            observed_at=(
                XEON_FRICTION_OBSERVED_AT
            ),
            friction_type="broker_commission",
            label=(
                "Published IBKR Germany SmartRouting "
                "entry commission"
            ),
            basis="position_bps",
            value=5.0,
            evidence_level="published",
            source="Interactive Brokers",
            source_url=(
                "https://www.interactivebrokers.com/"
                "en/pricing/commissions-stocks.php"
            ),
            position_size_eur=position_size_eur,
            notes=(
                "Published Germany fixed SmartRouting "
                "pricing is 0.05% of trade value for the "
                "relevant monthly trade-value band. "
                "This is published route pricing, not an "
                "account-specific executable quote."
            ),
        ),
        FrictionObservation(
            observation_id=(
                "xeon_ibkr_exit_commission_"
                "2026_08_29"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            access_route_id=(
                XEON_IBKR_ACCESS.access_route_id
            ),
            observed_at=(
                XEON_FRICTION_OBSERVED_AT
            ),
            friction_type="broker_commission",
            label=(
                "Published IBKR Germany SmartRouting "
                "exit commission"
            ),
            basis="position_bps",
            value=5.0,
            evidence_level="published",
            source="Interactive Brokers",
            source_url=(
                "https://www.interactivebrokers.com/"
                "en/pricing/commissions-stocks.php"
            ),
            position_size_eur=position_size_eur,
            notes=(
                "Uses the same published 0.05% Germany "
                "SmartRouting commission assumption for "
                "the eventual sale. Actual future pricing "
                "must be re-observed at execution."
            ),
        ),
        FrictionObservation(
            observation_id=(
                "xeon_ibkr_account_minimum_"
                "2026_08_29"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            access_route_id=(
                XEON_IBKR_ACCESS.access_route_id
            ),
            observed_at=(
                XEON_FRICTION_OBSERVED_AT
            ),
            friction_type="account_minimum",
            label="IBKR organization account minimum",
            basis="fixed_eur",
            value=0.0,
            evidence_level="published",
            source="Interactive Brokers",
            source_url=(
                "https://www.interactivebrokers.com/"
                "en/accounts/required-minimums.php"
            ),
            notes=(
                "IBKR publishes a zero account minimum "
                "for Individual, Joint, Trust and Org "
                "accounts."
            ),
        ),
        FrictionObservation(
            observation_id=(
                "xeon_ibkr_inactivity_fee_"
                "2026_08_29"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            access_route_id=(
                XEON_IBKR_ACCESS.access_route_id
            ),
            observed_at=(
                XEON_FRICTION_OBSERVED_AT
            ),
            friction_type="inactivity_fee",
            label="IBKR organization inactivity fee",
            basis="fixed_eur",
            value=0.0,
            evidence_level="published",
            source="Interactive Brokers",
            source_url=(
                "https://www.interactivebrokers.com/"
                "en/accounts/required-minimums.php"
            ),
            notes=(
                "IBKR publishes a zero inactivity fee "
                "for Individual, Joint, Trust and Org "
                "accounts."
            ),
        ),
    )


def build_xeon_return_components(
    position_size_eur: float,
    reference_yield_pct: float,
) -> tuple[ReturnComponent, ...]:
    observations = (
        get_xeon_friction_observations(
            position_size_eur=position_size_eur
        )
    )

    fund_fee = next(
        observation
        for observation in observations
        if observation.friction_type
        == "fund_fee"
    )

    commissions = tuple(
        observation
        for observation in observations
        if observation.friction_type
        == "broker_commission"
    )

    if len(commissions) != 2:
        raise ValueError(
            "Expected exactly two XEON broker "
            "commission observations."
        )

    entry_commission = commissions[0]
    exit_commission = commissions[1]

    return (
        ReturnComponent(
            component_id=(
                "xeon_reference_yield"
            ),
            component_type="reference_yield",
            label=(
                "€STR plus index spread before ETF fee"
            ),
            status="model_derived",
            basis="annualized_pct",
            value=reference_yield_pct,
            notes=(
                "Reference yield remains a model-derived "
                "economic starting point."
            ),
        ),
        ReturnComponent(
            component_id="xeon_product_fee",
            component_type="product_fee",
            label=fund_fee.label,
            status="published",
            basis=fund_fee.basis,
            value=fund_fee.value,
            source=fund_fee.source,
            source_url=fund_fee.source_url,
            notes=fund_fee.notes,
        ),
        ReturnComponent(
            component_id=(
                "xeon_entry_broker_commission"
            ),
            component_type="entry_execution_cost",
            label=entry_commission.label,
            status="published",
            basis=entry_commission.basis,
            value=entry_commission.value,
            source=entry_commission.source,
            source_url=(
                entry_commission.source_url
            ),
            notes=entry_commission.notes,
        ),
        ReturnComponent(
            component_id=(
                "xeon_exit_broker_commission"
            ),
            component_type="exit_execution_cost",
            label=exit_commission.label,
            status="published",
            basis=exit_commission.basis,
            value=exit_commission.value,
            source=exit_commission.source,
            source_url=(
                exit_commission.source_url
            ),
            notes=exit_commission.notes,
        ),
        ReturnComponent(
            component_id=(
                "xeon_spread_slippage"
            ),
            component_type=(
                "slippage_price_impact"
            ),
            label=(
                "XEON round-trip spread / "
                "slippage / market impact"
            ),
            status="unknown",
            basis="position_bps",
            value=None,
            notes=(
                "Free public evidence currently "
                "establishes trading activity but not "
                "position-size executable bid/ask depth. "
                "No spread or slippage value is guessed."
            ),
        ),
        ReturnComponent(
            component_id="xeon_access_fee",
            component_type="access_fee",
            label=(
                "Corporate custody / residual "
                "access cost"
            ),
            status="unknown",
            basis="annualized_pct",
            value=None,
            notes=(
                "Published zero account minimum and "
                "zero inactivity fee do not by themselves "
                "prove that every custody or corporate "
                "access cost for the exact execution setup "
                "is zero."
            ),
        ),
        ReturnComponent(
            component_id="xeon_fx_cost",
            component_type="fx_hedging_cost",
            label="FX hedging cost",
            status="known_zero",
            basis="annualized_pct",
            value=0.0,
            notes=(
                "XEON is EUR-denominated for the "
                "EUR-base treasury model."
            ),
        ),
    )