from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from treasury_intelligence.persistence.database import (
    connect_database,
)

from treasury_intelligence.persistence.market_evidence_store import (
    MarketEvidenceRecord,
    get_latest_market_evidence,
    insert_market_evidence,
)


RUN_ID = "milestone_16a2_validation"

OLDER_EVIDENCE_ID = (
    "milestone_16a2_fr_btf_mar_2026_08_31"
)

NEWER_EVIDENCE_ID = (
    "milestone_16a2_fr_btf_mar_2026_09_07"
)


def main() -> None:
    older_record = MarketEvidenceRecord(
        evidence_id=OLDER_EVIDENCE_ID,
        instrument_id="fr_btf_2027_03_10",
        market_id="fr_btf_2027_03_10_ibkr",
        access_route_id=(
            "fr_btf_2027_03_10_ibkr"
        ),
        evidence_type="market_return",
        observed_at=datetime(
            2026,
            8,
            31,
            tzinfo=timezone.utc,
        ),
        measure=(
            "auction_weighted_average_rate"
        ),
        numeric_value=Decimal("2.697"),
        unit="pct",
        source_reference=(
            "aft_btf_auction_2026_08_31"
        ),
        source_name="Agence France Tresor",
        source_url=(
            "https://www.aft.gouv.fr/"
        ),
        ingestion_run_id=RUN_ID,
        raw_payload={
            "served_eur": 1_696_000_000,
        },
    )

    newer_record = MarketEvidenceRecord(
        evidence_id=NEWER_EVIDENCE_ID,
        instrument_id="fr_btf_2027_03_10",
        market_id="fr_btf_2027_03_10_ibkr",
        access_route_id=(
            "fr_btf_2027_03_10_ibkr"
        ),
        evidence_type="market_return",
        observed_at=datetime(
            2026,
            9,
            7,
            tzinfo=timezone.utc,
        ),
        measure=(
            "auction_weighted_average_rate"
        ),
        numeric_value=Decimal("2.720"),
        unit="pct",
        source_reference=(
            "aft_btf_auction_2026_09_07"
        ),
        source_name="Agence France Tresor",
        source_url=(
            "https://www.aft.gouv.fr/"
        ),
        ingestion_run_id=RUN_ID,
        raw_payload={
            "bid_eur": 8_290_000_000,
            "served_eur": 1_600_000_000,
            "bid_to_cover": 5.18,
        },
    )

    connection = connect_database()

    try:
        first_insert = insert_market_evidence(
            connection=connection,
            record=older_record,
        )

        second_insert = insert_market_evidence(
            connection=connection,
            record=newer_record,
        )

        duplicate_insert = (
            insert_market_evidence(
                connection=connection,
                record=newer_record,
            )
        )

        latest_before_refresh = (
            get_latest_market_evidence(
                connection=connection,
                instrument_id=(
                    "fr_btf_2027_03_10"
                ),
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

        latest_after_refresh = (
            get_latest_market_evidence(
                connection=connection,
                instrument_id=(
                    "fr_btf_2027_03_10"
                ),
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

        print(
            "MILESTONE 16A.2 — "
            "POSTGRES MARKET EVIDENCE STORE"
        )

        print()

        print(
            "Older evidence inserted:       ",
            first_insert,
        )

        print(
            "Newer evidence inserted:       ",
            second_insert,
        )

        print(
            "Duplicate inserted again:      ",
            duplicate_insert,
        )

        print()

        assert latest_before_refresh is not None

        print(
            "Latest as of 2026-09-03:       ",
            latest_before_refresh[
                "evidence_id"
            ],
        )

        print(
            "Yield as of 2026-09-03:        ",
            f"{latest_before_refresh['numeric_value']}%",
        )

        print()

        assert latest_after_refresh is not None

        print(
            "Latest as of 2026-09-08:       ",
            latest_after_refresh[
                "evidence_id"
            ],
        )

        print(
            "Yield as of 2026-09-08:        ",
            f"{latest_after_refresh['numeric_value']}%",
        )

        print()

        assert first_insert is True
        assert second_insert is True

        assert duplicate_insert is False

        assert (
            latest_before_refresh[
                "evidence_id"
            ]
            == OLDER_EVIDENCE_ID
        )

        assert (
            latest_before_refresh[
                "numeric_value"
            ]
            == Decimal("2.697")
        )

        assert (
            latest_after_refresh[
                "evidence_id"
            ]
            == NEWER_EVIDENCE_ID
        )

        assert (
            latest_after_refresh[
                "numeric_value"
            ]
            == Decimal("2.720")
        )

        print(
            "Append-only inserts:           yes"
        )

        print(
            "Idempotent ingestion retry:    yes"
        )

        print(
            "Historical as-of query:        yes"
        )

        print(
            "Latest evidence resolution:    yes"
        )

        print()

        print(
            "All Milestone 16A.2 assertions passed."
        )

    finally:
        connection.rollback()
        connection.close()

        print()
        print(
            "Validation transaction rolled back; "
            "no fixture rows persisted."
        )


if __name__ == "__main__":
    main()
