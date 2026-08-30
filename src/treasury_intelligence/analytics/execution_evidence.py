from __future__ import annotations

from treasury_intelligence.models.execution_evidence import (
    PositionExecutionEvidence,
)

from treasury_intelligence.sources.xetra import (
    XetraAnnualTurnoverEvidence,
    XetraLiquidityMeasureEvidence,
)


def assess_xetra_position_execution_evidence(
    assessment_id: str,
    instrument_id: str,
    market_id: str,
    position_size_eur: float,
    xlm_evidence: XetraLiquidityMeasureEvidence,
    annual_turnover_evidence: XetraAnnualTurnoverEvidence,
    current_daily_turnover_eur: float | None,
    notes: str | None = None,
) -> PositionExecutionEvidence:
    if not assessment_id:
        raise ValueError(
            "Execution evidence assessment ID "
            "is required."
        )

    if not instrument_id:
        raise ValueError(
            "Instrument ID is required."
        )

    if not market_id:
        raise ValueError(
            "Market ID is required."
        )

    if position_size_eur <= 0:
        raise ValueError(
            "Position size must be greater "
            "than zero."
        )

    if (
        xlm_evidence.isin
        != annual_turnover_evidence.isin
    ):
        raise ValueError(
            "XLM and annual-turnover evidence "
            "must refer to the same ISIN."
        )

    if (
        current_daily_turnover_eur is not None
        and current_daily_turnover_eur <= 0
    ):
        raise ValueError(
            "Current daily turnover must be "
            "greater than zero when provided."
        )

    reference_order_size_eur = (
        xlm_evidence.measured_order_size_eur
    )

    position_to_reference_size_multiple = (
        position_size_eur
        / reference_order_size_eur
    )

    exact_position_size_match = (
        abs(
            position_size_eur
            - reference_order_size_eur
        )
        <= 0.01
    )

    market_activity_supported = (
        annual_turnover_evidence.annual_turnover_eur
        > 0
    )

    if current_daily_turnover_eur is not None:
        market_activity_supported = (
            market_activity_supported
            and current_daily_turnover_eur > 0
        )

    source_references = (
        xlm_evidence.source_reference,
        annual_turnover_evidence.source_reference,
    )

    if exact_position_size_match:
        return PositionExecutionEvidence(
            assessment_id=assessment_id,
            instrument_id=instrument_id,
            market_id=market_id,
            position_size_eur=position_size_eur,
            reference_order_size_eur=(
                reference_order_size_eur
            ),
            position_to_reference_size_multiple=(
                position_to_reference_size_multiple
            ),
            observed_roundtrip_cost_bps=(
                xlm_evidence.roundtrip_cost_bps
            ),
            observed_buy_cost_bps=(
                xlm_evidence.buy_cost_bps
            ),
            observed_sell_cost_bps=(
                xlm_evidence.sell_cost_bps
            ),
            position_sized_cost_supported=True,
            execution_evidence_status="supported",
            market_activity_supported=(
                market_activity_supported
            ),
            immediate_exit_supported=None,
            evidence_requirements=(),
            source_references=source_references,
            notes=notes,
        )

    evidence_requirements = (
        (
            "Position-sized implicit execution-cost "
            "evidence is unavailable for "
            f"EUR {position_size_eur:,.0f}; "
            "published Xetra XLM evidence is measured "
            f"at EUR {reference_order_size_eur:,.0f}."
        ),
        (
            "Current executable order-book depth "
            "for the requested position size remains "
            "unverified."
        ),
        (
            "Immediate exit capacity at the requested "
            "position size remains unverified."
        ),
    )

    return PositionExecutionEvidence(
        assessment_id=assessment_id,
        instrument_id=instrument_id,
        market_id=market_id,
        position_size_eur=position_size_eur,
        reference_order_size_eur=(
            reference_order_size_eur
        ),
        position_to_reference_size_multiple=(
            position_to_reference_size_multiple
        ),
        observed_roundtrip_cost_bps=None,
        observed_buy_cost_bps=None,
        observed_sell_cost_bps=None,
        position_sized_cost_supported=False,
        execution_evidence_status="insufficient",
        market_activity_supported=(
            market_activity_supported
        ),
        immediate_exit_supported=None,
        evidence_requirements=(
            evidence_requirements
        ),
        source_references=source_references,
        notes=notes,
    )