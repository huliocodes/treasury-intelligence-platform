from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
from typing import Iterable

from bs4 import BeautifulSoup

from treasury_intelligence.persistence.market_evidence_store import (
    MarketEvidenceRecord,
)


AFT_LATEST_AUCTIONS_URL = (
    "https://www.aft.gouv.fr/en/dernieres-adjudications"
)

AFT_SOURCE_NAME = "Agence France Tresor"

DEFAULT_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class AftBtfAuctionObservation:
    isin: str
    auction_date: str
    settlement_date: str
    maturity_date: str
    issue: str

    amount_bid_eur: Decimal
    amount_served_eur: Decimal

    marginal_rate_pct: Decimal
    bid_to_cover_ratio: Decimal
    weighted_average_rate_pct: Decimal

    source_url: str = AFT_LATEST_AUCTIONS_URL


def fetch_aft_latest_auctions_html(
    *,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> str:
    import subprocess

    command = [
        "curl",
        "-L",
        "--fail",
        "--silent",
        "--show-error",
        "--max-time",
        str(timeout_seconds),
        "-A",
        (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64)"
        ),
        AFT_LATEST_AUCTIONS_URL,
    ]

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if completed.returncode != 0:
        raise RuntimeError(
            "AFT acquisition via curl failed: "
            + completed.stderr.strip()
        )

    html = completed.stdout

    if not html.strip():
        raise RuntimeError(
            "AFT returned an empty response."
        )

    if "Just a moment..." in html:
        raise RuntimeError(
            "AFT returned a Cloudflare challenge "
            "instead of auction data."
        )

    return html


def _normalize_text(value: str) -> str:
    return " ".join(
        value.replace("\xa0", " ").split()
    )


def _parse_decimal(
    value: str,
    *,
    strip_percent: bool = False,
) -> Decimal:
    normalized = _normalize_text(value)

    if strip_percent:
        normalized = normalized.removesuffix("%")

    normalized = normalized.replace(",", "")

    return Decimal(normalized)


def _parse_date(value: str) -> str:
    parsed = datetime.strptime(
        _normalize_text(value),
        "%d/%m/%Y",
    )

    return parsed.date().isoformat()


def _row_map(table) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}

    for tr in table.find_all("tr"):
        cells = [
            _normalize_text(
                cell.get_text(
                    " ",
                    strip=True,
                )
            )
            for cell in tr.find_all(
                ["th", "td"]
            )
        ]

        if len(cells) < 2:
            continue

        label = cells[0].lower()

        rows[label] = cells[1:]

    return rows


def _find_latest_btf_table(soup: BeautifulSoup):
    heading = None

    for candidate in soup.find_all(
        ["h2", "h3", "h4"]
    ):
        text = _normalize_text(
            candidate.get_text(
                " ",
                strip=True,
            )
        ).lower()

        if "btf auctions" in text:
            heading = candidate
            break

    if heading is None:
        raise RuntimeError(
            "Could not locate AFT BTF auctions heading."
        )

    table = heading.find_next("table")

    if table is None:
        raise RuntimeError(
            "Could not locate AFT BTF auction table."
        )

    return table


