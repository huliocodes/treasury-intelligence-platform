from __future__ import annotations

import csv
import io
from dataclasses import dataclass

import requests


ECB_DATA_API_BASE_URL = "https://data-api.ecb.europa.eu/service/data"

ESTR_DATAFLOW = "EST"
ESTR_SERIES_KEY = "B.EU000A2X2A25.WT"


@dataclass(frozen=True)
class EstrObservation:
    reference_date: str
    rate_pct: float
    source: str = "ECB"
    benchmark_id: str = "estr"
    currency: str = "EUR"


def fetch_recent_estr(limit: int = 5) -> list[EstrObservation]:
    """
    Retrieve the most recent ECB euro short-term rate (â‚¬STR) observations.
    """

    if limit < 1:
        raise ValueError("limit must be at least 1")

    url = (
        f"{ECB_DATA_API_BASE_URL}/"
        f"{ESTR_DATAFLOW}/"
        f"{ESTR_SERIES_KEY}"
    )

    params = {
        "format": "csvdata",
        "lastNObservations": limit,
    }

    response = requests.get(
        url,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    reader = csv.DictReader(io.StringIO(response.text))

    observations: list[EstrObservation] = []

    for row in reader:
        reference_date = row.get("TIME_PERIOD")
        value = row.get("OBS_VALUE")

        if not reference_date or value in (None, ""):
            continue

        observations.append(
            EstrObservation(
                reference_date=reference_date,
                rate_pct=float(value),
            )
        )

    if not observations:
        raise ValueError("ECB response contained no usable â‚¬STR observations")

    observations.sort(
        key=lambda observation: observation.reference_date
    )

    return observations

def build_estr_market_evidence_record(
    *,
    observation: EstrObservation,
    ingestion_run_id: str,
):
    """
    Build one immutable warehouse evidence record for an
    ECB euro short-term rate (â‚¬STR) observation.
    """

    from datetime import datetime, timezone
    from decimal import Decimal
    from hashlib import sha256

    from treasury_intelligence.persistence.market_evidence_store import (
        MarketEvidenceRecord,
    )

    if not ingestion_run_id:
        raise ValueError(
            "ingestion_run_id is required."
        )

    evidence_key = "|".join(
        (
            "ecb",
            observation.benchmark_id,
            observation.reference_date,
            "rate",
        )
    )

    evidence_hash = sha256(
        evidence_key.encode("utf-8")
    ).hexdigest()[:16]

    evidence_id = (
        "ecb_estr_"
        f"{observation.reference_date}_"
        f"{evidence_hash}"
    )

    observed_at = datetime.fromisoformat(
        observation.reference_date
    ).replace(
        tzinfo=timezone.utc
    )

    return MarketEvidenceRecord(
        evidence_id=evidence_id,
        instrument_id=observation.benchmark_id,
        market_id=None,
        access_route_id=None,
        evidence_type="benchmark",
        observed_at=observed_at,
        measure="estr_rate",
        numeric_value=Decimal(
            str(observation.rate_pct)
        ),
        unit="pct",
        source_reference=(
            "ecb_estr_"
            f"{observation.reference_date}"
        ),
        source_name=observation.source,
        source_url=(
            "https://data-api.ecb.europa.eu/"
            "service/data/EST/"
            "B.EU000A2X2A25.WT"
        ),
        ingestion_run_id=ingestion_run_id,
        raw_payload={
            "benchmark_id": (
                observation.benchmark_id
            ),
            "reference_date": (
                observation.reference_date
            ),
            "rate_pct": str(
                observation.rate_pct
            ),
            "currency": observation.currency,
            "series_key": ESTR_SERIES_KEY,
            "dataflow": ESTR_DATAFLOW,
        },
    )

def load_latest_estr_observation(
    *,
    connection,
    as_of,
) -> EstrObservation:
    """
    Load the latest persisted ECB ESTR benchmark observation
    from the treasury evidence warehouse.
    """

    from treasury_intelligence.persistence.market_evidence_store import (
        get_latest_market_evidence,
    )

    evidence = get_latest_market_evidence(
        connection=connection,
        instrument_id="estr",
        evidence_type="benchmark",
        as_of=as_of,
    )

    if evidence is None:
        raise LookupError(
            "No persisted ECB ESTR benchmark evidence "
            "exists as of the requested timestamp."
        )

    if evidence.get("measure") != "estr_rate":
        raise ValueError(
            "Latest ESTR benchmark evidence must have "
            "measure='estr_rate'."
        )

    if evidence.get("unit") != "pct":
        raise ValueError(
            "Latest ESTR benchmark evidence must have "
            "unit='pct'."
        )

    numeric_value = evidence.get("numeric_value")

    if numeric_value is None:
        raise ValueError(
            "Latest ESTR benchmark evidence is missing "
            "numeric_value."
        )

    observed_at = evidence.get("observed_at")

    if observed_at is None:
        raise ValueError(
            "Latest ESTR benchmark evidence is missing "
            "observed_at."
        )

    raw_payload = evidence.get("raw_payload") or {}

    reference_date = (
        raw_payload.get("reference_date")
        or observed_at.date().isoformat()
    )

    return EstrObservation(
        reference_date=str(reference_date),
        rate_pct=float(numeric_value),
        source=(
            evidence.get("source_name")
            or "ECB"
        ),
        benchmark_id="estr",
        currency=(
            raw_payload.get("currency")
            or "EUR"
        ),
    )
