from __future__ import annotations

from collections import defaultdict

from treasury_intelligence.models.allocation_deltas import (
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.economic_comparisons import (
    AllocationReturnInput,
    EconomicComparisonLine,
    TreasuryEconomicComparison,
    UnallocatedReturnInput,
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


def _build_return_map(
    inputs: tuple[
        AllocationReturnInput,
        ...
    ],
) -> dict[
    PositionKey,
    AllocationReturnInput,
]:
    result: dict[
        PositionKey,
        AllocationReturnInput,
    ] = {}

    for item in inputs:
        key = _position_key(
            instrument_id=item.instrument_id,
            market_id=item.market_id,
            access_route_id=item.access_route_id,
        )

        if key in result:
            raise ValueError(
                "Duplicate allocation return input for "
                f"{key}."
            )

        result[key] = item

    return result


def _annual_return_eur(
    value_eur: float,
    annual_return_pct: float,
) -> float:
    return (
        value_eur
        * annual_return_pct
        / 100.0
    )


def _current_position_values(
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


def _proposed_position_values(
    state: TreasuryState,
    proposal: PortfolioProposal,
) -> tuple[
    dict[PositionKey, float],
    dict[PositionKey, str],
]:
    if proposal.proposal_status in (
        "no_actionable_allocation",
        "no_allocation_proposed",
    ):
        return _current_position_values(
            state
        )

    if (
        proposal.proposal_status
        != "allocation_proposed"
    ):
        raise ValueError(
            "Unsupported portfolio proposal status: "
            f"{proposal.proposal_status}"
        )

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
            instrument_id=line.instrument_id,
            market_id=line.market_id,
            access_route_id=line.access_route_id,
        )

        values[key] += line.allocation_eur
        labels[key] = line.label

    return (
        dict(values),
        labels,
    )


def _build_position_lines(
    side: str,
    values: dict[
        PositionKey,
        float,
    ],
    labels: dict[
        PositionKey,
        str,
    ],
    return_map: dict[
        PositionKey,
        AllocationReturnInput,
    ],
    missing_evidence: list[str],
) -> tuple[
    EconomicComparisonLine,
    ...
]:
    lines: list[
        EconomicComparisonLine
    ] = []

    for key in sorted(values):
        value_eur = values[key]

        if value_eur <= 0.01:
            continue

        return_input = return_map.get(
            key
        )

        if return_input is None:
            missing_evidence.append(
                f"{side} return evidence missing for "
                f"{labels.get(key, key[0])}."
            )

            lines.append(
                EconomicComparisonLine(
                    side=side,
                    allocation_type="position",
                    label=labels.get(
                        key,
                        key[0],
                    ),
                    value_eur=value_eur,
                    annual_return_pct=None,
                    annual_return_eur=None,
                    evidence_available=False,
                    instrument_id=key[0],
                    market_id=key[1],
                    access_route_id=key[2],
                    notes=(
                        "No defensible annual return "
                        "input supplied."
                    ),
                )
            )

            continue

        if not return_input.evidence_available:
            missing_evidence.append(
                f"{side} return evidence unavailable "
                f"for {return_input.label}."
            )

            lines.append(
                EconomicComparisonLine(
                    side=side,
                    allocation_type="position",
                    label=return_input.label,
                    value_eur=value_eur,
                    annual_return_pct=None,
                    annual_return_eur=None,
                    evidence_available=False,
                    instrument_id=key[0],
                    market_id=key[1],
                    access_route_id=key[2],
                    notes=(
                        return_input.notes
                    ),
                )
            )

            continue

        annual_return_pct = (
            return_input.annual_return_pct
        )

        if annual_return_pct is None:
            raise AssertionError(
                "Available return input unexpectedly "
                "contains no annual return."
            )

        lines.append(
            EconomicComparisonLine(
                side=side,
                allocation_type="position",
                label=return_input.label,
                value_eur=value_eur,
                annual_return_pct=(
                    annual_return_pct
                ),
                annual_return_eur=(
                    _annual_return_eur(
                        value_eur=(
                            value_eur
                        ),
                        annual_return_pct=(
                            annual_return_pct
                        ),
                    )
                ),
                evidence_available=True,
                instrument_id=key[0],
                market_id=key[1],
                access_route_id=key[2],
                notes=(
                    return_input.notes
                ),
            )
        )

    return tuple(
        lines
    )


def _build_unallocated_line(
    side: str,
    value_eur: float,
    return_input: UnallocatedReturnInput,
    missing_evidence: list[str],
) -> EconomicComparisonLine | None:
    if value_eur <= 0.01:
        return None

    if not return_input.evidence_available:
        missing_evidence.append(
            f"{side} return evidence unavailable for "
            "unallocated treasury capital."
        )

        return EconomicComparisonLine(
            side=side,
            allocation_type="unallocated",
            label="UNALLOCATED TREASURY",
            value_eur=value_eur,
            annual_return_pct=None,
            annual_return_eur=None,
            evidence_available=False,
            notes=return_input.notes,
        )

    annual_return_pct = (
        return_input.annual_return_pct
    )

    if annual_return_pct is None:
        raise AssertionError(
            "Available unallocated return input "
            "unexpectedly contains no annual return."
        )

    return EconomicComparisonLine(
        side=side,
        allocation_type="unallocated",
        label="UNALLOCATED TREASURY",
        value_eur=value_eur,
        annual_return_pct=annual_return_pct,
        annual_return_eur=(
            _annual_return_eur(
                value_eur=value_eur,
                annual_return_pct=(
                    annual_return_pct
                ),
            )
        ),
        evidence_available=True,
        notes=return_input.notes,
    )


def _sum_annual_returns(
    lines: tuple[
        EconomicComparisonLine,
        ...
    ],
) -> float | None:
    if any(
        not line.evidence_available
        for line in lines
    ):
        return None

    return sum(
        line.annual_return_eur or 0.0
        for line in lines
    )


def build_treasury_economic_comparison(
    comparison_id: str,
    state: TreasuryState,
    proposal: PortfolioProposal,
    delta: TreasuryAllocationDelta,
    current_position_returns: tuple[
        AllocationReturnInput,
        ...
    ],
    proposed_position_returns: tuple[
        AllocationReturnInput,
        ...
    ],
    current_unallocated_return: (
        UnallocatedReturnInput
    ),
    proposed_unallocated_return: (
        UnallocatedReturnInput
    ),
    notes: str | None = None,
) -> TreasuryEconomicComparison:
    if (
        state.mandate_id
        != proposal.mandate_id
        or state.mandate_id
        != delta.mandate_id
    ):
        raise ValueError(
            "Treasury state, proposal and delta must "
            "use the same mandate."
        )

    if (
        state.state_id
        != delta.state_id
    ):
        raise ValueError(
            "Allocation delta does not belong to the "
            "supplied treasury state."
        )

    if (
        proposal.proposal_id
        != delta.proposal_id
    ):
        raise ValueError(
            "Allocation delta does not belong to the "
            "supplied portfolio proposal."
        )

    if (
        abs(
            state.treasury_capital_eur
            - proposal.treasury_capital_eur
        )
        > 0.01
    ):
        raise ValueError(
            "Treasury state and proposal must use "
            "the same treasury capital."
        )

    current_return_map = (
        _build_return_map(
            current_position_returns
        )
    )

    proposed_return_map = (
        _build_return_map(
            proposed_position_returns
        )
    )

    (
        current_values,
        current_labels,
    ) = _current_position_values(
        state
    )

    (
        proposed_values,
        proposed_labels,
    ) = _proposed_position_values(
        state=state,
        proposal=proposal,
    )

    missing_evidence: list[str] = []

    current_position_lines = (
        _build_position_lines(
            side="current",
            values=current_values,
            labels=current_labels,
            return_map=current_return_map,
            missing_evidence=(
                missing_evidence
            ),
        )
    )

    proposed_position_lines = (
        _build_position_lines(
            side="proposed",
            values=proposed_values,
            labels=proposed_labels,
            return_map=proposed_return_map,
            missing_evidence=(
                missing_evidence
            ),
        )
    )

    current_unallocated_line = (
        _build_unallocated_line(
            side="current",
            value_eur=(
                delta.current_unallocated_capital_eur
            ),
            return_input=(
                current_unallocated_return
            ),
            missing_evidence=(
                missing_evidence
            ),
        )
    )

    proposed_unallocated_line = (
        _build_unallocated_line(
            side="proposed",
            value_eur=(
                delta.proposed_unallocated_capital_eur
            ),
            return_input=(
                proposed_unallocated_return
            ),
            missing_evidence=(
                missing_evidence
            ),
        )
    )

    current_lines = list(
        current_position_lines
    )

    proposed_lines = list(
        proposed_position_lines
    )

    if current_unallocated_line is not None:
        current_lines.append(
            current_unallocated_line
        )

    if proposed_unallocated_line is not None:
        proposed_lines.append(
            proposed_unallocated_line
        )

    current_lines_tuple = tuple(
        current_lines
    )

    proposed_lines_tuple = tuple(
        proposed_lines
    )

    current_annual_return_eur = (
        _sum_annual_returns(
            current_lines_tuple
        )
    )

    proposed_annual_return_eur = (
        _sum_annual_returns(
            proposed_lines_tuple
        )
    )

    unique_missing_evidence = tuple(
        dict.fromkeys(
            missing_evidence
        )
    )

    if (
        current_annual_return_eur is None
        or proposed_annual_return_eur is None
    ):
        return TreasuryEconomicComparison(
            comparison_id=comparison_id,
            mandate_id=state.mandate_id,
            state_id=state.state_id,
            proposal_id=proposal.proposal_id,
            delta_id=delta.delta_id,
            treasury_capital_eur=(
                state.treasury_capital_eur
            ),
            comparison_status="incomplete",
            current_annual_return_eur=(
                current_annual_return_eur
            ),
            proposed_annual_return_eur=(
                proposed_annual_return_eur
            ),
            incremental_annual_benefit_eur=None,
            incremental_annual_benefit_pct_of_treasury=None,
            current_lines=(
                current_lines_tuple
            ),
            proposed_lines=(
                proposed_lines_tuple
            ),
            missing_evidence=(
                unique_missing_evidence
            ),
            notes=notes,
        )

    incremental_annual_benefit_eur = (
        proposed_annual_return_eur
        - current_annual_return_eur
    )

    incremental_annual_benefit_pct_of_treasury = (
        incremental_annual_benefit_eur
        / state.treasury_capital_eur
        * 100.0
    )

    return TreasuryEconomicComparison(
        comparison_id=comparison_id,
        mandate_id=state.mandate_id,
        state_id=state.state_id,
        proposal_id=proposal.proposal_id,
        delta_id=delta.delta_id,
        treasury_capital_eur=(
            state.treasury_capital_eur
        ),
        comparison_status="complete",
        current_annual_return_eur=(
            current_annual_return_eur
        ),
        proposed_annual_return_eur=(
            proposed_annual_return_eur
        ),
        incremental_annual_benefit_eur=(
            incremental_annual_benefit_eur
        ),
        incremental_annual_benefit_pct_of_treasury=(
            incremental_annual_benefit_pct_of_treasury
        ),
        current_lines=(
            current_lines_tuple
        ),
        proposed_lines=(
            proposed_lines_tuple
        ),
        missing_evidence=(),
        notes=notes,
    )