def parse_latest_btf_auction(
    html: str,
) -> tuple[AftBtfAuctionObservation, ...]:
    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    table = _find_latest_btf_table(soup)

    rows = _row_map(table)

    required_rows = (
        "auction date",
        "issue",
        "settlement date",
        "maturity",
        "amount bid*",
        "amount served*",
        "marginal rate",
        "bid to cover ratio**",
        "weighted average rate",
        "isin code",
    )

    missing = [
        label
        for label in required_rows
        if label not in rows
    ]

    if missing:
        raise RuntimeError(
            "AFT BTF table is missing required rows: "
            + ", ".join(missing)
        )

    column_count = len(
        rows["isin code"]
    )

    for label in required_rows:
        if len(rows[label]) != column_count:
            raise RuntimeError(
                "AFT BTF table has inconsistent "
                f"column count for {label!r}."
            )

    observations = []

    for index in range(column_count):
        amount_bid_millions = _parse_decimal(
            rows["amount bid*"][index]
        )

        amount_served_millions = _parse_decimal(
            rows["amount served*"][index]
        )

        observation = AftBtfAuctionObservation(
            isin=rows["isin code"][index],
            auction_date=_parse_date(
                rows["auction date"][index]
            ),
            settlement_date=_parse_date(
                rows["settlement date"][index]
            ),
            maturity_date=_parse_date(
                rows["maturity"][index]
            ),
            issue=rows["issue"][index],
            amount_bid_eur=(
                amount_bid_millions
                * Decimal("1000000")
            ),
            amount_served_eur=(
                amount_served_millions
                * Decimal("1000000")
            ),
            marginal_rate_pct=_parse_decimal(
                rows["marginal rate"][index],
                strip_percent=True,
            ),
            bid_to_cover_ratio=_parse_decimal(
                rows["bid to cover ratio**"][index]
            ),
            weighted_average_rate_pct=(
                _parse_decimal(
                    rows[
                        "weighted average rate"
                    ][index],
                    strip_percent=True,
                )
            ),
        )

        observations.append(
            observation
        )

    if not observations:
        raise RuntimeError(
            "AFT BTF table produced no observations."
        )

    return tuple(observations)


def get_aft_btf_observation(
    *,
    observations: Iterable[
        AftBtfAuctionObservation
    ],
    isin: str,
) -> AftBtfAuctionObservation:
    matches = tuple(
        observation
        for observation in observations
        if observation.isin == isin
    )

    if len(matches) != 1:
        raise RuntimeError(
            "Expected exactly one AFT BTF "
            f"observation for ISIN {isin}; "
            f"found {len(matches)}."
        )

    return matches[0]


def build_aft_market_evidence_record(
    *,
    observation: AftBtfAuctionObservation,
    instrument_id: str,
    market_id: str | None,
    access_route_id: str | None,
    ingestion_run_id: str,
) -> MarketEvidenceRecord:
    evidence_key = "|".join(
        (
            "aft",
            "btf",
            observation.isin,
            observation.auction_date,
            "weighted_average_rate",
        )
    )

    evidence_hash = sha256(
        evidence_key.encode("utf-8")
    ).hexdigest()[:16]

    evidence_id = (
        "aft_btf_"
        f"{observation.isin.lower()}_"
        f"{observation.auction_date}_"
        f"{evidence_hash}"
    )

    observed_at = datetime.fromisoformat(
        observation.auction_date
    ).replace(
        tzinfo=timezone.utc
    )

    return MarketEvidenceRecord(
        evidence_id=evidence_id,
        instrument_id=instrument_id,
        market_id=market_id,
        access_route_id=access_route_id,
        evidence_type="market_return",
        observed_at=observed_at,
        measure="auction_weighted_average_rate",
        numeric_value=(
            observation.weighted_average_rate_pct
        ),
        unit="pct",
        source_reference=(
            f"aft_btf_auction_"
            f"{observation.auction_date}_"
            f"{observation.isin.lower()}"
        ),
        source_name=AFT_SOURCE_NAME,
        source_url=observation.source_url,
        ingestion_run_id=ingestion_run_id,
        raw_payload={
            "isin": observation.isin,
            "auction_date": (
                observation.auction_date
            ),
            "settlement_date": (
                observation.settlement_date
            ),
            "maturity_date": (
                observation.maturity_date
            ),
            "issue": observation.issue,
            "amount_bid_eur": str(
                observation.amount_bid_eur
            ),
            "amount_served_eur": str(
                observation.amount_served_eur
            ),
            "marginal_rate_pct": str(
                observation.marginal_rate_pct
            ),
            "bid_to_cover_ratio": str(
                observation.bid_to_cover_ratio
            ),
            "weighted_average_rate_pct": str(
                observation.weighted_average_rate_pct
            ),
        },
    )
