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

from treasury_intelligence.sources.ishares import (
    ERNX_IBKR_ACCESS,
    ERNX_INSTRUMENT,
    ERNX_MARKET,
)


def build_etf_position_analysis(
    snapshot: OpportunitySnapshot,
    position_size_eur: float,
    position_scale_eur: float | None,
    position_scale_reference: str,
    market_observation: MarketObservation | None = None,
    analysis_id: str | None = None,
    notes: str | None = None,
) -> PositionAnalysis:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    if position_scale_eur is not None and position_scale_eur <= 0:
        raise ValueError(
            "position_scale_eur must be greater than zero "
            "when provided."
        )

    if not position_scale_reference:
        raise ValueError(
            "position_scale_reference must not be empty."
        )

    position_pct_of_market = None

    if position_scale_eur is not None:
        position_pct_of_market = (
            position_size_eur
            / position_scale_eur
            * 100
        )

    observed_daily_turnover_eur = None
    position_pct_of_daily_turnover = None
    liquidity_evidence_level = None

    if (
        market_observation is not None
        and market_observation.daily_turnover_eur is not None
        and market_observation.daily_turnover_eur > 0
    ):
        observed_daily_turnover_eur = (
            market_observation.daily_turnover_eur
        )

        position_pct_of_daily_turnover = (
            position_size_eur
            / observed_daily_turnover_eur
            * 100
        )

        liquidity_evidence_level = "market_activity"

    resolved_analysis_id = (
        analysis_id
        or (
            f"{snapshot.instrument_id}_"
            f"{int(position_size_eur)}"
        )
    )

    resolved_notes = notes or (
        "ETF product scale and observed secondary-market "
        "activity provide context only. ETF liquidity can "
        "also depend on market makers and underlying-market "
        "liquidity. These observations do not by themselves "
        "establish immediate executable depth for the "
        "proposed position."
    )

    return PositionAnalysis(
        analysis_id=resolved_analysis_id,
        instrument_id=snapshot.instrument_id,
        market_id=snapshot.market_id,
        access_route_id=snapshot.access_route_id,
        position_size_eur=position_size_eur,
        entry_supported=None,
        immediate_exit_supported=None,
        position_pct_of_market=position_pct_of_market,
        position_pct_reference=position_scale_reference,
        observed_daily_turnover_eur=(
            observed_daily_turnover_eur
        ),
        position_pct_of_daily_turnover=(
            position_pct_of_daily_turnover
        ),
        liquidity_evidence_level=(
            liquidity_evidence_level
        ),
        reference_yield_pct=snapshot.yield_value_pct,
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=False,
        notes=resolved_notes,
    )


def build_sovereign_bill_position_analysis(
    snapshot: OpportunitySnapshot,
    market_observation: MarketObservation,
    position_size_eur: float,
    reference_yield_pct: float | None = None,
    analysis_id: str | None = None,
    notes: str | None = None,
) -> PositionAnalysis:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    position_pct_of_market = None

    if (
        snapshot.outstanding_amount_eur is not None
        and snapshot.outstanding_amount_eur > 0
    ):
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

    resolved_reference_yield_pct = (
        reference_yield_pct
        if reference_yield_pct is not None
        else snapshot.yield_value_pct
    )

    resolved_analysis_id = (
        analysis_id
        or (
            f"{snapshot.instrument_id}_"
            f"{int(position_size_eur)}"
        )
    )

    resolved_notes = notes or (
        "Issue outstanding provides sovereign-market scale "
        "context but does not prove that the proposed "
        "position can be executed immediately. Firm "
        "position-size bid/ask and available-size evidence "
        "remain required for executable economics."
    )

    return PositionAnalysis(
        analysis_id=resolved_analysis_id,
        instrument_id=snapshot.instrument_id,
        market_id=snapshot.market_id,
        access_route_id=snapshot.access_route_id,
        position_size_eur=position_size_eur,
        entry_supported=None,
        immediate_exit_supported=None,
        remaining_entry_capacity_eur=None,
        immediate_exit_coverage_pct=None,
        position_pct_of_market=position_pct_of_market,
        position_pct_reference="issue_outstanding",
        reference_yield_pct=resolved_reference_yield_pct,
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=(
            executable_economics_known
        ),
        rejection_reason=None,
        notes=resolved_notes,
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
    return build_sovereign_bill_position_analysis(
        snapshot=snapshot,
        market_observation=market_observation,
        position_size_eur=position_size_eur,
        reference_yield_pct=market_derived_yield_pct,
        analysis_id=(
            f"fr_btf_2027_03_10_"
            f"{int(position_size_eur)}"
        ),
        notes=(
            "Issue size supports broad capacity context, "
            "but does not prove that the full proposed position "
            "can be executed immediately at the observed price. "
            "Firm bid/ask and available size remain unknown."
        ),
    )


def build_xeon_position_analysis(
    snapshot: OpportunitySnapshot,
    position_size_eur: float,
    market_observation: MarketObservation | None = None,
) -> PositionAnalysis:
    return build_etf_position_analysis(
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        position_scale_eur=snapshot.fund_aum_eur,
        position_scale_reference="fund_aum",
        market_observation=market_observation,
        analysis_id=(
            f"xeon_{int(position_size_eur)}"
        ),
        notes=(
            "Fund AUM and observed daily market activity provide "
            "scale context only. Daily turnover does not establish "
            "immediate executable depth for this position."
        ),
    )


def build_ernx_position_analysis(
    snapshot: OpportunitySnapshot,
    position_size_eur: float,
    market_observation: MarketObservation | None = None,
) -> PositionAnalysis:
    return build_etf_position_analysis(
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        position_scale_eur=snapshot.share_class_aum_eur,
        position_scale_reference="share_class_aum",
        market_observation=market_observation,
        analysis_id=(
            f"ernx_{int(position_size_eur)}"
        ),
        notes=(
            "Share-class AUM and observed daily market activity "
            "provide scale context only. ETF liquidity can also "
            "depend on market makers and underlying liquidity, so "
            "daily screen turnover does not establish immediate "
            "executable depth."
        ),
    )