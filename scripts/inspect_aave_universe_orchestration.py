from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_DIR),
    )


from treasury_intelligence.analytics.generic_returns import (
    build_conservative_return_components,
)
from treasury_intelligence.analytics.positions import (
    build_aave_position_analysis,
)
from treasury_intelligence.analytics.risk_assessments import (
    get_aave_eurc_risk_assessments,
)
from treasury_intelligence.analytics.universe import (
    analyze_opportunity_position,
)
from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
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


POSITION_SIZES_EUR = (
    100_000.0,
    500_000.0,
    1_000_000.0,
    5_000_000.0,
)

HOLDING_PERIOD_DAYS = 365


def main() -> None:
    observation = fetch_aave_v3_base_eurc()

    snapshot = build_aave_eurc_snapshot(
        observation
    )

    risk_assessments = (
        get_aave_eurc_risk_assessments()
    )

    print("AAVE GENERIC UNIVERSE ORCHESTRATION")
    print("=" * 72)

    print(
        f"Observed at: "
        f"{observation.observed_at.isoformat()}"
    )

    print(
        f"Supply APY: "
        f"{observation.supply_apy_pct:.3f}%"
    )

    print(
        f"Total supplied: "
        f"EURC {observation.total_supplied:,.2f}"
    )

    print(
        f"Available liquidity: "
        f"EURC {observation.available_liquidity:,.2f}"
    )

    print(
        f"Supply cap: "
        f"{observation.supply_cap}"
    )

    print(
        f"Accessibility: "
        f"{AAVE_V3_BASE_EURC_ACCESSIBILITY.status}"
    )

    print(
        f"Risk dimensions: "
        f"{len(risk_assessments)}"
    )

    for position_size_eur in POSITION_SIZES_EUR:
        position = build_aave_position_analysis(
            observation=observation,
            position_size_eur=position_size_eur,
        )

        return_components = (
            build_conservative_return_components(
                instrument=(
                    AAVE_V3_BASE_EURC_INSTRUMENT
                ),
                market=(
                    AAVE_V3_BASE_EURC_MARKET
                ),
                snapshot=snapshot,
                reference_yield_includes_product_fee=True,
            )
        )

        network_cost = next(
            component
            for component in return_components
            if component.component_type
            == "network_cost"
        )

        fx_cost = next(
            component
            for component in return_components
            if component.component_type
            == "fx_hedging_cost"
        )

        candidate = analyze_opportunity_position(
            assessment_id=(
                "aave_v3_base_eurc_"
                f"{int(position_size_eur)}"
            ),
            label="Aave V3 Base EURC",
            mandate=MODEL_COMPANY_MANDATE,
            instrument=(
                AAVE_V3_BASE_EURC_INSTRUMENT
            ),
            market=(
                AAVE_V3_BASE_EURC_MARKET
            ),
            accessibility=(
                AAVE_V3_BASE_EURC_ACCESSIBILITY
            ),
            snapshot=snapshot,
            position_size_eur=position_size_eur,
            holding_period_days=(
                HOLDING_PERIOD_DAYS
            ),
            position_builder=(
                lambda size, observation=observation:
                build_aave_position_analysis(
                    observation=observation,
                    position_size_eur=size,
                )
            ),
            risk_assessments=(
                risk_assessments
            ),
            return_component_builder=(
                lambda _size, snapshot=snapshot:
                build_conservative_return_components(
                    instrument=(
                        AAVE_V3_BASE_EURC_INSTRUMENT
                    ),
                    market=(
                        AAVE_V3_BASE_EURC_MARKET
                    ),
                    snapshot=snapshot,
                    reference_yield_includes_product_fee=True,
                )
            ),
            market_observation=None,
            notes=(
                "Aave candidate generated through the "
                "generic normalized universe orchestration "
                "path using live reserve data."
            ),
        )

        print()
        print("-" * 72)

        print(
            f"Position: "
            f"EUR {position_size_eur:,.0f}"
        )

        print(
            f"Entry supported: "
            f"{position.entry_supported}"
        )

        print(
            f"Immediate exit supported: "
            f"{position.immediate_exit_supported}"
        )

        print(
            f"Immediate exit coverage: "
            f"{position.immediate_exit_coverage_pct:.2f}%"
        )

        print(
            f"Reference yield: "
            f"{position.reference_yield_pct:.3f}%"
        )

        print(
            f"Network cost status: "
            f"{network_cost.status}"
        )

        print(
            f"FX/conversion cost status: "
            f"{fx_cost.status}"
        )

        candidate_data = vars(candidate)

        print(
            f"Candidate fields: "
            f"{', '.join(sorted(candidate_data.keys()))}"
        )

        candidate_status = candidate_data.get(
            "candidate_status",
            candidate_data.get(
                "status",
                "FIELD_NOT_FOUND",
            ),
        )

        recommendation_ready = (
            candidate_data.get(
                "recommendation_ready",
                "FIELD_NOT_FOUND",
            )
        )

        print(
            f"Candidate status: "
            f"{candidate_status}"
        )

        print(
            f"Recommendation ready: "
            f"{recommendation_ready}"
        )

    print()
    print("=" * 72)

    print(
        "INTERPRETATION"
    )

    print(
        "Aave now uses the same normalized universe "
        "orchestration contract as the TradFi and MMF "
        "opportunities."
    )

    print(
        "Position-size reserve liquidity remains "
        "Aave-specific, while eligibility, position risk, "
        "return analysis, economics and candidate integration "
        "remain generic."
    )

    print(
        "The current Slovenian corporate route remains "
        "research-only, so Aave must not become "
        "recommendation-ready merely because protocol "
        "liquidity supports a given position."
    )


if __name__ == "__main__":
    main()