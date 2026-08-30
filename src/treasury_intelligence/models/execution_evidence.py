from __future__ import annotations

from dataclasses import dataclass


EXECUTION_EVIDENCE_STATUSES = (
    "supported",
    "insufficient",
    "unavailable",
)


@dataclass(frozen=True)
class PositionExecutionEvidence:
    assessment_id: str
    instrument_id: str
    market_id: str
    position_size_eur: float

    reference_order_size_eur: float | None
    position_to_reference_size_multiple: float | None

    observed_roundtrip_cost_bps: float | None
    observed_buy_cost_bps: float | None
    observed_sell_cost_bps: float | None

    position_sized_cost_supported: bool
    execution_evidence_status: str

    market_activity_supported: bool
    immediate_exit_supported: bool | None

    evidence_requirements: tuple[str, ...]

    source_references: tuple[str, ...]
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.assessment_id:
            raise ValueError(
                "Execution evidence assessment ID "
                "is required."
            )

        if not self.instrument_id:
            raise ValueError(
                "Instrument ID is required."
            )

        if not self.market_id:
            raise ValueError(
                "Market ID is required."
            )

        if self.position_size_eur <= 0:
            raise ValueError(
                "Position size must be greater "
                "than zero."
            )

        if (
            self.execution_evidence_status
            not in EXECUTION_EVIDENCE_STATUSES
        ):
            raise ValueError(
                "Unsupported execution evidence "
                "status: "
                f"{self.execution_evidence_status}"
            )

        if (
            self.reference_order_size_eur
            is not None
            and self.reference_order_size_eur <= 0
        ):
            raise ValueError(
                "Reference order size must be "
                "greater than zero."
            )

        if (
            self.position_to_reference_size_multiple
            is not None
            and self.position_to_reference_size_multiple
            <= 0
        ):
            raise ValueError(
                "Position-to-reference multiple "
                "must be greater than zero."
            )

        cost_values = (
            self.observed_roundtrip_cost_bps,
            self.observed_buy_cost_bps,
            self.observed_sell_cost_bps,
        )

        for cost in cost_values:
            if cost is not None and cost < 0:
                raise ValueError(
                    "Observed execution costs "
                    "cannot be negative."
                )

        if self.position_sized_cost_supported:
            if (
                self.observed_roundtrip_cost_bps
                is None
            ):
                raise ValueError(
                    "Supported position-sized "
                    "execution cost requires a "
                    "roundtrip cost."
                )

            if (
                self.execution_evidence_status
                != "supported"
            ):
                raise ValueError(
                    "Position-sized execution cost "
                    "cannot be supported while the "
                    "overall evidence status is not "
                    "supported."
                )

            if self.evidence_requirements:
                raise ValueError(
                    "Supported execution evidence "
                    "cannot contain unresolved "
                    "evidence requirements."
                )

        if (
            self.execution_evidence_status
            == "insufficient"
        ):
            if self.position_sized_cost_supported:
                raise ValueError(
                    "Insufficient execution evidence "
                    "cannot support a position-sized "
                    "cost."
                )

            if not self.evidence_requirements:
                raise ValueError(
                    "Insufficient execution evidence "
                    "requires at least one evidence "
                    "requirement."
                )