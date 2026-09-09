from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from html import unescape
import re

import requests

from treasury_intelligence.persistence.market_evidence_store import (
    MarketEvidenceRecord,
)

from treasury_intelligence.models.opportunities import (
    Accessibility,
    AccessRoute,
    Instrument,
    Market,
    MarketObservation,
    OpportunitySnapshot,
)


ERNX_INSTRUMENT = Instrument(
    instrument_id="ernx",
    provider="iShares / BlackRock",
    name="iShares € Ultrashort Bond UCITS ETF",
    instrument_type="ultrashort_ig_bond_etf",
    legal_structure="UCITS ETF",
    currency="EUR",
    yield_source="investment_grade_short_credit",
    isin="IE000RHYOR04",
    replication="physical_sampling",
    income_treatment="accumulating",
)


ERNX_MARKET = Market(
    market_id="ernx_xetra",
    instrument_id=ERNX_INSTRUMENT.instrument_id,
    venue="Xetra",
    venue_type="exchange",
    trading_currency="EUR",
    ticker="ERNX",
    settlement_cycle="T+2",
)


ERNX_IBKR_ACCESS = AccessRoute(
    access_route_id="ernx_xetra_ibkr",
    market_id=ERNX_MARKET.market_id,
    provider="Interactive Brokers",
    route_type="self_directed_brokerage",
    investor_type="corporate",
    jurisdiction="Slovenia",
)


ERNX_SOURCE_URL = (
    "https://www.ishares.com/uk/individual/en/"
    "products/327355/"
    "ishares-ultrashort-bond-ucits-etf"
)


@dataclass(frozen=True)
class ErnxReturnObservation:
    observed_at: datetime
    weighted_average_ytm_pct: float
    source_url: str

    def __post_init__(self) -> None:
        if self.observed_at.tzinfo is None:
            raise ValueError(
                "observed_at must be timezone-aware."
            )

        if self.weighted_average_ytm_pct <= 0:
            raise ValueError(
                "weighted_average_ytm_pct must be "
                "greater than zero."
            )


def fetch_ernx_return_observation(
) -> ErnxReturnObservation:
    response = requests.get(
        ERNX_SOURCE_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/140 Safari/537.36"
            ),
            "Accept-Language": (
                "en-GB,en;q=0.9"
            ),
        },
        timeout=30,
    )

    response.raise_for_status()

    html = unescape(
        response.text
    )

    match = re.search(
        (
            r'"yieldToWorst":\{'
            r'.*?'
            r'"asOfDate":(?P<date>\d{8})'
            r'.*?'
            r'"formattedValue":'
            r'"(?P<formatted>[0-9.]+)%"'
            r'.*?'
            r'"value":(?P<value>[0-9.]+)'
        ),
        html,
        flags=re.DOTALL,
    )

    if match is None:
        raise RuntimeError(
            "Unable to locate ERNX Weighted Average "
            "YTM in the iShares product page."
        )

    observed_at = datetime.strptime(
        match.group("date"),
        "%Y%m%d",
    ).replace(
        tzinfo=timezone.utc
    )

    formatted_value = float(
        match.group("formatted")
    )

    numeric_value = float(
        match.group("value")
    )

    if (
        abs(
            formatted_value
            - numeric_value
        )
        > 1e-9
    ):
        raise RuntimeError(
            "ERNX formatted and numeric YTM values "
            "do not match."
        )

    return ErnxReturnObservation(
        observed_at=observed_at,
        weighted_average_ytm_pct=(
            numeric_value
        ),
        source_url=ERNX_SOURCE_URL,
    )


