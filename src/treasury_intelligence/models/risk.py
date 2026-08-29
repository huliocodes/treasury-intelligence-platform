from __future__ import annotations

from dataclasses import dataclass


RISK_DIMENSIONS = (
    "principal_credit",
    "market",
    "liquidity",
    "currency_asset",
    "structural_counterparty",
    "technical",
    "operational_regulatory",
)


@dataclass(frozen=True)
class RiskObservation:
    observation_id: str

    instrument_id: str
    market_id: str

    observed_at: str

    risk_dimension: str
    observation_type: str

    value_text: str | None = None
    value_numeric: float | None = None
    unit: str | None = None

    position_size_eur: float | None = None

    evidence_level: str = "observed"

    source: str | None = None
    source_url: str | None = None

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.risk_dimension not in RISK_DIMENSIONS:
            raise ValueError(
                f"Unsupported risk dimension: "
                f"{self.risk_dimension}"
            )

        if (
            self.value_text is None
            and self.value_numeric is None
        ):
            raise ValueError(
                "RiskObservation requires value_text "
                "or value_numeric."
            )