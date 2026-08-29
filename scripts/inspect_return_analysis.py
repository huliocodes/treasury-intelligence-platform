from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.returns import (
    build_return_analysis,
    unknown_cost_component_names,
)

from treasury_intelligence.models.returns import (
    ReturnComponent,
)

from treasury_intelligence.sources.aave import (
    AAVE_V3_BASE_EURC_DIRECT_ACCESS,
    AAVE_V3_BASE_EURC_INSTRUMENT,
    AAVE_V3_BASE_EURC_MARKET,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_IBKR_ACCESS,
    BTF_2027_03_10_MARKET,
)

from treasury_intelligence.sources.ishares import (
    ERNX_IBKR_ACCESS,
    ERNX_INSTRUMENT,
    ERNX_MARKET,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_IBKR_ACCESS,
    XEON_INSTRUMENT,
    XEON_MARKET,
)


HOLDING_PERIOD_DAYS = 30


def build_aave_analysis():
    components = (
        ReturnComponent(
            component_id="aave_reference_yield",
            component_type="reference_yield",
            label="Aave EURC supply APY",
            status="observed",
            basis="annualized_pct",
            value=1.835,
            notes=(
                "Deterministic validation value based on "
                "the previously observed Aave EURC supply APY."
            ),
        ),
        ReturnComponent(
            component_id="aave_product_fee",
            component_type="product_fee",
            label="Embedded protocol product fee",
            status="known_zero",
            basis="annualized_pct",
            value=0.0,
        ),
        ReturnComponent(
            component_id="aave_entry_execution",
            component_type="entry_execution_cost",
            label="EUR to EURC entry execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="aave_exit_execution",
            component_type="exit_execution_cost",
            label="EURC to EUR exit execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="aave_network_cost",
            component_type="network_cost",
            label="Base network transaction cost",
            status="unknown",
            basis="fixed_eur",
            value=None,
        ),
        ReturnComponent(
            component_id="aave_fx_cost",
            component_type="fx_hedging_cost",
            label="Conventional FX hedging cost",
            status="not_applicable",
            basis="annualized_pct",
            value=None,
        ),
    )

    return build_return_analysis(
        analysis_id="aave_eurc_100k_return",
        instrument_id=(
            AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
        ),
        market_id=(
            AAVE_V3_BASE_EURC_MARKET.market_id
        ),
        access_route_id=(
            AAVE_V3_BASE_EURC_DIRECT_ACCESS.access_route_id
        ),
        position_size_eur=100_000,
        holding_period_days=HOLDING_PERIOD_DAYS,
        components=components,
    )


