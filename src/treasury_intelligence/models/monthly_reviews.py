from __future__ import annotations

from dataclasses import dataclass


MONTHLY_REVIEW_STATUSES = (
    "complete",
    "follow_up_required",
)

MONTHLY_REVIEW_ACTIONS = (
    "hold",
    "hold_switch_not_economic",
    "evidence_required",
    "review_for_rebalance",
)


@dataclass(frozen=True)
class MonthlyReviewReport:
    review_id: str

    mandate_id: str
    state_id: str
    proposal_id: str
    delta_id: str
    economic_comparison_id: str
    switching_friction_assessment_id: str
    rebalance_decision_id: str
    mandate_surveillance_id: str

    as_of: str
    treasury_capital_eur: float

    current_invested_capital_eur: float
    current_unallocated_capital_eur: float

    proposed_allocated_capital_eur: float
    proposed_unallocated_capital_eur: float

    gross_position_movement_eur: float

    mandate_surveillance_status: str

    rebalance_decision: str
    rebalance_decision_status: str

    review_action: str

    first_year_net_benefit_eur: float | None
    first_year_net_improvement_bps_of_treasury: (
        float | None
    )

    review_status: str

    mandate_blocking_reasons: tuple[
        str,
        ...
    ]

    evidence_blocked_candidate_labels: tuple[
        str,
        ...
    ]

    evidence_requirements: tuple[
        str,
        ...
    ]

    summary: str

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.review_id:
            raise ValueError(
                "review_id cannot be empty."
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

        if not self.delta_id:
            raise ValueError(
                "delta_id cannot be empty."
            )

        if not self.economic_comparison_id:
            raise ValueError(
                "economic_comparison_id cannot be empty."
            )

        if not self.switching_friction_assessment_id:
            raise ValueError(
                "switching_friction_assessment_id "
                "cannot be empty."
            )

        if not self.rebalance_decision_id:
            raise ValueError(
                "rebalance_decision_id cannot be empty."
            )

        if not self.mandate_surveillance_id:
            raise ValueError(
                "mandate_surveillance_id cannot be empty."
            )

        if not self.as_of:
            raise ValueError(
                "as_of cannot be empty."
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be greater "
                "than zero."
            )

        if self.current_invested_capital_eur < 0:
            raise ValueError(
                "current_invested_capital_eur cannot "
                "be negative."
            )

        if self.current_unallocated_capital_eur < 0:
            raise ValueError(
                "current_unallocated_capital_eur cannot "
                "be negative."
            )

        if self.proposed_allocated_capital_eur < 0:
            raise ValueError(
                "proposed_allocated_capital_eur cannot "
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

        current_total = (
            self.current_invested_capital_eur
            + self.current_unallocated_capital_eur
        )

        if (
            abs(
                current_total
                - self.treasury_capital_eur
            )
            > 0.01
        ):
            raise ValueError(
                "Current invested plus unallocated "
                "capital must equal treasury capital."
            )

        proposed_total = (
            self.proposed_allocated_capital_eur
            + self.proposed_unallocated_capital_eur
        )

        if (
            abs(
                proposed_total
                - self.treasury_capital_eur
            )
            > 0.01
        ):
            raise ValueError(
                "Proposed allocated plus unallocated "
                "capital must equal treasury capital."
            )

        if self.mandate_surveillance_status not in (
            "compliant",
            "evidence_required",
            "breach",
        ):
            raise ValueError(
                "Unsupported mandate surveillance status: "
                f"{self.mandate_surveillance_status}"
            )

        if self.rebalance_decision not in (
            "keep_current",
            "needs_review",
            "rebalance",
        ):
            raise ValueError(
                "Unsupported rebalance decision: "
                f"{self.rebalance_decision}"
            )

        if self.rebalance_decision_status not in (
            "decision_ready",
            "review_required",
        ):
            raise ValueError(
                "Unsupported rebalance decision status: "
                f"{self.rebalance_decision_status}"
            )

        if self.review_action not in (
            MONTHLY_REVIEW_ACTIONS
        ):
            raise ValueError(
                "Unsupported monthly review action: "
                f"{self.review_action}"
            )

        if self.review_status not in (
            MONTHLY_REVIEW_STATUSES
        ):
            raise ValueError(
                "Unsupported monthly review status: "
                f"{self.review_status}"
            )

        if (
            self.mandate_surveillance_status == "breach"
            and not self.mandate_blocking_reasons
        ):
            raise ValueError(
                "Mandate breach requires at least one "
                "blocking reason."
            )

        if (
            self.mandate_surveillance_status
            != "breach"
            and self.mandate_blocking_reasons
        ):
            raise ValueError(
                "Mandate blocking reasons require a "
                "breach surveillance status."
            )

        if (
            self.mandate_surveillance_status == "breach"
            and self.review_action
            != "review_for_rebalance"
        ):
            raise ValueError(
                "Mandate breach must result in "
                "review_for_rebalance."
            )

        if (
            self.mandate_surveillance_status
            == "evidence_required"
            and self.review_action
            != "evidence_required"
        ):
            raise ValueError(
                "Evidence-required mandate surveillance "
                "must result in evidence_required."
            )

        if self.review_status == "complete":
            if self.evidence_blocked_candidate_labels:
                raise ValueError(
                    "Complete monthly review cannot "
                    "contain evidence-blocked candidates."
                )

            if self.evidence_requirements:
                raise ValueError(
                    "Complete monthly review cannot "
                    "contain evidence requirements."
                )

        if self.review_status == "follow_up_required":
            if (
                not self.evidence_blocked_candidate_labels
                and not self.evidence_requirements
            ):
                raise ValueError(
                    "follow_up_required requires at least "
                    "one blocked candidate or evidence "
                    "requirement."
                )

        if (
            self.review_action == "evidence_required"
            and not self.evidence_requirements
        ):
            raise ValueError(
                "evidence_required review action requires "
                "at least one evidence requirement."
            )

        if not self.summary:
            raise ValueError(
                "summary cannot be empty."
            )
