from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

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

from treasury_intelligence.analytics.generic_risk import (
    build_unknown_risk_assessments,
)

from treasury_intelligence.analytics.generic_returns import (
    build_conservative_return_components,
)

from treasury_intelligence.analytics.ibkr_returns import (
    build_ibkr_return_components,
)

from treasury_intelligence.analytics.positions import (
    build_aave_position_analysis,
    build_bank_deposit_position_analysis,
    build_etf_position_analysis,
    build_money_market_fund_position_analysis,
    build_sovereign_bill_position_analysis,
)

from treasury_intelligence.analytics.risk_assessments import (
    get_aave_eurc_risk_assessments,
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

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)

from treasury_intelligence.sources.aave import (
    AAVE_V3_BASE_EURC_ACCESSIBILITY,
    AAVE_V3_BASE_EURC_INSTRUMENT,
    AAVE_V3_BASE_EURC_MARKET,
    fetch_aave_v3_base_eurc,
)

from treasury_intelligence.sources.aave_snapshot import (
    build_aave_eurc_snapshot,
)

from treasury_intelligence.sources.addiko import (
    ADDIKO_91_180_DAY_ACCESSIBILITY,
    ADDIKO_91_180_DAY_INSTRUMENT,
    ADDIKO_91_180_DAY_MARKET,
    ADDIKO_91_180_DAY_RATE,
    get_addiko_91_180_day_snapshot,
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


DEFAULT_HOLDING_PERIOD_DAYS = 365

ESTR_RATE_PCT = 2.188
ESTR_REFERENCE_DATE = "2026-08-27"

RISK_ASSESSED_AT = "2026-08-31"


CandidateBuilder = Callable[
    [float, TreasuryMandate],
    PortfolioCandidateAssessment,
]


@dataclass(frozen=True)
class UniverseOpportunity:
    key: str
    label: str
    candidate_builder: CandidateBuilder

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError(
                "Universe opportunity key is required."
            )

        if not self.label:
            raise ValueError(
                "Universe opportunity label is required."
            )


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


def build_xeon_universe_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    snapshot = build_xeon_snapshot(
        estr_rate_pct=ESTR_RATE_PCT,
        estr_reference_date=ESTR_REFERENCE_DATE,
    )

    market_observation = (
        get_xeon_market_observation()
    )

    size_id = _position_size_id(
        position_size_eur
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"xeon_{size_id}_universe"
        ),
        label="XEON",
        mandate=mandate,
        instrument=XEON_INSTRUMENT,
        market=XEON_MARKET,
        accessibility=XEON_ACCESSIBILITY,
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
        position_builder=lambda size: (
            build_etf_position_analysis(
                snapshot=snapshot,
                position_size_eur=size,
                position_scale_eur=XEON_FUND_AUM_EUR,
                position_scale_reference="fund_aum",
                market_observation=market_observation,
            )
        ),
        risk_assessments=(
            get_xeon_risk_assessments()
        ),
        return_component_builder=lambda _size: (
            build_ibkr_return_components(
                instrument=XEON_INSTRUMENT,
                market=XEON_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
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
                    "evidence and position size small "
                    "relative to fund scale"
                ),
            )
        ),
        market_observation=market_observation,
        notes=(
            "Production universe candidate built for "
            "an arbitrary XEON position size."
        ),
    )


