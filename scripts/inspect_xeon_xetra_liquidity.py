from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.sources.xetra import (
    XEON_XETRA_2024_TURNOVER,
    XEON_XETRA_XLM_100K,
)

from treasury_intelligence.sources.xtrackers import (
    get_xeon_market_observation,
)


POSITION_SIZES_EUR = (
    100_000,
    500_000,
    1_000_000,
)


def calculate_cost_eur(
    position_size_eur: float,
    cost_bps: float,
) -> float:
    return (
        position_size_eur
        * cost_bps
        / 10_000
    )


def main() -> None:
    xlm = XEON_XETRA_XLM_100K

    annual_turnover = (
        XEON_XETRA_2024_TURNOVER
    )

    market_observation = (
        get_xeon_market_observation()
    )

    print(
        "XEON XETRA LIQUIDITY EVIDENCE"
    )

    print()

    print(
        "This inspection separates observed "
        "liquidity evidence at a defined order "
        "size from unsupported extrapolation to "
        "larger treasury positions."
    )

    print()

    print("-" * 100)
    print()

    print("XETRA LIQUIDITY MEASURE")
    print()

    print(
        f"Instrument:                    "
        f"{xlm.instrument_name}"
    )

    print(
        f"ISIN:                          "
        f"{xlm.isin}"
    )

    print(
        f"Measured order size:           "
        f"EUR {xlm.measured_order_size_eur:,.0f}"
    )

    print(
        f"Buy implicit cost:             "
        f"{xlm.buy_cost_bps:.1f} bps"
    )

    print(
        f"Sell implicit cost:            "
        f"{xlm.sell_cost_bps:.1f} bps"
    )

    print(
        f"Roundtrip implicit cost:       "
        f"{xlm.roundtrip_cost_bps:.1f} bps"
    )

    buy_cost_eur = (
        calculate_cost_eur(
            position_size_eur=(
                xlm.measured_order_size_eur
            ),
            cost_bps=(
                xlm.buy_cost_bps
            ),
        )
    )

    sell_cost_eur = (
        calculate_cost_eur(
            position_size_eur=(
                xlm.measured_order_size_eur
            ),
            cost_bps=(
                xlm.sell_cost_bps
            ),
        )
    )

    roundtrip_cost_eur = (
        calculate_cost_eur(
            position_size_eur=(
                xlm.measured_order_size_eur
            ),
            cost_bps=(
                xlm.roundtrip_cost_bps
            ),
        )
    )

    print(
        f"Buy implicit cost:             "
        f"EUR {buy_cost_eur:,.2f}"
    )

    print(
        f"Sell implicit cost:            "
        f"EUR {sell_cost_eur:,.2f}"
    )

    print(
        f"Roundtrip implicit cost:       "
        f"EUR {roundtrip_cost_eur:,.2f}"
    )

    print(
        f"Evidence checked on:           "
        f"{xlm.evidence_checked_on}"
    )

    print()

    print(
        "XLM measures implicit transaction "
        "cost including market impact for the "
        "specified order size."
    )

    print()

    print("-" * 100)
    print()

    print("HISTORICAL XETRA MARKET ACTIVITY")
    print()

    print(
        f"Calendar year:                 "
        f"{annual_turnover.calendar_year}"
    )

    print(
        f"Annual turnover:               "
        f"EUR "
        f"{annual_turnover.annual_turnover_eur:,.0f}"
    )

    print(
        f"Xetra ETF turnover rank:       "
        f"#{annual_turnover.xetra_turnover_rank}"
    )

    print()

    print(
        "Historical turnover supports a strong "
        "market-activity conclusion but is not "
        "a current executable-order quote."
    )

    print()

    print("-" * 100)
    print()

    print("CURRENT PUBLIC MARKET OBSERVATION")
    print()

    print(
        f"Observed daily turnover:       "
        f"EUR "
        f"{market_observation.daily_turnover_eur:,.0f}"
    )

    print()

    print("-" * 100)
    print()

    print("POSITION-SIZE ANALYSIS")
    print()

    for position_size_eur in POSITION_SIZES_EUR:
        multiple_of_measured_size = (
            position_size_eur
            / xlm.measured_order_size_eur
        )

        daily_turnover_pct = (
            position_size_eur
            / market_observation.daily_turnover_eur
            * 100
        )

        print(
            f"EUR {position_size_eur:>10,.0f}"
        )

        print(
            f"  Multiple of XLM size:        "
            f"{multiple_of_measured_size:.1f}x"
        )

        print(
            f"  % of observed daily turnover:"
            f" {daily_turnover_pct:.2f}%"
        )

        if (
            position_size_eur
            == xlm.measured_order_size_eur
        ):
            print(
                f"  Position-sized XLM:          "
                f"{xlm.roundtrip_cost_bps:.1f} bps"
            )

            print(
                "  Execution-cost evidence:     "
                "SUPPORTED"
            )

        else:
            print(
                "  Position-sized XLM:          "
                "UNKNOWN"
            )

            print(
                "  Execution-cost evidence:     "
                "INSUFFICIENT"
            )

        print()

    print("-" * 100)
    print()

    print("EUR 500,000 TREASURY CASE")
    print()

    position_size_eur = 500_000

    xlm_size_multiple = (
        position_size_eur
        / xlm.measured_order_size_eur
    )

    turnover_share_pct = (
        position_size_eur
        / market_observation.daily_turnover_eur
        * 100
    )

    print(
        f"Position size:                 "
        f"EUR {position_size_eur:,.0f}"
    )

    print(
        f"XLM measured size:             "
        f"EUR {xlm.measured_order_size_eur:,.0f}"
    )

    print(
        f"Position / XLM size:           "
        f"{xlm_size_multiple:.1f}x"
    )

    print(
        f"Observed daily turnover:       "
        f"EUR "
        f"{market_observation.daily_turnover_eur:,.0f}"
    )

    print(
        f"Position / daily turnover:     "
        f"{turnover_share_pct:.2f}%"
    )

    print(
        "Strong market activity:        True"
    )

    print(
        "EUR 100k implicit cost known:   True"
    )

    print(
        "EUR 500k implicit cost known:   False"
    )

    print(
        "EUR 500k order-book depth:      UNKNOWN"
    )

    print(
        "Immediate EUR 500k exit:        UNKNOWN"
    )

    print()

    print("-" * 100)
    print()

    print("INTERPRETATION")
    print()

    print(
        "XEON has substantially stronger "
        "liquidity evidence than daily turnover "
        "alone suggested."
    )

    print()

    print(
        "For a EUR 100,000 position, Xetra "
        "publishes position-sized implicit "
        "transaction-cost evidence."
    )

    print()

    print(
        "The published 2.4-basis-point roundtrip "
        "XLM must not be multiplied, copied, or "
        "otherwise extrapolated to EUR 500,000 "
        "or EUR 1,000,000."
    )

    print()

    print(
        "For the model EUR 500,000 treasury "
        "position, market-activity evidence is "
        "strong but executable spread, market "
        "impact, order-book depth, and immediate "
        "exit capacity remain unresolved."
    )

    print()

    print(
        "ENTRY CAPACITY and EXIT LIQUIDITY remain "
        "separate questions."
    )


if __name__ == "__main__":
    main()