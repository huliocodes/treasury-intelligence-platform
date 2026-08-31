from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_DIR),
    )


from treasury_intelligence.analytics.bond_returns import (
    build_ibkr_europe_otc_bond_return_components,
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


POSITION_SIZES_EUR = (
    100_000.0,
    500_000.0,
    1_000_000.0,
    2_000_000.0,
    5_000_000.0,
)

HOLDING_PERIOD_DAYS = 365

ESTR_RATE_PCT = 2.188
ESTR_REFERENCE_DATE = "2026-08-27"

RISK_ASSESSED_AT = "2026-08-31"


@dataclass(frozen=True)
class UniverseOpportunity:
    key: str
    label: str
    candidate_builder: Callable[
        [float],
        PortfolioCandidateAssessment,
    ]


def build_xeon_candidate(
    position_size_eur: float,
) -> PortfolioCandidateAssessment:
    snapshot = build_xeon_snapshot(
        estr_rate_pct=ESTR_RATE_PCT,
        estr_reference_date=ESTR_REFERENCE_DATE,
    )

    market_observation = (
        get_xeon_market_observation()
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"xeon_{int(position_size_eur)}_matrix"
        ),
        label="XEON",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=XEON_INSTRUMENT,
        market=XEON_MARKET,
        accessibility=XEON_ACCESSIBILITY,
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=HOLDING_PERIOD_DAYS,
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
    )


