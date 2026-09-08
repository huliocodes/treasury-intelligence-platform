from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


SUPPORTED_EVIDENCE_TYPES = frozenset(
    {
        "market_return",
        "market_liquidity",
        "benchmark",
        "risk",
        "accessibility",
        "cost",
    }
)


@dataclass(frozen=True)
class MarketEvidenceRecord:
    evidence_id: str

    instrument_id: str
    evidence_type: str

    observed_at: datetime

    measure: str
    source_reference: str
    ingestion_run_id: str

    market_id: str | None = None
    access_route_id: str | None = None

    numeric_value: Decimal | None = None
    unit: str | None = None

    source_name: str | None = None
    source_url: str | None = None

    raw_payload: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.evidence_id:
            raise ValueError(
                "evidence_id is required."
            )

        if not self.instrument_id:
            raise ValueError(
                "instrument_id is required."
            )

        if (
            self.evidence_type
            not in SUPPORTED_EVIDENCE_TYPES
        ):
            raise ValueError(
                "Unsupported evidence_type: "
                f"{self.evidence_type}"
            )

        if not self.measure:
            raise ValueError(
                "measure is required."
            )

        if not self.source_reference:
            raise ValueError(
                "source_reference is required."
            )

        if not self.ingestion_run_id:
            raise ValueError(
                "ingestion_run_id is required."
            )

        if self.observed_at.tzinfo is None:
            raise ValueError(
                "observed_at must be timezone-aware."
            )


def insert_market_evidence(
    *,
    connection: Connection,
    record: MarketEvidenceRecord,
) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO market_evidence (
                evidence_id,
                instrument_id,
                market_id,
                access_route_id,
                evidence_type,
                observed_at,
                measure,
                numeric_value,
                unit,
                source_reference,
                source_name,
                source_url,
                ingestion_run_id,
                raw_payload
            )
            VALUES (
                %(evidence_id)s,
                %(instrument_id)s,
                %(market_id)s,
                %(access_route_id)s,
                %(evidence_type)s,
                %(observed_at)s,
                %(measure)s,
                %(numeric_value)s,
                %(unit)s,
                %(source_reference)s,
                %(source_name)s,
                %(source_url)s,
                %(ingestion_run_id)s,
                %(raw_payload)s
            )
            ON CONFLICT (evidence_id)
            DO NOTHING
            RETURNING evidence_id
            """,
            {
                "evidence_id": record.evidence_id,
                "instrument_id": record.instrument_id,
                "market_id": record.market_id,
                "access_route_id": (
                    record.access_route_id
                ),
                "evidence_type": (
                    record.evidence_type
                ),
                "observed_at": record.observed_at,
                "measure": record.measure,
                "numeric_value": (
                    record.numeric_value
                ),
                "unit": record.unit,
                "source_reference": (
                    record.source_reference
                ),
                "source_name": record.source_name,
                "source_url": record.source_url,
                "ingestion_run_id": (
                    record.ingestion_run_id
                ),
                "raw_payload": Jsonb(
                    record.raw_payload or {}
                ),
            },
        )

        return cursor.fetchone() is not None


def get_latest_market_evidence(
    *,
    connection: Connection,
    instrument_id: str,
    evidence_type: str,
    as_of: datetime,
) -> dict[str, Any] | None:
    if (
        evidence_type
        not in SUPPORTED_EVIDENCE_TYPES
    ):
        raise ValueError(
            "Unsupported evidence_type: "
            f"{evidence_type}"
        )

    if as_of.tzinfo is None:
        raise ValueError(
            "as_of must be timezone-aware."
        )

    with connection.cursor(
        row_factory=dict_row
    ) as cursor:
        cursor.execute(
            """
            SELECT
                evidence_id,
                instrument_id,
                market_id,
                access_route_id,
                evidence_type,
                observed_at,
                measure,
                numeric_value,
                unit,
                source_reference,
                source_name,
                source_url,
                ingestion_run_id,
                raw_payload,
                ingested_at
            FROM market_evidence
            WHERE instrument_id = %(instrument_id)s
              AND evidence_type = %(evidence_type)s
              AND observed_at <= %(as_of)s
            ORDER BY
                observed_at DESC,
                ingested_at DESC,
                evidence_id DESC
            LIMIT 1
            """,
            {
                "instrument_id": instrument_id,
                "evidence_type": evidence_type,
                "as_of": as_of,
            },
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)
