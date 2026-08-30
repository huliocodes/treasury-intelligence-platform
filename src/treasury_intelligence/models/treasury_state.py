from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TreasuryPosition:
    position_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    label: str

    current_value_eur: float

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.position_id:
            raise ValueError(
                "position_id cannot be empty."
            )

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

        if self.current_value_eur <= 0:
            raise ValueError(
                "current_value_eur must be "
                "greater than zero."
            )


@dataclass(frozen=True)
class TreasuryState:
    state_id: str

    mandate_id: str
    as_of: str

    treasury_capital_eur: float

    positions: tuple[
        TreasuryPosition,
        ...
    ]

    invested_capital_eur: float
    unallocated_capital_eur: float

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.state_id:
            raise ValueError(
                "state_id cannot be empty."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id cannot be empty."
            )

        if not self.as_of:
            raise ValueError(
                "as_of cannot be empty."
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be "
                "greater than zero."
            )

        if self.invested_capital_eur < 0:
            raise ValueError(
                "invested_capital_eur cannot "
                "be negative."
            )

        if self.unallocated_capital_eur < 0:
            raise ValueError(
                "unallocated_capital_eur cannot "
                "be negative."
            )

        position_ids = [
            position.position_id
            for position in self.positions
        ]

        if len(position_ids) != len(
            set(position_ids)
        ):
            raise ValueError(
                "Treasury state contains duplicate "
                "position IDs."
            )

        calculated_invested_capital = sum(
            position.current_value_eur
            for position in self.positions
        )

        if (
            abs(
                calculated_invested_capital
                - self.invested_capital_eur
            )
            > 0.01
        ):
            raise ValueError(
                "invested_capital_eur must equal "
                "the sum of current position values."
            )

        capital_difference = abs(
            (
                self.invested_capital_eur
                + self.unallocated_capital_eur
            )
            - self.treasury_capital_eur
        )

        if capital_difference > 0.01:
            raise ValueError(
                "Invested plus unallocated capital "
                "must equal treasury capital."
            )