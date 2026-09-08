from __future__ import annotations

from datetime import datetime, timezone

from treasury_intelligence.persistence.database import (
    connect_database,
)

from treasury_intelligence.persistence.market_evidence_store import (
    insert_market_evidence,
)

from treasury_intelligence.sources.aft import (
    build_aft_market_evidence_record,
    fetch_aft_latest_auctions_html,
    get_aft_btf_observation,
    parse_latest_btf_auction,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_IBKR_ACCESS,
    BTF_2027_03_10_MARKET,
)


TARGET_ISIN = BTF_2027_03_10.isin


def main() -> None:
    if TARGET_ISIN is None:
        raise RuntimeError(
            "French March BTF ISIN is required."
        )

    html = fetch_aft_latest_auctions_html()

    observations = parse_latest_btf_auction(
        html
    )

    observation = get_aft_btf_observation(
        observations=observations,
        isin=TARGET_ISIN,
    )

    ingestion_run_id = (
        "aft_btf_"
        + datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%SZ"
        )
    )

    record = build_aft_market_evidence_record(
        observation=observation,
        instrument_id=(
            BTF_2027_03_10.instrument_id
        ),
        market_id=(
            BTF_2027_03_10_MARKET.market_id
        ),
        access_route_id=(
            BTF_2027_03_10_IBKR_ACCESS.access_route_id
        ),
        ingestion_run_id=ingestion_run_id,
    )

    with connect_database() as connection:
        inserted = insert_market_evidence(
            connection=connection,
            record=record,
        )

    print(
        "AFT BTF INGESTION"
    )

    print(
        f"ISIN:                  "
        f"{observation.isin}"
    )

    print(
        f"Auction date:          "
        f"{observation.auction_date}"
    )

    print(
        f"Maturity:              "
        f"{observation.maturity_date}"
    )

    print(
        f"Weighted avg rate:     "
        f"{observation.weighted_average_rate_pct}%"
    )

    print(
        f"Amount bid:            "
        f"EUR {observation.amount_bid_eur:,.0f}"
    )

    print(
        f"Amount served:         "
        f"EUR {observation.amount_served_eur:,.0f}"
    )

    print(
        f"Bid-to-cover:          "
        f"{observation.bid_to_cover_ratio}"
    )

    print(
        f"Evidence ID:           "
        f"{record.evidence_id}"
    )

    print(
        f"Inserted:              "
        f"{inserted}"
    )


if __name__ == "__main__":
    main()
