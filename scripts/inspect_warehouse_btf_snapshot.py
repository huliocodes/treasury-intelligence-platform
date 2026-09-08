from __future__ import annotations

from treasury_intelligence.analytics.universe_candidates import (
    _build_french_btf_universe_candidate,
)
from treasury_intelligence.persistence.database import (
    connect_database,
)
from treasury_intelligence.persistence.opportunity_snapshots import (
    load_latest_opportunity_snapshot,
)
from treasury_intelligence.risks.france import (
    get_btf_risk_assessments,
)
from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_ACCESSIBILITY,
    BTF_2027_03_10_MARKET,
    get_btf_2027_03_10_market_observation,
    get_btf_2027_03_10_snapshot,
)


POSITION_SIZE_EUR = 5_000_000.0


def main() -> None:
    legacy_snapshot = (
        get_btf_2027_03_10_snapshot()
    )

    with connect_database() as connection:
        warehouse_snapshot = (
            load_latest_opportunity_snapshot(
                connection=connection,
                structural_snapshot=legacy_snapshot,
            )
        )

    market_observation = (
        get_btf_2027_03_10_market_observation()
    )

    legacy_candidate = (
        _build_french_btf_universe_candidate(
            position_size_eur=POSITION_SIZE_EUR,
            mandate=__import__(
                "treasury_intelligence.policies.mandate",
                fromlist=["MODEL_COMPANY_MANDATE"],
            ).MODEL_COMPANY_MANDATE,
            holding_period_days=30,
            instrument=BTF_2027_03_10,
            market=BTF_2027_03_10_MARKET,
            accessibility=(
                BTF_2027_03_10_ACCESSIBILITY
            ),
            snapshot=legacy_snapshot,
            market_observation=market_observation,
            risk_assessments=(
                get_btf_risk_assessments()
            ),
            assessment_key="btf_legacy",
            label="French BTF Mar 2027 legacy",
        )
    )

    warehouse_candidate = (
        _build_french_btf_universe_candidate(
            position_size_eur=POSITION_SIZE_EUR,
            mandate=__import__(
                "treasury_intelligence.policies.mandate",
                fromlist=["MODEL_COMPANY_MANDATE"],
            ).MODEL_COMPANY_MANDATE,
            holding_period_days=30,
            instrument=BTF_2027_03_10,
            market=BTF_2027_03_10_MARKET,
            accessibility=(
                BTF_2027_03_10_ACCESSIBILITY
            ),
            snapshot=warehouse_snapshot,
            market_observation=market_observation,
            risk_assessments=(
                get_btf_risk_assessments()
            ),
            assessment_key="btf_warehouse",
            label="French BTF Mar 2027 warehouse",
        )
    )

    print(
        "MILESTONE 16C.2 — WAREHOUSE-BACKED "
        "BTF SNAPSHOT"
    )
    print()

    print("LEGACY SNAPSHOT")
    print(
        f"Observed: {legacy_snapshot.observed_date}"
    )
    print(
        "Yield:    "
        f"{legacy_snapshot.yield_value_pct:.3f}%"
    )
    print(
        f"Source:   {legacy_snapshot.source}"
    )
    print()

    print("WAREHOUSE SNAPSHOT")
    print(
        f"Observed: {warehouse_snapshot.observed_date}"
    )
    print(
        "Yield:    "
        f"{warehouse_snapshot.yield_value_pct:.3f}%"
    )
    print(
        f"Source:   {warehouse_snapshot.source}"
    )
    print(
        f"Snapshot: {warehouse_snapshot.snapshot_id}"
    )
    print()

    print("LEGACY CANDIDATE")
    print(
        "Status:   "
        f"{legacy_candidate.candidate_status}"
    )
    print(
        "Return:   "
        f"{legacy_candidate.defensible_return_pct:.3f}%"
    )
    print()

    print("WAREHOUSE CANDIDATE")
    print(
        "Status:   "
        f"{warehouse_candidate.candidate_status}"
    )
    print(
        "Return:   "
        f"{warehouse_candidate.defensible_return_pct:.3f}%"
    )
    print()

    assert (
        legacy_snapshot.observed_date
        == "2026-08-31"
    )
    assert abs(
        legacy_snapshot.yield_value_pct
        - 2.697
    ) < 0.000001

    assert (
        warehouse_snapshot.observed_date
        == "2026-09-07"
    )
    assert abs(
        warehouse_snapshot.yield_value_pct
        - 2.720
    ) < 0.000001

    assert (
        warehouse_snapshot.instrument_id
        == legacy_snapshot.instrument_id
    )
    assert (
        warehouse_snapshot.market_id
        == legacy_snapshot.market_id
    )
    assert (
        warehouse_snapshot.access_route_id
        == legacy_snapshot.access_route_id
    )
    assert (
        warehouse_snapshot.outstanding_amount_eur
        == legacy_snapshot.outstanding_amount_eur
    )
    assert (
        warehouse_snapshot.early_exit_possible
        == legacy_snapshot.early_exit_possible
    )

    assert (
        warehouse_candidate.candidate_status
        == legacy_candidate.candidate_status
    )

    assert (
        warehouse_candidate.defensible_return_pct
        > legacy_candidate.defensible_return_pct
    )

    expected_delta = (
        warehouse_snapshot.yield_value_pct
        - legacy_snapshot.yield_value_pct
    )

    actual_delta = (
        warehouse_candidate.defensible_return_pct
        - legacy_candidate.defensible_return_pct
    )

    assert abs(
        expected_delta - actual_delta
    ) < 0.000001

    print(
        "Warehouse evidence propagated through the "
        "existing candidate analytics successfully."
    )
    print()
    print(
        "Production source functions were not changed."
    )
    print(
        "All Milestone 16C.2 assertions passed."
    )


if __name__ == "__main__":
    main()
