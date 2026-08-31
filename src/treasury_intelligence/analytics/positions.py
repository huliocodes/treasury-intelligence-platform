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

from treasury_intelligence.sources.banks import (
    BankDepositRate,
    interpret_bank_deposit_position,
)


STRONG_INFERRED_MAX_POSITION_PCT_OF_SCALE = 0.50


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

    if (
        position_scale_eur is not None
        and position_scale_eur <= 0
    ):
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

    liquidity_evidence_level = None

    strong_inferred_scale_support = (
        position_pct_of_market is not None
        and position_pct_of_market
        <= STRONG_INFERRED_MAX_POSITION_PCT_OF_SCALE
    )

    if (
        strong_inferred_scale_support
        and market_observation is not None
    ):
        liquidity_evidence_level = (
            "etf_scale_and_market_structure"
        )

    elif market_observation is not None:
        if (
            market_observation.bid_price is not None
            and market_observation.ask_price is not None
        ):
            liquidity_evidence_level = (
                "displayed_quote"
            )

        elif (
            market_observation.daily_turnover_eur
            is not None
            or market_observation.daily_volume_units
            is not None
        ):
            liquidity_evidence_level = (
                "market_activity"
            )

    resolved_analysis_id = (
        analysis_id
        or (
            f"{snapshot.instrument_id}_"
            f"{int(position_size_eur)}"
        )
    )

    resolved_notes = notes or (
        "ETF liquidity is assessed using position size "
        "relative to product scale together with observed "
        "secondary-market evidence and ETF market structure. "
        "A sufficiently small position can support a strong "
        "inference of practical liquidity without pretending "
        "that position-size executable depth was directly "
        "observed. Direct contradictory evidence, when "
        "available, takes precedence."
    )

    return PositionAnalysis(
        analysis_id=resolved_analysis_id,
        instrument_id=snapshot.instrument_id,
        market_id=snapshot.market_id,
        access_route_id=snapshot.access_route_id,
        position_size_eur=position_size_eur,
        entry_supported=None,
        immediate_exit_supported=None,
        position_pct_of_market=(
            position_pct_of_market
        ),
        position_pct_reference=(
            position_scale_reference
        ),
        observed_daily_turnover_eur=(
            observed_daily_turnover_eur
        ),
        position_pct_of_daily_turnover=(
            position_pct_of_daily_turnover
        ),
        liquidity_evidence_level=(
            liquidity_evidence_level
        ),
        reference_yield_pct=(
            snapshot.yield_value_pct
        ),
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

    liquidity_evidence_level = None

    strong_inferred_scale_support = (
        position_pct_of_market is not None
        and position_pct_of_market
        <= STRONG_INFERRED_MAX_POSITION_PCT_OF_SCALE
    )

    if strong_inferred_scale_support:
        liquidity_evidence_level = (
            "sovereign_issue_scale"
        )

    elif (
        market_observation.bid_price is not None
        and market_observation.ask_price is not None
        and market_observation.bid_size is not None
        and market_observation.ask_size is not None
    ):
        liquidity_evidence_level = (
            "displayed_quote_with_size"
        )

    elif (
        market_observation.bid_price is not None
        and market_observation.ask_price is not None
    ):
        liquidity_evidence_level = (
            "displayed_quote"
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
        "Sovereign-bill liquidity is assessed using the "
        "proposed position relative to the outstanding issue "
        "together with the existence of an observable "
        "secondary market. A sufficiently small position can "
        "support a strong inference of practical liquidity "
        "without claiming that a firm position-size quote was "
        "directly observed."
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
        position_pct_of_market=(
            position_pct_of_market
        ),
        position_pct_reference=(
            "issue_outstanding"
        ),
        observed_daily_turnover_eur=None,
        position_pct_of_daily_turnover=None,
        liquidity_evidence_level=(
            liquidity_evidence_level
        ),
        reference_yield_pct=(
            resolved_reference_yield_pct
        ),
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=(
            executable_economics_known
        ),
        rejection_reason=None,
        notes=resolved_notes,
    )


def build_money_market_fund_position_analysis(
    snapshot: OpportunitySnapshot,
    position_size_eur: float,
    minimum_initial_investment_eur: float,
    analysis_id: str | None = None,
    notes: str | None = None,
) -> PositionAnalysis:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    if minimum_initial_investment_eur < 0:
        raise ValueError(
            "minimum_initial_investment_eur cannot be negative."
        )

    entry_supported = (
        position_size_eur
        >= minimum_initial_investment_eur
    )

    rejection_reason = None

    if not entry_supported:
        rejection_reason = (
            "position is below the published minimum "
            "initial investment"
        )

    position_pct_of_market = None

    if (
        snapshot.fund_aum_eur is not None
        and snapshot.fund_aum_eur > 0
    ):
        position_pct_of_market = (
            position_size_eur
            / snapshot.fund_aum_eur
            * 100
        )

    resolved_analysis_id = (
        analysis_id
        or (
            f"{snapshot.instrument_id}_"
            f"{int(position_size_eur)}"
        )
    )

    resolved_notes = notes or (
        "Published fund minimums can establish whether "
        "the proposed allocation meets stated subscription "
        "terms. Fund AUM provides scale context only. "
        "Published daily or same-day redemption terms do "
        "not by themselves prove that an arbitrary position "
        "can always be redeemed immediately under all market "
        "conditions. Corporate accessibility is evaluated "
        "separately from this position analysis."
    )

    return PositionAnalysis(
        analysis_id=resolved_analysis_id,
        instrument_id=snapshot.instrument_id,
        market_id=snapshot.market_id,
        access_route_id=snapshot.access_route_id,
        position_size_eur=position_size_eur,
        entry_supported=entry_supported,
        immediate_exit_supported=None,
        remaining_entry_capacity_eur=None,
        immediate_exit_coverage_pct=None,
        position_pct_of_market=(
            position_pct_of_market
        ),
        position_pct_reference="fund_aum",
        observed_daily_turnover_eur=None,
        position_pct_of_daily_turnover=None,
        liquidity_evidence_level=(
            "fund_dealing_terms"
        ),
        reference_yield_pct=(
            snapshot.yield_value_pct
        ),
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=False,
        rejection_reason=rejection_reason,
        notes=resolved_notes,
    )


def build_bank_deposit_position_analysis(
    snapshot: OpportunitySnapshot,
    rate: BankDepositRate,
    position_size_eur: float,
    analysis_id: str | None = None,
    notes: str | None = None,
) -> PositionAnalysis:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    interpretation = interpret_bank_deposit_position(
        rate=rate,
        position_size_eur=position_size_eur,
    )

    entry_supported = (
        interpretation.minimum_amount_supported
    )

    if (
        interpretation.maximum_amount_supported
        is False
    ):
        entry_supported = False

    rejection_reason = None

    if not interpretation.minimum_amount_supported:
        rejection_reason = (
            "position is below the published minimum "
            "deposit amount"
        )

    elif (
        interpretation.maximum_amount_supported
        is False
    ):
        rejection_reason = (
            "position exceeds the published maximum "
            "deposit amount"
        )

    immediate_exit_supported = (
        True
        if rate.early_withdrawal
        else False
    )

    immediate_exit_coverage_pct = (
        100.0
        if immediate_exit_supported
        else 0.0
    )

    executable_yield_pct = (
        interpretation.executable_rate_pct
    )

    executable_economics_known = (
        interpretation.published_rate_is_executable
    )

    resolved_analysis_id = (
        analysis_id
        or (
            f"{snapshot.instrument_id}_"
            f"{int(position_size_eur)}"
        )
    )

    resolved_notes = notes or (
        "Published bank-deposit amount limits establish "
        "whether the proposed allocation fits the stated "
        "product terms. The published rate remains a "
        "reference rate unless the bank evidence establishes "
        "a firm non-negotiated rate. Early-withdrawal terms "
        "are modeled separately from initial placement "
        "settlement. A deposit with no early withdrawal "
        "therefore has zero immediate exit coverage while "
        "the term remains active."
    )

    return PositionAnalysis(
        analysis_id=resolved_analysis_id,
        instrument_id=snapshot.instrument_id,
        market_id=snapshot.market_id,
        access_route_id=snapshot.access_route_id,
        position_size_eur=position_size_eur,
        entry_supported=entry_supported,
        immediate_exit_supported=(
            immediate_exit_supported
        ),
        remaining_entry_capacity_eur=None,
        immediate_exit_coverage_pct=(
            immediate_exit_coverage_pct
        ),
        position_pct_of_market=None,
        position_pct_reference=None,
        observed_daily_turnover_eur=None,
        position_pct_of_daily_turnover=None,
        liquidity_evidence_level=(
            "published_withdrawal_terms"
        ),
        reference_yield_pct=(
            interpretation.published_rate_pct
        ),
        executable_yield_pct=(
            executable_yield_pct
        ),
        position_adjusted_yield_pct=None,
        executable_economics_known=(
            executable_economics_known
        ),
        rejection_reason=rejection_reason,
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
        support.immediate_exit_coverage_pct
        >= 100
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
            "position exceeds remaining protocol "
            "supply capacity"
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
        immediate_exit_supported=(
            immediate_exit_supported
        ),
        remaining_entry_capacity_eur=(
            support.remaining_entry_capacity
        ),
        immediate_exit_coverage_pct=(
            support.immediate_exit_coverage_pct
        ),
        position_pct_of_market=(
            position_pct_of_market
        ),
        position_pct_reference=(
            "current_total_supplied"
        ),
        reference_yield_pct=(
            observation.supply_apy_pct
        ),
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
        reference_yield_pct=(
            market_derived_yield_pct
        ),
        analysis_id=(
            f"fr_btf_2027_03_10_"
            f"{int(position_size_eur)}"
        ),
        notes=(
            "The proposed position is evaluated relative "
            "to the outstanding sovereign issue and the "
            "observable secondary market. A sufficiently "
            "small position may support a strong inferred "
            "liquidity conclusion without claiming that "
            "firm position-size executable depth was "
            "directly observed."
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
        position_scale_eur=(
            snapshot.fund_aum_eur
        ),
        position_scale_reference="fund_aum",
        market_observation=market_observation,
        analysis_id=(
            f"xeon_{int(position_size_eur)}"
        ),
        notes=(
            "XEON position size is evaluated relative to "
            "fund scale together with observed Xetra market "
            "evidence and ETF market structure. This may "
            "support a strong inferred liquidity conclusion "
            "without pretending that a firm quote for the "
            "full position was directly observed."
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
        position_scale_eur=(
            snapshot.share_class_aum_eur
        ),
        position_scale_reference=(
            "share_class_aum"
        ),
        market_observation=market_observation,
        analysis_id=(
            f"ernx_{int(position_size_eur)}"
        ),
        notes=(
            "ERNX position size is evaluated relative to "
            "share-class scale together with observed "
            "secondary-market evidence and ETF market "
            "structure. This may support a strong inferred "
            "liquidity conclusion without claiming that "
            "firm position-size executable depth was "
            "directly observed."
        ),
    )