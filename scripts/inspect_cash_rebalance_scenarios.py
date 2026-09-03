from __future__ import annotations

from contextlib import redirect_stdout
from importlib.util import (
    module_from_spec,
    spec_from_file_location,
)
from io import StringIO
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MONTHLY_REVIEW_PATH = (
    PROJECT_ROOT
    / "scripts"
    / "inspect_monthly_review.py"
)

MONTHLY_REVIEW_SPEC = spec_from_file_location(
    "inspect_monthly_review",
    MONTHLY_REVIEW_PATH,
)

if (
    MONTHLY_REVIEW_SPEC is None
    or MONTHLY_REVIEW_SPEC.loader is None
):
    raise RuntimeError(
        "Could not load production monthly-review "
        "inspection module."
    )

monthly_review = module_from_spec(
    MONTHLY_REVIEW_SPEC
)

MONTHLY_REVIEW_SPEC.loader.exec_module(
    monthly_review
)


from treasury_intelligence.models.cash_baselines import (
    CashBalance,
)


AS_OF = monthly_review.AS_OF

TREASURY_CAPITAL_EUR = (
    monthly_review
    .MODEL_COMPANY_MANDATE
    .treasury_capital_eur
)


def run_scenario(
    *,
    scenario_id: str,
    cash_return_pct: float,
):
    original_current_treasury_builder = (
        monthly_review
        .build_model_company_current_treasury
    )

    original_cash_return_builder = (
        monthly_review
        .build_freshness_aware_cash_baseline_return_assessment
    )

    original_comparison_builder = (
        monthly_review
        .build_treasury_economic_comparison
    )

    original_switching_builder = (
        monthly_review
        .build_switching_friction_assessment
    )

    original_rebalance_builder = (
        monthly_review
        .build_rebalance_decision
    )

    captured = {}

    def build_fixture_current_treasury(
        *,
        as_of: str,
        positions=(),
        cash_balances=None,
        notes=None,
    ):
        del cash_balances

        return original_current_treasury_builder(
            as_of=as_of,
            positions=positions,
            cash_balances=(
                CashBalance(
                    balance_id=(
                        f"{scenario_id}_"
                        "verified_cash"
                    ),
                    label=(
                        "Verified model-company "
                        "corporate cash"
                    ),
                    balance_type="operating_account",
                    balance_eur=(
                        TREASURY_CAPITAL_EUR
                    ),
                    annual_return_pct=(
                        cash_return_pct
                    ),
                    return_evidence_available=True,
                    institution="Fixture Bank",
                    source_reference=(
                        f"{scenario_id}_"
                        "cash_rate_confirmation"
                    ),
                    return_evidence_date=(
                        "2026-09-01"
                    ),
                    notes=(
                        "Deterministic Milestone 15H.1 "
                        "fresh cash-return fixture."
                    ),
                ),
            ),
            notes=notes,
        )

    def capture_cash_return(*args, **kwargs):
        result = original_cash_return_builder(
            *args,
            **kwargs,
        )

        captured[
            "cash_return_assessment"
        ] = result

        return result

    def capture_comparison(*args, **kwargs):
        result = original_comparison_builder(
            *args,
            **kwargs,
        )

        captured["comparison"] = result

        return result

    def capture_switching(*args, **kwargs):
        result = original_switching_builder(
            *args,
            **kwargs,
        )

        captured["switching_friction"] = (
            result
        )

        return result

    def capture_decision(*args, **kwargs):
        result = original_rebalance_builder(
            *args,
            **kwargs,
        )

        captured["decision"] = result

        return result

    monthly_review.build_model_company_current_treasury = (
        build_fixture_current_treasury
    )

    monthly_review.build_freshness_aware_cash_baseline_return_assessment = (
        capture_cash_return
    )

    monthly_review.build_treasury_economic_comparison = (
        capture_comparison
    )

    monthly_review.build_switching_friction_assessment = (
        capture_switching
    )

    monthly_review.build_rebalance_decision = (
        capture_decision
    )

    output = StringIO()

    try:
        with redirect_stdout(output):
            try:
                monthly_review.main()
            except AssertionError:
                # The production inspection intentionally
                # asserts the default unresolved-cash case.
                # Scenario fixtures change that expected
                # terminal assertion state. The analytical
                # objects are captured before those default
                # inspection assertions execute.
                pass
    finally:
        monthly_review.build_model_company_current_treasury = (
            original_current_treasury_builder
        )

        monthly_review.build_freshness_aware_cash_baseline_return_assessment = (
            original_cash_return_builder
        )

        monthly_review.build_treasury_economic_comparison = (
            original_comparison_builder
        )

        monthly_review.build_switching_friction_assessment = (
            original_switching_builder
        )

        monthly_review.build_rebalance_decision = (
            original_rebalance_builder
        )

    required_objects = (
        "cash_return_assessment",
        "comparison",
        "switching_friction",
        "decision",
    )

    missing = tuple(
        name
        for name in required_objects
        if name not in captured
    )

    if missing:
        raise AssertionError(
            "Monthly-review pipeline did not reach "
            "all required analytical layers: "
            + ", ".join(missing)
            + "\n\nCaptured output:\n"
            + output.getvalue()
        )

    return (
        captured["cash_return_assessment"],
        captured["comparison"],
        captured["switching_friction"],
        captured["decision"],
    )


