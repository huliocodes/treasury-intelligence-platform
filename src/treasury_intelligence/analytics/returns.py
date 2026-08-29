from __future__ import annotations

from treasury_intelligence.models.returns import (
    ReturnAnalysis,
    ReturnComponent,
)


COST_COMPONENT_TYPES = {
    "product_fee",
    "access_fee",
    "entry_execution_cost",
    "exit_execution_cost",
    "slippage_price_impact",
    "network_cost",
    "fx_hedging_cost",
    "operational_cost",
    "tax_cost",
    "liquidity_cost",
    "other_cost",
}


def _reference_yield_component(
    components: tuple[ReturnComponent, ...],
) -> ReturnComponent:
    matches = tuple(
        component
        for component in components
        if component.component_type
        == "reference_yield"
    )

    if len(matches) != 1:
        raise ValueError(
            "Return analysis requires exactly one "
            "reference_yield component."
        )

    component = matches[0]

    if component.basis != "annualized_pct":
        raise ValueError(
            "reference_yield must use "
            "basis='annualized_pct'."
        )

    return component


def _cost_components(
    components: tuple[ReturnComponent, ...],
) -> tuple[ReturnComponent, ...]:
    return tuple(
        component
        for component in components
        if component.component_type
        in COST_COMPONENT_TYPES
    )


def _known_cost_components(
    components: tuple[ReturnComponent, ...],
) -> tuple[ReturnComponent, ...]:
    return tuple(
        component
        for component in _cost_components(
            components
        )
        if component.status
        not in (
            "unknown",
            "not_applicable",
        )
    )


def _unknown_cost_components(
    components: tuple[ReturnComponent, ...],
) -> tuple[ReturnComponent, ...]:
    return tuple(
        component
        for component in _cost_components(
            components
        )
        if component.status == "unknown"
    )


def _known_recurring_annualized_cost_pct(
    components: tuple[ReturnComponent, ...],
) -> float:
    return sum(
        component.value or 0.0
        for component in _known_cost_components(
            components
        )
        if component.basis == "annualized_pct"
    )


def _known_one_time_cost_bps(
    components: tuple[ReturnComponent, ...],
) -> float:
    return sum(
        component.value or 0.0
        for component in _known_cost_components(
            components
        )
        if component.basis == "position_bps"
    )


def _known_fixed_cost_eur(
    components: tuple[ReturnComponent, ...],
) -> float:
    return sum(
        component.value or 0.0
        for component in _known_cost_components(
            components
        )
        if component.basis == "fixed_eur"
    )


def _bps_cost_to_eur(
    position_size_eur: float,
    cost_bps: float,
) -> float:
    return (
        position_size_eur
        * cost_bps
        / 10_000
    )


def _eur_cost_to_bps(
    position_size_eur: float,
    cost_eur: float,
) -> float:
    return (
        cost_eur
        / position_size_eur
        * 10_000
    )


def _annualize_one_time_cost_pct(
    one_time_cost_bps: float,
    holding_period_days: int,
) -> float:
    holding_period_cost_pct = (
        one_time_cost_bps
        / 100
    )

    return (
        holding_period_cost_pct
        * 365
        / holding_period_days
    )


def build_return_analysis(
    analysis_id: str,
    instrument_id: str,
    market_id: str,
    access_route_id: str,
    position_size_eur: float,
    holding_period_days: int,
    components: tuple[ReturnComponent, ...],
    notes: str | None = None,
) -> ReturnAnalysis:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    if holding_period_days <= 0:
        raise ValueError(
            "holding_period_days must be greater than zero."
        )

    reference_component = (
        _reference_yield_component(
            components
        )
    )

    reference_yield_pct = (
        reference_component.value
    )

    recurring_cost_pct = (
        _known_recurring_annualized_cost_pct(
            components
        )
    )

    one_time_bps = (
        _known_one_time_cost_bps(
            components
        )
    )

    fixed_cost_eur = (
        _known_fixed_cost_eur(
            components
        )
    )

    fixed_cost_bps = (
        _eur_cost_to_bps(
            position_size_eur=position_size_eur,
            cost_eur=fixed_cost_eur,
        )
    )

    total_one_time_bps = (
        one_time_bps
        + fixed_cost_bps
    )

    bps_cost_eur = (
        _bps_cost_to_eur(
            position_size_eur=position_size_eur,
            cost_bps=one_time_bps,
        )
    )

    total_one_time_cost_eur = (
        bps_cost_eur
        + fixed_cost_eur
    )

    one_time_annualized_pct = (
        _annualize_one_time_cost_pct(
            one_time_cost_bps=(
                total_one_time_bps
            ),
            holding_period_days=(
                holding_period_days
            ),
        )
    )

    total_annualized_cost_pct = (
        recurring_cost_pct
        + one_time_annualized_pct
    )

    unknown_costs = (
        _unknown_cost_components(
            components
        )
    )

    unknown_cost_count = len(
        unknown_costs
    )

    return_after_known_costs_pct = None

    if reference_yield_pct is not None:
        return_after_known_costs_pct = (
            reference_yield_pct
            - total_annualized_cost_pct
        )

    economics_complete = (
        reference_yield_pct is not None
        and unknown_cost_count == 0
    )

    realistic_expected_return_pct = None

    if economics_complete:
        realistic_expected_return_pct = (
            return_after_known_costs_pct
        )

    return ReturnAnalysis(
        analysis_id=analysis_id,
        instrument_id=instrument_id,
        market_id=market_id,
        access_route_id=access_route_id,
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
        reference_yield_pct=(
            reference_yield_pct
        ),
        known_recurring_annualized_cost_pct=(
            recurring_cost_pct
        ),
        known_one_time_cost_eur=(
            total_one_time_cost_eur
        ),
        known_one_time_cost_bps=(
            total_one_time_bps
        ),
        known_one_time_cost_annualized_pct=(
            one_time_annualized_pct
        ),
        known_total_annualized_cost_pct=(
            total_annualized_cost_pct
        ),
        return_after_known_costs_pct=(
            return_after_known_costs_pct
        ),
        realistic_expected_return_pct=(
            realistic_expected_return_pct
        ),
        economics_complete=(
            economics_complete
        ),
        unknown_cost_component_count=(
            unknown_cost_count
        ),
        components=components,
        notes=notes,
    )


def unknown_cost_component_names(
    analysis: ReturnAnalysis,
) -> tuple[str, ...]:
    return tuple(
        component.label
        for component in analysis.components
        if (
            component.component_type
            in COST_COMPONENT_TYPES
            and component.status == "unknown"
        )
    )