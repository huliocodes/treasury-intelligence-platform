from __future__ import annotations

from decimal import Decimal
from typing import Any

from psycopg import Connection
from psycopg.rows import dict_row

from treasury_intelligence.models.opportunities import (
    OpportunitySnapshot,
)


def get_latest_market_return_evidence(
    *,
    connection: Connection,
    instrument_id: str,
    market_id: str,
    access_route_id: str,
    measure: str,
) -> dict[str, Any] | None:
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
                measure,
                observed_at,
                observed_date,
                numeric_value,
                unit,
                source_reference,
                source_name,
                source_url,
                ingestion_run_id,
                raw_payload,
                ingested_at
            FROM analytics_marts.latest_market_evidence
            WHERE instrument_id = %(instrument_id)s
              AND market_id = %(market_id)s
              AND access_route_id = %(access_route_id)s
              AND evidence_type = 'market_return'
              AND measure = %(measure)s
            LIMIT 1
            """,
            {
                "instrument_id": instrument_id,
                "market_id": market_id,
                "access_route_id": access_route_id,
                "measure": measure,
            },
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)


def build_opportunity_snapshot_from_market_return_evidence(
    *,
    evidence: dict[str, Any],
    structural_snapshot: OpportunitySnapshot,
) -> OpportunitySnapshot:
    required_fields = (
        "evidence_id",
        "instrument_id",
        "market_id",
        "access_route_id",
        "evidence_type",
        "measure",
        "observed_date",
        "numeric_value",
        "unit",
        "source_reference",
    )

    missing_fields = [
        field
        for field in required_fields
        if evidence.get(field) is None
    ]

    if missing_fields:
        raise ValueError(
            "Market return evidence missing required fields: "
            + ", ".join(missing_fields)
        )

    if evidence["evidence_type"] != "market_return":
        raise ValueError(
            "Evidence must have evidence_type "
            "'market_return'."
        )

    if evidence["instrument_id"] != (
        structural_snapshot.instrument_id
    ):
        raise ValueError(
            "Evidence instrument does not match "
            "structural snapshot."
        )

    if evidence["market_id"] != (
        structural_snapshot.market_id
    ):
        raise ValueError(
            "Evidence market does not match "
            "structural snapshot."
        )

    if evidence["access_route_id"] != (
        structural_snapshot.access_route_id
    ):
        raise ValueError(
            "Evidence access route does not match "
            "structural snapshot."
        )

    if evidence["unit"] != "pct":
        raise ValueError(
            "Market return evidence unit must be 'pct'."
        )

    numeric_value = evidence["numeric_value"]

    if not isinstance(
        numeric_value,
        (Decimal, int, float),
    ):
        raise ValueError(
            "Market return numeric_value must be numeric."
        )

    raw_payload = evidence.get("raw_payload") or {}

    yield_basis = (
        "Latest persisted market-return evidence from "
        "the treasury intelligence warehouse. "
        f"Source reference: "
        f"{evidence['source_reference']}. "
        "This remains published market evidence rather "
        "than a firm executable secondary-market quote."
    )

    if raw_payload.get("auction_date"):
        yield_basis += (
            " Auction date: "
            f"{raw_payload['auction_date']}."
        )

    notes = (
        structural_snapshot.notes
        or ""
    )

    warehouse_note = (
        " Market return refreshed from "
        "analytics_marts.latest_market_evidence using "
        f"evidence_id={evidence['evidence_id']} and "
        f"ingestion_run_id="
        f"{evidence.get('ingestion_run_id')}."
    )

    return OpportunitySnapshot(
        snapshot_id=(
            f"{evidence['instrument_id']}_"
            f"{evidence['measure']}_"
            f"{evidence['observed_date'].isoformat()}"
        ),
        instrument_id=evidence["instrument_id"],
        market_id=evidence["market_id"],
        access_route_id=evidence["access_route_id"],
        observed_date=(
            evidence["observed_date"].isoformat()
        ),
        yield_measure=evidence["measure"],
        yield_value_pct=float(numeric_value),
        yield_basis=yield_basis,
        annual_fee_pct=(
            structural_snapshot.annual_fee_pct
        ),
        benchmark_id=(
            structural_snapshot.benchmark_id
        ),
        benchmark_spread_bps=(
            structural_snapshot.benchmark_spread_bps
        ),
        duration_years=(
            structural_snapshot.duration_years
        ),
        average_maturity_years=(
            structural_snapshot.average_maturity_years
        ),
        fund_aum_eur=(
            structural_snapshot.fund_aum_eur
        ),
        share_class_aum_eur=(
            structural_snapshot.share_class_aum_eur
        ),
        outstanding_amount_eur=(
            structural_snapshot.outstanding_amount_eur
        ),
        holdings_count=(
            structural_snapshot.holdings_count
        ),
        price_status=(
            structural_snapshot.price_status
        ),
        quote_firmness=(
            structural_snapshot.quote_firmness
        ),
        early_exit_possible=(
            structural_snapshot.early_exit_possible
        ),
        source=(
            evidence.get("source_name")
            or structural_snapshot.source
        ),
        source_url=(
            evidence.get("source_url")
            or structural_snapshot.source_url
        ),
        notes=notes + warehouse_note,
    )


def load_latest_opportunity_snapshot(
    *,
    connection: Connection,
    structural_snapshot: OpportunitySnapshot,
) -> OpportunitySnapshot:
    evidence = get_latest_market_return_evidence(
        connection=connection,
        instrument_id=(
            structural_snapshot.instrument_id
        ),
        market_id=structural_snapshot.market_id,
        access_route_id=(
            structural_snapshot.access_route_id
        ),
        measure=structural_snapshot.yield_measure,
    )

    if evidence is None:
        raise LookupError(
            "No latest market-return evidence found for "
            f"{structural_snapshot.instrument_id} / "
            f"{structural_snapshot.market_id} / "
            f"{structural_snapshot.access_route_id} / "
            f"{structural_snapshot.yield_measure}."
        )

    return (
        build_opportunity_snapshot_from_market_return_evidence(
            evidence=evidence,
            structural_snapshot=structural_snapshot,
        )
    )
