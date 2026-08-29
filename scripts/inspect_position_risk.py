from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.position_risk import (
    build_position_risk_assessments,
    get_liquidity_position_risk,
)

from treasury_intelligence.analytics.risk_assessments import (
    get_aave_eurc_risk_assessments,
    get_xeon_risk_assessments,
)

from treasury_intelligence.models.liquidity import (
    LiquidityEvidenceAssessment,
)

from treasury_intelligence.models.opportunities import (
    PositionAnalysis,
)

from treasury_intelligence.sources.aave import (
    AAVE_V3_BASE_EURC_DIRECT_ACCESS,
    AAVE_V3_BASE_EURC_INSTRUMENT,
    AAVE_V3_BASE_EURC_MARKET,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
)


def build_aave_supported_position(
) -> PositionAnalysis:
    return PositionAnalysis(
        analysis_id="test_aave_eurc_100k",
        instrument_id=(
            AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
        ),
        market_id=(
            AAVE_V3_BASE_EURC_MARKET.market_id
        ),
        access_route_id=(
            AAVE_V3_BASE_EURC_DIRECT_ACCESS.access_route_id
        ),
        position_size_eur=100_000,
        entry_supported=True,
        immediate_exit_supported=True,
        remaining_entry_capacity_eur=10_000_000,
        immediate_exit_coverage_pct=100.0,
        position_pct_of_market=None,
        position_pct_reference=None,
        observed_daily_turnover_eur=None,
        position_pct_of_daily_turnover=None,
        liquidity_evidence_level="position_depth",
        reference_yield_pct=None,
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=False,
        rejection_reason=None,
        notes="Deterministic 4C validation fixture.",
    )


def build_aave_unsupported_position(
) -> PositionAnalysis:
    return PositionAnalysis(
        analysis_id="test_aave_eurc_5m",
        instrument_id=(
            AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
        ),
        market_id=(
            AAVE_V3_BASE_EURC_MARKET.market_id
        ),
        access_route_id=(
            AAVE_V3_BASE_EURC_DIRECT_ACCESS.access_route_id
        ),
        position_size_eur=5_000_000,
        entry_supported=True,
        immediate_exit_supported=False,
        remaining_entry_capacity_eur=10_000_000,
        immediate_exit_coverage_pct=72.27,
        position_pct_of_market=None,
        position_pct_reference=None,
        observed_daily_turnover_eur=None,
        position_pct_of_daily_turnover=None,
        liquidity_evidence_level="position_depth",
        reference_yield_pct=None,
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=False,
        rejection_reason=None,
        notes="Deterministic 4C validation fixture.",
    )


