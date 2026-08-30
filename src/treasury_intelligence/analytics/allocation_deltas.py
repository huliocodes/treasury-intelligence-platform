from __future__ import annotations

from collections import defaultdict

from treasury_intelligence.models.allocation_deltas import (
    AllocationDeltaLine,
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.portfolio_proposals import (
    PortfolioProposal,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryState,
)


PositionKey = tuple[
    str,
    str,
    str,
]


def _position_key(
    instrument_id: str,
    market_id: str,
    access_route_id: str,
) -> PositionKey:
    return (
        instrument_id,
        market_id,
        access_route_id,
    )


def _classify_action(
    current_value_eur: float,
    proposed_value_eur: float,
) -> str:
    tolerance = 0.01

    if (
        current_value_eur <= tolerance
        and proposed_value_eur > tolerance
    ):
        return "open"

    if (
        current_value_eur > tolerance
        and proposed_value_eur <= tolerance
    ):
        return "close"

    delta_eur = (
        proposed_value_eur
        - current_value_eur
    )

    if delta_eur > tolerance:
        return "increase"

    if delta_eur < -tolerance:
        return "decrease"

    return "unchanged"


def _current_allocations(
    state: TreasuryState,
) -> tuple[
    dict[PositionKey, float],
    dict[PositionKey, str],
]:
    values: dict[
        PositionKey,
        float,
    ] = defaultdict(float)

    labels: dict[
        PositionKey,
        str,
    ] = {}

    for position in state.positions:
        key = _position_key(
            instrument_id=(
                position.instrument_id
            ),
            market_id=(
                position.market_id
            ),
            access_route_id=(
                position.access_route_id
            ),
        )

        values[key] += (
            position.current_value_eur
        )

        if key not in labels:
            labels[key] = position.label

    return (
        dict(values),
        labels,
    )


def _proposal_allocations(
    proposal: PortfolioProposal,
) -> tuple[
    dict[PositionKey, float],
    dict[PositionKey, str],
]:
    values: dict[
        PositionKey,
        float,
    ] = defaultdict(float)

    labels: dict[
        PositionKey,
        str,
    ] = {}

    for line in proposal.allocation_lines:
        key = _position_key(
            instrument_id=(
                line.instrument_id
            ),
            market_id=(
                line.market_id
            ),
            access_route_id=(
                line.access_route_id
            ),
        )

        values[key] += (
            line.allocation_eur
        )

        labels[key] = line.label

    return (
        dict(values),
        labels,
    )


def build_treasury_allocation_delta(
    delta_id: str,
    state: TreasuryState,
    proposal: PortfolioProposal,
    notes: str | None = None,
) -> TreasuryAllocationDelta:
    if (
        state.mandate_id
        != proposal.mandate_id
    ):
        raise ValueError(
            "Treasury state and portfolio proposal "
            "must use the same mandate."
        )

    if (
        abs(
            state.treasury_capital_eur
            - proposal.treasury_capital_eur
        )
        > 0.01
    ):
        raise ValueError(
            "Treasury state and portfolio proposal "
            "must use the same treasury capital."
        )

    (
        current_values,
        current_labels,
    ) = _current_allocations(
        state
    )

    if proposal.proposal_status in (
        "no_actionable_allocation",
        "no_allocation_proposed",
    ):
        proposed_values = dict(
            current_values
        )

        proposed_labels = dict(
            current_labels
        )

        proposed_invested_capital_eur = (
            state.invested_capital_eur
        )

        proposed_unallocated_capital_eur = (
            state.unallocated_capital_eur
        )

    elif (
        proposal.proposal_status
        == "allocation_proposed"
    ):
        (
            proposed_values,
            proposed_labels,
        ) = _proposal_allocations(
            proposal
        )

        proposed_invested_capital_eur = (
            proposal.allocated_capital_eur
        )

        proposed_unallocated_capital_eur = (
            proposal.unallocated_capital_eur
        )

    else:
        raise ValueError(
            "Unsupported portfolio proposal status: "
            f"{proposal.proposal_status}"
        )

    all_keys = sorted(
        set(current_values)
        | set(proposed_values)
    )

    delta_lines: list[
        AllocationDeltaLine
    ] = []

    for key in all_keys:
        current_value_eur = (
            current_values.get(
                key,
                0.0,
            )
        )

        proposed_value_eur = (
            proposed_values.get(
                key,
                0.0,
            )
        )

        delta_eur = (
            proposed_value_eur
            - current_value_eur
        )

        label = (
            proposed_labels.get(key)
            or current_labels.get(key)
            or key[0]
        )

        delta_lines.append(
            AllocationDeltaLine(
                instrument_id=key[0],
                market_id=key[1],
                access_route_id=key[2],
                label=label,
                current_value_eur=(
                    current_value_eur
                ),
                proposed_value_eur=(
                    proposed_value_eur
                ),
                delta_eur=delta_eur,
                action=_classify_action(
                    current_value_eur=(
                        current_value_eur
                    ),
                    proposed_value_eur=(
                        proposed_value_eur
                    ),
                ),
            )
        )

    gross_position_movement_eur = sum(
        abs(line.delta_eur)
        for line in delta_lines
    )

    change_required = any(
        abs(line.delta_eur) > 0.01
        for line in delta_lines
    )

    return TreasuryAllocationDelta(
        delta_id=delta_id,
        mandate_id=state.mandate_id,
        state_id=state.state_id,
        proposal_id=proposal.proposal_id,
        treasury_capital_eur=(
            state.treasury_capital_eur
        ),
        current_invested_capital_eur=(
            state.invested_capital_eur
        ),
        proposed_invested_capital_eur=(
            proposed_invested_capital_eur
        ),
        current_unallocated_capital_eur=(
            state.unallocated_capital_eur
        ),
        proposed_unallocated_capital_eur=(
            proposed_unallocated_capital_eur
        ),
        gross_position_movement_eur=(
            gross_position_movement_eur
        ),
        change_required=change_required,
        delta_lines=tuple(
            delta_lines
        ),
        notes=notes,
    )