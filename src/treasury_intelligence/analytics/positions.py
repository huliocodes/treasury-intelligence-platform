from __future__ import annotations

from treasury_intelligence.models.opportunities import (
    MarketObservation,
    OpportunitySnapshot,
    PositionAnalysis,
)

from treasury_intelligence.sources.aave import (
    AAVE_V3_BASE_EURC_DIRECT_ACCESS,
    AAVE_V3_BASE_EURC_INSTRUMENT,
    AAVE_V3_BASE_EURC_MARKET,
    AaveReserveObservation,
    analyze_position_support,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_IBKR_ACCESS,
    BTF_2027_03_10_MARKET,
)


def build_aave_position_analysis(
    observation: AaveReserveObservation,
    position_size_eur: float,
) -> PositionAnalysis:
    support = analyze_position_support(
        observation=observation,
        position_size=position_size_eur,
    )

    immediate_exit_supported = (
        support.immediate_exit_coverage_pct >= 100
    )

    position_pct_of_market = None

    if observation.total_supplied > 0:
        position_pct_of_market = (
            position_size_eur
            / observation.total_supplied
            * 100
        )

    rejection_reason = None

    if not support.entry_supported:
        rejection_reason = (
            "position exceeds remaining protocol supply capacity"
        )

    notes = (
        "Capacity analysis treats EURC position amount as "
        "approximately EUR-equivalent for sizing only. "
        "EURC asset/redemption risk is not modeled here. "
        "Supply APY is current protocol APY and has not "
        "been simulated after adding the proposed position."
    )

    return PositionAnalysis(
        analysis_id=(
            f"aave_v3_base_eurc_"
            f"{int(position_size_eur)}"
        ),
        instrument_id=(
            AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
        ),
        market_id=(
            AAVE_V3_BASE_EURC_MARKET.market_id
        ),
        access_route_id=(
            AAVE_V3_BASE_EURC_DIRECT_ACCESS.access_route_id
        ),
        position_size_eur=position_size_eur,
        entry_supported=support.entry_supported,
        immediate_exit_supported=immediate_exit_supported,
        remaining_entry_capacity_eur=(
            support.remaining_entry_capacity
        ),
        immediate_exit_coverage_pct=(
            support.immediate_exit_coverage_pct
        ),
        position_pct_of_market=position_pct_of_market,
        position_pct_reference="current_total_supplied",
        reference_yield_pct=observation.supply_apy_pct,
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=False,
        rejection_reason=rejection_reason,
        notes=notes,
    )


def build_btf_position_analysis(
    snapshot: OpportunitySnapshot,
    market_observation: MarketObservation,
    position_size_eur: float,
    market_derived_yield_pct: float,
) -> PositionAnalysis:
    position_pct_of_market = None

    if snapshot.outstanding_amount_eur:
        position_pct_of_market = (
            position_size_eur
            / snapshot.outstanding_amount_eur
            * 100
        )

    executable_economics_known = (
        market_observation.bid_price is not None
        and market_observation.ask_price is not None
        and market_observation.ask_size is not None
    )

    notes = (
        "Issue size supports broad capacity context, "
        "but does not prove that the full proposed position "
        "can be executed immediately at the observed price. "
        "Firm bid/ask and available size remain unknown."
    )

    return PositionAnalysis(
        analysis_id=(
            f"fr_btf_2027_03_10_"
            f"{int(position_size_eur)}"
        ),
        instrument_id=BTF_2027_03_10.instrument_id,
        market_id=BTF_2027_03_10_MARKET.market_id,
        access_route_id=(
            BTF_2027_03_10_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=position_size_eur,
        entry_supported=None,
        immediate_exit_supported=None,
        remaining_entry_capacity_eur=None,
        immediate_exit_coverage_pct=None,
        position_pct_of_market=position_pct_of_market,
        position_pct_reference="issue_outstanding",
        reference_yield_pct=market_derived_yield_pct,
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=(
            executable_economics_known
        ),
        rejection_reason=None,
        notes=notes,
    )