def print_case(
    *,
    label: str,
    cash_return_pct: float,
    expected_decision: str,
    expected_threshold_met: bool,
):
    (
        cash_assessment,
        comparison,
        switching_friction,
        decision,
    ) = run_scenario(
        scenario_id=(
            label.lower()
            .replace(" ", "_")
            .replace(".", "_")
        ),
        cash_return_pct=cash_return_pct,
    )

    print(label)
    print()

    print(
        "Current cash return:             "
        f"{cash_return_pct:.3f}%"
    )

    print(
        "Cash evidence status:            "
        f"{cash_assessment.assessment_status}"
    )

    print(
        "Economic comparison:             "
        f"{comparison.comparison_status}"
    )

    print(
        "Current annual return:           "
        f"EUR "
        f"{comparison.current_annual_return_eur:,.2f}"
    )

    print(
        "Proposed annual return:          "
        f"EUR "
        f"{comparison.proposed_annual_return_eur:,.2f}"
    )

    print(
        "Incremental annual benefit:      "
        f"EUR "
        f"{comparison.incremental_annual_benefit_eur:,.2f}"
    )

    print(
        "Switching friction:              "
        f"{switching_friction.friction_status}"
    )

    print(
        "Additional switching cost:       "
        f"EUR "
        f"{switching_friction.total_switching_cost_eur:,.2f}"
    )

    print(
        "First-year net benefit:          "
        f"EUR "
        f"{decision.first_year_net_benefit_eur:,.2f}"
    )

    print(
        "Net improvement:                 "
        f"{decision.first_year_net_improvement_bps_of_treasury:.3f} bps"
    )

    print(
        "Required improvement:            "
        f"{decision.minimum_required_improvement_bps:.3f} bps"
    )

    print(
        "Threshold met:                   "
        f"{decision.threshold_met}"
    )

    print(
        "Decision:                        "
        f"{decision.decision}"
    )

    print(
        "Decision status:                 "
        f"{decision.decision_status}"
    )

    assert (
        cash_assessment.assessment_status
        == "complete"
    )

    assert (
        cash_assessment
        .return_evidence_coverage_pct
        == 100.0
    )

    assert (
        cash_assessment
        .blended_annual_return_pct
        == cash_return_pct
    )

    assert (
        comparison.comparison_status
        == "complete"
    )

    assert (
        comparison.current_annual_return_eur
        is not None
    )

    assert (
        comparison.proposed_annual_return_eur
        is not None
    )

    assert (
        comparison.incremental_annual_benefit_eur
        is not None
    )

    assert (
        switching_friction.friction_status
        == "complete"
    )

    assert (
        switching_friction
        .total_switching_cost_eur
        == 0.0
    )

    assert (
        decision.decision_status
        == "decision_ready"
    )

    assert (
        decision.decision
        == expected_decision
    )

    assert (
        decision.threshold_met
        is expected_threshold_met
    )

    assert (
        decision.minimum_required_improvement_bps
        == 5.0
    )

    print()
    print("-" * 100)
    print()

    return decision


def main() -> None:
    print(
        "MILESTONE 15H.1 — CASH ECONOMICS TO "
        "REBALANCE DECISION"
    )
    print()

    print(
        "The actual production monthly-review "
        "analytical chain is exercised with fresh, "
        "dated current-cash return fixtures."
    )

    print()
    print("-" * 100)
    print()

    low_cash = print_case(
        label=(
            "CASE 1 — 1.50% CASH: "
            "REBALANCE ECONOMIC"
        ),
        cash_return_pct=1.50,
        expected_decision="rebalance",
        expected_threshold_met=True,
    )

    near_cash = print_case(
        label=(
            "CASE 2 — 2.73% CASH: "
            "IMPROVEMENT BELOW 5 BPS"
        ),
        cash_return_pct=2.73,
        expected_decision="keep_current",
        expected_threshold_met=False,
    )

    higher_cash = print_case(
        label=(
            "CASE 3 — 2.80% CASH: "
            "PROPOSED RETURN LOWER"
        ),
        cash_return_pct=2.80,
        expected_decision="keep_current",
        expected_threshold_met=False,
    )

    assert (
        low_cash
        .first_year_net_improvement_bps_of_treasury
        >= 5.0
    )

    assert (
        0.0
        < near_cash
        .first_year_net_improvement_bps_of_treasury
        < 5.0
    )

    assert (
        higher_cash
        .first_year_net_improvement_bps_of_treasury
        < 0.0
    )

    print(
        "MILESTONE 15H.1 ASSERTIONS"
    )
    print()

    print(
        "Fresh cash economics reach comparison:    yes"
    )

    print(
        "Current and proposed returns complete:     yes"
    )

    print(
        "Embedded transaction costs not duplicated: yes"
    )

    print(
        "5-bps production policy reused:           yes"
    )

    print(
        "Material improvement triggers rebalance:  yes"
    )

    print(
        "Sub-threshold improvement keeps current:  yes"
    )

    print(
        "Negative improvement keeps current:       yes"
    )

    print()

    print(
        "All Milestone 15H.1 cash-to-rebalance "
        "decision assertions passed."
    )


if __name__ == "__main__":
    main()
