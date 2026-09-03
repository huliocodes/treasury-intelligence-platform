from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from treasury_intelligence.models.freshness import (
    EvidenceFreshnessType,
)


EvidenceRefreshAction = Literal[
    "refresh",
    "establish_provenance",
]

EvidenceRefreshReason = Literal[
    "stale",
    "future_dated",
    "undated",
]


@dataclass(frozen=True)
class EvidenceRefreshItem:
    refresh_item_id: str

    dependency_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    evidence_type: EvidenceFreshnessType

    source_reference: str

    observed_date: str | None
    maximum_age_days: int

    action: EvidenceRefreshAction
    reason: EvidenceRefreshReason

    age_days: int | None = None

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.refresh_item_id:
            raise ValueError(
                "refresh_item_id is required."
            )

        if not self.dependency_id:
            raise ValueError(
                "dependency_id is required."
            )

        if not self.instrument_id:
            raise ValueError(
                "instrument_id is required."
            )

        if not self.market_id:
            raise ValueError(
                "market_id is required."
            )

        if not self.access_route_id:
            raise ValueError(
                "access_route_id is required."
            )

        if not self.source_reference:
            raise ValueError(
                "source_reference is required."
            )

        if self.maximum_age_days < 0:
            raise ValueError(
                "maximum_age_days cannot be negative."
            )

        if self.reason == "undated":
            if self.observed_date is not None:
                raise ValueError(
                    "Undated refresh items cannot have "
                    "an observed_date."
                )

            if self.age_days is not None:
                raise ValueError(
                    "Undated refresh items cannot have "
                    "age_days."
                )

            if self.action != "establish_provenance":
                raise ValueError(
                    "Undated evidence must use the "
                    "establish_provenance action."
                )

        else:
            if self.observed_date is None:
                raise ValueError(
                    "Dated refresh items require an "
                    "observed_date."
                )

            if self.age_days is None:
                raise ValueError(
                    "Dated refresh items require "
                    "age_days."
                )

            if self.action != "refresh":
                raise ValueError(
                    "Stale or future-dated evidence "
                    "must use the refresh action."
                )


@dataclass(frozen=True)
class EvidenceRefreshPlan:
    plan_id: str
    as_of: str

    items: tuple[
        EvidenceRefreshItem,
        ...
    ]

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.plan_id:
            raise ValueError(
                "plan_id is required."
            )

        if not self.as_of:
            raise ValueError(
                "as_of is required."
            )

        item_ids = tuple(
            item.refresh_item_id
            for item in self.items
        )

        if len(set(item_ids)) != len(item_ids):
            raise ValueError(
                "Refresh item IDs must be unique."
            )

    @property
    def actionable_count(self) -> int:
        return len(self.items)

    @property
    def stale_count(self) -> int:
        return sum(
            item.reason == "stale"
            for item in self.items
        )

    @property
    def future_dated_count(self) -> int:
        return sum(
            item.reason == "future_dated"
            for item in self.items
        )

    @property
    def undated_count(self) -> int:
        return sum(
            item.reason == "undated"
            for item in self.items
        )

    @property
    def refresh_count(self) -> int:
        return sum(
            item.action == "refresh"
            for item in self.items
        )

    @property
    def establish_provenance_count(
        self,
    ) -> int:
        return sum(
            item.action == "establish_provenance"
            for item in self.items
        )
