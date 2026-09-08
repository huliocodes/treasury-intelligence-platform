from __future__ import annotations

from datetime import datetime, timezone

from treasury_intelligence.persistence.database import (
    connect_database,
)

from treasury_intelligence.persistence.market_evidence_store import (
    insert_market_evidence,
)

from treasury_intelligence.sources.aave import (
    build_aave_market_evidence_records,
    fetch_aave_v3_base_eurc,
)


def main() -> None:
    observation = fetch_aave_v3_base_eurc()

    ingestion_run_id = (
        "aave_v3_base_eurc_"
        + datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%SZ"
        )
    )

    records = build_aave_market_evidence_records(
        observation=observation,
        ingestion_run_id=ingestion_run_id,
    )

    with connect_database() as connection:
        inserted = tuple(
            insert_market_evidence(
                connection=connection,
                record=record,
            )
            for record in records
        )

    print("AAVE V3 BASE EURC INGESTION")
    print()
    print(
        "Observed at:          "
        f"{observation.observed_at.isoformat()}"
    )
    print(
        "Supply APY:           "
        f"{observation.supply_apy_pct:.6f}%"
    )
    print(
        "Total supplied:       "
        f"{observation.total_supplied:,.2f} EURC"
    )
    print(
        "Total borrowed:       "
        f"{observation.total_borrowed:,.2f} EURC"
    )
    print(
        "Available liquidity:  "
        f"{observation.available_liquidity:,.2f} EURC"
    )
    print(
        "Utilization:          "
        f"{observation.utilization_pct:.2f}%"
    )
    print(
        "Supply cap:           "
        f"{observation.supply_cap}"
    )
    print()

    for record, was_inserted in zip(
        records,
        inserted,
        strict=True,
    ):
        print(
            f"{record.evidence_type} / "
            f"{record.measure}"
        )
        print(
            f"  Evidence ID: {record.evidence_id}"
        )
        print(
            f"  Inserted:    {was_inserted}"
        )


if __name__ == "__main__":
    main()
