from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from treasury_intelligence.persistence.database import (
    connect_database,
)

from treasury_intelligence.persistence.market_evidence_store import (
    MarketEvidenceRecord,
    insert_market_evidence,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_IBKR_ACCESS,
    BTF_2027_03_10_MARKET,
    get_btf_2027_03_10_snapshot,
)


BACKFILL_RUN_ID = (
    "v1_0_1_market_evidence_backfill"
)

EVIDENCE_ID = (
    "v1_fr_btf_fr0129704153_"
    "2026-08-31_market_return"
)


def main() -> None:
    snapshot = get_btf_2027_03_10_snapshot()

    if BTF_2027_03_10.isin != "FR0129704153":
        raise RuntimeError(
            "Unexpected French March BTF ISIN."
        )

    if snapshot.observed_date != "2026-08-31":
        raise RuntimeError(
            "Unexpected V1 BTF observation date."
        )

    if abs(
        snapshot.yield_value_pct - 2.697
    ) > 0.000001:
        raise RuntimeError(
            "Unexpected V1 BTF yield."
        )

    record = MarketEvidenceRecord(
        evidence_id=EVIDENCE_ID,
        instrument_id=(
            BTF_2027_03_10.instrument_id
        ),
        market_id=(
            BTF_2027_03_10_MARKET.market_id
        ),
        access_route_id=(
            BTF_2027_03_10_IBKR_ACCESS.access_route_id
        ),
        evidence_type="market_return",
        observed_at=datetime(
            2026,
            8,
            31,
            tzinfo=timezone.utc,
        ),
        measure=snapshot.yield_measure,
        numeric_value=Decimal(
            str(
                snapshot.yield_value_pct
            )
        ),
        unit="pct",
        source_reference=(
            "v1_0_1_fr_btf_2027_03_10_"
            "auction_2026_08_31"
        ),
        source_name=(
            snapshot.source
            or "Agence France Tresor"
        ),
        source_url=snapshot.source_url,
        ingestion_run_id=BACKFILL_RUN_ID,
        raw_payload={
            "source_state": "v1.0.1",
            "isin": BTF_2027_03_10.isin,
            "observed_date": (
                snapshot.observed_date
            ),
            "yield_measure": (
                snapshot.yield_measure
            ),
            "yield_value_pct": str(
                snapshot.yield_value_pct
            ),
            "outstanding_amount_eur": (
                None
                if (
                    snapshot
                    .outstanding_amount_eur
                    is None
                )
                else str(
                    snapshot
                    .outstanding_amount_eur
                )
            ),
            "quote_firmness": (
                snapshot.quote_firmness
            ),
            "price_status": (
                snapshot.price_status
            ),
            "backfill_reason": (
                "Preserve the immutable V1 market "
                "observation in the append-only "
                "PostgreSQL evidence history."
            ),
        },
    )

    with connect_database() as connection:
        inserted = insert_market_evidence(
            connection=connection,
            record=record,
        )

    print(
        "V1 FRENCH BTF EVIDENCE BACKFILL"
    )

    print()

    print(
        f"Evidence ID:        "
        f"{record.evidence_id}"
    )

    print(
        f"Instrument:         "
        f"{record.instrument_id}"
    )

    print(
        f"Observed at:        "
        f"{record.observed_at.isoformat()}"
    )

    print(
        f"Yield:              "
        f"{record.numeric_value}%"
    )

    print(
        f"Source state:       "
        f"v1.0.1"
    )

    print(
        f"Inserted:           "
        f"{inserted}"
    )


if __name__ == "__main__":
    main()