def build_amundi_universe_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    snapshot = (
        build_amundi_smart_overnight_snapshot(
            estr_rate_pct=ESTR_RATE_PCT,
            estr_reference_date=ESTR_REFERENCE_DATE,
        )
    )

    risk = build_unknown_risk_assessments(
        instrument_id=(
            AMUNDI_SMART_OVERNIGHT_INSTRUMENT.instrument_id
        ),
        market_id=(
            AMUNDI_SMART_OVERNIGHT_MARKET.market_id
        ),
        assessed_at=RISK_ASSESSED_AT,
    )

    size_id = _position_size_id(
        position_size_eur
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"amundi_smart_overnight_"
            f"{size_id}_universe"
        ),
        label="Amundi Smart Overnight",
        mandate=mandate,
        instrument=(
            AMUNDI_SMART_OVERNIGHT_INSTRUMENT
        ),
        market=AMUNDI_SMART_OVERNIGHT_MARKET,
        accessibility=(
            AMUNDI_SMART_OVERNIGHT_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
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
        return_component_builder=lambda _size: (
            build_conservative_return_components(
                instrument=(
                    AMUNDI_SMART_OVERNIGHT_INSTRUMENT
                ),
                market=AMUNDI_SMART_OVERNIGHT_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
            )
        ),
        notes=(
            "Production universe candidate built for "
            "an arbitrary Amundi position size."
        ),
    )


def build_ernx_universe_candidate(
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
            f"ernx_{size_id}_universe"
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
            "Production universe candidate built for "
            "an arbitrary ERNX position size."
        ),
    )


def build_btf_universe_candidate(
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
            f"btf_{size_id}_universe"
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
            "Production universe candidate built for "
            "an arbitrary French BTF position size."
        ),
    )


def build_bubill_universe_candidate(
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
            f"bubill_{size_id}_universe"
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
            "Production universe candidate built for "
            "an arbitrary German Bubill position size."
        ),
    )


def build_blackrock_universe_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
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
        assessed_at=RISK_ASSESSED_AT,
    )

    size_id = _position_size_id(
        position_size_eur
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"blackrock_ics_{size_id}_universe"
        ),
        label="BlackRock ICS Euro Liquidity",
        mandate=mandate,
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
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
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
        return_component_builder=lambda _size: (
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
        notes=(
            "Production universe candidate built for "
            "an arbitrary BlackRock MMF position size."
        ),
    )


def build_spiko_universe_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    snapshot = get_spiko_eu_tbills_snapshot()

    risk = build_unknown_risk_assessments(
        instrument_id=(
            SPIKO_EU_TBILLS_INSTRUMENT.instrument_id
        ),
        market_id=(
            SPIKO_EU_TBILLS_MARKET.market_id
        ),
        assessed_at=RISK_ASSESSED_AT,
    )

    size_id = _position_size_id(
        position_size_eur
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"spiko_{size_id}_universe"
        ),
        label="Spiko EU T-Bills",
        mandate=mandate,
        instrument=(
            SPIKO_EU_TBILLS_INSTRUMENT
        ),
        market=SPIKO_EU_TBILLS_MARKET,
        accessibility=(
            SPIKO_EU_TBILLS_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
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
        return_component_builder=lambda _size: (
            build_conservative_return_components(
                instrument=(
                    SPIKO_EU_TBILLS_INSTRUMENT
                ),
                market=SPIKO_EU_TBILLS_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
            )
        ),
        notes=(
            "Production universe candidate built for "
            "an arbitrary Spiko position size."
        ),
    )


def build_addiko_universe_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    snapshot = (
        get_addiko_91_180_day_snapshot()
    )

    risk = build_unknown_risk_assessments(
        instrument_id=(
            ADDIKO_91_180_DAY_INSTRUMENT.instrument_id
        ),
        market_id=(
            ADDIKO_91_180_DAY_MARKET.market_id
        ),
        assessed_at=RISK_ASSESSED_AT,
    )

    size_id = _position_size_id(
        position_size_eur
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"addiko_{size_id}_universe"
        ),
        label="Addiko 91-180d Deposit",
        mandate=mandate,
        instrument=(
            ADDIKO_91_180_DAY_INSTRUMENT
        ),
        market=ADDIKO_91_180_DAY_MARKET,
        accessibility=(
            ADDIKO_91_180_DAY_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=holding_period_days,
        position_builder=lambda size: (
            build_bank_deposit_position_analysis(
                snapshot=snapshot,
                rate=ADDIKO_91_180_DAY_RATE,
                position_size_eur=size,
            )
        ),
        risk_assessments=risk,
        return_component_builder=lambda _size: (
            build_conservative_return_components(
                instrument=(
                    ADDIKO_91_180_DAY_INSTRUMENT
                ),
                market=ADDIKO_91_180_DAY_MARKET,
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
            )
        ),
        notes=(
            "Production universe candidate built for "
            "an arbitrary Addiko deposit position size."
        ),
    )


