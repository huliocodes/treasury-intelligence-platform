from __future__ import annotations

from datetime import datetime, timezone

from treasury_intelligence.persistence.database import (
    connect_database,
)

from treasury_intelligence.persistence.market_evidence_store import (
    insert_market_evidence,
)

from treasury_intelligence.sources.ishares import (
    build_ernx_market_evidence_record,
    fetch_ernx_return_observation,
)


def main() -> None:
    observation = (
        fetch_ernx_return_observation()
    )

    ingestion_run_id = (
        "ernx_"
        + datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%SZ"
        )
    )

    record = (
        build_ernx_market_evidence_record(
            observation=observation,
            ingestion_run_id=(
                ingestion_run_id
            ),
        )
    )

    with connect_database() as connection:
        inserted = insert_market_evidence(
            connection=connection,
            record=record,
        )

    print("ERNX MARKET-RETURN INGESTION")
    print()

    print(
        "Observed at:          "
        f"{observation.observed_at.isoformat()}"
    )

    print(
        "Weighted Avg YTM:     "
        f"{observation.weighted_average_ytm_pct:.3f}%"
    )

    print(
        "Evidence ID:          "
        f"{record.evidence_id}"
    )

    print(
        "Evidence type:        "
        f"{record.evidence_type}"
    )

    print(
        "Measure:              "
        f"{record.measure}"
    )

    print(
        "Inserted:             "
        f"{inserted}"
    )


if __name__ == "__main__":
    main()
