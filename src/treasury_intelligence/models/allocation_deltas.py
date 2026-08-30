from __future__ import annotations

from dataclasses import dataclass


ALLOCATION_DELTA_ACTIONS = (
    "open",
    "increase",
    "decrease",
    "close",
    "unchanged",
)


@dataclass(frozen=True)
class AllocationDeltaLine:
    instrument_id: str
    market_id: str
    access_route_id: str

    label: str

    current_value_eur: float
    proposed_value_eur: float
    delta_eur: float

    action: str

    def __post_init__(self) -> None:
        if not self.instrument_id:
            raise ValueError(
                "instrument_id cannot be empty."
            )

        if not self.market_id:
            raise ValueError(
                "market_id cannot be empty."
            )

        if not self.access_route_id:
            raise ValueError(
                "access_route_id cannot be empty."
            )

        if not self.label:
            raise ValueError(
                "label cannot be empty."
            )

        if self.current_value_eur < 0:
            raise ValueError(
                "current_value_eur cannot be negative."
            )

        if self.proposed_value_eur < 0:
            raise ValueError(
                "proposed_value_eur cannot be negative."
            )

        expected_delta = (
            self.proposed_value_eur
            - self.current_value_eur
        )

        if abs(expected_delta - self.delta_eur) > 0.01:
            raise ValueError(
                "delta_eur must equal proposed value "
                "minus current value."
            )

        if self.action not in ALLOCATION_DELTA_ACTIONS:
            raise ValueError(
                "Unsupported allocation delta action: "
                f"{self.action}"
            )


@dataclass(frozen=True)
class TreasuryAllocationDelta:
    delta_id: str

    mandate_id: str
    state_id: str
    proposal_id: str

    treasury_capital_eur: float

    current_invested_capital_eur: float
    proposed_invested_capital_eur: float

    current_unallocated_capital_eur: float
    proposed_unallocated_capital_eur: float

    gross_position_movement_eur: float

    change_required: bool

    delta_lines: tuple[
        AllocationDeltaLine,
        ...
    ]

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.delta_id:
            raise ValueError(
                "delta_id cannot be empty."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id cannot be empty."
            )

        if not self.state_id:
            raise ValueError(
                "state_id cannot be empty."
            )

        if not self.proposal_id:
            raise ValueError(
                "proposal_id cannot be empty."
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be "
                "greater than zero."
            )

        if self.current_invested_capital_eur < 0:
            raise ValueError(
                "current_invested_capital_eur cannot "
                "be negative."
            )

        if self.proposed_invested_capital_eur < 0:
            raise ValueError(
                "proposed_invested_capital_eur cannot "
                "be negative."
            )

        if self.current_unallocated_capital_eur < 0:
            raise ValueError(
                "current_unallocated_capital_eur cannot "
                "be negative."
            )

        if self.proposed_unallocated_capital_eur < 0:
            raise ValueError(
                "proposed_unallocated_capital_eur cannot "
                "be negative."
            )

        if self.gross_position_movement_eur < 0:
            raise ValueError(
                "gross_position_movement_eur cannot "
                "be negative."
            )

        current_difference = abs(
            (
                self.current_invested_capital_eur
                + self.current_unallocated_capital_eur
            )
            - self.treasury_capital_eur
        )

        if current_difference > 0.01:
            raise ValueError(
                "Current invested plus unallocated "
                "capital must equal treasury capital."
            )

        proposed_difference = abs(
            (
                self.proposed_invested_capital_eur
                + self.proposed_unallocated_capital_eur
            )
            - self.treasury_capital_eur
        )

        if proposed_difference > 0.01:
            raise ValueError(
                "Proposed invested plus unallocated "
                "capital must equal treasury capital."
            )

        calculated_movement = sum(
            abs(line.delta_eur)
            for line in self.delta_lines
        )

        if (
            abs(
                calculated_movement
                - self.gross_position_movement_eur
            )
            > 0.01
        ):
            raise ValueError(
                "gross_position_movement_eur must equal "
                "the sum of absolute position deltas."
            )

        calculated_change_required = any(
            abs(line.delta_eur) > 0.01
            for line in self.delta_lines
        )

        if (
            calculated_change_required
            != self.change_required
        ):
            raise ValueError(
                "change_required does not match the "
                "position deltas."
            )