def build_amundi_candidate(
    position_size_eur: float,
) -> PortfolioCandidateAssessment:
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
        assessed_at=RISK_ASSESSED_AT,
    )

    return analyze_opportunity_position(
        assessment_id=(
            "amundi_smart_overnight_"
            f"{int(position_size_eur)}_matrix"
        ),
        label="Amundi Smart Overnight",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=(
            AMUNDI_SMART_OVERNIGHT_INSTRUMENT
        ),
        market=AMUNDI_SMART_OVERNIGHT_MARKET,
        accessibility=(
            AMUNDI_SMART_OVERNIGHT_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=position_size_eur,
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
    )


def build_ernx_candidate(
    position_size_eur: float,
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

    return analyze_opportunity_position(
        assessment_id=(
            f"ernx_{int(position_size_eur)}_matrix"
        ),
        label="ERNX",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=ERNX_INSTRUMENT,
        market=ERNX_MARKET,
        accessibility=ERNX_ACCESSIBILITY,
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=HOLDING_PERIOD_DAYS,
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
    )


def build_btf_candidate(
    position_size_eur: float,
) -> PortfolioCandidateAssessment:
    snapshot = get_btf_2027_03_10_snapshot()

    market_observation = (
        get_btf_2027_03_10_market_observation()
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"btf_{int(position_size_eur)}_matrix"
        ),
        label="French BTF",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=BTF_2027_03_10,
        market=BTF_2027_03_10_MARKET,
        accessibility=(
            BTF_2027_03_10_ACCESSIBILITY
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
    )


def build_bubill_candidate(
    position_size_eur: float,
) -> PortfolioCandidateAssessment:
    snapshot = (
        get_bubill_2027_07_14_snapshot()
    )

    market_observation = (
        get_bubill_2027_07_14_market_observation()
    )

    risk = build_unknown_risk_assessments(
        instrument_id=(
            BUBILL_2027_07_14.instrument_id
        ),
        market_id=(
            BUBILL_2027_07_14_MARKET.market_id
        ),
        assessed_at=RISK_ASSESSED_AT,
    )

    return analyze_opportunity_position(
        assessment_id=(
            f"bubill_{int(position_size_eur)}_matrix"
        ),
        label="German Bubill",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=BUBILL_2027_07_14,
        market=BUBILL_2027_07_14_MARKET,
        accessibility=(
            BUBILL_2027_07_14_ACCESSIBILITY
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
        risk_assessments=risk,
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
    )


def build_blackrock_candidate(
    position_size_eur: float,
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

    return analyze_opportunity_position(
        assessment_id=(
            "blackrock_ics_"
            f"{int(position_size_eur)}_matrix"
        ),
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
        position_size_eur=position_size_eur,
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
    )


def build_spiko_candidate(
    position_size_eur: float,
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

    return analyze_opportunity_position(
        assessment_id=(
            f"spiko_{int(position_size_eur)}_matrix"
        ),
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
        position_size_eur=position_size_eur,
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
    )


def build_addiko_candidate(
    position_size_eur: float,
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

    return analyze_opportunity_position(
        assessment_id=(
            f"addiko_{int(position_size_eur)}_matrix"
        ),
        label="Addiko 91-180d Deposit",
        mandate=MODEL_COMPANY_MANDATE,
        instrument=(
            ADDIKO_91_180_DAY_INSTRUMENT
        ),
        market=ADDIKO_91_180_DAY_MARKET,
        accessibility=(
            ADDIKO_91_180_DAY_ACCESSIBILITY
        ),
        snapshot=snapshot,
        position_size_eur=position_size_eur,
        holding_period_days=HOLDING_PERIOD_DAYS,
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
    )


def build_aave_candidate_factory():
    observation = fetch_aave_v3_base_eurc()

    snapshot = build_aave_eurc_snapshot(
        observation
    )

    risk = get_aave_eurc_risk_assessments()

    def build_candidate(
        position_size_eur: float,
    ) -> PortfolioCandidateAssessment:
        return analyze_opportunity_position(
            assessment_id=(
                f"aave_{int(position_size_eur)}_matrix"
            ),
            label="Aave V3 Base EURC",
            mandate=MODEL_COMPANY_MANDATE,
            instrument=(
                AAVE_V3_BASE_EURC_INSTRUMENT
            ),
            market=AAVE_V3_BASE_EURC_MARKET,
            accessibility=(
                AAVE_V3_BASE_EURC_ACCESSIBILITY
            ),
            snapshot=snapshot,
            position_size_eur=position_size_eur,
            holding_period_days=HOLDING_PERIOD_DAYS,
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
        )

    return build_candidate, observation


def build_opportunity_universe():
    aave_builder, aave_observation = (
        build_aave_candidate_factory()
    )

    opportunities = (
        UniverseOpportunity(
            key="addiko",
            label="Addiko Deposit",
            candidate_builder=build_addiko_candidate,
        ),
        UniverseOpportunity(
            key="xeon",
            label="XEON",
            candidate_builder=build_xeon_candidate,
        ),
        UniverseOpportunity(
            key="amundi",
            label="Amundi Overnight",
            candidate_builder=build_amundi_candidate,
        ),
        UniverseOpportunity(
            key="ernx",
            label="ERNX",
            candidate_builder=build_ernx_candidate,
        ),
        UniverseOpportunity(
            key="btf",
            label="French BTF",
            candidate_builder=build_btf_candidate,
        ),
        UniverseOpportunity(
            key="bubill",
            label="German Bubill",
            candidate_builder=build_bubill_candidate,
        ),
        UniverseOpportunity(
            key="blackrock",
            label="BlackRock MMF",
            candidate_builder=build_blackrock_candidate,
        ),
        UniverseOpportunity(
            key="spiko",
            label="Spiko",
            candidate_builder=build_spiko_candidate,
        ),
        UniverseOpportunity(
            key="aave",
            label="Aave EURC",
            candidate_builder=aave_builder,
        ),
    )

    return opportunities, aave_observation


def short_status(
    candidate: PortfolioCandidateAssessment,
) -> str:
    if candidate.recommendation_ready:
        return "READY"

    if candidate.candidate_status == "blocked":
        return "BLOCK"

    if candidate.candidate_status == "needs_evidence":
        return "EVID"

    return candidate.candidate_status.upper()


def format_return(
    candidate: PortfolioCandidateAssessment,
) -> str:
    if candidate.defensible_return_pct is None:
        return "-"

    return (
        f"{candidate.defensible_return_pct:.3f}%"
    )


def print_matrix(
    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ],
    opportunities: tuple[
        UniverseOpportunity,
        ...
    ],
) -> None:
    print()
    print("V1 UNIVERSE POSITION MATRIX")
    print("=" * 118)

    header = (
        f"{'Opportunity':<20}"
        f"{'EUR 100k':>18}"
        f"{'EUR 500k':>18}"
        f"{'EUR 1m':>18}"
        f"{'EUR 2m':>18}"
        f"{'EUR 5m':>18}"
    )

    print(header)
    print("-" * 118)

    for opportunity in opportunities:
        candidates = (
            candidates_by_opportunity[
                opportunity.key
            ]
        )

        cells = []

        for candidate in candidates:
            cells.append(
                f"{short_status(candidate)} "
                f"{format_return(candidate)}"
            )

        print(
            f"{opportunity.label:<20}"
            f"{cells[0]:>18}"
            f"{cells[1]:>18}"
            f"{cells[2]:>18}"
            f"{cells[3]:>18}"
            f"{cells[4]:>18}"
        )

    print("=" * 118)


def print_detail(
    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ],
    opportunities: tuple[
        UniverseOpportunity,
        ...
    ],
) -> None:
    print()
    print("POSITION-SIZE DETAIL")
    print("=" * 118)

    for opportunity in opportunities:
        print()
        print(opportunity.label)
        print("-" * 118)

        for candidate in (
            candidates_by_opportunity[
                opportunity.key
            ]
        ):
            print(
                f"EUR {candidate.position_size_eur:>11,.0f}"
                f" | eligibility: "
                f"{candidate.eligibility_status:<14}"
                f" | liquidity: "
                f"{candidate.liquidity_position_status:<13}"
                f" | economics: "
                f"{candidate.economics_status:<10}"
                f" | return: "
                f"{format_return(candidate):>7}"
                f" | status: "
                f"{candidate.candidate_status:<20}"
                f" | ready: "
                f"{candidate.recommendation_ready}"
            )


def print_evidence_summary(
    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ],
    opportunities: tuple[
        UniverseOpportunity,
        ...
    ],
) -> None:
    print()
    print("EVIDENCE / BLOCKER SUMMARY AT EUR 5M")
    print("=" * 118)

    for opportunity in opportunities:
        candidate = (
            candidates_by_opportunity[
                opportunity.key
            ][-1]
        )

        print()
        print(
            f"{opportunity.label} "
            f"- EUR {candidate.position_size_eur:,.0f}"
        )

        print(
            f"Candidate status: "
            f"{candidate.candidate_status}"
        )

        print(
            f"Unknown base risk dimensions: "
            f"{candidate.base_risk_unknown_dimension_count}"
        )

        print(
            f"Evidence requirements: "
            f"{len(candidate.evidence_requirements)}"
        )

        for requirement in (
            candidate.evidence_requirements
        ):
            print(
                f"  EVIDENCE: {requirement}"
            )

        print(
            f"Blocking reasons: "
            f"{len(candidate.blocking_reasons)}"
        )

        for reason in candidate.blocking_reasons:
            print(
                f"  BLOCKER: {reason}"
            )


def print_summary(
    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ],
    opportunities: tuple[
        UniverseOpportunity,
        ...
    ],
    aave_observation,
) -> None:
    all_candidates = [
        candidate
        for opportunity in opportunities
        for candidate in (
            candidates_by_opportunity[
                opportunity.key
            ]
        )
    ]

    print()
    print("MATRIX SUMMARY")
    print("=" * 118)

    print(
        "Opportunities:",
        len(opportunities),
    )

    print(
        "Position sizes:",
        len(POSITION_SIZES_EUR),
    )

    print(
        "Total candidate assessments:",
        len(all_candidates),
    )

    print(
        "Recommendation-ready:",
        sum(
            candidate.recommendation_ready
            for candidate in all_candidates
        ),
    )

    print(
        "Needs evidence:",
        sum(
            candidate.candidate_status
            == "needs_evidence"
            for candidate in all_candidates
        ),
    )

    print(
        "Blocked:",
        sum(
            candidate.candidate_status
            == "blocked"
            for candidate in all_candidates
        ),
    )

    print()
    print("Live Aave observation used once:")

    print(
        f"  observed_at: "
        f"{aave_observation.observed_at.isoformat()}"
    )

    print(
        f"  supply_apy_pct: "
        f"{aave_observation.supply_apy_pct:.3f}%"
    )

    print(
        f"  available_liquidity: "
        f"EURC "
        f"{aave_observation.available_liquidity:,.2f}"
    )

    print()
    print(
        "This matrix is diagnostic. It does not allocate "
        "the EUR 5M treasury and it does not override "
        "eligibility, evidence, or accessibility blockers."
    )


def main() -> None:
    opportunities, aave_observation = (
        build_opportunity_universe()
    )

    candidates_by_opportunity: dict[
        str,
        list[PortfolioCandidateAssessment],
    ] = {}

    for opportunity in opportunities:
        candidates = []

        for position_size_eur in (
            POSITION_SIZES_EUR
        ):
            candidate = (
                opportunity.candidate_builder(
                    position_size_eur
                )
            )

            candidates.append(candidate)

        candidates_by_opportunity[
            opportunity.key
        ] = candidates

    print_matrix(
        candidates_by_opportunity=(
            candidates_by_opportunity
        ),
        opportunities=opportunities,
    )

    print_detail(
        candidates_by_opportunity=(
            candidates_by_opportunity
        ),
        opportunities=opportunities,
    )

    print_evidence_summary(
        candidates_by_opportunity=(
            candidates_by_opportunity
        ),
        opportunities=opportunities,
    )

    print_summary(
        candidates_by_opportunity=(
            candidates_by_opportunity
        ),
        opportunities=opportunities,
        aave_observation=aave_observation,
    )


if __name__ == "__main__":
    main()
