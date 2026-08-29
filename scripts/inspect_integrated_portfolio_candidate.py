from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.economics import (
    build_economics_evidence_assessment,
)

from treasury_intelligence.analytics.eligibility import (
    evaluate_eligibility,
)

from treasury_intelligence.analytics.frictions import (
    build_xeon_return_components,
)

from treasury_intelligence.analytics.portfolio import (
    build_integrated_portfolio_candidate,
)

from treasury_intelligence.analytics.position_risk import (
    build_position_risk_assessments,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
)

from treasury_intelligence.analytics.risk_assessments import (
    get_xeon_risk_assessments,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.liquidity import (
    LiquidityEvidenceAssessment,
)

from treasury_intelligence.models.opportunities import (
    PositionAnalysis,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_ACCESSIBILITY,
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
)


POSITION_SIZE_EUR = 500_000

HOLDING_PERIOD_DAYS = 365

REFERENCE_YIELD_PCT = 2.273


def build_xeon_position(
) -> PositionAnalysis:
    return PositionAnalysis(
        analysis_id=(
            "xeon_500k_integrated_position"
        ),
        instrument_id=(
            XEON_INSTRUMENT.instrument_id
        ),
        market_id=(
            XEON_MARKET.market_id
        ),
        access_route_id=(
            XEON_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=(
            POSITION_SIZE_EUR
        ),
        entry_supported=None,
        immediate_exit_supported=None,
        remaining_entry_capacity_eur=None,
        immediate_exit_coverage_pct=None,
        position_pct_of_market=None,
        position_pct_reference=None,
        observed_daily_turnover_eur=(
            19_360_381
        ),
        position_pct_of_daily_turnover=(
            POSITION_SIZE_EUR
            / 19_360_381
            * 100
        ),
        liquidity_evidence_level=(
            "market_activity"
        ),
        reference_yield_pct=(
            REFERENCE_YIELD_PCT
        ),
        executable_yield_pct=None,
        position_adjusted_yield_pct=None,
        executable_economics_known=False,
        rejection_reason=None,
        notes=(
            "Deterministic 6B XEON integration fixture "
            "using the previously validated public "
            "market-activity observation."
        ),
    )


def build_xeon_liquidity_assessment(
    position: PositionAnalysis,
) -> LiquidityEvidenceAssessment:
    return LiquidityEvidenceAssessment(
        assessment_id=(
            f"{position.analysis_id}_liquidity"
        ),
        instrument_id=(
            position.instrument_id
        ),
        market_id=(
            position.market_id
        ),
        access_route_id=(
            position.access_route_id
        ),
        position_size_eur=(
            position.position_size_eur
        ),
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
            "Observed market activity establishes that "
            "XEON trades on the sampled market, but does "
            "not establish position-size immediate "
            "liquidity."
        ),
        missing_evidence=(
            "Position-size executable bid/ask depth "
            "is required."
        ),
        notes=(
            "Deterministic 6B validation fixture based "
            "on the previously validated XEON market "
            "activity evidence."
        ),
    )


def build_xeon_return_analysis():
    components = (
        build_xeon_return_components(
            position_size_eur=(
                POSITION_SIZE_EUR
            ),
            reference_yield_pct=(
                REFERENCE_YIELD_PCT
            ),
        )
    )

    return build_return_analysis(
        analysis_id=(
            "xeon_500k_365d_integrated_return"
        ),
        instrument_id=(
            XEON_INSTRUMENT.instrument_id
        ),
        market_id=(
            XEON_MARKET.market_id
        ),
        access_route_id=(
            XEON_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=(
            POSITION_SIZE_EUR
        ),
        holding_period_days=(
            HOLDING_PERIOD_DAYS
        ),
        components=components,
        notes=(
            "365-day XEON scenario using the "
            "validated 5B friction evidence."
        ),
    )


def main() -> None:
    position = build_xeon_position()

    liquidity = (
        build_xeon_liquidity_assessment(
            position
        )
    )

    eligibility = evaluate_eligibility(
        mandate=MODEL_COMPANY_MANDATE,
        instrument=XEON_INSTRUMENT,
        market=XEON_MARKET,
        accessibility=XEON_ACCESSIBILITY,
        position=position,
    )

    base_risk = (
        get_xeon_risk_assessments()
    )

    position_risk = (
        build_position_risk_assessments(
            risk_assessments=base_risk,
            position=position,
            liquidity_assessment=liquidity,
        )
    )

    return_analysis = (
        build_xeon_return_analysis()
    )

    economics = (
        build_economics_evidence_assessment(
            return_analysis
        )
    )

    candidate = (
        build_integrated_portfolio_candidate(
            assessment_id=(
                "xeon_500k_integrated_candidate"
            ),
            label="XEON",
            eligibility=eligibility,
            risk_assessments=base_risk,
            position_risk_assessments=(
                position_risk
            ),
            economics=economics,
            return_analysis=return_analysis,
            notes=(
                "6B integrated portfolio-candidate "
                "validation."
            ),
        )
    )

    print(
        "INTEGRATED PORTFOLIO CANDIDATE"
    )

    print()

    print(
        "Portfolio state below is derived from "
        "analytical objects rather than manually "
        "copied status strings."
    )

    print()

    print("-" * 100)
    print()

    print(candidate.label)
    print()

    print(
        f"Position size:                "
        f"EUR {candidate.position_size_eur:,.0f}"
    )

    print(
        f"Candidate status:             "
        f"{candidate.candidate_status}"
    )

    print(
        f"Recommendation ready:         "
        f"{candidate.recommendation_ready}"
    )

    print(
        f"Eligibility:                  "
        f"{candidate.eligibility_status}"
    )

    print(
        f"Position liquidity:           "
        f"{candidate.liquidity_position_status}"
    )

    print(
        f"Economics:                    "
        f"{candidate.economics_status}"
    )

    print(
        f"Unknown base-risk dimensions: "
        f"{candidate.base_risk_unknown_dimension_count}"
    )

    if (
        candidate.defensible_return_pct
        is None
    ):
        print(
            "Defensible return measure:     UNKNOWN"
        )
    else:
        print(
            f"Defensible return measure:     "
            f"{candidate.defensible_return_pct:.3f}%"
        )

    print(
        f"Return measure context:        "
        f"{candidate.defensible_return_measure}"
    )

    if candidate.blocking_reasons:
        print()
        print("BLOCKING REASONS")

        for reason in (
            candidate.blocking_reasons
        ):
            print(
                f"  - {reason}"
            )

    if candidate.evidence_requirements:
        print()
        print("EVIDENCE REQUIRED")

        for requirement in (
            candidate.evidence_requirements
        ):
            print(
                f"  - {requirement}"
            )

    print()
    print("-" * 100)
    print()

    print("SOURCE ANALYSIS CHECK")
    print()

    print(
        f"Eligibility object:           "
        f"{eligibility.overall_status}"
    )

    liquidity_risk = next(
        assessment
        for assessment in position_risk
        if assessment.risk_dimension
        == "liquidity"
    )

    print(
        f"Position-risk object:         "
        f"{liquidity_risk.position_risk_status}"
    )

    print(
        f"Economics object:             "
        f"{economics.economics_status}"
    )

    print(
        f"Economics blocking gaps:      "
        f"{economics.blocking_gap_count}"
    )

    print(
        f"Return after known costs:     "
        f"{return_analysis.return_after_known_costs_pct:.3f}%"
    )

    print(
        f"Realistic expected return:    "
        f"{return_analysis.realistic_expected_return_pct}"
    )

    print()

    print("INTERPRETATION")
    print()

    print(
        "The portfolio candidate did not receive "
        "manually supplied eligibility, liquidity, "
        "risk-count, or economics statuses."
    )

    print(
        "Those values were derived from the existing "
        "analysis objects."
    )

    print(
        "XEON therefore remains evidence-blocked for "
        "the modeled EUR 500k position rather than "
        "being forced into a recommendation."
    )


if __name__ == "__main__":
    main()