def build_xeon_unknown_position(
) -> PositionAnalysis:
    return PositionAnalysis(
        analysis_id="test_xeon_5m",
        instrument_id=(
            XEON_INSTRUMENT.instrument_id
        ),
        market_id=(
            XEON_MARKET.market_id
        ),
        access_route_id=(
            XEON_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=5_000_000,
        entry_supported=None,
        immediate_exit_supported=None,
        remaining_entry_capacity_eur=None,
        immediate_exit_coverage_pct=None,
        position_pct_of_market=None,
        position_pct_reference=None,
        observed_daily_turnover_eur=19_360_381,
        position_pct_of_daily_turnover=25.83,
        liquidity_evidence_level="market_activity",
        reference_yield_pct=None,
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=False,
        rejection_reason=None,
        notes="Deterministic 4C validation fixture.",
    )


def build_supported_liquidity_assessment(
    position: PositionAnalysis,
) -> LiquidityEvidenceAssessment:
    return LiquidityEvidenceAssessment(
        assessment_id=(
            f"{position.analysis_id}_liquidity"
        ),
        instrument_id=position.instrument_id,
        market_id=position.market_id,
        access_route_id=position.access_route_id,
        position_size_eur=position.position_size_eur,
        evidence_level="position_depth",
        evidence_rank=5,
        market_activity_observed=False,
        displayed_quote_observed=False,
        displayed_size_observed=False,
        executable_quote_observed=False,
        position_depth_observed=True,
        immediate_liquidity_supported=True,
        sufficient_for_immediate_liquidity=True,
        strongest_supported_claim=(
            "Position-size immediate liquidity is directly "
            "supported."
        ),
        missing_evidence=None,
        notes="Deterministic 4C validation fixture.",
    )


def build_unsupported_liquidity_assessment(
    position: PositionAnalysis,
) -> LiquidityEvidenceAssessment:
    return LiquidityEvidenceAssessment(
        assessment_id=(
            f"{position.analysis_id}_liquidity"
        ),
        instrument_id=position.instrument_id,
        market_id=position.market_id,
        access_route_id=position.access_route_id,
        position_size_eur=position.position_size_eur,
        evidence_level="position_depth",
        evidence_rank=5,
        market_activity_observed=False,
        displayed_quote_observed=False,
        displayed_size_observed=False,
        executable_quote_observed=False,
        position_depth_observed=True,
        immediate_liquidity_supported=False,
        sufficient_for_immediate_liquidity=True,
        strongest_supported_claim=(
            "Position-size immediate liquidity is directly "
            "not supported."
        ),
        missing_evidence=None,
        notes="Deterministic 4C validation fixture.",
    )


def build_unknown_liquidity_assessment(
    position: PositionAnalysis,
) -> LiquidityEvidenceAssessment:
    return LiquidityEvidenceAssessment(
        assessment_id=(
            f"{position.analysis_id}_liquidity"
        ),
        instrument_id=position.instrument_id,
        market_id=position.market_id,
        access_route_id=position.access_route_id,
        position_size_eur=position.position_size_eur,
        evidence_level="market_activity",
        evidence_rank=1,
        market_activity_observed=True,
        displayed_quote_observed=False,
        displayed_size_observed=False,
        executable_quote_observed=False,
        position_depth_observed=False,
        immediate_liquidity_supported=None,
        sufficient_for_immediate_liquidity=False,
        strongest_supported_claim=(
            "Market activity is observed, but position-size "
            "immediate liquidity is not established."
        ),
        missing_evidence=(
            "Position-size executable depth is required."
        ),
        notes="Deterministic 4C validation fixture.",
    )


def print_case(
    label: str,
    position: PositionAnalysis,
    liquidity_assessment: LiquidityEvidenceAssessment,
    base_risk_assessments,
) -> None:
    assessments = (
        build_position_risk_assessments(
            risk_assessments=(
                base_risk_assessments
            ),
            position=position,
            liquidity_assessment=(
                liquidity_assessment
            ),
        )
    )

    liquidity_risk = (
        get_liquidity_position_risk(
            assessments
        )
    )

    print(label)
    print()

    print(
        f"Position size:           "
        f"EUR {position.position_size_eur:,.0f}"
    )

    print(
        f"Base liquidity risk:     "
        f"{liquidity_risk.base_risk_level}"
    )

    print(
        f"Position-sensitive:      "
        f"{liquidity_risk.position_sensitive}"
    )

    print(
        f"Position risk status:    "
        f"{liquidity_risk.position_risk_status}"
    )

    print(
        f"Evidence sufficient:     "
        f"{liquidity_risk.evidence_sufficient}"
    )

    if (
        position.immediate_exit_coverage_pct
        is not None
    ):
        print(
            f"Immediate exit coverage: "
            f"{position.immediate_exit_coverage_pct:.2f}%"
        )
    else:
        print(
            "Immediate exit coverage: UNKNOWN"
        )

    print()

    print(
        f"Rationale: "
        f"{liquidity_risk.rationale}"
    )

    print()
    print("-" * 80)
    print()


def main() -> None:
    aave_risk = (
        get_aave_eurc_risk_assessments()
    )

    xeon_risk = (
        get_xeon_risk_assessments()
    )

    aave_100k = (
        build_aave_supported_position()
    )

    aave_5m = (
        build_aave_unsupported_position()
    )

    xeon_5m = (
        build_xeon_unknown_position()
    )

    print("POSITION-AWARE RISK")
    print()

    print(
        "Position size modifies a risk conclusion only when "
        "position-specific evidence supports doing so."
    )

    print()
    print("-" * 80)
    print()

    print_case(
        label="AAVE EURC - EUR 100K",
        position=aave_100k,
        liquidity_assessment=(
            build_supported_liquidity_assessment(
                aave_100k
            )
        ),
        base_risk_assessments=aave_risk,
    )

    print_case(
        label="AAVE EURC - EUR 5M",
        position=aave_5m,
        liquidity_assessment=(
            build_unsupported_liquidity_assessment(
                aave_5m
            )
        ),
        base_risk_assessments=aave_risk,
    )

    print_case(
        label="XEON - EUR 5M",
        position=xeon_5m,
        liquidity_assessment=(
            build_unknown_liquidity_assessment(
                xeon_5m
            )
        ),
        base_risk_assessments=xeon_risk,
    )

    print("INTERPRETATION")
    print()

    print(
        "supported means direct evidence supports immediate "
        "liquidity for the modeled position size."
    )

    print(
        "not_supported means direct evidence shows the modeled "
        "position cannot currently be fully exited immediately."
    )

    print(
        "unknown means the available evidence does not establish "
        "position-size executable liquidity."
    )

    print(
        "These statuses do not automatically become qualitative "
        "low, moderate, high, or very-high risk ratings."
    )


if __name__ == "__main__":
    main()