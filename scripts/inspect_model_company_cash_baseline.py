from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.cash_returns import (
    build_cash_baseline_return_assessment,
)

from treasury_intelligence.cash_baselines import (
    build_model_company_cash_baseline,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
)


AS_OF = "2026-09-03"


def main() -> None:
    print(
        "MODEL-COMPANY CURRENT-CASH BASELINE"
    )
    print()

    default_baseline = (
        build_model_company_cash_baseline(
            as_of=AS_OF,
        )
    )

    default_assessment = (
        build_cash_baseline_return_assessment(
            assessment_id=(
                "model_company_default_cash_return"
            ),
            baseline=default_baseline,
        )
    )

    print("CASE 1 — DEFAULT UNRESOLVED BASELINE")
    print()

    print(
        f"Total cash:                    "
        f"EUR {default_baseline.total_cash_eur:,.0f}"
    )

    print(
        f"Balances:                      "
        f"{len(default_baseline.balances)}"
    )

    print(
        f"Return evidence coverage:      "
        f"{default_assessment.return_evidence_coverage_pct:.1f}%"
    )

    print(
        f"Assessment status:             "
        f"{default_assessment.assessment_status}"
    )

    assert (
        default_baseline.total_cash_eur
        == MODEL_COMPANY_MANDATE.treasury_capital_eur
    )

    assert len(default_baseline.balances) == 1

    assert (
        default_baseline.balances[0].institution
        is None
    )

    assert (
        default_baseline.balances[0]
        .annual_return_pct
        is None
    )

    assert (
        default_baseline.balances[0]
        .return_evidence_available
        is False
    )

    assert (
        default_assessment.assessment_status
        == "incomplete"
    )

    print()
    print("CASE 2 — PARTIALLY EVIDENCED CASH")
    print()

    partial_balances = (
        CashBalance(
            balance_id="fixture_operating_cash",
            label="Operating account",
            balance_type="operating_account",
            balance_eur=2_000_000.0,
            annual_return_pct=1.00,
            return_evidence_available=True,
            institution="Fixture Bank A",
            source_reference=(
                "fixture_bank_a_statement"
            ),
            notes=(
                "Deterministic validation fixture."
            ),
        ),
        CashBalance(
            balance_id="fixture_unresolved_cash",
            label="Unresolved secondary cash",
            balance_type="other_cash",
            balance_eur=3_000_000.0,
            annual_return_pct=None,
            return_evidence_available=False,
            institution="Fixture Bank B",
            source_reference=None,
            notes=(
                "Deterministic validation fixture."
            ),
        ),
    )

    partial_baseline = (
        build_model_company_cash_baseline(
            as_of=AS_OF,
            balances=partial_balances,
        )
    )

    partial_assessment = (
        build_cash_baseline_return_assessment(
            assessment_id=(
                "model_company_partial_cash_return"
            ),
            baseline=partial_baseline,
        )
    )

    print(
        f"Total cash:                    "
        f"EUR {partial_baseline.total_cash_eur:,.0f}"
    )

    print(
        f"Known-return cash:             "
        f"EUR {partial_assessment.known_return_balance_eur:,.0f}"
    )

    print(
        f"Unknown-return cash:           "
        f"EUR {partial_assessment.unknown_return_balance_eur:,.0f}"
    )

    print(
        f"Return evidence coverage:      "
        f"{partial_assessment.return_evidence_coverage_pct:.1f}%"
    )

    print(
        f"Assessment status:             "
        f"{partial_assessment.assessment_status}"
    )

    assert (
        partial_assessment.known_return_balance_eur
        == 2_000_000.0
    )

    assert (
        partial_assessment.unknown_return_balance_eur
        == 3_000_000.0
    )

    assert (
        partial_assessment.return_evidence_coverage_pct
        == 40.0
    )

    assert (
        partial_assessment.blended_annual_return_pct
        is None
    )

    assert (
        partial_assessment.assessment_status
        == "incomplete"
    )

    print()
    print("CASE 3 — FULLY EVIDENCED CASH")
    print()

    complete_balances = (
        CashBalance(
            balance_id="fixture_operating_account",
            label="Operating account",
            balance_type="operating_account",
            balance_eur=2_000_000.0,
            annual_return_pct=0.50,
            return_evidence_available=True,
            institution="Fixture Bank A",
            source_reference=(
                "fixture_operating_statement"
            ),
            notes=(
                "Deterministic validation fixture."
            ),
        ),
        CashBalance(
            balance_id="fixture_savings_account",
            label="Savings account",
            balance_type="savings_account",
            balance_eur=3_000_000.0,
            annual_return_pct=1.50,
            return_evidence_available=True,
            institution="Fixture Bank B",
            source_reference=(
                "fixture_savings_statement"
            ),
            notes=(
                "Deterministic validation fixture."
            ),
        ),
    )

    complete_baseline = (
        build_model_company_cash_baseline(
            as_of=AS_OF,
            balances=complete_balances,
        )
    )

    complete_assessment = (
        build_cash_baseline_return_assessment(
            assessment_id=(
                "model_company_complete_cash_return"
            ),
            baseline=complete_baseline,
        )
    )

    expected_blended_return_pct = (
        (
            2_000_000.0 * 0.50
            + 3_000_000.0 * 1.50
        )
        / 5_000_000.0
    )

    print(
        f"Total cash:                    "
        f"EUR {complete_baseline.total_cash_eur:,.0f}"
    )

    print(
        f"Return evidence coverage:      "
        f"{complete_assessment.return_evidence_coverage_pct:.1f}%"
    )

    print(
        f"Blended annual return:         "
        f"{complete_assessment.blended_annual_return_pct:.3f}%"
    )

    print(
        f"Assessment status:             "
        f"{complete_assessment.assessment_status}"
    )

    assert (
        complete_assessment.assessment_status
        == "complete"
    )

    assert (
        complete_assessment.return_evidence_coverage_pct
        == 100.0
    )

    assert (
        complete_assessment.blended_annual_return_pct
        == expected_blended_return_pct
    )

    print()
    print("CASE 4 — RECONCILIATION GUARD")
    print()

    reconciliation_rejected = False

    try:
        build_model_company_cash_baseline(
            as_of=AS_OF,
            balances=(
                CashBalance(
                    balance_id="fixture_bad_total",
                    label="Incomplete treasury cash",
                    balance_type="operating_account",
                    balance_eur=4_000_000.0,
                    annual_return_pct=1.00,
                    return_evidence_available=True,
                    institution="Fixture Bank",
                    source_reference=(
                        "fixture_statement"
                    ),
                ),
            ),
        )
    except ValueError:
        reconciliation_rejected = True

    print(
        f"Non-reconciling baseline rejected: "
        f"{reconciliation_rejected}"
    )

    assert reconciliation_rejected

    print()
    print("-" * 100)
    print()
    print("MILESTONE 15C ASSERTIONS")
    print()

    print(
        "Default cash remains unresolved:       yes"
    )

    print(
        "Multiple cash balances supported:      yes"
    )

    print(
        "Partial evidence stays incomplete:     yes"
    )

    print(
        "Complete evidence produces blend:      yes"
    )

    print(
        "Treasury reconciliation enforced:      yes"
    )

    print()

    print(
        "All Milestone 15C current-cash "
        "baseline assertions passed."
    )


if __name__ == "__main__":
    main()
