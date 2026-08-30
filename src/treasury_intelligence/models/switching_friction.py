from __future__ import annotations

from dataclasses import dataclass


SWITCHING_FRICTION_STATUSES = (
    "complete",
    "incomplete",
)


@dataclass(frozen=True)
class SwitchingFrictionInput:
    instrument_id: str
    market_id: str
    access_route_id: str

    label: str
    action: str

    friction_bps: float | None
    fixed_cost_eur: float | None

    evidence_available: bool

    source_reference: str | None = None
    notes: str | None = None

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

        if self.action not in (
            "open",
            "increase",
            "decrease",
            "close",
        ):
            raise ValueError(
                "Switching friction input must apply "
                "to a changed allocation."
            )

        if self.evidence_available:
            if self.friction_bps is None:
                raise ValueError(
                    "Available friction evidence "
                    "requires friction_bps."
                )

            if self.fixed_cost_eur is None:
                raise ValueError(
                    "Available friction evidence "
                    "requires fixed_cost_eur."
                )

            if self.friction_bps < 0:
                raise ValueError(
                    "friction_bps cannot be negative."
                )

            if self.fixed_cost_eur < 0:
                raise ValueError(
                    "fixed_cost_eur cannot be negative."
                )

        else:
            if self.friction_bps is not None:
                raise ValueError(
                    "friction_bps must be None when "
                    "evidence_available=False."
                )

            if self.fixed_cost_eur is not None:
                raise ValueError(
                    "fixed_cost_eur must be None when "
                    "evidence_available=False."
                )


@dataclass(frozen=True)
class SwitchingFrictionLine:
    instrument_id: str
    market_id: str
    access_route_id: str

    label: str
    action: str

    movement_eur: float

    friction_bps: float | None
    fixed_cost_eur: float | None
    switching_cost_eur: float | None

    evidence_available: bool

    notes: str | None = None

    def __post_init__(self) -> None:
        if self.movement_eur <= 0:
            raise ValueError(
                "movement_eur must be greater "
                "than zero."
            )

        if self.action not in (
            "open",
            "increase",
            "decrease",
            "close",
        ):
            raise ValueError(
                "Switching friction line must apply "
                "to a changed allocation."
            )

        if self.evidence_available:
            if self.friction_bps is None:
                raise ValueError(
                    "Available friction line requires "
                    "friction_bps."
                )

            if self.fixed_cost_eur is None:
                raise ValueError(
                    "Available friction line requires "
                    "fixed_cost_eur."
                )

            if self.switching_cost_eur is None:
                raise ValueError(
                    "Available friction line requires "
                    "switching_cost_eur."
                )

        else:
            if self.friction_bps is not None:
                raise ValueError(
                    "Unavailable friction line requires "
                    "friction_bps=None."
                )

            if self.fixed_cost_eur is not None:
                raise ValueError(
                    "Unavailable friction line requires "
                    "fixed_cost_eur=None."
                )

            if self.switching_cost_eur is not None:
                raise ValueError(
                    "Unavailable friction line requires "
                    "switching_cost_eur=None."
                )


@dataclass(frozen=True)
class SwitchingFrictionAssessment:
    assessment_id: str

    mandate_id: str
    delta_id: str
    economic_comparison_id: str

    gross_position_movement_eur: float

    friction_status: str

    known_switching_cost_eur: float
    total_switching_cost_eur: float | None

    incremental_annual_benefit_eur: float | None
    first_year_net_benefit_eur: float | None

    payback_days: float | None

    net_benefit_available: bool

    friction_lines: tuple[
        SwitchingFrictionLine,
        ...
    ]

    missing_evidence: tuple[
        str,
        ...
    ]

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.assessment_id:
            raise ValueError(
                "assessment_id cannot be empty."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id cannot be empty."
            )

        if not self.delta_id:
            raise ValueError(
                "delta_id cannot be empty."
            )

        if not self.economic_comparison_id:
            raise ValueError(
                "economic_comparison_id cannot "
                "be empty."
            )

        if self.gross_position_movement_eur < 0:
            raise ValueError(
                "gross_position_movement_eur cannot "
                "be negative."
            )

        if self.friction_status not in (
            SWITCHING_FRICTION_STATUSES
        ):
            raise ValueError(
                "Unsupported friction status: "
                f"{self.friction_status}"
            )

        if self.known_switching_cost_eur < 0:
            raise ValueError(
                "known_switching_cost_eur cannot "
                "be negative."
            )

        if (
            self.total_switching_cost_eur is not None
            and self.total_switching_cost_eur < 0
        ):
            raise ValueError(
                "total_switching_cost_eur cannot "
                "be negative."
            )

        calculated_known_cost = sum(
            line.switching_cost_eur or 0.0
            for line in self.friction_lines
            if line.evidence_available
        )

        if (
            abs(
                calculated_known_cost
                - self.known_switching_cost_eur
            )
            > 0.01
        ):
            raise ValueError(
                "known_switching_cost_eur must equal "
                "the sum of known friction costs."
            )

        if self.friction_status == "complete":
            if self.total_switching_cost_eur is None:
                raise ValueError(
                    "Complete friction assessment "
                    "requires total switching cost."
                )

            if self.missing_evidence:
                raise ValueError(
                    "Complete friction assessment "
                    "cannot contain missing evidence."
                )

        if self.friction_status == "incomplete":
            if self.total_switching_cost_eur is not None:
                raise ValueError(
                    "Incomplete friction assessment "
                    "cannot expose total switching cost."
                )

            if not self.missing_evidence:
                raise ValueError(
                    "Incomplete friction assessment "
                    "requires missing evidence."
                )

        if self.net_benefit_available:
            if self.incremental_annual_benefit_eur is None:
                raise ValueError(
                    "Available net benefit requires "
                    "incremental annual benefit."
                )

            if self.total_switching_cost_eur is None:
                raise ValueError(
                    "Available net benefit requires "
                    "total switching cost."
                )

            if self.first_year_net_benefit_eur is None:
                raise ValueError(
                    "Available net benefit requires "
                    "first-year net benefit."
                )

        else:
            if self.first_year_net_benefit_eur is not None:
                raise ValueError(
                    "Unavailable net benefit requires "
                    "first_year_net_benefit_eur=None."
                )