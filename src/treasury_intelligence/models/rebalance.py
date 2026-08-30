from __future__ import annotations

from dataclasses import dataclass


REBALANCE_DECISIONS = (
    "keep_current",
    "needs_review",
    "rebalance",
)

REBALANCE_DECISION_STATUSES = (
    "decision_ready",
    "review_required",
)


@dataclass(frozen=True)
class RebalancePolicy:
    policy_id: str

    minimum_first_year_net_improvement_bps_of_treasury: float

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.policy_id:
            raise ValueError(
                "policy_id cannot be empty."
            )

        if (
            self.minimum_first_year_net_improvement_bps_of_treasury
            < 0
        ):
            raise ValueError(
                "minimum_first_year_net_improvement_bps_of_treasury "
                "cannot be negative."
            )


@dataclass(frozen=True)
class RebalanceDecision:
    decision_id: str

    mandate_id: str
    policy_id: str

    delta_id: str
    economic_comparison_id: str
    switching_friction_assessment_id: str

    treasury_capital_eur: float

    allocation_change_required: bool

    economic_comparison_status: str
    friction_status: str

    incremental_annual_benefit_eur: float | None
    total_switching_cost_eur: float | None
    first_year_net_benefit_eur: float | None

    first_year_net_improvement_bps_of_treasury: (
        float | None
    )

    minimum_required_improvement_bps: float

    decision: str
    decision_status: str

    threshold_met: bool | None

    rationale: str

    evidence_requirements: tuple[
        str,
        ...
    ]

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.decision_id:
            raise ValueError(
                "decision_id cannot be empty."
            )

        if not self.mandate_id:
            raise ValueError(
                "mandate_id cannot be empty."
            )

        if not self.policy_id:
            raise ValueError(
                "policy_id cannot be empty."
            )

        if self.treasury_capital_eur <= 0:
            raise ValueError(
                "treasury_capital_eur must be "
                "greater than zero."
            )

        if self.minimum_required_improvement_bps < 0:
            raise ValueError(
                "minimum_required_improvement_bps "
                "cannot be negative."
            )

        if self.decision not in REBALANCE_DECISIONS:
            raise ValueError(
                "Unsupported rebalance decision: "
                f"{self.decision}"
            )

        if (
            self.decision_status
            not in REBALANCE_DECISION_STATUSES
        ):
            raise ValueError(
                "Unsupported rebalance decision status: "
                f"{self.decision_status}"
            )

        if self.decision == "needs_review":
            if self.decision_status != "review_required":
                raise ValueError(
                    "needs_review requires "
                    "review_required status."
                )

            if not self.evidence_requirements:
                raise ValueError(
                    "needs_review requires evidence "
                    "requirements."
                )

            if self.threshold_met is not None:
                raise ValueError(
                    "needs_review cannot expose "
                    "threshold_met."
                )

        if self.decision in (
            "keep_current",
            "rebalance",
        ):
            if self.decision_status != "decision_ready":
                raise ValueError(
                    "Decision-ready actions require "
                    "decision_ready status."
                )

            if self.evidence_requirements:
                raise ValueError(
                    "Decision-ready result cannot contain "
                    "evidence requirements."
                )

        if self.decision == "rebalance":
            if not self.allocation_change_required:
                raise ValueError(
                    "rebalance requires an allocation "
                    "change."
                )

            if self.threshold_met is not True:
                raise ValueError(
                    "rebalance requires threshold_met=True."
                )

            if self.first_year_net_benefit_eur is None:
                raise ValueError(
                    "rebalance requires first-year "
                    "net benefit."
                )

            if self.first_year_net_benefit_eur <= 0:
                raise ValueError(
                    "rebalance requires positive "
                    "first-year net benefit."
                )