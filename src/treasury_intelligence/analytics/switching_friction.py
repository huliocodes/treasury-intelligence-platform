from __future__ import annotations

from treasury_intelligence.models.allocation_deltas import (
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.economic_comparisons import (
    TreasuryEconomicComparison,
)

from treasury_intelligence.models.switching_friction import (
    SwitchingFrictionAssessment,
    SwitchingFrictionInput,
    SwitchingFrictionLine,
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


def _build_friction_map(
    inputs: tuple[
        SwitchingFrictionInput,
        ...
    ],
) -> dict[
    PositionKey,
    SwitchingFrictionInput,
]:
    result: dict[
        PositionKey,
        SwitchingFrictionInput,
    ] = {}

    for item in inputs:
        key = _position_key(
            instrument_id=item.instrument_id,
            market_id=item.market_id,
            access_route_id=item.access_route_id,
        )

        if key in result:
            raise ValueError(
                "Duplicate switching friction input "
                f"for {key}."
            )

        result[key] = item

    return result


def _calculate_switching_cost(
    movement_eur: float,
    friction_bps: float,
    fixed_cost_eur: float,
) -> float:
    variable_cost_eur = (
        movement_eur
        * friction_bps
        / 10_000.0
    )

    return (
        variable_cost_eur
        + fixed_cost_eur
    )


def build_switching_friction_assessment(
    assessment_id: str,
    delta: TreasuryAllocationDelta,
    economic_comparison: TreasuryEconomicComparison,
    friction_inputs: tuple[
        SwitchingFrictionInput,
        ...
    ],
    notes: str | None = None,
) -> SwitchingFrictionAssessment:
    if (
        delta.mandate_id
        != economic_comparison.mandate_id
    ):
        raise ValueError(
            "Allocation delta and economic comparison "
            "must use the same mandate."
        )

    if (
        delta.delta_id
        != economic_comparison.delta_id
    ):
        raise ValueError(
            "Economic comparison does not belong to "
            "the supplied allocation delta."
        )

    friction_map = (
        _build_friction_map(
            friction_inputs
        )
    )

    changed_lines = tuple(
        line
        for line in delta.delta_lines
        if abs(line.delta_eur) > 0.01
    )

    changed_keys = {
        _position_key(
            instrument_id=line.instrument_id,
            market_id=line.market_id,
            access_route_id=line.access_route_id,
        )
        for line in changed_lines
    }

    unused_input_keys = (
        set(friction_map)
        - changed_keys
    )

    if unused_input_keys:
        raise ValueError(
            "Switching friction inputs were supplied "
            "for allocations that do not change."
        )

    friction_lines: list[
        SwitchingFrictionLine
    ] = []

    missing_evidence: list[str] = []

    for line in changed_lines:
        key = _position_key(
            instrument_id=line.instrument_id,
            market_id=line.market_id,
            access_route_id=line.access_route_id,
        )

        friction_input = (
            friction_map.get(
                key
            )
        )

        movement_eur = abs(
            line.delta_eur
        )

        if friction_input is None:
            missing_evidence.append(
                "switching friction evidence missing "
                f"for {line.label} ({line.action})."
            )

            friction_lines.append(
                SwitchingFrictionLine(
                    instrument_id=line.instrument_id,
                    market_id=line.market_id,
                    access_route_id=(
                        line.access_route_id
                    ),
                    label=line.label,
                    action=line.action,
                    movement_eur=movement_eur,
                    friction_bps=None,
                    fixed_cost_eur=None,
                    switching_cost_eur=None,
                    evidence_available=False,
                    notes=(
                        "No switching friction input "
                        "was supplied."
                    ),
                )
            )

            continue

        if (
            friction_input.action
            != line.action
        ):
            raise ValueError(
                "Switching friction action does not "
                f"match allocation delta for "
                f"{line.label}."
            )

        if not friction_input.evidence_available:
            missing_evidence.append(
                "switching friction evidence "
                f"unavailable for "
                f"{friction_input.label} "
                f"({friction_input.action})."
            )

            friction_lines.append(
                SwitchingFrictionLine(
                    instrument_id=line.instrument_id,
                    market_id=line.market_id,
                    access_route_id=(
                        line.access_route_id
                    ),
                    label=friction_input.label,
                    action=line.action,
                    movement_eur=movement_eur,
                    friction_bps=None,
                    fixed_cost_eur=None,
                    switching_cost_eur=None,
                    evidence_available=False,
                    notes=(
                        friction_input.notes
                    ),
                )
            )

            continue

        friction_bps = (
            friction_input.friction_bps
        )

        fixed_cost_eur = (
            friction_input.fixed_cost_eur
        )

        if friction_bps is None:
            raise AssertionError(
                "Available friction input unexpectedly "
                "contains no friction_bps."
            )

        if fixed_cost_eur is None:
            raise AssertionError(
                "Available friction input unexpectedly "
                "contains no fixed_cost_eur."
            )

        switching_cost_eur = (
            _calculate_switching_cost(
                movement_eur=movement_eur,
                friction_bps=friction_bps,
                fixed_cost_eur=fixed_cost_eur,
            )
        )

        friction_lines.append(
            SwitchingFrictionLine(
                instrument_id=line.instrument_id,
                market_id=line.market_id,
                access_route_id=(
                    line.access_route_id
                ),
                label=friction_input.label,
                action=line.action,
                movement_eur=movement_eur,
                friction_bps=friction_bps,
                fixed_cost_eur=fixed_cost_eur,
                switching_cost_eur=(
                    switching_cost_eur
                ),
                evidence_available=True,
                notes=friction_input.notes,
            )
        )

    known_switching_cost_eur = sum(
        line.switching_cost_eur or 0.0
        for line in friction_lines
        if line.evidence_available
    )

    unique_missing_evidence = tuple(
        dict.fromkeys(
            missing_evidence
        )
    )

    if unique_missing_evidence:
        friction_status = "incomplete"
        total_switching_cost_eur = None

    else:
        friction_status = "complete"

        total_switching_cost_eur = (
            known_switching_cost_eur
        )

    incremental_annual_benefit_eur = (
        economic_comparison
        .incremental_annual_benefit_eur
    )

    net_benefit_available = (
        friction_status == "complete"
        and economic_comparison.comparison_status
        == "complete"
        and incremental_annual_benefit_eur
        is not None
    )

    if net_benefit_available:
        if total_switching_cost_eur is None:
            raise AssertionError(
                "Complete friction status unexpectedly "
                "contains no total cost."
            )

        if incremental_annual_benefit_eur is None:
            raise AssertionError(
                "Complete economic comparison "
                "unexpectedly contains no benefit."
            )

        first_year_net_benefit_eur = (
            incremental_annual_benefit_eur
            - total_switching_cost_eur
        )

        if incremental_annual_benefit_eur > 0:
            payback_days = (
                total_switching_cost_eur
                / incremental_annual_benefit_eur
                * 365.0
            )
        else:
            payback_days = None

    else:
        first_year_net_benefit_eur = None
        payback_days = None

    return SwitchingFrictionAssessment(
        assessment_id=assessment_id,
        mandate_id=delta.mandate_id,
        delta_id=delta.delta_id,
        economic_comparison_id=(
            economic_comparison.comparison_id
        ),
        gross_position_movement_eur=(
            delta.gross_position_movement_eur
        ),
        friction_status=friction_status,
        known_switching_cost_eur=(
            known_switching_cost_eur
        ),
        total_switching_cost_eur=(
            total_switching_cost_eur
        ),
        incremental_annual_benefit_eur=(
            incremental_annual_benefit_eur
        ),
        first_year_net_benefit_eur=(
            first_year_net_benefit_eur
        ),
        payback_days=payback_days,
        net_benefit_available=(
            net_benefit_available
        ),
        friction_lines=tuple(
            friction_lines
        ),
        missing_evidence=(
            unique_missing_evidence
        ),
        notes=notes,
    )