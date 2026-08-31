from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_DIR),
    )


from treasury_intelligence.analytics.bubill_risk_assessments import (
    get_bubill_risk_assessments,
)

from treasury_intelligence.analytics.generic_risk import (
    build_unknown_risk_assessments,
)

from treasury_intelligence.analytics.generic_returns import (
    build_conservative_return_components,
)

from treasury_intelligence.analytics.positions import (
    build_etf_position_analysis,
    build_money_market_fund_position_analysis,
    build_sovereign_bill_position_analysis,
)

from treasury_intelligence.analytics.risk_assessments import (
    get_btf_risk_assessments,
    get_ernx_risk_assessments,
    get_xeon_risk_assessments,
)

from treasury_intelligence.analytics.universe import (
    analyze_opportunity_position,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.sources.amundi import (
    AMUNDI_SMART_OVERNIGHT_ACCESSIBILITY,
    AMUNDI_SMART_OVERNIGHT_FUND_AUM_EUR,
    AMUNDI_SMART_OVERNIGHT_INSTRUMENT,
    AMUNDI_SMART_OVERNIGHT_MARKET,
    build_amundi_smart_overnight_snapshot,
)

from treasury_intelligence.sources.blackrock import (
    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0,
    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_ACCESSIBILITY,
    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MARKET,
    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MINIMUM_EUR,
    get_blackrock_ics_euro_liquidity_core_t0_snapshot,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_ACCESSIBILITY,
    BTF_2027_03_10_MARKET,
    get_btf_2027_03_10_market_observation,
    get_btf_2027_03_10_snapshot,
)

from treasury_intelligence.sources.germany import (
    BUBILL_2027_07_14,
    BUBILL_2027_07_14_ACCESSIBILITY,
    BUBILL_2027_07_14_MARKET,
    get_bubill_2027_07_14_market_observation,
    get_bubill_2027_07_14_snapshot,
)

from treasury_intelligence.sources.ishares import (
    ERNX_ACCESSIBILITY,
    ERNX_INSTRUMENT,
    ERNX_MARKET,
    get_ernx_market_observation,
    get_ernx_snapshot,
)

from treasury_intelligence.sources.spiko import (
    SPIKO_EU_TBILLS_ACCESSIBILITY,
    SPIKO_EU_TBILLS_INSTRUMENT,
    SPIKO_EU_TBILLS_MARKET,
    SPIKO_EU_TBILLS_MINIMUM_EUR,
    get_spiko_eu_tbills_snapshot,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_ACCESSIBILITY,
    XEON_FUND_AUM_EUR,
    XEON_INSTRUMENT,
    XEON_MARKET,
    build_xeon_snapshot,
    get_xeon_market_observation,
)


POSITION_SIZE_EUR = 1_000_000.0
HOLDING_PERIOD_DAYS = 365

ESTR_RATE_PCT = 2.188
ESTR_REFERENCE_DATE = "2026-08-27"


def print_candidate(
    candidate,
) -> None:
    print(candidate.label)
    print("-" * 70)

    print(
        "Position:",
        f"EUR {candidate.position_size_eur:,.0f}",
    )

    print(
        "Eligibility:",
        candidate.eligibility_status,
    )

    print(
        "Liquidity:",
        candidate.liquidity_position_status,
    )

    print(
        "Economics:",
        candidate.economics_status,
    )

    print(
        "Unknown base risk dimensions:",
        candidate.base_risk_unknown_dimension_count,
    )

    print(
        "Defensible return:",
        (
            f"{candidate.defensible_return_pct:.3f}%"
            if candidate.defensible_return_pct
            is not None
            else None
        ),
    )

    print(
        "Candidate status:",
        candidate.candidate_status,
    )

    print(
        "Recommendation ready:",
        candidate.recommendation_ready,
    )

    print(
        "Evidence requirements:",
        len(candidate.evidence_requirements),
    )

    print(
        "Blocking reasons:",
        len(candidate.blocking_reasons),
    )

    print()


def build_xeon_candidate():
    snapshot = build_xeon_snapshot(
        estr_rate_pct=ESTR_RATE_PCT,
        estr_reference_date=ESTR_REFERENCE_DATE,
    )

    market_observation = (
        get_xeon_market_observation()
    )

    return analyze_opportunity_position(
        assessment_id="xeon_1m_universe",
        label="XEON",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=XEON_INSTRUMENT,
        market=XEON_MARKET,
        accessibility=XEON_ACCESSIBILITY,
        snapshot=snapshot,
        position_size_eur=POSITION_SIZE_EUR,
        holding_period_days=HOLDING_PERIOD_DAYS,
        position_builder=lambda size: (
            build_etf_position_analysis(
                snapshot=snapshot,
                position_size_eur=size,
                position_scale_eur=XEON_FUND_AUM_EUR,
                position_scale_reference="fund_aum",
                market_observation=(
                    market_observation
                ),
            )
        ),
        risk_assessments=(
            get_xeon_risk_assessments()
        ),
        return_component_builder=lambda size: (
            build_conservative_return_components(
                instrument=XEON_INSTRUMENT,
                market=XEON_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
            )
        ),
        market_observation=market_observation,
    )


def build_amundi_candidate():
    snapshot = (
        build_amundi_smart_overnight_snapshot(
            estr_rate_pct=ESTR_RATE_PCT,
            estr_reference_date=(
                ESTR_REFERENCE_DATE
            ),
        )
    )

    risk = build_unknown_risk_assessments(
        instrument_id=(
            AMUNDI_SMART_OVERNIGHT_INSTRUMENT.instrument_id
        ),
        market_id=(
            AMUNDI_SMART_OVERNIGHT_MARKET.market_id
        ),
        assessed_at="2026-08-31",
    )

    return analyze_opportunity_position(
        assessment_id="amundi_1m_universe",
        label="Amundi Smart Overnight",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=(
            AMUNDI_SMART_OVERNIGHT_INSTRUMENT
        ),
        market=(
            AMUNDI_SMART_OVERNIGHT_MARKET
        ),
        accessibility=(
            AMUNDI_SMART_OVERNIGHT_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=POSITION_SIZE_EUR,
        holding_period_days=HOLDING_PERIOD_DAYS,
        position_builder=lambda size: (
            build_etf_position_analysis(
                snapshot=snapshot,
                position_size_eur=size,
                position_scale_eur=(
                    AMUNDI_SMART_OVERNIGHT_FUND_AUM_EUR
                ),
                position_scale_reference="fund_aum",
                market_observation=None,
            )
        ),
        risk_assessments=risk,
        return_component_builder=lambda size: (
            build_conservative_return_components(
                instrument=(
                    AMUNDI_SMART_OVERNIGHT_INSTRUMENT
                ),
                market=(
                    AMUNDI_SMART_OVERNIGHT_MARKET
                ),
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
            )
        ),
    )


def build_ernx_candidate():
    snapshot = get_ernx_snapshot()
    market_observation = (
        get_ernx_market_observation()
    )

    return analyze_opportunity_position(
        assessment_id="ernx_1m_universe",
        label="ERNX",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=ERNX_INSTRUMENT,
        market=ERNX_MARKET,
        accessibility=ERNX_ACCESSIBILITY,
        snapshot=snapshot,
        position_size_eur=POSITION_SIZE_EUR,
        holding_period_days=HOLDING_PERIOD_DAYS,
        position_builder=lambda size: (
            build_etf_position_analysis(
                snapshot=snapshot,
                position_size_eur=size,
                position_scale_eur=(
                    snapshot.share_class_aum_eur
                    or snapshot.fund_aum_eur
                    or 1.0
                ),
                position_scale_reference=(
                    "share_class_aum"
                    if snapshot.share_class_aum_eur
                    is not None
                    else "fund_aum"
                ),
                market_observation=(
                    market_observation
                ),
            )
        ),
        risk_assessments=(
            get_ernx_risk_assessments()
        ),
        return_component_builder=lambda size: (
            build_conservative_return_components(
                instrument=ERNX_INSTRUMENT,
                market=ERNX_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=None,
            )
        ),
        market_observation=market_observation,
    )


def build_btf_candidate():
    snapshot = get_btf_2027_03_10_snapshot()

    market_observation = (
        get_btf_2027_03_10_market_observation()
    )

    return analyze_opportunity_position(
        assessment_id="btf_1m_universe",
        label="French BTF",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=BTF_2027_03_10,
        market=BTF_2027_03_10_MARKET,
        accessibility=(
            BTF_2027_03_10_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=POSITION_SIZE_EUR,
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
            get_btf_risk_assessments()
        ),
        return_component_builder=lambda size: (
            build_conservative_return_components(
                instrument=BTF_2027_03_10,
                market=BTF_2027_03_10_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=None,
            )
        ),
        market_observation=market_observation,
    )


def build_bubill_candidate():
    snapshot = (
        get_bubill_2027_07_14_snapshot()
    )

    market_observation = (
        get_bubill_2027_07_14_market_observation()
    )

    return analyze_opportunity_position(
        assessment_id="bubill_1m_universe",
        label="German Bubill",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=BUBILL_2027_07_14,
        market=BUBILL_2027_07_14_MARKET,
        accessibility=(
            BUBILL_2027_07_14_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=POSITION_SIZE_EUR,
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
            get_bubill_risk_assessments()
        ),
        return_component_builder=lambda size: (
            build_conservative_return_components(
                instrument=BUBILL_2027_07_14,
                market=BUBILL_2027_07_14_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=None,
            )
        ),
        market_observation=market_observation,
    )


def build_blackrock_candidate():
    snapshot = (
        get_blackrock_ics_euro_liquidity_core_t0_snapshot()
    )

    risk = build_unknown_risk_assessments(
        instrument_id=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0
            .instrument_id
        ),
        market_id=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MARKET
            .market_id
        ),
        assessed_at="2026-08-31",
    )

    return analyze_opportunity_position(
        assessment_id="blackrock_1m_universe",
        label="BlackRock ICS Euro Liquidity",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0
        ),
        market=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MARKET
        ),
        accessibility=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=POSITION_SIZE_EUR,
        holding_period_days=HOLDING_PERIOD_DAYS,
        position_builder=lambda size: (
            build_money_market_fund_position_analysis(
                snapshot=snapshot,
                position_size_eur=size,
                minimum_initial_investment_eur=(
                    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MINIMUM_EUR
                ),
            )
        ),
        risk_assessments=risk,
        return_component_builder=lambda size: (
            build_conservative_return_components(
                instrument=(
                    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0
                ),
                market=(
                    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MARKET
                ),
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
            )
        ),
    )


