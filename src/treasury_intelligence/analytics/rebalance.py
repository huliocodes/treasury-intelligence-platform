from __future__ import annotations

from treasury_intelligence.models.allocation_deltas import (
    TreasuryAllocationDelta,
)

from treasury_intelligence.models.economic_comparisons import (
    TreasuryEconomicComparison,
)

from treasury_intelligence.models.rebalance import (
    RebalanceDecision,
    RebalancePolicy,
)

from treasury_intelligence.models.switching_friction import (
    SwitchingFrictionAssessment,
)


def _eur_to_treasury_bps(
    value_eur: float,
    treasury_capital_eur: float,
) -> float:
    return (
        value_eur
        / treasury_capital_eur
        * 10_000.0
    )


def build_rebalance_decision(
    decision_id: str,
    policy: RebalancePolicy,
    delta: TreasuryAllocationDelta,
    economic_comparison: TreasuryEconomicComparison,
    switching_friction: SwitchingFrictionAssessment,
    notes: str | None = None,
) -> RebalanceDecision:
    if (
        delta.mandate_id
        != economic_comparison.mandate_id
        or delta.mandate_id
        != switching_friction.mandate_id
    ):
        raise ValueError(
            "Delta, economic comparison and switching "
            "friction must use the same mandate."
        )

    if (
        delta.delta_id
        != economic_comparison.delta_id
    ):
        raise ValueError(
            "Economic comparison does not belong to "
            "the supplied allocation delta."
        )

    if (
        delta.delta_id
        != switching_friction.delta_id
    ):
        raise ValueError(
            "Switching friction does not belong to "
            "the supplied allocation delta."
        )

    if (
        economic_comparison.comparison_id
        != switching_friction.economic_comparison_id
    ):
        raise ValueError(
            "Switching friction does not belong to "
            "the supplied economic comparison."
        )

    treasury_capital_eur = (
        delta.treasury_capital_eur
    )

    if not delta.change_required:
        return RebalanceDecision(
            decision_id=decision_id,
            mandate_id=delta.mandate_id,
            policy_id=policy.policy_id,
            delta_id=delta.delta_id,
            economic_comparison_id=(
                economic_comparison.comparison_id
            ),
            switching_friction_assessment_id=(
                switching_friction.assessment_id
            ),
            treasury_capital_eur=(
                treasury_capital_eur
            ),
            allocation_change_required=False,
            economic_comparison_status=(
                economic_comparison.comparison_status
            ),
            friction_status=(
                switching_friction.friction_status
            ),
            incremental_annual_benefit_eur=(
                economic_comparison
                .incremental_annual_benefit_eur
            ),
            total_switching_cost_eur=(
                switching_friction
                .total_switching_cost_eur
            ),
            first_year_net_benefit_eur=(
                switching_friction
                .first_year_net_benefit_eur
            ),
            first_year_net_improvement_bps_of_treasury=0.0,
            minimum_required_improvement_bps=(
                policy
                .minimum_first_year_net_improvement_bps_of_treasury
            ),
            decision="keep_current",
            decision_status="decision_ready",
            threshold_met=False,
            rationale=(
                "The proposed allocation does not differ "
                "from the current treasury allocation, so "
                "no rebalance is required."
            ),
            evidence_requirements=(),
            notes=notes,
        )

    evidence_requirements: list[str] = []

    if (
        economic_comparison.comparison_status
        != "complete"
    ):
        evidence_requirements.extend(
            economic_comparison.missing_evidence
        )

    if (
        switching_friction.friction_status
        != "complete"
    ):
        evidence_requirements.extend(
            switching_friction.missing_evidence
        )

    unique_evidence_requirements = tuple(
        dict.fromkeys(
            evidence_requirements
        )
    )

    if unique_evidence_requirements:
        return RebalanceDecision(
            decision_id=decision_id,
            mandate_id=delta.mandate_id,
            policy_id=policy.policy_id,
            delta_id=delta.delta_id,
            economic_comparison_id=(
                economic_comparison.comparison_id
            ),
            switching_friction_assessment_id=(
                switching_friction.assessment_id
            ),
            treasury_capital_eur=(
                treasury_capital_eur
            ),
            allocation_change_required=True,
            economic_comparison_status=(
                economic_comparison.comparison_status
            ),
            friction_status=(
                switching_friction.friction_status
            ),
            incremental_annual_benefit_eur=(
                economic_comparison
                .incremental_annual_benefit_eur
            ),
            total_switching_cost_eur=(
                switching_friction
                .total_switching_cost_eur
            ),
            first_year_net_benefit_eur=None,
            first_year_net_improvement_bps_of_treasury=None,
            minimum_required_improvement_bps=(
                policy
                .minimum_first_year_net_improvement_bps_of_treasury
            ),
            decision="needs_review",
            decision_status="review_required",
            threshold_met=None,
            rationale=(
                "The proposed allocation differs from "
                "the current treasury state, but the "
                "economic benefit cannot yet be judged "
                "against the rebalance threshold because "
                "required evidence is incomplete."
            ),
            evidence_requirements=(
                unique_evidence_requirements
            ),
            notes=notes,
        )

    first_year_net_benefit_eur = (
        switching_friction
        .first_year_net_benefit_eur
    )

    if first_year_net_benefit_eur is None:
        raise AssertionError(
            "Complete economic and friction evidence "
            "unexpectedly produced no first-year "
            "net benefit."
        )

    improvement_bps = (
        _eur_to_treasury_bps(
            value_eur=(
                first_year_net_benefit_eur
            ),
            treasury_capital_eur=(
                treasury_capital_eur
            ),
        )
    )

    minimum_required_bps = (
        policy
        .minimum_first_year_net_improvement_bps_of_treasury
    )

    threshold_met = (
        improvement_bps
        >= minimum_required_bps
        and first_year_net_benefit_eur > 0
    )

    if first_year_net_benefit_eur <= 0:
        return RebalanceDecision(
            decision_id=decision_id,
            mandate_id=delta.mandate_id,
            policy_id=policy.policy_id,
            delta_id=delta.delta_id,
            economic_comparison_id=(
                economic_comparison.comparison_id
            ),
            switching_friction_assessment_id=(
                switching_friction.assessment_id
            ),
            treasury_capital_eur=(
                treasury_capital_eur
            ),
            allocation_change_required=True,
            economic_comparison_status="complete",
            friction_status="complete",
            incremental_annual_benefit_eur=(
                economic_comparison
                .incremental_annual_benefit_eur
            ),
            total_switching_cost_eur=(
                switching_friction
                .total_switching_cost_eur
            ),
            first_year_net_benefit_eur=(
                first_year_net_benefit_eur
            ),
            first_year_net_improvement_bps_of_treasury=(
                improvement_bps
            ),
            minimum_required_improvement_bps=(
                minimum_required_bps
            ),
            decision="keep_current",
            decision_status="decision_ready",
            threshold_met=False,
            rationale=(
                "The proposed allocation does not "
                "produce a positive first-year net "
                "economic benefit after switching costs."
            ),
            evidence_requirements=(),
            notes=notes,
        )

    if not threshold_met:
        return RebalanceDecision(
            decision_id=decision_id,
            mandate_id=delta.mandate_id,
            policy_id=policy.policy_id,
            delta_id=delta.delta_id,
            economic_comparison_id=(
                economic_comparison.comparison_id
            ),
            switching_friction_assessment_id=(
                switching_friction.assessment_id
            ),
            treasury_capital_eur=(
                treasury_capital_eur
            ),
            allocation_change_required=True,
            economic_comparison_status="complete",
            friction_status="complete",
            incremental_annual_benefit_eur=(
                economic_comparison
                .incremental_annual_benefit_eur
            ),
            total_switching_cost_eur=(
                switching_friction
                .total_switching_cost_eur
            ),
            first_year_net_benefit_eur=(
                first_year_net_benefit_eur
            ),
            first_year_net_improvement_bps_of_treasury=(
                improvement_bps
            ),
            minimum_required_improvement_bps=(
                minimum_required_bps
            ),
            decision="keep_current",
            decision_status="decision_ready",
            threshold_met=False,
            rationale=(
                "The proposed allocation produces a "
                "positive first-year net benefit, but "
                "the improvement is below the minimum "
                "rebalance threshold."
            ),
            evidence_requirements=(),
            notes=notes,
        )

    return RebalanceDecision(
        decision_id=decision_id,
        mandate_id=delta.mandate_id,
        policy_id=policy.policy_id,
        delta_id=delta.delta_id,
        economic_comparison_id=(
            economic_comparison.comparison_id
        ),
        switching_friction_assessment_id=(
            switching_friction.assessment_id
        ),
        treasury_capital_eur=(
            treasury_capital_eur
        ),
        allocation_change_required=True,
        economic_comparison_status="complete",
        friction_status="complete",
        incremental_annual_benefit_eur=(
            economic_comparison
            .incremental_annual_benefit_eur
        ),
        total_switching_cost_eur=(
            switching_friction
            .total_switching_cost_eur
        ),
        first_year_net_benefit_eur=(
            first_year_net_benefit_eur
        ),
        first_year_net_improvement_bps_of_treasury=(
            improvement_bps
        ),
        minimum_required_improvement_bps=(
            minimum_required_bps
        ),
        decision="rebalance",
        decision_status="decision_ready",
        threshold_met=True,
        rationale=(
            "The proposed allocation produces a "
            "positive first-year net economic benefit "
            "after switching costs and meets the "
            "minimum rebalance threshold."
        ),
        evidence_requirements=(),
        notes=notes,
    )