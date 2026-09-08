from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from treasury_intelligence.persistence.database import (
    connect_database,
)

from treasury_intelligence.persistence.market_evidence_store import (
    get_latest_market_evidence,
)


INSTRUMENT_ID = "fr_btf_2027_03_10"


def main() -> None:
    with connect_database() as connection:
        as_of_sep_3 = (
            get_latest_market_evidence(
                connection=connection,
                instrument_id=INSTRUMENT_ID,
                evidence_type="market_return",
                as_of=datetime(
                    2026,
                    9,
                    3,
                    23,
                    59,
                    59,
                    tzinfo=timezone.utc,
                ),
            )
        )

        as_of_sep_8 = (
            get_latest_market_evidence(
                connection=connection,
                instrument_id=INSTRUMENT_ID,
                evidence_type="market_return",
                as_of=datetime(
                    2026,
                    9,
                    8,
                    23,
                    59,
                    59,
                    tzinfo=timezone.utc,
                ),
            )
        )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    evidence_id,
                    observed_at,
                    numeric_value,
                    source_reference,
                    ingestion_run_id
                FROM market_evidence
                WHERE instrument_id = %s
                  AND evidence_type =
                      'market_return'
                ORDER BY
                    observed_at,
                    evidence_id
                """,
                (
                    INSTRUMENT_ID,
                ),
            )

            history = cursor.fetchall()

    print(
        "MILESTONE 16A.4 — "
        "HISTORICAL BTF EVIDENCE"
    )

    print()

    print(
        "Persisted observations:        ",
        len(history),
    )

    for row in history:
        print(
            "  ",
            row[1].date().isoformat(),
            f"{row[2]}%",
            row[0],
        )

    print()

    assert as_of_sep_3 is not None
    assert as_of_sep_8 is not None

    print(
        "Latest as of 2026-09-03:       ",
        as_of_sep_3["evidence_id"],
    )

    print(
        "Yield as of 2026-09-03:        ",
        f"{as_of_sep_3['numeric_value']}%",
    )

    print()

    print(
        "Latest as of 2026-09-08:       ",
        as_of_sep_8["evidence_id"],
    )

    print(
        "Yield as of 2026-09-08:        ",
        f"{as_of_sep_8['numeric_value']}%",
    )

    assert len(history) == 2

    assert (
        history[0][1]
        < history[1][1]
    )

    assert (
        as_of_sep_3["numeric_value"]
        == Decimal("2.697")
    )

    assert (
        as_of_sep_3[
            "observed_at"
        ].date().isoformat()
        == "2026-08-31"
    )

    assert (
        as_of_sep_8["numeric_value"]
        == Decimal("2.720")
    )

    assert (
        as_of_sep_8[
            "observed_at"
        ].date().isoformat()
        == "2026-09-07"
    )

    assert (
        as_of_sep_3["evidence_id"]
        != as_of_sep_8["evidence_id"]
    )

    print()

    print(
        "Immutable historical rows:     yes"
    )

    print(
        "V1 state reproducible:         yes"
    )

    print(
        "Current state reproducible:    yes"
    )

    print(
        "As-of resolution works:        yes"
    )

    print(
        "Source code overwrite needed:  no"
    )

    print()

    print(
        "All Milestone 16A.4 "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
