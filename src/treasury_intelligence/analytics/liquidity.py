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
    "fund_dealing_terms": 1,
    "market_activity": 1,
    "displayed_quote": 2,
    "displayed_quote_with_size": 3,
    "strong_inferred": 4,
    "executable_quote": 5,
    "position_depth": 6,
}


STRONG_INFERRED_POSITION_LEVELS = (
    "etf_scale_and_market_structure",
    "sovereign_issue_scale",
)


def classify_liquidity_evidence(
    market_observation: MarketObservation | None,
    position: PositionAnalysis,
) -> str:
    if (
        position.immediate_exit_supported
        is not None
        and position.immediate_exit_coverage_pct
        is not None
    ):
        return "position_depth"

    if (
        position.liquidity_evidence_level
        in STRONG_INFERRED_POSITION_LEVELS
    ):
        return "strong_inferred"

    if (
        position.liquidity_evidence_level
        == "fund_dealing_terms"
    ):
        return "fund_dealing_terms"

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
        market_observation.daily_turnover_eur
        is not None
        or market_observation.daily_volume_units
        is not None
    ):
        return "market_activity"

    return "none"


def strongest_supported_claim(
    evidence_level: str,
) -> str:
    claims = {
        "none": (
            "No direct or sufficiently strong inferred "
            "liquidity evidence is available."
        ),
        "fund_dealing_terms": (
            "Published fund subscription or redemption "
            "dealing terms provide evidence of the fund's "
            "normal dealing process, but they do not "
            "establish unconditional immediate liquidity "
            "for the proposed position."
        ),
        "market_activity": (
            "The market shows observed trading activity, "
            "but the observation alone does not establish "
            "practical liquidity for the proposed position."
        ),
        "displayed_quote": (
            "A two-sided public quote is observable, but "
            "displayed prices without size do not by "
            "themselves establish practical liquidity for "
            "the proposed position."
        ),
        "displayed_quote_with_size": (
            "A two-sided quote with displayed size is "
            "observable, but displayed size alone does not "
            "prove that the full proposed position can be "
            "exited immediately."
        ),
        "strong_inferred": (
            "Multiple structural and position-size signals "
            "support a strong inference that the modeled "
            "position is practically liquid under normal "
            "market conditions. This is not a direct "
            "position-size executable quote or guarantee."
        ),
        "executable_quote": (
            "Executable pricing evidence is available, but "
            "full position-size exit capacity has not yet "
            "been directly proven."
        ),
        "position_depth": (
            "Direct position-size-specific liquidity "
            "evidence is available and supports a direct "
            "immediate-liquidity conclusion."
        ),
    }

    return claims[evidence_level]


def missing_liquidity_evidence(
    evidence_level: str,
) -> str | None:
    missing = {
        "none": (
            "Obtain market, product-scale, dealing, or "
            "position-size evidence sufficient to support "
            "either a strong inferred or direct liquidity "
            "conclusion."
        ),
        "fund_dealing_terms": (
            "Published fund dealing terms establish the "
            "normal subscription or redemption process but "
            "not guaranteed immediate exit. Obtain stronger "
            "evidence on redemption capacity, settlement "
            "behavior, gates, suspension conditions, or "
            "position-size liquidity where required."
        ),
        "market_activity": (
            "Combine market activity with relevant "
            "position-size and product-structure evidence, "
            "or obtain stronger executable depth."
        ),
        "displayed_quote": (
            "Obtain displayed size, broader structural "
            "liquidity evidence, or stronger executable "
            "depth for the proposed position."
        ),
        "displayed_quote_with_size": (
            "Obtain position-size executable depth or "
            "sufficient structural and scale evidence to "
            "support a strong inferred conclusion."
        ),
        "strong_inferred": None,
        "executable_quote": (
            "Obtain evidence that executable liquidity "
            "covers the full proposed position size."
        ),
        "position_depth": None,
    }

    return missing[evidence_level]


def _inferred_immediate_liquidity(
    evidence_level: str,
    position: PositionAnalysis,
) -> bool | None:
    if (
        position.immediate_exit_supported
        is not None
    ):
        return position.immediate_exit_supported

    if evidence_level == "strong_inferred":
        return True

    return None


def assess_liquidity_evidence(
    market_observation: MarketObservation | None,
    position: PositionAnalysis,
) -> LiquidityEvidenceAssessment:
    evidence_level = classify_liquidity_evidence(
        market_observation=market_observation,
        position=position,
    )

    evidence_rank = (
        LIQUIDITY_EVIDENCE_RANKS[
            evidence_level
        ]
    )

    market_activity_observed = (
        evidence_level
        in (
            "market_activity",
            "displayed_quote",
            "displayed_quote_with_size",
            "strong_inferred",
            "executable_quote",
            "position_depth",
        )
    )

    displayed_quote_observed = (
        evidence_level
        in (
            "displayed_quote",
            "displayed_quote_with_size",
            "executable_quote",
            "position_depth",
        )
    )

    displayed_size_observed = (
        evidence_level
        in (
            "displayed_quote_with_size",
            "executable_quote",
            "position_depth",
        )
    )

    executable_quote_observed = (
        evidence_level
        in (
            "executable_quote",
            "position_depth",
        )
    )

    position_depth_observed = (
        evidence_level == "position_depth"
    )

    immediate_liquidity_supported = (
        _inferred_immediate_liquidity(
            evidence_level=evidence_level,
            position=position,
        )
    )

    sufficient_for_immediate_liquidity = (
        immediate_liquidity_supported
        is not None
        and evidence_level
        in (
            "strong_inferred",
            "position_depth",
        )
    )

    return LiquidityEvidenceAssessment(
        assessment_id=(
            f"{position.analysis_id}_"
            "liquidity_evidence"
        ),
        instrument_id=(
            position.instrument_id
        ),
        market_id=position.market_id,
        access_route_id=(
            position.access_route_id
        ),
        position_size_eur=(
            position.position_size_eur
        ),
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
            immediate_liquidity_supported
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
            "Liquidity conclusions distinguish direct "
            "position-depth evidence from strong inferred "
            "evidence. Strong inference may use position "
            "size, product or issue scale, market structure, "
            "and observable secondary-market evidence. "
            "Direct contradictory evidence always takes "
            "precedence over inference."
        ),
    )