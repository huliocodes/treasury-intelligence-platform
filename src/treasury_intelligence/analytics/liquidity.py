from __future__ import annotations

from treasury_intelligence.models.liquidity import (
    LiquidityEvidenceAssessment,
)

from treasury_intelligence.models.opportunities import (
    MarketObservation,
    PositionAnalysis,
)


LIQUIDITY_EVIDENCE_RANKS = {
    "none": 0,
    "market_activity": 1,
    "displayed_quote": 2,
    "displayed_quote_with_size": 3,
    "executable_quote": 4,
    "position_depth": 5,
}


def classify_liquidity_evidence(
    market_observation: MarketObservation | None,
    position: PositionAnalysis,
) -> str:
    if position.immediate_exit_supported is not None:
        if (
            position.immediate_exit_coverage_pct
            is not None
        ):
            return "position_depth"

    if market_observation is None:
        return "none"

    if (
        market_observation.bid_price is not None
        and market_observation.ask_price is not None
        and market_observation.bid_size is not None
        and market_observation.ask_size is not None
    ):
        return "displayed_quote_with_size"

    if (
        market_observation.bid_price is not None
        and market_observation.ask_price is not None
    ):
        return "displayed_quote"

    if (
        market_observation.daily_turnover_eur is not None
        or market_observation.daily_volume_units is not None
    ):
        return "market_activity"

    return "none"


def strongest_supported_claim(
    evidence_level: str,
) -> str:
    claims = {
        "none": (
            "No direct market-liquidity evidence is available."
        ),
        "market_activity": (
            "The market shows observed trading activity, but the "
            "observation does not establish executable liquidity "
            "for the proposed position."
        ),
        "displayed_quote": (
            "A two-sided public quote is observable, but displayed "
            "prices without size do not establish executable "
            "liquidity for the proposed position."
        ),
        "displayed_quote_with_size": (
            "A two-sided quote with displayed size is observable, "
            "but displayed size alone does not prove that the full "
            "proposed position can be exited immediately."
        ),
        "executable_quote": (
            "Executable pricing evidence is available, but full "
            "position-size exit capacity has not yet been proven."
        ),
        "position_depth": (
            "Position-size-specific liquidity evidence is available "
            "and can support an immediate-liquidity conclusion."
        ),
    }

    return claims[evidence_level]


def missing_liquidity_evidence(
    evidence_level: str,
) -> str | None:
    missing = {
        "none": (
            "Obtain public market activity or quote evidence, then "
            "progress toward position-size-specific executable "
            "liquidity evidence."
        ),
        "market_activity": (
            "Obtain a current two-sided quote and displayed size "
            "where available, followed by position-size-specific "
            "executable depth."
        ),
        "displayed_quote": (
            "Obtain displayed bid/ask size or stronger executable "
            "depth evidence for the proposed position."
        ),
        "displayed_quote_with_size": (
            "Obtain position-size-specific executable depth or an "
            "equivalent firm execution indication."
        ),
        "executable_quote": (
            "Obtain evidence that executable liquidity covers the "
            "full proposed position size."
        ),
        "position_depth": None,
    }

    return missing[evidence_level]


def assess_liquidity_evidence(
    market_observation: MarketObservation | None,
    position: PositionAnalysis,
) -> LiquidityEvidenceAssessment:
    evidence_level = classify_liquidity_evidence(
        market_observation=market_observation,
        position=position,
    )

    evidence_rank = LIQUIDITY_EVIDENCE_RANKS[
        evidence_level
    ]

    market_activity_observed = (
        evidence_rank
        >= LIQUIDITY_EVIDENCE_RANKS[
            "market_activity"
        ]
    )

    displayed_quote_observed = (
        evidence_rank
        >= LIQUIDITY_EVIDENCE_RANKS[
            "displayed_quote"
        ]
    )

    displayed_size_observed = (
        evidence_rank
        >= LIQUIDITY_EVIDENCE_RANKS[
            "displayed_quote_with_size"
        ]
    )

    executable_quote_observed = (
        evidence_rank
        >= LIQUIDITY_EVIDENCE_RANKS[
            "executable_quote"
        ]
    )

    position_depth_observed = (
        evidence_rank
        >= LIQUIDITY_EVIDENCE_RANKS[
            "position_depth"
        ]
    )

    sufficient_for_immediate_liquidity = (
        position_depth_observed
        and position.immediate_exit_supported
        is not None
    )

    return LiquidityEvidenceAssessment(
        assessment_id=(
            f"{position.analysis_id}_liquidity_evidence"
        ),
        instrument_id=position.instrument_id,
        market_id=position.market_id,
        access_route_id=position.access_route_id,
        position_size_eur=position.position_size_eur,
        evidence_level=evidence_level,
        evidence_rank=evidence_rank,
        market_activity_observed=(
            market_activity_observed
        ),
        displayed_quote_observed=(
            displayed_quote_observed
        ),
        displayed_size_observed=(
            displayed_size_observed
        ),
        executable_quote_observed=(
            executable_quote_observed
        ),
        position_depth_observed=(
            position_depth_observed
        ),
        immediate_liquidity_supported=(
            position.immediate_exit_supported
        ),
        sufficient_for_immediate_liquidity=(
            sufficient_for_immediate_liquidity
        ),
        strongest_supported_claim=(
            strongest_supported_claim(
                evidence_level
            )
        ),
        missing_evidence=(
            missing_liquidity_evidence(
                evidence_level
            )
        ),
        notes=(
            "Evidence strength and liquidity conclusion are kept "
            "separate. Market activity or displayed quotes can "
            "improve confidence without proving that the proposed "
            "position can be exited immediately."
        ),
    )