def build_spiko_candidate():
    snapshot = get_spiko_eu_tbills_snapshot()

    risk = build_unknown_risk_assessments(
        instrument_id=(
            SPIKO_EU_TBILLS_INSTRUMENT.instrument_id
        ),
        market_id=(
            SPIKO_EU_TBILLS_MARKET.market_id
        ),
        assessed_at="2026-08-31",
    )

    return analyze_opportunity_position(
        assessment_id="spiko_1m_universe",
        label="Spiko EU T-Bills",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=(
            SPIKO_EU_TBILLS_INSTRUMENT
        ),
        market=SPIKO_EU_TBILLS_MARKET,
        accessibility=(
            SPIKO_EU_TBILLS_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=POSITION_SIZE_EUR,
        holding_period_days=HOLDING_PERIOD_DAYS,
        position_builder=lambda size: (
            build_money_market_fund_position_analysis(
                snapshot=snapshot,
                position_size_eur=size,
                minimum_initial_investment_eur=(
                    SPIKO_EU_TBILLS_MINIMUM_EUR
                ),
            )
        ),
        risk_assessments=risk,
        return_component_builder=lambda size: (
            build_conservative_return_components(
                instrument=(
                    SPIKO_EU_TBILLS_INSTRUMENT
                ),
                market=SPIKO_EU_TBILLS_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
            )
        ),
    )


def main() -> None:
    candidates = (
        build_xeon_candidate(),
        build_amundi_candidate(),
        build_ernx_candidate(),
        build_btf_candidate(),
        build_bubill_candidate(),
        build_blackrock_candidate(),
        build_spiko_candidate(),
    )

    print()
    print("UNIVERSE ORCHESTRATION")
    print("=" * 70)
    print()

    for candidate in candidates:
        print_candidate(candidate)

    print("=" * 70)
    print()

    print(
        "Candidate count:",
        len(candidates),
    )

    print(
        "Recommendation-ready:",
        sum(
            candidate.recommendation_ready
            for candidate in candidates
        ),
    )

    print(
        "Needs evidence:",
        sum(
            candidate.candidate_status
            == "needs_evidence"
            for candidate in candidates
        ),
    )

    print(
        "Blocked:",
        sum(
            candidate.candidate_status
            == "blocked"
            for candidate in candidates
        ),
    )


if __name__ == "__main__":
    main()