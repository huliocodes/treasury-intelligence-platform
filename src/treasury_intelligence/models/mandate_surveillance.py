from __future__ import annotations

from dataclasses import dataclass


HOLDING_MANDATE_STATUSES = (
    "compliant",
    "evidence_required",
    "breach",
)

TREASURY_MANDATE_SURVEILLANCE_STATUSES = (
    "compliant",
    "evidence_required",
    "breach",
)


@dataclass(frozen=True)
class CurrentHoldingMandateAssessment:
    assessment_id: str

    mandate_id: str
    position_id: str

    instrument_id: str
    market_id: str
    access_route_id: str

    position_size_eur: float

    status: str

    blocking_reasons: tuple[str, ...]
    evidence_requirements: tuple[str, ...]

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.assessment_id:
            raise ValueError(
                "assessment_id is required."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id is required."
            )

        if not self.position_id:
            raise ValueError(
                "position_id is required."
            )

        if self.position_size_eur <= 0:
            raise ValueError(
                "position_size_eur must be greater than zero."
            )

        if self.status not in HOLDING_MANDATE_STATUSES:
            raise ValueError(
                "Unsupported holding mandate status: "
                f"{self.status}"
            )

        if (
            self.status == "breach"
            and not self.blocking_reasons
        ):
            raise ValueError(
                "A breach assessment requires at least "
                "one blocking reason."
            )

        if (
            self.status == "evidence_required"
            and not self.evidence_requirements
        ):
            raise ValueError(
                "An evidence_required assessment requires "
                "at least one evidence requirement."
            )

        if (
            self.status == "compliant"
            and (
                self.blocking_reasons
                or self.evidence_requirements
            )
        ):
            raise ValueError(
                "A compliant assessment cannot contain "
                "blocking reasons or evidence requirements."
            )


@dataclass(frozen=True)
class TreasuryMandateSurveillance:
    surveillance_id: str

    mandate_id: str
    treasury_state_id: str
    as_of: str

    holding_assessments: tuple[
        CurrentHoldingMandateAssessment,
        ...
    ]

    status: str

    breach_position_count: int
    evidence_required_position_count: int
    compliant_position_count: int

    blocking_reasons: tuple[str, ...]
    evidence_requirements: tuple[str, ...]

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.surveillance_id:
            raise ValueError(
                "surveillance_id is required."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id is required."
            )

        if not self.treasury_state_id:
            raise ValueError(
                "treasury_state_id is required."
            )

        if not self.as_of:
            raise ValueError(
                "as_of is required."
            )

        if (
            self.status
            not in TREASURY_MANDATE_SURVEILLANCE_STATUSES
        ):
            raise ValueError(
                "Unsupported treasury mandate surveillance "
                f"status: {self.status}"
            )

        counts = (
            self.breach_position_count
            + self.evidence_required_position_count
            + self.compliant_position_count
        )

        if counts != len(self.holding_assessments):
            raise ValueError(
                "Holding-status counts must equal the number "
                "of holding assessments."
            )

        if (
            self.status == "breach"
            and self.breach_position_count == 0
        ):
            raise ValueError(
                "A breach surveillance result requires at "
                "least one breached position."
            )

        if (
            self.status == "evidence_required"
            and (
                self.breach_position_count != 0
                or self.evidence_required_position_count == 0
            )
        ):
            raise ValueError(
                "An evidence_required surveillance result "
                "requires no breaches and at least one "
                "position requiring evidence."
            )

        if (
            self.status == "compliant"
            and (
                self.breach_position_count != 0
                or self.evidence_required_position_count != 0
            )
        ):
            raise ValueError(
                "A compliant surveillance result cannot "
                "contain breached or evidence-required "
                "positions."
            )
