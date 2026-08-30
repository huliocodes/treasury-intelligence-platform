from __future__ import annotations

from dataclasses import dataclass


XETRA_SOURCE_CHECKED_ON = "2026-08-30"

XETRA_XLM_URL = (
    "https://www.cashmarket.deutsche-boerse.com/"
    "cash-en/trading/etfs-etps/"
    "xetra-liquidity-measure-etfs"
)

XETRA_2024_ETF_FACTS_URL = (
    "https://www.xetra.com/resource/blob/"
    "4270758/"
    "3c804ea03572e8630f91e7d3af7de01b/"
    "data/"
    "ETFs%20auf%20Xetra%20-%20Zahlen%20und%20"
    "Fakten%20Jahr%202024_final_en.pdf"
)


@dataclass(frozen=True)
class XetraLiquidityMeasureEvidence:
    instrument_name: str
    isin: str
    measured_order_size_eur: float
    buy_cost_bps: float
    sell_cost_bps: float
    roundtrip_cost_bps: float
    evidence_checked_on: str
    source_reference: str
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.instrument_name:
            raise ValueError(
                "Instrument name is required."
            )

        if not self.isin:
            raise ValueError(
                "ISIN is required."
            )

        if self.measured_order_size_eur <= 0:
            raise ValueError(
                "Measured order size must be "
                "greater than zero."
            )

        if self.buy_cost_bps < 0:
            raise ValueError(
                "Buy cost cannot be negative."
            )

        if self.sell_cost_bps < 0:
            raise ValueError(
                "Sell cost cannot be negative."
            )

        if self.roundtrip_cost_bps < 0:
            raise ValueError(
                "Roundtrip cost cannot be negative."
            )

        expected_roundtrip_bps = (
            self.buy_cost_bps
            + self.sell_cost_bps
        )

        if (
            abs(
                expected_roundtrip_bps
                - self.roundtrip_cost_bps
            )
            > 0.000001
        ):
            raise ValueError(
                "XLM buy and sell costs must "
                "reconcile to roundtrip cost."
            )


@dataclass(frozen=True)
class XetraAnnualTurnoverEvidence:
    instrument_name: str
    isin: str
    calendar_year: int
    annual_turnover_eur: float
    xetra_turnover_rank: int
    evidence_checked_on: str
    source_reference: str
    notes: str | None = None

    def __post_init__(self) -> None:
        if self.annual_turnover_eur <= 0:
            raise ValueError(
                "Annual turnover must be greater "
                "than zero."
            )

        if self.xetra_turnover_rank <= 0:
            raise ValueError(
                "Xetra turnover rank must be "
                "greater than zero."
            )


XEON_XETRA_XLM_100K = (
    XetraLiquidityMeasureEvidence(
        instrument_name=(
            "Xtrackers II EUR Overnight Rate "
            "Swap UCITS ETF 1C"
        ),
        isin="LU0290358497",
        measured_order_size_eur=100_000,
        buy_cost_bps=1.2,
        sell_cost_bps=1.2,
        roundtrip_cost_bps=2.4,
        evidence_checked_on=(
            XETRA_SOURCE_CHECKED_ON
        ),
        source_reference=(
            XETRA_XLM_URL
        ),
        notes=(
            "Deutsche Boerse publishes XEON 1C "
            "among Xetra Top Liquids with an XLM "
            "of 2.4 basis points roundtrip for a "
            "EUR 100,000 order, split into 1.2 "
            "basis points buy and 1.2 basis points "
            "sell. XLM measures implicit transaction "
            "costs including market impact for the "
            "specified order size. This evidence "
            "must not be extrapolated mechanically "
            "to larger position sizes."
        ),
    )
)


XEON_XETRA_2024_TURNOVER = (
    XetraAnnualTurnoverEvidence(
        instrument_name=(
            "Xtrackers II EUR Overnight Rate "
            "Swap UCITS ETF 1C"
        ),
        isin="LU0290358497",
        calendar_year=2024,
        annual_turnover_eur=5_240_000_000,
        xetra_turnover_rank=4,
        evidence_checked_on=(
            XETRA_SOURCE_CHECKED_ON
        ),
        source_reference=(
            XETRA_2024_ETF_FACTS_URL
        ),
        notes=(
            "Deutsche Boerse reported EUR 5.24 "
            "billion of Xetra turnover for XEON "
            "during 2024, ranking it fourth among "
            "ETFs by Xetra turnover that year. "
            "Historical turnover supports market-"
            "activity evidence but does not prove "
            "current executable depth for a "
            "specific order."
        ),
    )
)