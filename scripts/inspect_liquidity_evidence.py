from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.liquidity import (
    assess_liquidity_evidence,
)

from treasury_intelligence.analytics.positions import (
    build_aave_position_analysis,
    build_ernx_position_analysis,
    build_xeon_position_analysis,
)

from treasury_intelligence.sources.aave import (
    fetch_aave_v3_base_eurc,
)

from treasury_intelligence.sources.ecb import (
    fetch_recent_estr,
)

from treasury_intelligence.sources.ishares import (
    get_ernx_market_observation,
    get_ernx_snapshot,
)

from treasury_intelligence.sources.xtrackers import (
    build_xeon_snapshot,
    get_xeon_market_observation,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
    1_000_000,
    5_000_000,
)


def print_assessment(
    label: str,
    assessment,
) -> None:
    immediate_liquidity = (
        "unknown"
        if (
            assessment.immediate_liquidity_supported
            is None
        )
        else (
            "yes"
            if assessment.immediate_liquidity_supported
            else "no"
        )
    )

    sufficient = (
        "yes"
        if (
            assessment.sufficient_for_immediate_liquidity
        )
        else "no"
    )

    print(
        f"EUR {assessment.position_size_eur:>10,.0f} | "
        f"level: {assessment.evidence_level:<26} | "
        f"immediate exit: {immediate_liquidity:<7} | "
        f"sufficient: {sufficient}"
    )


def main() -> None:
    aave_observation = fetch_aave_v3_base_eurc()

    estr = fetch_recent_estr(limit=1)[-1]

    xeon_snapshot = build_xeon_snapshot(
        estr_rate_pct=estr.rate_pct,
        estr_reference_date=estr.reference_date,
    )

    xeon_market_observation = (
        get_xeon_market_observation()
    )

    ernx_snapshot = get_ernx_snapshot()

    ernx_market_observation = (
        get_ernx_market_observation()
    )

    print("LIQUIDITY EVIDENCE QUALITY")
    print()

    print("EVIDENCE LADDER")
    print()
    print("0  none")
    print("1  market_activity")
    print("2  displayed_quote")
    print("3  displayed_quote_with_size")
    print("4  executable_quote")
    print("5  position_depth")
    print()

    print("AAVE V3 BASE EURC")
    print()

    for position_size in POSITION_SIZES_EUR:
        position = build_aave_position_analysis(
            observation=aave_observation,
            position_size_eur=position_size,
        )

        assessment = assess_liquidity_evidence(
            market_observation=None,
            position=position,
        )

        print_assessment(
            "AAVE V3 BASE EURC",
            assessment,
        )

    print()
    print("XEON XETRA")
    print()

    for position_size in POSITION_SIZES_EUR:
        position = build_xeon_position_analysis(
            snapshot=xeon_snapshot,
            position_size_eur=position_size,
            market_observation=(
                xeon_market_observation
            ),
        )

        assessment = assess_liquidity_evidence(
            market_observation=(
                xeon_market_observation
            ),
            position=position,
        )

        print_assessment(
            "XEON",
            assessment,
        )

    print()
    print("ERNX XETRA")
    print()

    for position_size in POSITION_SIZES_EUR:
        position = build_ernx_position_analysis(
            snapshot=ernx_snapshot,
            position_size_eur=position_size,
            market_observation=(
                ernx_market_observation
            ),
        )

        assessment = assess_liquidity_evidence(
            market_observation=(
                ernx_market_observation
            ),
            position=position,
        )

        print_assessment(
            "ERNX",
            assessment,
        )

    print()
    print("INTERPRETATION")
    print()

    print(
        "Market activity improves the evidence base but does not "
        "prove immediate position-size liquidity."
    )

    print(
        "Displayed quotes and displayed size are progressively "
        "stronger observations but still do not automatically "
        "establish full executable depth."
    )

    print(
        "Only position-size-specific depth evidence can directly "
        "support a yes/no immediate-liquidity conclusion."
    )


if __name__ == "__main__":
    main()