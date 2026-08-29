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

from treasury_intelligence.analytics.portfolio_construction import (
    build_portfolio_construction,
)

from treasury_intelligence.analytics.portfolio_proposals import (
    build_portfolio_proposal,
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
            "xeon_500k_proposal_position"
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
            "Deterministic 6D XEON integration fixture "
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
            "Deterministic 6D validation fixture based "
            "on previously validated XEON market "
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
            "xeon_500k_365d_proposal_return"
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


def build_xeon_candidate():
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

    return build_integrated_portfolio_candidate(
        assessment_id=(
            "xeon_500k_proposal_candidate"
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
            "6D proposal integration candidate."
        ),
    )


def main() -> None:
    candidate = (
        build_xeon_candidate()
    )

    candidates = (
        candidate,
    )

    construction = (
        build_portfolio_construction(
            construction_id=(
                "model_company_current_construction"
            ),
            mandate=MODEL_COMPANY_MANDATE,
            candidates=candidates,
            instructions=(),
            notes=(
                "Current candidate universe contains "
                "no recommendation-ready allocation."
            ),
        )
    )

    proposal = (
        build_portfolio_proposal(
            proposal_id=(
                "model_company_current_proposal"
            ),
            construction=construction,
            candidates=candidates,
            notes=(
                "6D decision-ready treasury proposal."
            ),
        )
    )

    print("TREASURY PORTFOLIO PROPOSAL")
    print()

    print(
        "The proposal below is assembled from the "
        "integrated analytical candidate and validated "
        "portfolio construction state."
    )

    print()

    print("-" * 100)
    print()

    print(
        f"Treasury capital:             "
        f"EUR {proposal.treasury_capital_eur:,.0f}"
    )

    print(
        f"Candidates evaluated:         "
        f"{proposal.candidate_count}"
    )

    print(
        f"Recommendation ready:         "
        f"{proposal.recommendation_ready_candidate_count}"
    )

    print(
        f"Proposed allocation:          "
        f"EUR {proposal.allocated_capital_eur:,.0f}"
    )

    print(
        f"Unallocated capital:          "
        f"EUR {proposal.unallocated_capital_eur:,.0f}"
    )

    print(
        f"Proposal status:              "
        f"{proposal.proposal_status}"
    )

    print(
        f"Decision:                     "
        f"{proposal.decision}"
    )

    print()

    if (
        proposal.evidence_blocked_candidate_labels
    ):
        print("EVIDENCE-BLOCKED CANDIDATES")

        for label in (
            proposal
            .evidence_blocked_candidate_labels
        ):
            print(
                f"  - {label}"
            )

        print()

    if proposal.allocation_lines:
        print("PROPOSED ALLOCATIONS")

        for line in proposal.allocation_lines:
            print(
                f"  {line.label:<20} "
                f"EUR {line.allocation_eur:>12,.0f} | "
                f"{line.allocation_pct_of_treasury:>6.2f}%"
            )

        print()

    print("RATIONALE")
    print()

    print(
        proposal.rationale
    )

    print()

    print("-" * 100)
    print()

    print("SOURCE STATE CHECK")
    print()

    print(
        f"XEON candidate status:        "
        f"{candidate.candidate_status}"
    )

    print(
        f"XEON recommendation ready:    "
        f"{candidate.recommendation_ready}"
    )

    print(
        f"Construction status:          "
        f"{construction.construction_status}"
    )

    print(
        f"Construction allocation:      "
        f"EUR {construction.allocated_capital_eur:,.0f}"
    )

    print(
        f"Proposal decision:            "
        f"{proposal.decision}"
    )

    print()

    print("INTERPRETATION")
    print()

    print(
        "XEON remains evidence-blocked upstream."
    )

    print(
        "Portfolio construction therefore allocates "
        "no capital."
    )

    print(
        "The proposal layer preserves that result and "
        "produces HOLD UNALLOCATED rather than inventing "
        "an investment recommendation."
    )


if __name__ == "__main__":
    main()