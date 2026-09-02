from __future__ import annotations

from treasury_intelligence.analytics.icash_risk_assessments import (
    get_icash_risk_assessments,
)

from treasury_intelligence.analytics.local_broker_returns import (
    build_local_broker_return_components,
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

from treasury_intelligence.sources.ecb import (
    fetch_recent_estr,
)

from treasury_intelligence.sources.icash import (
    ICASH_ACCESSIBILITY,
    ICASH_INSTRUMENT,
    ICASH_MARKET,
    get_icash_market_observation,
    get_icash_snapshot,
)


POSITION_SIZES_EUR = (
    100_000.0,
    500_000.0,
    1_000_000.0,
    2_000_000.0,
    5_000_000.0,
)

HOLDING_PERIOD_DAYS = 365


def _latest_estr():
    observations = fetch_recent_estr(limit=5)

    return observations[-1]


def _build_position_analysis(
    position_size_eur: float,
    snapshot,
):
    market_observation = (
        get_icash_market_observation()
    )

    position_scale_eur = (
        snapshot.share_class_aum_eur
        or snapshot.fund_aum_eur
    )

    if position_scale_eur is None:
        raise ValueError(
            "ICASH requires fund scale."
        )

    return build_etf_position_analysis(
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        position_scale_eur=position_scale_eur,
        position_scale_reference="fund_aum",
        market_observation=market_observation,
        notes=(
            "ICASH liquidity is assessed conservatively "
            "using position size relative to current fund "
            "NAV plus verified LJSE market structure. The "
            "existence of a market maker does not establish "
            "large executable depth."
        ),
    )


def build_candidate(
    position_size_eur: float,
    snapshot,
):
    market_observation = (
        get_icash_market_observation()
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"icash_{int(position_size_eur)}_standalone"
        ),
        label="ICASH",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=ICASH_INSTRUMENT,
        market=ICASH_MARKET,
        accessibility=ICASH_ACCESSIBILITY,
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=HOLDING_PERIOD_DAYS,
        position_builder=lambda size: (
            _build_position_analysis(
                size,
                snapshot,
            )
        ),
        risk_assessments=(
            get_icash_risk_assessments()
        ),
        return_component_builder=lambda _size: (
            build_local_broker_return_components(
                instrument=ICASH_INSTRUMENT,
                market=ICASH_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=False,
            )
        ),
        market_observation=market_observation,
        notes=(
            "Standalone Milestone 13E.5A ICASH analysis."
        ),
    )


def _format_return(
    value: float | None,
) -> str:
    if value is None:
        return "None"

    return f"{value:.3f}"


def main() -> None:
    estr = _latest_estr()

    snapshot = get_icash_snapshot(
        estr_rate_pct=estr.rate_pct,
        estr_reference_date=estr.reference_date,
    )

    if snapshot.fund_aum_eur is None:
        raise ValueError(
            "Expected ICASH fund AUM."
        )

    threshold_eur = (
        snapshot.fund_aum_eur
        * 0.005
    )

    print("===== ICASH =====")
    print(
        f"instrument_id={ICASH_INSTRUMENT.instrument_id}"
    )
    print(
        f"isin={ICASH_INSTRUMENT.isin}"
    )
    print(
        f"ticker={ICASH_MARKET.ticker}"
    )
    print(
        f"estr_reference_date={estr.reference_date}"
    )
    print(
        f"estr_rate_pct={estr.rate_pct:.3f}"
    )
    print(
        "reference_yield_measure="
        f"{snapshot.yield_measure}"
    )
    print(
        "reference_yield_pct="
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
        "strong_inferred_0_50pct_threshold_eur="
        f"{threshold_eur:,.0f}"
    )

    print()
    print("===== POSITION MATRIX =====")

    for position_size_eur in POSITION_SIZES_EUR:
        position = _build_position_analysis(
            position_size_eur,
            snapshot,
        )

        candidate = build_candidate(
            position_size_eur,
            snapshot,
        )

        print()
        print(
            f"position_size_eur={position_size_eur:,.0f}"
        )

        print(
            "position_pct_of_fund="
            f"{position.position_pct_of_market:.6f}%"
        )

        print(
            "position_liquidity_evidence="
            f"{position.liquidity_evidence_level}"
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

        for requirement in (
            candidate.evidence_requirements
        ):
            print(
                "evidence_requirement="
                f"{requirement}"
            )


if __name__ == "__main__":
    main()
