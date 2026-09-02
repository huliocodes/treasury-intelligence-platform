from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.allocation_deltas import (
    build_treasury_allocation_delta,
)

from treasury_intelligence.analytics.cash_returns import (
    build_cash_baseline_return_assessment,
    build_unallocated_return_input,
)

from treasury_intelligence.analytics.economic_comparisons import (
    build_treasury_economic_comparison,
)

from treasury_intelligence.analytics.economics import (
    build_economics_evidence_assessment,
)

from treasury_intelligence.analytics.eligibility import (
    evaluate_eligibility,
)

from treasury_intelligence.analytics.frictions import (
    build_xeon_return_components,
)

from treasury_intelligence.analytics.liquidity import (
    assess_liquidity_evidence,
)

from treasury_intelligence.analytics.monthly_reviews import (
    build_monthly_review_report,
)

from treasury_intelligence.analytics.mandate_surveillance import (
    build_treasury_mandate_surveillance,
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

from treasury_intelligence.analytics.positions import (
    build_xeon_position_analysis,
)

from treasury_intelligence.analytics.rebalance import (
    build_rebalance_decision,
)

from treasury_intelligence.analytics.review_returns import (
    build_allocation_return_input,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
)

from treasury_intelligence.analytics.risk_assessments import (
    get_xeon_risk_assessments,
)

from treasury_intelligence.analytics.risk_sufficiency import (
    assess_risk_evidence_sufficiency,
)

from treasury_intelligence.analytics.switching_friction import (
    build_switching_friction_assessment,
)

from treasury_intelligence.analytics.treasury_state import (
    build_treasury_state,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
    CashBaseline,
)

from treasury_intelligence.models.rebalance import (
    RebalancePolicy,
)

from treasury_intelligence.sources.ecb import (
    fetch_recent_estr,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_ACCESSIBILITY,
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
    build_xeon_snapshot,
    get_xeon_market_observation,
)


POSITION_SIZE_EUR = 500_000

HOLDING_PERIOD_DAYS = 365

REBALANCE_THRESHOLD_BPS = 5.0

AS_OF = "2026-08-30"


def build_xeon_pipeline():
    estr = fetch_recent_estr(
        limit=1
    )[-1]

    snapshot = build_xeon_snapshot(
        estr_rate_pct=estr.rate_pct,
        estr_reference_date=(
            estr.reference_date
        ),
    )

    market_observation = (
        get_xeon_market_observation()
    )

    position = (
        build_xeon_position_analysis(
            snapshot=snapshot,
            position_size_eur=(
                POSITION_SIZE_EUR
            ),
            market_observation=(
                market_observation
            ),
        )
    )

    liquidity = (
        assess_liquidity_evidence(
            market_observation=(
                market_observation
            ),
            position=position,
        )
    )

    eligibility = (
        evaluate_eligibility(
            mandate=MODEL_COMPANY_MANDATE,
            instrument=XEON_INSTRUMENT,
            market=XEON_MARKET,
            accessibility=(
                XEON_ACCESSIBILITY
            ),
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
            liquidity_assessment=(
                liquidity
            ),
        )
    )

    risk_sufficiency = (
        assess_risk_evidence_sufficiency(
            mandate=MODEL_COMPANY_MANDATE,
            risk_assessments=base_risk,
        )
    )

    pre_fee_reference_yield_pct = (
        estr.rate_pct
        + snapshot.benchmark_spread_bps
        / 100
    )

    return_analysis = (
        build_return_analysis(
            analysis_id=(
                "monthly_review_xeon_"
                "500k_365d_return"
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
            components=(
                build_xeon_return_components(
                    position_size_eur=(
                        POSITION_SIZE_EUR
                    ),
                    reference_yield_pct=(
                        pre_fee_reference_yield_pct
                    ),
                )
            ),
            notes=(
                "Monthly-review XEON economics use "
                "the pre-fund-fee benchmark-linked "
                "reference yield. The fund fee is "
                "modeled separately by the friction "
                "component layer."
            ),
        )
    )

    economics = (
        build_economics_evidence_assessment(
            return_analysis
        )
    )

    review_return = (
        build_allocation_return_input(
            label="XEON",
            return_analysis=(
                return_analysis
            ),
            economics=economics,
            notes=(
                "Review-return input derived from "
                "the XEON economics analysis."
            ),
        )
    )

    candidate = (
        build_integrated_portfolio_candidate(
            assessment_id=(
                "monthly_review_xeon_"
                "500k_candidate"
            ),
            label="XEON",
            eligibility=eligibility,
            risk_assessments=base_risk,
            position_risk_assessments=(
                position_risk
            ),
            risk_sufficiency=(
                risk_sufficiency
            ),
            economics=economics,
            return_analysis=(
                return_analysis
            ),
            notes=(
                "XEON candidate derived through "
                "the integrated monthly-review "
                "pipeline."
            ),
        )
    )

    return (
        estr,
        snapshot,
        market_observation,
        position,
        liquidity,
        eligibility,
        base_risk,
        position_risk,
        risk_sufficiency,
        pre_fee_reference_yield_pct,
        return_analysis,
        economics,
        review_return,
        candidate,
    )


def build_model_company_cash_baseline(
    total_cash_eur: float,
) -> CashBaseline:
    if total_cash_eur <= 0:
        return CashBaseline(
            baseline_id=(
                "model_company_cash_baseline_"
                "2026_08_30"
            ),
            mandate_id=(
                MODEL_COMPANY_MANDATE.mandate_id
            ),
            as_of=AS_OF,
            total_cash_eur=0.0,
            balances=(),
            notes=(
                "No currently unallocated treasury "
                "cash exists in this state."
            ),
        )

    unresolved_cash = CashBalance(
        balance_id=(
            "model_company_unresolved_"
            "corporate_cash"
        ),
        label="Unresolved corporate cash",
        balance_type="other_cash",
        balance_eur=total_cash_eur,
        annual_return_pct=None,
        return_evidence_available=False,
        institution=None,
        source_reference=None,
        notes=(
            "The model company does not yet have "
            "verified account-level balance and "
            "cash-remuneration evidence. No bank "
            "allocation or return is invented."
        ),
    )

    return CashBaseline(
        baseline_id=(
            "model_company_cash_baseline_"
            "2026_08_30"
        ),
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        as_of=AS_OF,
        total_cash_eur=total_cash_eur,
        balances=(
            unresolved_cash,
        ),
        notes=(
            "Current unallocated model-company "
            "treasury cash baseline. The full balance "
            "is represented explicitly while its "
            "return remains unresolved."
        ),
    )


def main() -> None:
    print(
        "REAL INTEGRATED MONTHLY TREASURY REVIEW"
    )

    print()

    (
        estr,
        snapshot,
        market_observation,
        position,
        liquidity,
        eligibility,
        base_risk,
        position_risk,
        risk_sufficiency,
        pre_fee_reference_yield_pct,
        return_analysis,
        economics,
        review_return,
        candidate,
    ) = build_xeon_pipeline()

    candidates = (
        candidate,
    )

    construction = (
        build_portfolio_construction(
            construction_id=(
                "monthly_review_construction_"
                "2026_08_30"
            ),
            mandate=(
                MODEL_COMPANY_MANDATE
            ),
            candidates=candidates,
            instructions=(),
            notes=(
                "Portfolio construction consumes "
                "the integrated XEON candidate. "
                "No allocation instruction is "
                "issued because the candidate is "
                "not recommendation-ready."
            ),
        )
    )

    proposal = (
        build_portfolio_proposal(
            proposal_id=(
                "monthly_review_proposal_"
                "2026_08_30"
            ),
            construction=construction,
            candidates=candidates,
            notes=(
                "Monthly-review proposal derived "
                "from integrated analytical "
                "pipeline objects."
            ),
        )
    )

    state = (
        build_treasury_state(
            state_id=(
                "monthly_review_state_"
                "2026_08_30"
            ),
            mandate=(
                MODEL_COMPANY_MANDATE
            ),
            as_of=AS_OF,
            positions=(),
            notes=(
                "Model company currently modeled "
                "as fully unallocated."
            ),
        )
    )

    delta = (
        build_treasury_allocation_delta(
            delta_id=(
                "monthly_review_delta_"
                "2026_08_30"
            ),
            state=state,
            proposal=proposal,
            notes=(
                "Allocation delta derived from "
                "current treasury state and the "
                "current portfolio proposal."
            ),
        )
    )

    cash_baseline = (
        build_model_company_cash_baseline(
            total_cash_eur=(
                state.unallocated_capital_eur
            ),
        )
    )

    cash_return_assessment = (
        build_cash_baseline_return_assessment(
            assessment_id=(
                "model_company_cash_return_"
                "2026_08_30"
            ),
            baseline=cash_baseline,
            notes=(
                "Current model-company cash return "
                "assessment derived from the explicit "
                "cash baseline."
            ),
        )
    )

    current_unallocated_return = (
        build_unallocated_return_input(
            assessment=(
                cash_return_assessment
            ),
            notes=(
                "Current unallocated treasury return "
                "derived from the current cash-baseline "
                "return assessment."
            ),
        )
    )

    if (
        proposal.unallocated_capital_eur
        != state.unallocated_capital_eur
    ):
        raise ValueError(
            "The current 8A.3 integration can reuse "
            "the current cash-baseline return for the "
            "proposed unallocated balance only when "
            "the proposal leaves unallocated capital "
            "unchanged."
        )

    proposed_unallocated_return = (
        build_unallocated_return_input(
            assessment=(
                cash_return_assessment
            ),
            notes=(
                "Proposed unallocated treasury return "
                "uses the same cash-baseline assessment "
                "because the current proposal leaves "
                "unallocated capital unchanged."
            ),
        )
    )

    proposed_position_returns = ()

    if proposal.allocation_lines:
        proposed_position_returns = (
            review_return,
        )

    comparison = (
        build_treasury_economic_comparison(
            comparison_id=(
                "monthly_review_economics_"
                "2026_08_30"
            ),
            state=state,
            proposal=proposal,
            delta=delta,
            current_position_returns=(),
            proposed_position_returns=(
                proposed_position_returns
            ),
            current_unallocated_return=(
                current_unallocated_return
            ),
            proposed_unallocated_return=(
                proposed_unallocated_return
            ),
            notes=(
                "Economic comparison consumes "
                "derived position-return evidence "
                "and cash-baseline return evidence. "
                "Unknown economics remain explicit."
            ),
        )
    )

    switching_friction = (
        build_switching_friction_assessment(
            assessment_id=(
                "monthly_review_switching_"
                "friction_2026_08_30"
            ),
            delta=delta,
            economic_comparison=(
                comparison
            ),
            friction_inputs=(),
            notes=(
                "No switching-friction input is "
                "required when no allocation "
                "movement is proposed."
            ),
        )
    )

    policy = RebalancePolicy(
        policy_id=(
            "monthly_review_validation_policy"
        ),
        minimum_first_year_net_improvement_bps_of_treasury=(
            REBALANCE_THRESHOLD_BPS
        ),
        notes=(
            "Five-basis-point threshold remains "
            "a deterministic validation policy, "
            "not a production treasury policy."
        ),
    )

    decision = (
        build_rebalance_decision(
            decision_id=(
                "monthly_review_decision_"
                "2026_08_30"
            ),
            policy=policy,
            delta=delta,
            economic_comparison=(
                comparison
            ),
            switching_friction=(
                switching_friction
            ),
            notes=(
                "Rebalance decision derived from "
                "the integrated monthly-review "
                "pipeline."
            ),
        )
    )

    mandate_surveillance = (
        build_treasury_mandate_surveillance(
            surveillance_id=(
                "monthly_review_mandate_"
                "surveillance_2026_08_30"
            ),
            state=state,
            holding_assessments=(),
            notes=(
                "The current modeled treasury state "
                "contains no invested positions. "
                "Therefore there are no current holdings "
                "to assess for mandate deterioration."
            ),
        )
    )

    review = (
        build_monthly_review_report(
            review_id=(
                "monthly_review_2026_08_30"
            ),
            state=state,
            proposal=proposal,
            delta=delta,
            economic_comparison=(
                comparison
            ),
            switching_friction=(
                switching_friction
            ),
            rebalance_decision=(
                decision
            ),
            mandate_surveillance=(
                mandate_surveillance
            ),
            notes=(
                "7D/8A integrated monthly-review "
                "pipeline."
            ),
        )
    )

    liquidity_risk = next(
        assessment
        for assessment in position_risk
        if (
            assessment.risk_dimension
            == "liquidity"
        )
    )

    print("SOURCE / MARKET")
    print()

    print(
        f"€STR reference date:           "
        f"{estr.reference_date}"
    )

    print(
        f"€STR rate:                     "
        f"{estr.rate_pct:.3f}%"
    )

    print(
        f"XEON pre-fee reference yield:  "
        f"{pre_fee_reference_yield_pct:.3f}%"
    )

    print(
        f"XEON snapshot yield:           "
        f"{snapshot.yield_value_pct:.3f}%"
    )

    print(
        f"XEON annual fund fee:          "
        f"{snapshot.annual_fee_pct:.3f}%"
    )

    print(
        f"Observed daily turnover:       "
        f"EUR "
        f"{market_observation.daily_turnover_eur:,.0f}"
    )

    print()

    print("UPSTREAM ANALYTICS")
    print()

    print(
        f"Position size:                 "
        f"EUR {position.position_size_eur:,.0f}"
    )

    print(
        f"Liquidity evidence:            "
        f"{liquidity.evidence_level}"
    )

    print(
        f"Immediate liquidity:           "
        f"{liquidity.immediate_liquidity_supported}"
    )

    print(
        f"Eligibility:                   "
        f"{eligibility.overall_status}"
    )

    print(
        f"Base-risk dimensions:          "
        f"{len(base_risk)}"
    )

    print(
        f"Position liquidity risk:       "
        f"{liquidity_risk.position_risk_status}"
    )

    print(
        f"Economics status:              "
        f"{economics.economics_status}"
    )

    print(
        f"Economics blocking gaps:       "
        f"{economics.blocking_gap_count}"
    )

    print(
        f"Return after known costs:      "
        f"{return_analysis.return_after_known_costs_pct:.3f}%"
    )

    if (
        return_analysis.realistic_expected_return_pct
        is None
    ):
        realistic_return_text = "UNKNOWN"
    else:
        realistic_return_text = (
            f"{return_analysis.realistic_expected_return_pct:.3f}%"
        )

    print(
        f"Realistic expected return:     "
        f"{realistic_return_text}"
    )

    if review_return.annual_return_pct is None:
        review_return_text = "UNKNOWN"
    else:
        review_return_text = (
            f"{review_return.annual_return_pct:.3f}%"
        )

    print(
        f"Review return input:           "
        f"{review_return_text}"
    )

    print()

    print("CURRENT CASH BASELINE")
    print()

    print(
        f"Baseline total cash:           "
        f"EUR {cash_baseline.total_cash_eur:,.0f}"
    )

    print(
        f"Cash balance count:            "
        f"{len(cash_baseline.balances)}"
    )

    print(
        f"Return evidence coverage:      "
        f"{cash_return_assessment.return_evidence_coverage_pct:.2f}%"
    )

    print(
        f"Cash economics status:         "
        f"{cash_return_assessment.assessment_status}"
    )

    if (
        cash_return_assessment.blended_annual_return_pct
        is None
    ):
        cash_return_text = "UNKNOWN"
    else:
        cash_return_text = (
            f"{cash_return_assessment.blended_annual_return_pct:.3f}%"
        )

    print(
        f"Blended cash return:           "
        f"{cash_return_text}"
    )

    print(
        f"Review cash evidence:          "
        f"{current_unallocated_return.evidence_available}"
    )

    print()

    print("PORTFOLIO")
    print()

    print(
        f"Candidate status:              "
        f"{candidate.candidate_status}"
    )

    print(
        f"Recommendation ready:          "
        f"{candidate.recommendation_ready}"
    )

    print(
        f"Construction status:           "
        f"{construction.construction_status}"
    )

    print(
        f"Proposal status:               "
        f"{proposal.proposal_status}"
    )

    print(
        f"Proposal decision:             "
        f"{proposal.decision}"
    )

    print()

    print("REVIEW / REBALANCE")
    print()

    print(
        f"Treasury capital:              "
        f"EUR {review.treasury_capital_eur:,.0f}"
    )

    print(
        f"Current invested:              "
        f"EUR "
        f"{review.current_invested_capital_eur:,.0f}"
    )

    print(
        f"Current unallocated:           "
        f"EUR "
        f"{review.current_unallocated_capital_eur:,.0f}"
    )

    print(
        f"Proposed allocated:            "
        f"EUR "
        f"{review.proposed_allocated_capital_eur:,.0f}"
    )

    print(
        f"Proposed unallocated:          "
        f"EUR "
        f"{review.proposed_unallocated_capital_eur:,.0f}"
    )

    print(
        f"Gross position movement:       "
        f"EUR "
        f"{review.gross_position_movement_eur:,.0f}"
    )

    print(
        f"Economic comparison:           "
        f"{comparison.comparison_status}"
    )

    print(
        f"Switching friction:            "
        f"{switching_friction.friction_status}"
    )

    print(
        f"Mandate surveillance:          "
        f"{review.mandate_surveillance_status}"
    )

    print(
        f"Rebalance decision:            "
        f"{review.rebalance_decision}"
    )

    print(
        f"Decision status:               "
        f"{review.rebalance_decision_status}"
    )

    print(
        f"Final review action:           "
        f"{review.review_action}"
    )

    print(
        f"Monthly review status:         "
        f"{review.review_status}"
    )

    print()

    print("SUMMARY")
    print()

    print(
        review.summary
    )

    if (
        review.evidence_blocked_candidate_labels
    ):
        print()
        print(
            "EVIDENCE-BLOCKED CANDIDATES"
        )
        print()

        for label in (
            review.evidence_blocked_candidate_labels
        ):
            print(
                f"  - {label}"
            )

    if cash_return_assessment.evidence_requirements:
        print()
        print(
            "CASH BASELINE EVIDENCE REQUIREMENTS"
        )
        print()

        for requirement in (
            cash_return_assessment.evidence_requirements
        ):
            print(
                f"  - {requirement}"
            )

    if review.evidence_requirements:
        print()
        print(
            "REVIEW EVIDENCE REQUIREMENTS"
        )
        print()

        for requirement in (
            review.evidence_requirements
        ):
            print(
                f"  - {requirement}"
            )

    print()
    print("-" * 100)
    print()

    print("PIPELINE CHECK")
    print()

    print(
        "The monthly review above was not "
        "constructed by manually instantiating "
        "PortfolioProposal, TreasuryAllocationDelta, "
        "TreasuryEconomicComparison, "
        "SwitchingFrictionAssessment, or "
        "RebalanceDecision."
    )

    print()

    print(
        "Those objects were produced by the existing "
        "analytics functions."
    )

    print()

    print(
        "XEON return evidence crosses into the "
        "review layer through the validated "
        "economics-to-review-return adapter."
    )

    print()

    print(
        "The XEON return model uses the pre-fund-fee "
        "benchmark-linked reference yield. The fund "
        "fee and execution costs are then applied "
        "exactly once by the return-component model."
    )

    print()

    print(
        "Current corporate cash return evidence now "
        "crosses into the review layer through "
        "CashBaseline, CashBaselineReturnAssessment, "
        "and build_unallocated_return_input."
    )

    print()

    print(
        "The model-company cash composition is not "
        "invented. Until account-level balance and "
        "return evidence exists, the full unallocated "
        "balance remains explicitly unresolved."
    )


if __name__ == "__main__":
    main()