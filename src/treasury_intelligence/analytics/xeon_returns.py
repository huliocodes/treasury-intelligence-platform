from __future__ import annotations

from treasury_intelligence.analytics.access_returns import (
    apply_xeon_access_cost_evidence,
)

from treasury_intelligence.analytics.execution_evidence import (
    assess_xetra_position_execution_evidence,
)

from treasury_intelligence.analytics.execution_returns import (
    apply_xeon_execution_evidence,
)

from treasury_intelligence.analytics.frictions import (
    build_xeon_return_components,
)

from treasury_intelligence.sources.ibkr import (
    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE,
)

from treasury_intelligence.sources.xetra import (
    XEON_XETRA_2024_TURNOVER,
    XEON_XETRA_XLM_100K,
)


def build_xeon_evidence_enriched_return_components(
    assessment_id: str,
    instrument_id: str,
    market_id: str,
    position_size_eur: float,
    reference_yield_pct: float,
    current_daily_turnover_eur: float | None,
) -> tuple:
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

    base_components = (
        build_xeon_return_components(
            position_size_eur=(
                position_size_eur
            ),
            reference_yield_pct=(
                reference_yield_pct
            ),
        )
    )

    execution_evidence = (
        assess_xetra_position_execution_evidence(
            assessment_id=assessment_id,
            instrument_id=instrument_id,
            market_id=market_id,
            position_size_eur=position_size_eur,
            xlm_evidence=(
                XEON_XETRA_XLM_100K
            ),
            annual_turnover_evidence=(
                XEON_XETRA_2024_TURNOVER
            ),
            current_daily_turnover_eur=(
                current_daily_turnover_eur
            ),
            notes=(
                "Position-sized public Xetra "
                "execution evidence used to enrich "
                "XEON return components."
            ),
        )
    )

    execution_enriched_components = (
        apply_xeon_execution_evidence(
            components=base_components,
            execution_evidence=(
                execution_evidence
            ),
        )
    )

    fully_enriched_components = (
        apply_xeon_access_cost_evidence(
            components=(
                execution_enriched_components
            ),
            access_cost_evidence=(
                IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE
            ),
        )
    )

    return fully_enriched_components