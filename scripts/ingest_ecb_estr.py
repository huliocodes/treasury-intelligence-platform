from __future__ import annotations

from datetime import datetime, timezone

from treasury_intelligence.persistence.database import (
    connect_database,
)

from treasury_intelligence.persistence.market_evidence_store import (
    insert_market_evidence,
)

from treasury_intelligence.sources.ecb import (
    build_estr_market_evidence_record,
    fetch_recent_estr,
)


def main() -> None:
    observations = fetch_recent_estr(
        limit=1
    )

    if len(observations) != 1:
        raise RuntimeError(
            "Expected exactly one latest ECB €STR "
            "observation."
        )

    observation = observations[0]

    ingestion_run_id = (
        "ecb_estr_"
        + datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%SZ"
        )
    )

    record = build_estr_market_evidence_record(
        observation=observation,
        ingestion_run_id=ingestion_run_id,
    )

    with connect_database() as connection:
        inserted = insert_market_evidence(
            connection=connection,
            record=record,
        )

    print("ECB ESTR INGESTION")
    print()
    print(
        f"Reference date:      "
        f"{observation.reference_date}"
    )
    print(
        f"Rate:                "
        f"{observation.rate_pct}%"
    )
    print(
        f"Benchmark:           "
        f"{observation.benchmark_id}"
    )
    print(
        f"Evidence ID:         "
        f"{record.evidence_id}"
    )
    print(
        f"Evidence type:       "
        f"{record.evidence_type}"
    )
    print(
        f"Measure:             "
        f"{record.measure}"
    )
    print(
        f"Inserted:            "
        f"{inserted}"
    )


if __name__ == "__main__":
    main()