def build_btf_analysis():
    components = (
        ReturnComponent(
            component_id="btf_reference_yield",
            component_type="reference_yield",
            label="Model-derived BTF annualized yield",
            status="model_derived",
            basis="annualized_pct",
            value=2.731,
        ),
        ReturnComponent(
            component_id="btf_product_fee",
            component_type="product_fee",
            label="Instrument product fee",
            status="known_zero",
            basis="annualized_pct",
            value=0.0,
        ),
        ReturnComponent(
            component_id="btf_access_fee",
            component_type="access_fee",
            label="Broker access / custody cost",
            status="unknown",
            basis="annualized_pct",
            value=None,
        ),
        ReturnComponent(
            component_id="btf_entry_execution",
            component_type="entry_execution_cost",
            label="Secondary-market entry execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="btf_exit_execution",
            component_type="exit_execution_cost",
            label="Secondary-market exit execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="btf_fx_cost",
            component_type="fx_hedging_cost",
            label="FX hedging cost",
            status="known_zero",
            basis="annualized_pct",
            value=0.0,
        ),
    )

    return build_return_analysis(
        analysis_id="btf_500k_return",
        instrument_id=BTF_2027_03_10.instrument_id,
        market_id=BTF_2027_03_10_MARKET.market_id,
        access_route_id=(
            BTF_2027_03_10_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=500_000,
        holding_period_days=HOLDING_PERIOD_DAYS,
        components=components,
    )


def build_xeon_analysis():
    components = (
        ReturnComponent(
            component_id="xeon_reference_yield",
            component_type="reference_yield",
            label="€STR plus index spread before ETF fee",
            status="model_derived",
            basis="annualized_pct",
            value=2.273,
        ),
        ReturnComponent(
            component_id="xeon_product_fee",
            component_type="product_fee",
            label="XEON all-in fund fee",
            status="published",
            basis="annualized_pct",
            value=0.10,
        ),
        ReturnComponent(
            component_id="xeon_access_fee",
            component_type="access_fee",
            label="Broker access / custody cost",
            status="unknown",
            basis="annualized_pct",
            value=None,
        ),
        ReturnComponent(
            component_id="xeon_entry_execution",
            component_type="entry_execution_cost",
            label="ETF entry execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="xeon_exit_execution",
            component_type="exit_execution_cost",
            label="ETF exit execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="xeon_fx_cost",
            component_type="fx_hedging_cost",
            label="FX hedging cost",
            status="known_zero",
            basis="annualized_pct",
            value=0.0,
        ),
    )

    return build_return_analysis(
        analysis_id="xeon_500k_return",
        instrument_id=XEON_INSTRUMENT.instrument_id,
        market_id=XEON_MARKET.market_id,
        access_route_id=(
            XEON_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=500_000,
        holding_period_days=HOLDING_PERIOD_DAYS,
        components=components,
    )


def build_ernx_analysis():
    components = (
        ReturnComponent(
            component_id="ernx_reference_yield",
            component_type="reference_yield",
            label="ERNX weighted average YTM",
            status="published",
            basis="annualized_pct",
            value=2.88,
        ),
        ReturnComponent(
            component_id="ernx_product_fee",
            component_type="product_fee",
            label="ERNX TER",
            status="published",
            basis="annualized_pct",
            value=0.09,
        ),
        ReturnComponent(
            component_id="ernx_access_fee",
            component_type="access_fee",
            label="Broker access / custody cost",
            status="unknown",
            basis="annualized_pct",
            value=None,
        ),
        ReturnComponent(
            component_id="ernx_entry_execution",
            component_type="entry_execution_cost",
            label="ETF entry execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="ernx_exit_execution",
            component_type="exit_execution_cost",
            label="ETF exit execution cost",
            status="unknown",
            basis="position_bps",
            value=None,
        ),
        ReturnComponent(
            component_id="ernx_fx_cost",
            component_type="fx_hedging_cost",
            label="FX hedging cost",
            status="known_zero",
            basis="annualized_pct",
            value=0.0,
        ),
    )

    return build_return_analysis(
        analysis_id="ernx_500k_return",
        instrument_id=ERNX_INSTRUMENT.instrument_id,
        market_id=ERNX_MARKET.market_id,
        access_route_id=(
            ERNX_IBKR_ACCESS.access_route_id
        ),
        position_size_eur=500_000,
        holding_period_days=HOLDING_PERIOD_DAYS,
        components=components,
    )


def print_component(
    component: ReturnComponent,
) -> None:
    if component.value is None:
        value_text = "UNKNOWN"
    elif component.basis == "annualized_pct":
        value_text = (
            f"{component.value:.3f}% annualized"
        )
    elif component.basis == "position_bps":
        value_text = (
            f"{component.value:.2f} bps"
        )
    elif component.basis == "fixed_eur":
        value_text = (
            f"EUR {component.value:,.2f}"
        )
    else:
        value_text = str(component.value)

    print(
        f"{component.component_type:<25} | "
        f"{component.status:<15} | "
        f"{component.basis:<15} | "
        f"{value_text:<20} | "
        f"{component.label}"
    )


def print_analysis(
    label: str,
    analysis,
) -> None:
    print(label)
    print()

    print(
        f"Position size:                   "
        f"EUR {analysis.position_size_eur:,.0f}"
    )

    print(
        f"Holding period:                  "
        f"{analysis.holding_period_days} days"
    )

    if analysis.reference_yield_pct is None:
        print(
            "Reference yield:                  UNKNOWN"
        )
    else:
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

    if (
        analysis.return_after_known_costs_pct
        is None
    ):
        print(
            "Return after known costs:         UNKNOWN"
        )
    else:
        print(
            f"Return after known costs:         "
            f"{analysis.return_after_known_costs_pct:.3f}%"
        )

    if (
        analysis.realistic_expected_return_pct
        is None
    ):
        print(
            "Realistic expected return:        UNKNOWN"
        )
    else:
        print(
            f"Realistic expected return:        "
            f"{analysis.realistic_expected_return_pct:.3f}%"
        )

    print(
        f"Economics complete:               "
        f"{analysis.economics_complete}"
    )

    print(
        f"Unknown cost components:          "
        f"{analysis.unknown_cost_component_count}"
    )

    unknown_names = (
        unknown_cost_component_names(
            analysis
        )
    )

    if unknown_names:
        print(
            "Missing economics:"
        )

        for name in unknown_names:
            print(
                f"  - {name}"
            )

    print()
    print("COMPONENTS")
    print()

    for component in analysis.components:
        print_component(component)

    print()
    print("-" * 120)
    print()


def main() -> None:
    print("RETURN & FRICTION ANALYSIS")
    print()

    print(
        "Recurring costs remain annualized, while one-time "
        "costs are stored in their native position-relative "
        "or fixed-EUR form."
    )

    print(
        "One-time costs are annualized only after applying "
        "the modeled holding period."
    )

    print(
        "Unknown costs are never silently treated as zero."
    )

    print()
    print("-" * 120)
    print()

    print_analysis(
        "AAVE V3 BASE EURC",
        build_aave_analysis(),
    )

    print_analysis(
        "FRENCH BTF",
        build_btf_analysis(),
    )

    print_analysis(
        "XEON",
        build_xeon_analysis(),
    )

    print_analysis(
        "ERNX",
        build_ernx_analysis(),
    )

    print("INTERPRETATION")
    print()

    print(
        "Reference yield is an annualized economic starting "
        "measure."
    )

    print(
        "Recurring fees are modeled directly as annualized "
        "percentage costs."
    )

    print(
        "Execution costs may instead be modeled as basis "
        "points of position size or fixed EUR amounts."
    )

    print(
        "Holding period determines the annualized impact of "
        "one-time costs."
    )

    print(
        "Realistic expected return remains UNKNOWN whenever "
        "required cost components remain unknown."
    )


if __name__ == "__main__":
    main()