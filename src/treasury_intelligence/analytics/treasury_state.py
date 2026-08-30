from __future__ import annotations

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryPosition,
    TreasuryState,
)


def build_treasury_state(
    state_id: str,
    mandate: TreasuryMandate,
    as_of: str,
    positions: tuple[
        TreasuryPosition,
        ...
    ],
    notes: str | None = None,
) -> TreasuryState:
    invested_capital_eur = sum(
        position.current_value_eur
        for position in positions
    )

    if (
        invested_capital_eur
        > mandate.treasury_capital_eur + 0.01
    ):
        raise ValueError(
            "Current position values exceed "
            "treasury capital."
        )

    unallocated_capital_eur = (
        mandate.treasury_capital_eur
        - invested_capital_eur
    )

    if abs(unallocated_capital_eur) <= 0.01:
        unallocated_capital_eur = 0.0

    return TreasuryState(
        state_id=state_id,
        mandate_id=mandate.mandate_id,
        as_of=as_of,
        treasury_capital_eur=(
            mandate.treasury_capital_eur
        ),
        positions=positions,
        invested_capital_eur=(
            invested_capital_eur
        ),
        unallocated_capital_eur=(
            unallocated_capital_eur
        ),
        notes=notes,
    )