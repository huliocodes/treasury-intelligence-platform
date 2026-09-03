from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from treasury_intelligence.models.freshness import (
    EvidenceFreshnessType,
)


FreshnessDependencyDateStatus = Literal[
    "dated",
    "undated",
]


@dataclass(frozen=True)
class EvidenceFreshnessDependency:
    dependency_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    evidence_type: EvidenceFreshnessType

    source_reference: str

    observed_date: str | None

    required_for_recommendation: bool

    notes: str | None = None

    def __post_init__(self) -> None:
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

        if (
            self.observed_date is not None
            and not self.observed_date
        ):
            raise ValueError(
                "observed_date cannot be empty."
            )

    @property
    def date_status(
        self,
    ) -> FreshnessDependencyDateStatus:
        if self.observed_date is None:
            return "undated"

        return "dated"


@dataclass(frozen=True)
class OpportunityFreshnessDependencies:
    instrument_id: str
    market_id: str
    access_route_id: str

    dependencies: tuple[
        EvidenceFreshnessDependency,
        ...
    ]

    def __post_init__(self) -> None:
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

        if not self.dependencies:
            raise ValueError(
                "At least one freshness dependency "
                "is required."
            )

        dependency_ids = tuple(
            dependency.dependency_id
            for dependency in self.dependencies
        )

        if len(set(dependency_ids)) != len(
            dependency_ids
        ):
            raise ValueError(
                "Freshness dependency IDs must be "
                "unique."
            )

        for dependency in self.dependencies:
            if (
                dependency.instrument_id
                != self.instrument_id
            ):
                raise ValueError(
                    "Dependency instrument does not "
                    "match dependency set."
                )

            if (
                dependency.market_id
                != self.market_id
            ):
                raise ValueError(
                    "Dependency market does not match "
                    "dependency set."
                )

            if (
                dependency.access_route_id
                != self.access_route_id
            ):
                raise ValueError(
                    "Dependency access route does not "
                    "match dependency set."
                )

    @property
    def required_dependencies(
        self,
    ) -> tuple[
        EvidenceFreshnessDependency,
        ...
    ]:
        return tuple(
            dependency
            for dependency in self.dependencies
            if dependency.required_for_recommendation
        )

    @property
    def undated_required_dependencies(
        self,
    ) -> tuple[
        EvidenceFreshnessDependency,
        ...
    ]:
        return tuple(
            dependency
            for dependency
            in self.required_dependencies
            if dependency.observed_date is None
        )
