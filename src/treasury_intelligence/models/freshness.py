from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


EvidenceFreshnessType = Literal[
    "market_return",
    "market_liquidity",
    "benchmark",
    "risk",
    "accessibility",
    "cost",
]

FreshnessStatus = Literal[
    "fresh",
    "stale",
    "future_dated",
]


@dataclass(frozen=True)
class EvidenceFreshnessRequirement:
    evidence_type: EvidenceFreshnessType
    maximum_age_days: int

    def __post_init__(self) -> None:
        if self.maximum_age_days < 0:
            raise ValueError(
                "maximum_age_days cannot be negative."
            )


@dataclass(frozen=True)
class EvidenceFreshnessAssessment:
    evidence_type: EvidenceFreshnessType
    observed_date: str
    as_of: str
    age_days: int
    maximum_age_days: int
    status: FreshnessStatus

    @property
    def usable(self) -> bool:
        return self.status == "fresh"
