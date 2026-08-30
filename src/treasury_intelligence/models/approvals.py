from __future__ import annotations

from dataclasses import dataclass

from treasury_intelligence.models.portfolio_construction import (
    PortfolioAllocationLine,
)


APPROVAL_STATUSES = (
    "pending",
    "approved",
    "rejected",
)


@dataclass(frozen=True)
class ApprovalRecord:
    approval_id: str

    recommendation_id: str
    mandate_id: str

    approval_status: str

    proposed_allocation_eur: float
    authorized_allocation_eur: float

    allocation_lines: tuple[
        PortfolioAllocationLine,
        ...
    ]

    decided_by: str | None
    decided_at: str | None

    rationale: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if (
            self.approval_status
            not in APPROVAL_STATUSES
        ):
            raise ValueError(
                "Unsupported approval status: "
                f"{self.approval_status}"
            )

        if self.proposed_allocation_eur <= 0:
            raise ValueError(
                "proposed_allocation_eur must be "
                "greater than zero."
            )

        if self.authorized_allocation_eur < 0:
            raise ValueError(
                "authorized_allocation_eur cannot "
                "be negative."
            )

        if not self.allocation_lines:
            raise ValueError(
                "An approval record requires at least "
                "one proposed allocation line."
            )

        if self.approval_status == "pending":
            if self.authorized_allocation_eur != 0:
                raise ValueError(
                    "A pending approval cannot authorize "
                    "capital."
                )

            if self.decided_by is not None:
                raise ValueError(
                    "A pending approval cannot have "
                    "decided_by."
                )

            if self.decided_at is not None:
                raise ValueError(
                    "A pending approval cannot have "
                    "decided_at."
                )

        if self.approval_status == "approved":
            if (
                abs(
                    self.authorized_allocation_eur
                    - self.proposed_allocation_eur
                )
                > 0.01
            ):
                raise ValueError(
                    "An approved recommendation must "
                    "authorize the exact proposed "
                    "allocation. Partial approval requires "
                    "a revised upstream recommendation."
                )

            if not self.decided_by:
                raise ValueError(
                    "An approved record requires "
                    "decided_by."
                )

            if not self.decided_at:
                raise ValueError(
                    "An approved record requires "
                    "decided_at."
                )

        if self.approval_status == "rejected":
            if self.authorized_allocation_eur != 0:
                raise ValueError(
                    "A rejected approval cannot authorize "
                    "capital."
                )

            if not self.decided_by:
                raise ValueError(
                    "A rejected record requires "
                    "decided_by."
                )

            if not self.decided_at:
                raise ValueError(
                    "A rejected record requires "
                    "decided_at."
                )