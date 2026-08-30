from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.execution_evidence import (
    assess_xetra_position_execution_evidence,
)

from treasury_intelligence.sources.xetra import (
    XEON_XETRA_2024_TURNOVER,
    XEON_XETRA_XLM_100K,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_INSTRUMENT,
    XEON_MARKET,
    get_xeon_market_observation,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
    1_000_000,
)


def print_assessment(
    position_size_eur: float,
) -> None:
    market_observation = (
        get_xeon_market_observation()
    )

    assessment = (
        assess_xetra_position_execution_evidence(
            assessment_id=(
                "xeon_xetra_execution_"
                f"{int(position_size_eur)}"
            ),
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=(
                XEON_MARKET.market_id
            ),
            position_size_eur=(
                position_size_eur
            ),
            xlm_evidence=(
                XEON_XETRA_XLM_100K
            ),
            annual_turnover_evidence=(
                XEON_XETRA_2024_TURNOVER
            ),
            current_daily_turnover_eur=(
                market_observation.daily_turnover_eur
            ),
            notes=(
                "Position-aware XEON execution "
                "evidence assessment."
            ),
        )
    )

    print(
        f"EUR {position_size_eur:,.0f} POSITION"
    )

    print()

    print(
        f"Evidence status:               "
        f"{assessment.execution_evidence_status}"
    )

    print(
        f"Market activity supported:     "
        f"{assessment.market_activity_supported}"
    )

    print(
        f"Reference order size:          "
        f"EUR "
        f"{assessment.reference_order_size_eur:,.0f}"
    )

    print(
        f"Position / reference size:     "
        f"{assessment.position_to_reference_size_multiple:.1f}x"
    )

    print(
        f"Position-sized cost supported: "
        f"{assessment.position_sized_cost_supported}"
    )

    if (
        assessment.observed_roundtrip_cost_bps
        is None
    ):
        roundtrip_text = "UNKNOWN"
    else:
        roundtrip_text = (
            f"{assessment.observed_roundtrip_cost_bps:.1f} bps"
        )

    print(
        f"Roundtrip implicit cost:       "
        f"{roundtrip_text}"
    )

    if (
        assessment.observed_buy_cost_bps
        is None
    ):
        buy_text = "UNKNOWN"
    else:
        buy_text = (
            f"{assessment.observed_buy_cost_bps:.1f} bps"
        )

    print(
        f"Buy implicit cost:             "
        f"{buy_text}"
    )

    if (
        assessment.observed_sell_cost_bps
        is None
    ):
        sell_text = "UNKNOWN"
    else:
        sell_text = (
            f"{assessment.observed_sell_cost_bps:.1f} bps"
        )

    print(
        f"Sell implicit cost:            "
        f"{sell_text}"
    )

    print(
        f"Immediate exit supported:      "
        f"{assessment.immediate_exit_supported}"
    )

    if assessment.evidence_requirements:
        print()
        print(
            "EVIDENCE REQUIREMENTS"
        )

        print()

        for requirement in (
            assessment.evidence_requirements
        ):
            print(
                f"  - {requirement}"
            )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print(
        "XEON POSITION-AWARE EXECUTION EVIDENCE"
    )

    print()

    print(
        "Published Xetra liquidity evidence is "
        "applied only to the position size for "
        "which it was actually measured."
    )

    print()

    print(
        "Evidence from a EUR 100,000 XLM "
        "measurement is not extrapolated to larger "
        "treasury allocations."
    )

    print()

    print("-" * 100)
    print()

    for position_size_eur in POSITION_SIZES_EUR:
        print_assessment(
            position_size_eur=(
                position_size_eur
            ),
        )

    print("COMPARISON")
    print()

    print(
        "EUR 100,000"
    )

    print(
        "  Market activity:             SUPPORTED"
    )

    print(
        "  Position-sized cost:         SUPPORTED"
    )

    print(
        "  Roundtrip XLM:               2.4 bps"
    )

    print(
        "  Immediate exit:              UNKNOWN"
    )

    print()

    print(
        "EUR 500,000"
    )

    print(
        "  Market activity:             SUPPORTED"
    )

    print(
        "  Position-sized cost:         INSUFFICIENT"
    )

    print(
        "  Roundtrip XLM:               UNKNOWN"
    )

    print(
        "  Immediate exit:              UNKNOWN"
    )

    print()

    print(
        "EUR 1,000,000"
    )

    print(
        "  Market activity:             SUPPORTED"
    )

    print(
        "  Position-sized cost:         INSUFFICIENT"
    )

    print(
        "  Roundtrip XLM:               UNKNOWN"
    )

    print(
        "  Immediate exit:              UNKNOWN"
    )

    print()

    print("INTERPRETATION")
    print()

    print(
        "XEON is no longer one undifferentiated "
        "liquidity case."
    )

    print()

    print(
        "At EUR 100,000, direct public Xetra "
        "evidence supports a position-sized "
        "implicit transaction-cost observation."
    )

    print()

    print(
        "At EUR 500,000 and EUR 1,000,000, "
        "surrounding market activity remains strong "
        "but execution-cost evidence remains "
        "insufficient because the published XLM "
        "measurement is smaller than the proposed "
        "treasury position."
    )

    print()

    print(
        "Immediate exit remains UNKNOWN at every "
        "position size because XLM execution-cost "
        "evidence is not the same thing as a live "
        "order-book depth guarantee."
    )


if __name__ == "__main__":
    main()