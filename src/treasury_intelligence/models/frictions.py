from __future__ import annotations

from dataclasses import dataclass


FRICTION_TYPES = (
    "fund_fee",
    "broker_commission",
    "account_minimum",
    "inactivity_fee",
    "custody_fee",
    "bid_ask_spread",
    "slippage_price_impact",
    "exchange_fee",
    "clearing_fee",
    "network_fee",
    "conversion_cost",
    "other",
)


FRICTION_BASIS = (
    "annualized_pct",
    "position_bps",
    "fixed_eur",
)


FRICTION_EVIDENCE_LEVELS = (
    "observed",
    "published",
    "model_derived",
    "estimated",
    "executable",
)


@dataclass(frozen=True)
class FrictionObservation:
    observation_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    observed_at: str

    friction_type: str

    label: str

    basis: str
    value: float | None

    evidence_level: str

    source: str
    source_url: str

    position_size_eur: float | None = None

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.friction_type not in FRICTION_TYPES:
            raise ValueError(
                "Unsupported friction type: "
                f"{self.friction_type}"
            )

        if self.basis not in FRICTION_BASIS:
            raise ValueError(
                "Unsupported friction basis: "
                f"{self.basis}"
            )

        if (
            self.evidence_level
            not in FRICTION_EVIDENCE_LEVELS
        ):
            raise ValueError(
                "Unsupported friction evidence level: "
                f"{self.evidence_level}"
            )

        if (
            self.value is not None
            and self.value < 0
        ):
            raise ValueError(
                "Friction observation value cannot "
                "be negative."
            )

        if (
            self.position_size_eur is not None
            and self.position_size_eur <= 0
        ):
            raise ValueError(
                "position_size_eur must be greater "
                "than zero when provided."
            )