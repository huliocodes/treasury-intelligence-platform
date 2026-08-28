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
    Retrieve the most recent ECB euro short-term rate (€STR) observations.
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
        raise ValueError("ECB response contained no usable €STR observations")

    observations.sort(
        key=lambda observation: observation.reference_date
    )

    return observations