def _build_aave_candidate_builder() -> CandidateBuilder:
    observation = fetch_aave_v3_base_eurc()

    snapshot = build_aave_eurc_snapshot(
        observation
    )

    risk = get_aave_eurc_risk_assessments()

    def build_candidate(
        position_size_eur: float,
        mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    ) -> PortfolioCandidateAssessment:
        size_id = _position_size_id(
            position_size_eur
        )

        return analyze_opportunity_position(
            assessment_id=(
                f"aave_{size_id}_universe"
            ),
            label="Aave V3 Base EURC",
            mandate=mandate,
            instrument=(
                AAVE_V3_BASE_EURC_INSTRUMENT
            ),
            market=AAVE_V3_BASE_EURC_MARKET,
            accessibility=(
                AAVE_V3_BASE_EURC_ACCESSIBILITY
            ),
            snapshot=snapshot,
            position_size_eur=position_size_eur,
            holding_period_days=(
                DEFAULT_HOLDING_PERIOD_DAYS
            ),
            position_builder=lambda size: (
                build_aave_position_analysis(
                    observation=observation,
                    position_size_eur=size,
                )
            ),
            risk_assessments=risk,
            return_component_builder=lambda _size: (
                build_conservative_return_components(
                    instrument=(
                        AAVE_V3_BASE_EURC_INSTRUMENT
                    ),
                    market=AAVE_V3_BASE_EURC_MARKET,
                    snapshot=snapshot,
                    reference_yield_includes_product_fee=True,
                )
            ),
            notes=(
                "Production universe candidate built for "
                "an arbitrary Aave EURC position size."
            ),
        )

    return build_candidate


def build_model_company_opportunity_universe(
) -> tuple[
    UniverseOpportunity,
    ...
]:
    aave_builder = (
        _build_aave_candidate_builder()
    )

    return (
        UniverseOpportunity(
            key="addiko",
            label="Addiko Deposit",
            candidate_builder=(
                build_addiko_universe_candidate
            ),
        ),
        UniverseOpportunity(
            key="xeon",
            label="XEON",
            candidate_builder=(
                build_xeon_universe_candidate
            ),
        ),
        UniverseOpportunity(
            key="amundi",
            label="Amundi Overnight",
            candidate_builder=(
                build_amundi_universe_candidate
            ),
        ),
        UniverseOpportunity(
            key="ernx",
            label="ERNX",
            candidate_builder=(
                build_ernx_universe_candidate
            ),
        ),
        UniverseOpportunity(
            key="btf",
            label="French BTF",
            candidate_builder=(
                build_btf_universe_candidate
            ),
        ),
        UniverseOpportunity(
            key="bubill",
            label="German Bubill",
            candidate_builder=(
                build_bubill_universe_candidate
            ),
        ),
        UniverseOpportunity(
            key="blackrock",
            label="BlackRock MMF",
            candidate_builder=(
                build_blackrock_universe_candidate
            ),
        ),
        UniverseOpportunity(
            key="spiko",
            label="Spiko",
            candidate_builder=(
                build_spiko_universe_candidate
            ),
        ),
        UniverseOpportunity(
            key="aave",
            label="Aave EURC",
            candidate_builder=aave_builder,
        ),
    )


def analyze_opportunity_universe_at_position_size(
    *,
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
) -> tuple[
    PortfolioCandidateAssessment,
    ...
]:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero."
        )

    opportunities = (
        build_model_company_opportunity_universe()
    )

    return tuple(
        opportunity.candidate_builder(
            position_size_eur,
            mandate,
        )
        for opportunity in opportunities
    )