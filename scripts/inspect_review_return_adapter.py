from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.economics import (
    build_economics_evidence_assessment,
)

from treasury_intelligence.analytics.review_returns import (
    build_allocation_return_input,
)

from treasury_intelligence.analytics.returns import (
    build_return_analysis,
)

from treasury_intelligence.models.returns import (
    ReturnComponent,
)


def build_complete_analysis():
    return build_return_analysis(
        analysis_id="complete_return_fixture",
        instrument_id="instrument_complete",
        market_id="market_complete",
        access_route_id="access_complete",
        position_size_eur=500_000,
        holding_period_days=365,
        components=(
            ReturnComponent(
                component_id="complete_reference_yield",
                component_type="reference_yield",
                label="Reference yield",
                status="published",
                basis="annualized_pct",
                value=3.0,
                source="fixture",
                source_url=None,
                notes=(
                    "Deterministic published "
                    "reference-yield fixture."
                ),
            ),
            ReturnComponent(
                component_id="complete_product_fee",
                component_type="product_fee",
                label="Product fee",
                status="published",
                basis="annualized_pct",
                value=0.10,
                source="fixture",
                source_url=None,
                notes=(
                    "Deterministic published "
                    "recurring-fee fixture."
                ),
            ),
        ),
        notes=(
            "Deterministic complete economics fixture."
        ),
    )


def build_incomplete_analysis():
    return build_return_analysis(
        analysis_id="incomplete_return_fixture",
        instrument_id="instrument_incomplete",
        market_id="market_incomplete",
        access_route_id="access_incomplete",
        position_size_eur=500_000,
        holding_period_days=365,
        components=(
            ReturnComponent(
                component_id="incomplete_reference_yield",
                component_type="reference_yield",
                label="Reference yield",
                status="published",
                basis="annualized_pct",
                value=3.0,
                source="fixture",
                source_url=None,
                notes=(
                    "Deterministic published "
                    "reference-yield fixture."
                ),
            ),
            ReturnComponent(
                component_id="unknown_slippage",
                component_type="slippage_price_impact",
                label="Executable slippage / price impact",
                status="unknown",
                basis="position_bps",
                value=None,
                source=None,
                source_url=None,
                notes=(
                    "Position-size executable slippage "
                    "and price-impact evidence is "
                    "intentionally unavailable."
                ),
            ),
        ),
        notes=(
            "Deterministic incomplete economics fixture."
        ),
    )


def print_result(
    title: str,
    return_analysis,
    economics,
    allocation_return,
) -> None:
    print(title)
    print()

    print(
        f"Return analysis:               "
        f"{return_analysis.analysis_id}"
    )

    print(
        f"Economics status:              "
        f"{economics.economics_status}"
    )

    print(
        f"Realistic return available:    "
        f"{economics.realistic_expected_return_available}"
    )

    if (
        return_analysis.return_after_known_costs_pct
        is None
    ):
        known_cost_return = "UNKNOWN"
    else:
        known_cost_return = (
            f"{return_analysis.return_after_known_costs_pct:.3f}%"
        )

    print(
        f"Return after known costs:      "
        f"{known_cost_return}"
    )

    if (
        return_analysis.realistic_expected_return_pct
        is None
    ):
        realistic_return = "UNKNOWN"
    else:
        realistic_return = (
            f"{return_analysis.realistic_expected_return_pct:.3f}%"
        )

    print(
        f"Realistic expected return:     "
        f"{realistic_return}"
    )

    print(
        f"Adapter evidence available:    "
        f"{allocation_return.evidence_available}"
    )

    if allocation_return.annual_return_pct is None:
        adapter_return = "UNKNOWN"
    else:
        adapter_return = (
            f"{allocation_return.annual_return_pct:.3f}%"
        )

    print(
        f"Adapter annual return:         "
        f"{adapter_return}"
    )

    print(
        f"Adapter source reference:      "
        f"{allocation_return.source_reference}"
    )

    print()
    print("-" * 100)
    print()


def main() -> None:
    print(
        "REVIEW RETURN ADAPTER"
    )

    print()

    print(
        "The adapter converts existing return/economics "
        "analysis into the return input required by the "
        "treasury review comparison layer."
    )

    print()

    print(
        "Incomplete economics must remain UNKNOWN rather "
        "than leaking return-after-known-costs into the "
        "review as a realistic expected return."
    )

    print()
    print("-" * 100)
    print()

    complete_analysis = (
        build_complete_analysis()
    )

    complete_economics = (
        build_economics_evidence_assessment(
            complete_analysis
        )
    )

    complete_input = (
        build_allocation_return_input(
            label="COMPLETE POSITION",
            return_analysis=complete_analysis,
            economics=complete_economics,
            notes=(
                "Complete adapter fixture."
            ),
        )
    )

    print_result(
        title="CASE 1 — COMPLETE ECONOMICS",
        return_analysis=complete_analysis,
        economics=complete_economics,
        allocation_return=complete_input,
    )

    incomplete_analysis = (
        build_incomplete_analysis()
    )

    incomplete_economics = (
        build_economics_evidence_assessment(
            incomplete_analysis
        )
    )

    incomplete_input = (
        build_allocation_return_input(
            label="INCOMPLETE POSITION",
            return_analysis=incomplete_analysis,
            economics=incomplete_economics,
            notes=(
                "Incomplete adapter fixture."
            ),
        )
    )

    print_result(
        title="CASE 2 — INCOMPLETE ECONOMICS",
        return_analysis=incomplete_analysis,
        economics=incomplete_economics,
        allocation_return=incomplete_input,
    )

    print("INTERPRETATION")
    print()

    print(
        "Complete economics may cross the boundary into "
        "treasury economic comparison."
    )

    print(
        "Incomplete economics remains unavailable even "
        "when a return-after-known-costs figure exists."
    )

    print(
        "This prevents unknown spread, slippage, access "
        "costs or other blocking frictions from being "
        "silently treated as zero."
    )


if __name__ == "__main__":
    main()