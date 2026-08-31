from __future__ import annotations

from treasury_intelligence.analytics.bond_returns import (
    build_ibkr_europe_otc_bond_return_components,
)

from treasury_intelligence.analytics.bubill_risk_assessments import (
    get_bubill_risk_assessments,
)

from treasury_intelligence.analytics.execution_estimates import (
    ETF_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS,
    SOVEREIGN_BILL_STRONG_INFERRED_ROUNDTRIP_SLIPPAGE_BPS,
)

from treasury_intelligence.analytics.ibkr_returns import (
    build_ibkr_return_components,
)

from treasury_intelligence.analytics.positions import (
    build_etf_position_analysis,
    build_sovereign_bill_position_analysis,
)

from treasury_intelligence.analytics.risk_assessments import (
    get_btf_risk_assessments,
    get_ernx_risk_assessments,
)

from treasury_intelligence.analytics.universe import (
    analyze_opportunity_position,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
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

from treasury_intelligence.sources.ibkr import (
    IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE,
    IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE,
)

from treasury_intelligence.sources.ibkr_fixed_income import (
    IBKR_EUROPE_OTC_BOND_EVIDENCE,
)

from treasury_intelligence.sources.ishares import (
    ERNX_ACCESSIBILITY,
    ERNX_INSTRUMENT,
    ERNX_MARKET,
    get_ernx_market_observation,
    get_ernx_snapshot,
)


DEFAULT_HOLDING_PERIOD_DAYS = 365


def _position_size_id(
    position_size_eur: float,
) -> str:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    return str(
        int(
            round(
                position_size_eur
            )
        )
    )


def build_ernx_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    snapshot = get_ernx_snapshot()

    market_observation = (
        get_ernx_market_observation()
    )

    position_scale_eur = (
        snapshot.share_class_aum_eur
        or snapshot.fund_aum_eur
    )

    if position_scale_eur is None:
        raise ValueError(
            "ERNX requires a fund or share-class "
            "scale for position analysis."
        )

    position_scale_reference = (
        "share_class_aum"
        if snapshot.share_class_aum_eur is not None
        else "fund_aum"
    )

    size_id = _position_size_id(
        position_size_eur
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"ernx_{size_id}_recommendation"
        ),
        label="ERNX",
        mandate=mandate,
        instrument=ERNX_INSTRUMENT,
        market=ERNX_MARKET,
        accessibility=ERNX_ACCESSIBILITY,
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
        position_builder=lambda size: (
            build_etf_position_analysis(
                snapshot=snapshot,
                position_size_eur=size,
                position_scale_eur=(
                    position_scale_eur
                ),
                position_scale_reference=(
                    position_scale_reference
                ),
                market_observation=(
                    market_observation
                ),
            )
        ),
        risk_assessments=(
            get_ernx_risk_assessments()
        ),
        return_component_builder=lambda _size: (
            build_ibkr_return_components(
                instrument=ERNX_INSTRUMENT,
                market=ERNX_MARKET,
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
                    "Conservative estimate for a strongly "
                    "inferred liquid institutional ETF "
                    "position with observed Xetra market "
                    "activity and position size small "
                    "relative to share-class scale"
                ),
            )
        ),
        market_observation=market_observation,
        notes=(
            "Reusable ERNX recommendation candidate "
            "built for an arbitrary position size."
        ),
    )


def build_btf_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    snapshot = (
        get_btf_2027_03_10_snapshot()
    )

    market_observation = (
        get_btf_2027_03_10_market_observation()
    )

    size_id = _position_size_id(
        position_size_eur
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"btf_{size_id}_recommendation"
        ),
        label="French BTF",
        mandate=mandate,
        instrument=BTF_2027_03_10,
        market=BTF_2027_03_10_MARKET,
        accessibility=(
            BTF_2027_03_10_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
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
            build_ibkr_europe_otc_bond_return_components(
                instrument=BTF_2027_03_10,
                market=BTF_2027_03_10_MARKET,
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
            "Reusable French BTF recommendation "
            "candidate built for an arbitrary "
            "position size."
        ),
    )


def build_bubill_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    snapshot = (
        get_bubill_2027_07_14_snapshot()
    )

    market_observation = (
        get_bubill_2027_07_14_market_observation()
    )

    size_id = _position_size_id(
        position_size_eur
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"bubill_{size_id}_recommendation"
        ),
        label="German Bubill",
        mandate=mandate,
        instrument=BUBILL_2027_07_14,
        market=BUBILL_2027_07_14_MARKET,
        accessibility=(
            BUBILL_2027_07_14_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
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
            build_ibkr_europe_otc_bond_return_components(
                instrument=BUBILL_2027_07_14,
                market=BUBILL_2027_07_14_MARKET,
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
            "Reusable German Bubill recommendation "
            "candidate built for an arbitrary "
            "position size."
        ),
    )