from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.frictions import (
    build_xeon_return_components,
    get_xeon_friction_observations,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
    unknown_cost_component_names,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
)


POSITION_SIZE_EUR = 500_000

REFERENCE_YIELD_PCT = 2.273


def build_analysis(
    holding_period_days: int,
):
    return build_return_analysis(
        analysis_id=(
            f"xeon_500k_{holding_period_days}d_"
            "friction_analysis"
        ),
        instrument_id=(
            XEON_INSTRUMENT.instrument_id
        ),
        market_id=(
            XEON_MARKET.market_id
        ),
        access_route_id=(
            XEON_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=POSITION_SIZE_EUR,
        holding_period_days=holding_period_days,
        components=(
            build_xeon_return_components(
                position_size_eur=(
                    POSITION_SIZE_EUR
                ),
                reference_yield_pct=(
                    REFERENCE_YIELD_PCT
                ),
            )
        ),
        notes=(
            "Scenario analysis using published route "
            "commission evidence. This is not an "
            "account-specific executable quote."
        ),
    )


def print_observations() -> None:
    observations = (
        get_xeon_friction_observations(
            position_size_eur=(
                POSITION_SIZE_EUR
            )
        )
    )

    print("XEON FRICTION EVIDENCE")
    print()

    for observation in observations:
        if observation.value is None:
            value_text = "UNKNOWN"
        elif (
            observation.basis
            == "annualized_pct"
        ):
            value_text = (
                f"{observation.value:.3f}% p.a."
            )
        elif (
            observation.basis
            == "position_bps"
        ):
            value_text = (
                f"{observation.value:.2f} bps"
            )
        elif (
            observation.basis
            == "fixed_eur"
        ):
            value_text = (
                f"EUR {observation.value:,.2f}"
            )
        else:
            value_text = str(
                observation.value
            )

        print(
            f"{observation.friction_type:<20} | "
            f"{observation.evidence_level:<12} | "
            f"{value_text:<15} | "
            f"{observation.label}"
        )

    print()
    print("-" * 100)
    print()


def print_analysis(
    holding_period_days: int,
) -> None:
    analysis = build_analysis(
        holding_period_days
    )

    print(
        f"XEON EUR {POSITION_SIZE_EUR:,.0f} "
        f"- {holding_period_days}-DAY "
        "HOLDING SCENARIO"
    )
    print()

    print(
        f"Reference yield:                  "
        f"{analysis.reference_yield_pct:.3f}%"
    )

    print(
        f"Known recurring annualized cost: "
        f"{analysis.known_recurring_annualized_cost_pct:.3f}%"
    )

    print(
        f"Known one-time cost:             "
        f"EUR {analysis.known_one_time_cost_eur:,.2f}"
    )

    print(
        f"Known one-time cost:             "
        f"{analysis.known_one_time_cost_bps:.2f} bps"
    )

    print(
        f"Annualized one-time cost:        "
        f"{analysis.known_one_time_cost_annualized_pct:.3f}%"
    )

    print(
        f"Known total annualized cost:     "
        f"{analysis.known_total_annualized_cost_pct:.3f}%"
    )

    print(
        f"Return after known costs:        "
        f"{analysis.return_after_known_costs_pct:.3f}%"
    )

    if (
        analysis.realistic_expected_return_pct
        is None
    ):
        print(
            "Realistic expected return:       UNKNOWN"
        )
    else:
        print(
            f"Realistic expected return:       "
            f"{analysis.realistic_expected_return_pct:.3f}%"
        )

    print(
        f"Economics complete:              "
        f"{analysis.economics_complete}"
    )

    print()

    missing = (
        unknown_cost_component_names(
            analysis
        )
    )

    print("Remaining unknown economics:")

    for name in missing:
        print(
            f"  - {name}"
        )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print_observations()

    print_analysis(
        holding_period_days=30
    )

    print_analysis(
        holding_period_days=365
    )

    print("INTERPRETATION")
    print()

    print(
        "The 30-day case is a scenario, not an "
        "assumption that monthly treasury review "
        "requires monthly liquidation."
    )

    print(
        "Published broker commission is now known, "
        "but spread, slippage, market impact, and "
        "residual corporate access economics remain "
        "unresolved."
    )

    print(
        "Therefore realistic expected return remains "
        "UNKNOWN in both scenarios."
    )


if __name__ == "__main__":
    main()