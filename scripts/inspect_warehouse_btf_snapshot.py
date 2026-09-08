from __future__ import annotations

from treasury_intelligence.analytics.risk_assessments import (
    get_btf_risk_assessments,
)
from treasury_intelligence.analytics.universe_candidates import (
    _build_french_btf_universe_candidate,
)
from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)
from treasury_intelligence.persistence.database import (
    connect_database,
)
from treasury_intelligence.persistence.opportunity_snapshots import (
    load_latest_opportunity_snapshot,
)
from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_ACCESSIBILITY,
    BTF_2027_03_10_MARKET,
    get_btf_2027_03_10_market_observation,
    get_btf_2027_03_10_snapshot,
)


POSITION_SIZE_EUR = 5_000_000.0
HOLDING_PERIOD_DAYS = 30


def build_candidate(
    *,
    snapshot,
    assessment_key: str,
    label: str,
):
    return _build_french_btf_universe_candidate(
        position_size_eur=POSITION_SIZE_EUR,
        mandate=MODEL_COMPANY_MANDATE,
        holding_period_days=HOLDING_PERIOD_DAYS,
        instrument=BTF_2027_03_10,
        market=BTF_2027_03_10_MARKET,
        accessibility=BTF_2027_03_10_ACCESSIBILITY,
        snapshot=snapshot,
        market_observation=(
            get_btf_2027_03_10_market_observation()
        ),
        risk_assessments=(
            get_btf_risk_assessments()
        ),
        assessment_key=assessment_key,
        label=label,
    )


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

    legacy_candidate = build_candidate(
        snapshot=legacy_snapshot,
        assessment_key="btf_legacy",
        label="French BTF Mar 2027 legacy",
    )

    warehouse_candidate = build_candidate(
        snapshot=warehouse_snapshot,
        assessment_key="btf_warehouse",
        label="French BTF Mar 2027 warehouse",
    )

    print(
        "MILESTONE 16C.2 — "
        "WAREHOUSE-BACKED BTF SNAPSHOT"
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
        warehouse_snapshot.yield_measure
        == legacy_snapshot.yield_measure
    )

    assert (
        warehouse_candidate.candidate_status
        == legacy_candidate.candidate_status
    )

    assert (
        warehouse_candidate.recommendation_ready
        == legacy_candidate.recommendation_ready
    )

    assert (
        legacy_candidate.defensible_return_pct
        is not None
    )

    assert (
        warehouse_candidate.defensible_return_pct
        is not None
    )

    expected_delta_pct = (
        warehouse_snapshot.yield_value_pct
        - legacy_snapshot.yield_value_pct
    )

    actual_delta_pct = (
        warehouse_candidate.defensible_return_pct
        - legacy_candidate.defensible_return_pct
    )

    print(
        "Snapshot yield delta:     "
        f"{expected_delta_pct * 100:.2f} bps"
    )

    print(
        "Candidate return delta:   "
        f"{actual_delta_pct * 100:.2f} bps"
    )

    assert abs(
        expected_delta_pct
        - 0.023
    ) < 0.000001

    assert abs(
        actual_delta_pct
        - expected_delta_pct
    ) < 0.000001

    print()
    print(
        "Warehouse evidence propagated through "
        "existing candidate analytics: yes"
    )

    print(
        "Legacy source fixture unchanged:       yes"
    )

    print(
        "External network required:             no"
    )

    print()
    print(
        "All Milestone 16C.2 assertions passed."
    )


if __name__ == "__main__":
    main()
