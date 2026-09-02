from __future__ import annotations

from treasury_intelligence.analytics.bond_returns import (
    build_ibkr_europe_otc_bond_return_components,
)

from treasury_intelligence.analytics.bubill_risk_assessments import (
    get_bubill_2027_08_18_risk_assessments,
)

from treasury_intelligence.analytics.execution_estimates import (
    SOVEREIGN_BILL_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS,
)

from treasury_intelligence.analytics.positions import (
    build_sovereign_bill_position_analysis,
)

from treasury_intelligence.analytics.universe import (
    analyze_opportunity_position,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.sources.germany import (
    BUBILL_2027_08_18,
    BUBILL_2027_08_18_ACCESSIBILITY,
    BUBILL_2027_08_18_MARKET,
    get_bubill_2027_08_18_market_observation,
    get_bubill_2027_08_18_snapshot,
)

from treasury_intelligence.sources.ibkr_fixed_income import (
    IBKR_EUROPE_OTC_BOND_EVIDENCE,
)


POSITION_SIZES_EUR = (
    100_000.0,
    500_000.0,
    1_000_000.0,
    2_000_000.0,
    5_000_000.0,
)

HOLDING_PERIOD_DAYS = 365


def build_candidate(
    position_size_eur: float,
):
    snapshot = (
        get_bubill_2027_08_18_snapshot()
    )

    market_observation = (
        get_bubill_2027_08_18_market_observation()
    )

    size_id = int(position_size_eur)

    return analyze_opportunity_position(
        assessment_id=(
            f"bubill_2027_08_18_{size_id}_validation"
        ),
        label="German Bubill Aug 2027",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=BUBILL_2027_08_18,
        market=BUBILL_2027_08_18_MARKET,
        accessibility=(
            BUBILL_2027_08_18_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=HOLDING_PERIOD_DAYS,
        position_builder=lambda size: (
            build_sovereign_bill_position_analysis(
                snapshot=snapshot,
                market_observation=(
                    market_observation
                ),
                position_size_eur=size,
            )
        ),
        risk_assessments=(
            get_bubill_2027_08_18_risk_assessments()
        ),
        return_component_builder=lambda size: (
            build_ibkr_europe_otc_bond_return_components(
                instrument=BUBILL_2027_08_18,
                market=BUBILL_2027_08_18_MARKET,
                snapshot=snapshot,
                position_size_eur=size,
                reference_yield_includes_product_fee=None,
                trading_cost_evidence=(
                    IBKR_EUROPE_OTC_BOND_EVIDENCE
                ),
                estimated_roundtrip_slippage_bps=(
                    SOVEREIGN_BILL_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS
                ),
            )
        ),
        market_observation=market_observation,
        notes=(
            "Milestone 13E.2A validation candidate for "
            "German Bubill DE000BU0E444 using the existing "
            "generic sovereign-bill analysis pipeline."
        ),
    )


def print_candidate_result(
    *,
    position_size_eur: float,
    outstanding_amount_eur: float,
) -> None:
    candidate = build_candidate(
        position_size_eur
    )

    position_pct = (
        position_size_eur
        / outstanding_amount_eur
        * 100
    )

    print(
        f"position_eur={position_size_eur:,.0f}"
    )
    print(
        f"position_pct_of_issue={position_pct:.6f}%"
    )
    print(
        "eligibility_status="
        f"{candidate.eligibility_status}"
    )
    print(
        "liquidity_position_status="
        f"{candidate.liquidity_position_status}"
    )
    print(
        f"economics_status={candidate.economics_status}"
    )
    print(
        "candidate_status="
        f"{candidate.candidate_status}"
    )

    if candidate.defensible_return_pct is None:
        print(
            "defensible_return_pct=None"
        )
    else:
        print(
            "defensible_return_pct="
            f"{candidate.defensible_return_pct:.3f}"
        )

    print(
        "defensible_return_measure="
        f"{candidate.defensible_return_measure}"
    )
    print(
        "recommendation_ready="
        f"{candidate.recommendation_ready}"
    )
    print(
        "base_risk_unknown_dimensions="
        f"{candidate.base_risk_unknown_dimension_count}"
    )
    print(
        "blocking_reasons="
        f"{len(candidate.blocking_reasons)}"
    )
    print(
        "evidence_requirements="
        f"{len(candidate.evidence_requirements)}"
    )

    if candidate.blocking_reasons:
        for reason in candidate.blocking_reasons:
            print(
                f"   blocker={reason}"
            )

    if candidate.evidence_requirements:
        for requirement in candidate.evidence_requirements:
            print(
                f"   evidence={requirement}"
            )

    print()


def main() -> None:
    snapshot = (
        get_bubill_2027_08_18_snapshot()
    )

    if snapshot.outstanding_amount_eur is None:
        raise ValueError(
            "German Bubill August 2027 snapshot must contain "
            "outstanding_amount_eur for position-scale analysis."
        )

    print("===== GERMAN BUBILL AUG 2027 =====")
    print(
        f"instrument_id={BUBILL_2027_08_18.instrument_id}"
    )
    print(
        f"isin={BUBILL_2027_08_18.isin}"
    )
    print(
        f"maturity={BUBILL_2027_08_18.maturity_date}"
    )
    print(
        "reference_yield_pct="
        f"{snapshot.yield_value_pct:.3f}"
    )
    print(
        "outstanding_amount_eur="
        f"{snapshot.outstanding_amount_eur:,.0f}"
    )

    print()
    print("===== POSITION MATRIX =====")

    for position_size_eur in POSITION_SIZES_EUR:
        print_candidate_result(
            position_size_eur=position_size_eur,
            outstanding_amount_eur=(
                snapshot.outstanding_amount_eur
            ),
        )

    five_million = build_candidate(
        5_000_000.0
    )

    five_million_pct = (
        5_000_000.0
        / snapshot.outstanding_amount_eur
        * 100
    )

    print("===== EUR 5M RESULT =====")
    print(
        "position_pct_of_issue="
        f"{five_million_pct:.6f}%"
    )
    print(
        "candidate_status="
        f"{five_million.candidate_status}"
    )
    print(
        "eligibility_status="
        f"{five_million.eligibility_status}"
    )
    print(
        "liquidity_position_status="
        f"{five_million.liquidity_position_status}"
    )
    print(
        "economics_status="
        f"{five_million.economics_status}"
    )

    if five_million.defensible_return_pct is None:
        print(
            "defensible_return_pct=None"
        )
    else:
        print(
            "defensible_return_pct="
            f"{five_million.defensible_return_pct:.3f}"
        )

    print(
        "defensible_return_measure="
        f"{five_million.defensible_return_measure}"
    )
    print(
        "recommendation_ready="
        f"{five_million.recommendation_ready}"
    )
    print(
        "blocking_reasons="
        f"{five_million.blocking_reasons}"
    )
    print(
        "evidence_requirements="
        f"{five_million.evidence_requirements}"
    )


if __name__ == "__main__":
    main()