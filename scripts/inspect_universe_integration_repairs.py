from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.generic_risk import (
    build_unknown_risk_assessments,
)

from treasury_intelligence.analytics.liquidity import (
    assess_liquidity_evidence,
)

from treasury_intelligence.analytics.positions import (
    build_money_market_fund_position_analysis,
)

from treasury_intelligence.models.risk import (
    RISK_DIMENSIONS,
)

from treasury_intelligence.sources.amundi import (
    AMUNDI_SMART_OVERNIGHT_INSTRUMENT,
    AMUNDI_SMART_OVERNIGHT_MARKET,
)

from treasury_intelligence.sources.blackrock import (
    BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MINIMUM_EUR,
    get_blackrock_ics_euro_liquidity_core_t0_snapshot,
)

from treasury_intelligence.sources.germany import (
    BUBILL_2027_07_14,
    BUBILL_2027_07_14_MARKET,
)

from treasury_intelligence.sources.spiko import (
    SPIKO_EU_TBILLS_MINIMUM_EUR,
    get_spiko_eu_tbills_snapshot,
)


def inspect_risk_baseline(
    label: str,
    instrument_id: str,
    market_id: str,
) -> None:
    assessments = build_unknown_risk_assessments(
        instrument_id=instrument_id,
        market_id=market_id,
        assessed_at="2026-08-31",
    )

    print(label)
    print("-" * 60)
    print(
        "Assessment count:",
        len(assessments),
    )

    print(
        "Dimensions:",
        ", ".join(
            assessment.risk_dimension
            for assessment in assessments
        ),
    )

    print(
        "All unknown:",
        all(
            assessment.risk_level == "unknown"
            for assessment in assessments
        ),
    )

    print(
        "All evidence insufficient:",
        all(
            not assessment.evidence_sufficient
            for assessment in assessments
        ),
    )

    print(
        "Matches risk dimensions:",
        tuple(
            assessment.risk_dimension
            for assessment in assessments
        )
        == RISK_DIMENSIONS,
    )

    print()


def inspect_mmf_liquidity(
    label: str,
    snapshot,
    minimum_initial_investment_eur: float,
) -> None:
    position = (
        build_money_market_fund_position_analysis(
            snapshot=snapshot,
            position_size_eur=1_000_000.0,
            minimum_initial_investment_eur=(
                minimum_initial_investment_eur
            ),
        )
    )

    liquidity = assess_liquidity_evidence(
        market_observation=None,
        position=position,
    )

    print(label)
    print("-" * 60)

    print(
        "Position evidence:",
        position.liquidity_evidence_level,
    )

    print(
        "Liquidity evidence:",
        liquidity.evidence_level,
    )

    print(
        "Evidence rank:",
        liquidity.evidence_rank,
    )

    print(
        "Market activity observed:",
        liquidity.market_activity_observed,
    )

    print(
        "Displayed quote observed:",
        liquidity.displayed_quote_observed,
    )

    print(
        "Position depth observed:",
        liquidity.position_depth_observed,
    )

    print(
        "Immediate liquidity supported:",
        liquidity.immediate_liquidity_supported,
    )

    print(
        "Sufficient for immediate liquidity:",
        liquidity.sufficient_for_immediate_liquidity,
    )

    print()


def main() -> None:
    inspect_risk_baseline(
        label="AMUNDI GENERIC RISK BASELINE",
        instrument_id=(
            AMUNDI_SMART_OVERNIGHT_INSTRUMENT.instrument_id
        ),
        market_id=(
            AMUNDI_SMART_OVERNIGHT_MARKET.market_id
        ),
    )

    inspect_risk_baseline(
        label="BUBILL GENERIC RISK BASELINE",
        instrument_id=BUBILL_2027_07_14.instrument_id,
        market_id=BUBILL_2027_07_14_MARKET.market_id,
    )

    blackrock = (
        get_blackrock_ics_euro_liquidity_core_t0_snapshot()
    )

    spiko = get_spiko_eu_tbills_snapshot()

    inspect_mmf_liquidity(
        label="BLACKROCK MMF LIQUIDITY",
        snapshot=blackrock,
        minimum_initial_investment_eur=(
            BLACKROCK_ICS_EURO_LIQUIDITY_CORE_T0_MINIMUM_EUR
        ),
    )

    inspect_mmf_liquidity(
        label="SPIKO MMF LIQUIDITY",
        snapshot=spiko,
        minimum_initial_investment_eur=(
            SPIKO_EU_TBILLS_MINIMUM_EUR
        ),
    )


if __name__ == "__main__":
    main()