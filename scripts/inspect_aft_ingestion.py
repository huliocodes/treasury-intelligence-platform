from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from treasury_intelligence.persistence.database import (
    connect_database,
)

from treasury_intelligence.persistence.market_evidence_store import (
    get_latest_market_evidence,
)

from treasury_intelligence.sources.aft import (
    fetch_aft_latest_auctions_html,
    get_aft_btf_observation,
    parse_latest_btf_auction,
)


TARGET_ISIN = "FR0129704153"


def main() -> None:
    html = fetch_aft_latest_auctions_html()

    observations = parse_latest_btf_auction(
        html
    )

    observation = get_aft_btf_observation(
        observations=observations,
        isin=TARGET_ISIN,
    )

    print(
        "MILESTONE 16A.3 — LIVE AFT INGESTION"
    )

    print()

    print(
        "Parsed BTF observations:       ",
        len(observations),
    )

    print(
        "Target ISIN:                   ",
        observation.isin,
    )

    print(
        "Auction date:                  ",
        observation.auction_date,
    )

    print(
        "Settlement date:               ",
        observation.settlement_date,
    )

    print(
        "Maturity date:                 ",
        observation.maturity_date,
    )

    print(
        "Weighted-average rate:         ",
        observation.weighted_average_rate_pct,
    )

    print(
        "Amount bid EUR:                ",
        observation.amount_bid_eur,
    )

    print(
        "Amount served EUR:             ",
        observation.amount_served_eur,
    )

    print(
        "Bid-to-cover:                  ",
        observation.bid_to_cover_ratio,
    )

    assert len(observations) >= 4

    assert observation.isin == TARGET_ISIN

    assert (
        observation.auction_date
        == "2026-09-07"
    )

    assert (
        observation.settlement_date
        == "2026-09-09"
    )

    assert (
        observation.maturity_date
        == "2027-03-10"
    )

    assert (
        observation.weighted_average_rate_pct
        == Decimal("2.720")
    )

    assert (
        observation.amount_bid_eur
        == Decimal("8290000000")
    )

    assert (
        observation.amount_served_eur
        == Decimal("1600000000")
    )

    assert (
        observation.bid_to_cover_ratio
        == Decimal("5.18")
    )

    with connect_database() as connection:
        latest = get_latest_market_evidence(
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

    assert latest is not None

    print()

    print(
        "Persisted evidence ID:         ",
        latest["evidence_id"],
    )

    print(
        "Persisted observed_at:         ",
        latest["observed_at"],
    )

    print(
        "Persisted rate:                ",
        latest["numeric_value"],
    )

    assert (
        latest["numeric_value"]
        == Decimal("2.720")
    )

    assert (
        latest["observed_at"].date().isoformat()
        == "2026-09-07"
    )

    print()

    print(
        "Live AFT acquisition:          yes"
    )

    print(
        "Structured BTF parsing:        yes"
    )

    print(
        "Normalized evidence:           yes"
    )

    print(
        "PostgreSQL persistence:        yes"
    )

    print(
        "Append-only evidence store reused: yes"
    )

    print()

    print(
        "All Milestone 16A.3 assertions passed."
    )


if __name__ == "__main__":
    main()
