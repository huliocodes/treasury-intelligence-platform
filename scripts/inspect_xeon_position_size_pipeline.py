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

from treasury_intelligence.analytics.portfolio import (
    build_integrated_portfolio_candidate,
)

from treasury_intelligence.analytics.portfolio_construction import (
    build_portfolio_construction,
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

from treasury_intelligence.analytics.xeon_returns import (
    build_xeon_evidence_enriched_return_components,
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

from treasury_intelligence.models.portfolio_construction import (
    AllocationInstruction,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_ACCESSIBILITY,
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
    get_xeon_market_observation,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
)

HOLDING_PERIOD_DAYS = 365

REFERENCE_YIELD_PCT = 2.273


def format_pct(
    value: float | None,
) -> str:
    if value is None:
        return "UNKNOWN"

    return f"{value:.3f}%"


def build_xeon_position(
    position_size_eur: float,
    observed_daily_turnover_eur: float,
) -> PositionAnalysis:
    return PositionAnalysis(
        analysis_id=(
            "xeon_position_size_pipeline_"
            f"{int(position_size_eur)}"
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
            position_size_eur
        ),
        entry_supported=None,
        immediate_exit_supported=None,
        remaining_entry_capacity_eur=None,
        immediate_exit_coverage_pct=None,
        position_pct_of_market=None,
        position_pct_reference=None,
        observed_daily_turnover_eur=(
            observed_daily_turnover_eur
        ),
        position_pct_of_daily_turnover=(
            position_size_eur
            / observed_daily_turnover_eur
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
            "Position-size-specific XEON pipeline "
            "analysis using public Xetra market "
            "activity and separately modeled "
            "execution-cost evidence."
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
        evidence_level=(
            "market_activity"
        ),
        evidence_rank=1,
        market_activity_observed=True,
        displayed_quote_observed=False,
        displayed_size_observed=False,
        executable_quote_observed=False,
        position_depth_observed=False,
        immediate_liquidity_supported=None,
        sufficient_for_immediate_liquidity=False,
        strongest_supported_claim=(
            "Observed market activity establishes "
            "that XEON trades on the sampled market. "
            "Published Xetra XLM may establish "
            "position-sized implicit execution cost "
            "for a matching order size, but does not "
            "by itself establish immediate executable "
            "bid depth for the modeled position."
        ),
        missing_evidence=(
            "Position-size executable bid/ask depth "
            "or equivalent immediate-liquidity "
            "evidence is required."
        ),
        notes=(
            "Liquidity remains deliberately separate "
            "from execution-cost evidence. XLM "
            "transaction-cost evidence is not treated "
            "as proof of immediate exit capacity."
        ),
    )


def build_xeon_candidate(
    position_size_eur: float,
):
    market_observation = (
        get_xeon_market_observation()
    )

    position = (
        build_xeon_position(
            position_size_eur=(
                position_size_eur
            ),
            observed_daily_turnover_eur=(
                market_observation
                .daily_turnover_eur
            ),
        )
    )

    liquidity = (
        build_xeon_liquidity_assessment(
            position=position,
        )
    )

    eligibility = (
        evaluate_eligibility(
            mandate=MODEL_COMPANY_MANDATE,
            instrument=XEON_INSTRUMENT,
            market=XEON_MARKET,
            accessibility=XEON_ACCESSIBILITY,
            position=position,
        )
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

    components = (
        build_xeon_evidence_enriched_return_components(
            assessment_id=(
                "xeon_pipeline_execution_"
                f"{int(position_size_eur)}"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=(
                XEON_MARKET.market_id
            ),
            position_size_eur=(
                position_size_eur
            ),
            reference_yield_pct=(
                REFERENCE_YIELD_PCT
            ),
            current_daily_turnover_eur=(
                market_observation
                .daily_turnover_eur
            ),
        )
    )

    return_analysis = (
        build_return_analysis(
            analysis_id=(
                "xeon_pipeline_return_"
                f"{int(position_size_eur)}"
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
                position_size_eur
            ),
            holding_period_days=(
                HOLDING_PERIOD_DAYS
            ),
            components=components,
            notes=(
                "XEON full candidate-pipeline return "
                "analysis using centralized "
                "evidence-enriched return components."
            ),
        )
    )

    economics = (
        build_economics_evidence_assessment(
            return_analysis
        )
    )

    candidate = (
        build_integrated_portfolio_candidate(
            assessment_id=(
                "xeon_pipeline_candidate_"
                f"{int(position_size_eur)}"
            ),
            label=(
                f"XEON EUR "
                f"{position_size_eur:,.0f}"
            ),
            eligibility=eligibility,
            risk_assessments=base_risk,
            position_risk_assessments=(
                position_risk
            ),
            economics=economics,
            return_analysis=return_analysis,
            notes=(
                "8B.5 position-size candidate "
                "integration."
            ),
        )
    )

    liquidity_risk = next(
        assessment
        for assessment in position_risk
        if assessment.risk_dimension
        == "liquidity"
    )

    return {
        "position": position,
        "liquidity": liquidity,
        "eligibility": eligibility,
        "base_risk": base_risk,
        "position_risk": position_risk,
        "liquidity_risk": liquidity_risk,
        "return_analysis": return_analysis,
        "economics": economics,
        "candidate": candidate,
    }


def build_construction_for_candidate(
    candidate,
):
    instructions = ()

    if candidate.recommendation_ready:
        instructions = (
            AllocationInstruction(
                candidate_assessment_id=(
                    candidate.assessment_id
                ),
                allocation_eur=(
                    candidate.position_size_eur
                ),
            ),
        )

    return build_portfolio_construction(
        construction_id=(
            "xeon_pipeline_construction_"
            f"{int(candidate.position_size_eur)}"
        ),
        mandate=MODEL_COMPANY_MANDATE,
        candidates=(
            candidate,
        ),
        instructions=instructions,
        notes=(
            "8B.5 construction follows upstream "
            "candidate readiness and does not "
            "force an allocation."
        ),
    )


def print_reasons(
    title: str,
    values: tuple,
) -> None:
    if not values:
        return

    print()
    print(title)

    for value in values:
        print(
            f"  - {value}"
        )


def print_case(
    result: dict,
) -> None:
    position = result["position"]
    liquidity = result["liquidity"]
    eligibility = result["eligibility"]
    liquidity_risk = result["liquidity_risk"]
    return_analysis = result["return_analysis"]
    economics = result["economics"]
    candidate = result["candidate"]

    construction = (
        build_construction_for_candidate(
            candidate=candidate,
        )
    )

    print(
        f"EUR {position.position_size_eur:,.0f} POSITION"
    )
    print()

    print(
        "POSITION"
    )
    print()

    print(
        f"Daily turnover:               "
        f"EUR "
        f"{position.observed_daily_turnover_eur:,.0f}"
    )

    print(
        f"Position / daily turnover:    "
        f"{position.position_pct_of_daily_turnover:.2f}%"
    )

    print(
        f"Immediate exit supported:     "
        f"{position.immediate_exit_supported}"
    )

    print()

    print(
        "LIQUIDITY"
    )
    print()

    print(
        f"Evidence level:               "
        f"{liquidity.evidence_level}"
    )

    print(
        f"Market activity observed:     "
        f"{liquidity.market_activity_observed}"
    )

    print(
        f"Position depth observed:      "
        f"{liquidity.position_depth_observed}"
    )

    print(
        f"Immediate liquidity:          "
        f"{liquidity.immediate_liquidity_supported}"
    )

    print(
        f"Sufficient evidence:          "
        f"{liquidity.sufficient_for_immediate_liquidity}"
    )

    print()

    print(
        "ELIGIBILITY"
    )
    print()

    print(
        f"Overall status:               "
        f"{eligibility.overall_status}"
    )

    print()

    print(
        "POSITION-AWARE RISK"
    )
    print()

    print(
        f"Liquidity risk status:        "
        f"{liquidity_risk.position_risk_status}"
    )

    print()

    print(
        "ECONOMICS"
    )
    print()

    print(
        f"Return after known costs:     "
        f"{format_pct(return_analysis.return_after_known_costs_pct)}"
    )

    print(
        f"Realistic expected return:    "
        f"{format_pct(return_analysis.realistic_expected_return_pct)}"
    )

    print(
        f"Economics status:             "
        f"{economics.economics_status}"
    )

    print(
        f"Economics blocking gaps:      "
        f"{economics.blocking_gap_count}"
    )

    print()

    print(
        "INTEGRATED CANDIDATE"
    )
    print()

    print(
        f"Candidate status:             "
        f"{candidate.candidate_status}"
    )

    print(
        f"Recommendation ready:         "
        f"{candidate.recommendation_ready}"
    )

    print(
        f"Candidate eligibility:        "
        f"{candidate.eligibility_status}"
    )

    print(
        f"Candidate liquidity:          "
        f"{candidate.liquidity_position_status}"
    )

    print(
        f"Candidate economics:          "
        f"{candidate.economics_status}"
    )

    print(
        f"Unknown base-risk dimensions: "
        f"{candidate.base_risk_unknown_dimension_count}"
    )

    print(
        f"Defensible return:            "
        f"{format_pct(candidate.defensible_return_pct)}"
    )

    print(
        f"Return context:               "
        f"{candidate.defensible_return_measure}"
    )

    print_reasons(
        title="BLOCKING REASONS",
        values=(
            candidate.blocking_reasons
        ),
    )

    print_reasons(
        title="EVIDENCE REQUIRED",
        values=(
            candidate.evidence_requirements
        ),
    )

    print()

    print(
        "PORTFOLIO CONSTRUCTION"
    )
    print()

    print(
        f"Construction status:          "
        f"{construction.construction_status}"
    )

    print(
        f"Recommendation-ready count:  "
        f"{construction.recommendation_ready_candidate_count}"
    )

    print(
        f"Allocated capital:            "
        f"EUR {construction.allocated_capital_eur:,.0f}"
    )

    print(
        f"Unallocated capital:          "
        f"EUR {construction.unallocated_capital_eur:,.0f}"
    )

    if construction.validation_issues:
        print()

        print(
            "CONSTRUCTION VALIDATION ISSUES"
        )

        for issue in (
            construction.validation_issues
        ):
            print(
                f"  - {issue}"
            )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print(
        "XEON POSITION-SIZE FULL CANDIDATE PIPELINE"
    )

    print()

    print(
        "This inspection compares EUR 100k and "
        "EUR 500k XEON allocations through the "
        "existing eligibility, liquidity, risk, "
        "economics, candidate, and portfolio-"
        "construction layers."
    )

    print()

    print(
        "Execution-cost evidence and immediate-"
        "liquidity evidence remain separate."
    )

    print()

    print("=" * 100)
    print()

    results = []

    for position_size_eur in (
        POSITION_SIZES_EUR
    ):
        result = (
            build_xeon_candidate(
                position_size_eur=(
                    position_size_eur
                ),
            )
        )

        results.append(
            result
        )

        print_case(
            result=result,
        )

    print(
        "POSITION-SIZE COMPARISON"
    )

    print()

    print(
        f"{'Measure':<35}"
        f"{'EUR 100k':<25}"
        f"{'EUR 500k':<25}"
    )

    print(
        "-" * 85
    )

    for result in results:
        pass

    result_100k = results[0]
    result_500k = results[1]

    rows = (
        (
            "Eligibility",
            result_100k[
                "candidate"
            ].eligibility_status,
            result_500k[
                "candidate"
            ].eligibility_status,
        ),
        (
            "Liquidity position status",
            result_100k[
                "candidate"
            ].liquidity_position_status,
            result_500k[
                "candidate"
            ].liquidity_position_status,
        ),
        (
            "Economics",
            result_100k[
                "candidate"
            ].economics_status,
            result_500k[
                "candidate"
            ].economics_status,
        ),
        (
            "Realistic return",
            format_pct(
                result_100k[
                    "return_analysis"
                ].realistic_expected_return_pct
            ),
            format_pct(
                result_500k[
                    "return_analysis"
                ].realistic_expected_return_pct
            ),
        ),
        (
            "Candidate status",
            result_100k[
                "candidate"
            ].candidate_status,
            result_500k[
                "candidate"
            ].candidate_status,
        ),
        (
            "Recommendation ready",
            str(
                result_100k[
                    "candidate"
                ].recommendation_ready
            ),
            str(
                result_500k[
                    "candidate"
                ].recommendation_ready
            ),
        ),
    )

    for label, value_100k, value_500k in rows:
        print(
            f"{label:<35}"
            f"{str(value_100k):<25}"
            f"{str(value_500k):<25}"
        )

    print()

    print(
        "INTERPRETATION"
    )
    print()

    print(
        "EUR 100k now has evidence-complete "
        "return economics. If it remains "
        "non-ready, the output identifies the "
        "remaining non-economic gate rather than "
        "silently treating economics completion "
        "as recommendation readiness."
    )

    print()

    print(
        "EUR 500k should remain economically "
        "incomplete because the EUR 100k Xetra "
        "XLM observation is not extrapolated to "
        "five times the measured order size."
    )

    print()

    print(
        "Portfolio construction follows the "
        "upstream candidate assessment. It does "
        "not allocate capital merely because an "
        "instrument has an attractive or "
        "calculable return."
    )


if __name__ == "__main__":
    main()