def build_ernx_market_evidence_record(
    *,
    observation: ErnxReturnObservation,
    ingestion_run_id: str,
) -> MarketEvidenceRecord:
    observed_date = (
        observation.observed_at
        .date()
        .isoformat()
    )

    return MarketEvidenceRecord(
        evidence_id=(
            "ernx_weighted_average_ytm_"
            f"{observed_date}"
        ),
        instrument_id=(
            ERNX_INSTRUMENT.instrument_id
        ),
        market_id=ERNX_MARKET.market_id,
        access_route_id=(
            ERNX_IBKR_ACCESS.access_route_id
        ),
        evidence_type="market_return",
        observed_at=observation.observed_at,
        measure="weighted_average_ytm",
        numeric_value=Decimal(
            str(
                observation
                .weighted_average_ytm_pct
            )
        ),
        unit="pct",
        source_reference=(
            "ishares_ernx_weighted_average_ytm"
        ),
        source_name="iShares / BlackRock",
        source_url=observation.source_url,
        ingestion_run_id=ingestion_run_id,
        raw_payload={
            "ticker": "ERNX",
            "measure_label": (
                "Weighted Average YTM"
            ),
            "reference_yield_includes_product_fee": (
                False
            ),
            "observed_date": observed_date,
            "weighted_average_ytm_pct": (
                observation
                .weighted_average_ytm_pct
            ),
        },
    )


ERNX_ACCESSIBILITY = Accessibility(
    access_route_id=ERNX_IBKR_ACCESS.access_route_id,
    entity_type="Slovenian d.o.o.",
    jurisdiction="Slovenia",
    technical_access="yes",
    corporate_operational_access="supported",
    status="eligible_v1",
    evidence_level="supported_route",
    notes=(
        "IBKR supports Slovenian organization accounts "
        "and Xetra ETF trading. Account-specific trading "
        "permissions remain an execution-stage operational "
        "check rather than a V1 accessibility blocker."
    ),
)


def get_ernx_snapshot() -> OpportunitySnapshot:
    return OpportunitySnapshot(
        snapshot_id="ernx_xetra_ibkr_2026-08-28",
        instrument_id=ERNX_INSTRUMENT.instrument_id,
        market_id=ERNX_MARKET.market_id,
        access_route_id=ERNX_IBKR_ACCESS.access_route_id,
        observed_date="2026-08-28",
        yield_measure="weighted_average_ytm",
        yield_value_pct=2.91,
        yield_basis=(
            "Portfolio weighted average yield to maturity; "
            "published separately from the fund TER and "
            "not guaranteed realized return"
        ),
        annual_fee_pct=0.09,
        duration_years=0.36,
        average_maturity_years=0.62,
        fund_aum_eur=6_132_789_997.0,
        share_class_aum_eur=2_795_682_028.0,
        holdings_count=671,
        source="iShares / BlackRock",
        source_url=(
            "https://www.ishares.com/uk/individual/en/"
            "products/327355/"
            "ishares-ultrashort-bond-ucits-etf"
        ),
        notes=(
            "BlackRock reported Weighted Average YTM "
            "of 2.91% and TER of 0.09% separately as of "
            "28 Aug 2026. The model therefore treats the "
            "YTM as pre-product-fee and deducts the TER."
        ),
    )


def get_ernx_market_observation() -> MarketObservation:
    last_price = 5.605
    daily_volume_units = 265_072

    daily_turnover_eur = (
        last_price
        * daily_volume_units
    )

    return MarketObservation(
        observation_id=(
            "ernx_xetra_2026_08_21_market_activity"
        ),
        instrument_id=ERNX_INSTRUMENT.instrument_id,
        market_id=ERNX_MARKET.market_id,
        observed_at="2026-08-21",
        observation_type=(
            "delayed_public_market_activity"
        ),
        last_price=last_price,
        daily_volume_units=daily_volume_units,
        daily_turnover_eur=daily_turnover_eur,
        source="MarketScreener",
        source_url=(
            "https://www.marketscreener.com/quote/etf/"
            "ISHARES-ULTRASHORT-BOND-U-137131876/"
        ),
        notes=(
            "Delayed Xetra market observation. Daily volume "
            "is market-activity evidence only and does not "
            "by itself establish immediate executable depth "
            "for a proposed position."
        ),
    )
