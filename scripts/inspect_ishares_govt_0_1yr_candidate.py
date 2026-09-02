from __future__ import annotations

from treasury_intelligence.analytics.execution_estimates import (
    ETF_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS,
)

from treasury_intelligence.analytics.ibkr_returns import (
    build_ibkr_return_components,
)

from treasury_intelligence.analytics.ishares_govt_0_1yr_risk_assessments import (
    get_ishares_govt_0_1yr_risk_assessments,
)

from treasury_intelligence.analytics.positions import (
    build_etf_position_analysis,
)

from treasury_intelligence.analytics.universe import (
    analyze_opportunity_position,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.sources.ibkr import (
    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE,
    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE,
)

from treasury_intelligence.sources.ishares_govt_0_1yr import (
    ISHARES_GOVT_0_1YR_ACCESSIBILITY,
    ISHARES_GOVT_0_1YR_INSTRUMENT,
    ISHARES_GOVT_0_1YR_MARKET,
    get_ishares_govt_0_1yr_market_observation,
    get_ishares_govt_0_1yr_snapshot,
)


POSITION_SIZES_EUR = (
    100_000.0,
    500_000.0,
    1_000_000.0,
    2_000_000.0,
    5_000_000.0,
)

HOLDING_PERIOD_DAYS = 365


def _size_id(
    position_size_eur: float,
) -> str:
    return f"{int(position_size_eur):d}"


def _build_position_analysis(
    position_size_eur: float,
):
    snapshot = get_ishares_govt_0_1yr_snapshot()

    market_observation = (
        get_ishares_govt_0_1yr_market_observation()
    )

    position_scale_eur = (
        snapshot.share_class_aum_eur
        or snapshot.fund_aum_eur
    )

    if position_scale_eur is None:
        raise ValueError(
            "iShares Govt Bond 0-1yr requires fund "
            "or share-class scale."
        )

    position_scale_reference = (
        "share_class_aum"
        if snapshot.share_class_aum_eur is not None
        else "fund_aum"
    )

    return build_etf_position_analysis(
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        position_scale_eur=position_scale_eur,
        position_scale_reference=(
            position_scale_reference
        ),
        market_observation=market_observation,
    )


def build_candidate(
    position_size_eur: float,
):
    snapshot = get_ishares_govt_0_1yr_snapshot()

    market_observation = (
        get_ishares_govt_0_1yr_market_observation()
    )

    return analyze_opportunity_position(
        assessment_id=(
            "ishares_govt_0_1yr_"
            f"{_size_id(position_size_eur)}_standalone"
        ),
        label="iShares € Govt Bond 0-1yr",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=ISHARES_GOVT_0_1YR_INSTRUMENT,
        market=ISHARES_GOVT_0_1YR_MARKET,
        accessibility=ISHARES_GOVT_0_1YR_ACCESSIBILITY,
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=HOLDING_PERIOD_DAYS,
        position_builder=lambda size: (
            _build_position_analysis(size)
        ),
        risk_assessments=(
            get_ishares_govt_0_1yr_risk_assessments()
        ),
        return_component_builder=lambda _size: (
            build_ibkr_return_components(
                instrument=ISHARES_GOVT_0_1YR_INSTRUMENT,
                market=ISHARES_GOVT_0_1YR_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=False,
                access_cost_evidence=(
                    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE
                ),
                trading_cost_evidence=(
                    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE
                ),
                estimated_roundtrip_slippage_bps=(
                    ETF_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS
                ),
                estimated_slippage_basis=(
                    "Conservative V1 roundtrip ETF execution "
                    "estimate. This economics assumption does "
                    "not upgrade the separate position-size "
                    "liquidity conclusion."
                ),
            )
        ),
        market_observation=market_observation,
        notes=(
            "Standalone Milestone 13E.4A analysis using "
            "generic ETF position, liquidity, risk, "
            "eligibility and return infrastructure."
        ),
    )


def _format_return(
    value: float | None,
) -> str:
    if value is None:
        return "None"

    return f"{value:.3f}"


def _print_candidate(
    position_size_eur: float,
) -> None:
    position = _build_position_analysis(
        position_size_eur
    )

    candidate = build_candidate(
        position_size_eur
    )

    print()
    print(
        f"position_size_eur={position_size_eur:,.0f}"
    )

    if position.position_pct_of_market is None:
        print("position_pct_of_share_class=None")
    else:
        print(
            "position_pct_of_share_class="
            f"{position.position_pct_of_market:.6f}%"
        )

    print(
        "position_liquidity_evidence="
        f"{position.liquidity_evidence_level}"
    )

    print(
        "observed_daily_turnover_eur="
        f"{position.observed_daily_turnover_eur}"
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
        "economics_status="
        f"{candidate.economics_status}"
    )

    print(
        "candidate_status="
        f"{candidate.candidate_status}"
    )

    print(
        "defensible_return_pct="
        f"{_format_return(candidate.defensible_return_pct)}"
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
                "blocking_reason="
                f"{reason}"
            )

    if candidate.evidence_requirements:
        for requirement in candidate.evidence_requirements:
            print(
                "evidence_requirement="
                f"{requirement}"
            )


def main() -> None:
    snapshot = get_ishares_govt_0_1yr_snapshot()

    if snapshot.share_class_aum_eur is None:
        raise ValueError(
            "Expected exact share-class AUM."
        )

    threshold_eur = (
        snapshot.share_class_aum_eur
        * 0.005
    )

    print(
        "===== ISHARES GOVT BOND 0-1YR ====="
    )

    print(
        "instrument_id="
        f"{ISHARES_GOVT_0_1YR_INSTRUMENT.instrument_id}"
    )

    print(
        "isin="
        f"{ISHARES_GOVT_0_1YR_INSTRUMENT.isin}"
    )

    print(
        "ticker="
        f"{ISHARES_GOVT_0_1YR_MARKET.ticker}"
    )

    print(
        "reference_ytm_pct="
        f"{snapshot.yield_value_pct:.3f}"
    )

    print(
        "annual_fee_pct="
        f"{snapshot.annual_fee_pct:.3f}"
    )

    print(
        "fund_aum_eur="
        f"{snapshot.fund_aum_eur:,.0f}"
    )

    print(
        "share_class_aum_eur="
        f"{snapshot.share_class_aum_eur:,.0f}"
    )

    print(
        "duration_years="
        f"{snapshot.duration_years}"
    )

    print(
        "average_maturity_years="
        f"{snapshot.average_maturity_years}"
    )

    print(
        "holdings_count="
        f"{snapshot.holdings_count}"
    )

    print(
        "strong_inferred_0_50pct_threshold_eur="
        f"{threshold_eur:,.0f}"
    )

    print(
        "modeled_roundtrip_slippage_bps="
        f"{ETF_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS:.1f}"
    )

    print()
    print("===== POSITION MATRIX =====")

    for position_size_eur in POSITION_SIZES_EUR:
        _print_candidate(position_size_eur)


if __name__ == "__main__":
    main()
