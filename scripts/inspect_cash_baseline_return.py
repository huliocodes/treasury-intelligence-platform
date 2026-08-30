from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.cash_returns import (
    build_cash_baseline_return_assessment,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
    CashBaseline,
)


AS_OF = "2026-08-30"


def print_assessment(
    label: str,
    baseline: CashBaseline,
) -> None:
    assessment = (
        build_cash_baseline_return_assessment(
            assessment_id=(
                f"{baseline.baseline_id}_return"
            ),
            baseline=baseline,
            notes=(
                "Deterministic 8A.2 cash-return "
                "assessment fixture."
            ),
        )
    )

    print(label)
    print()

    print(
        f"Baseline ID:                  "
        f"{assessment.baseline_id}"
    )

    print(
        f"Total cash:                   "
        f"EUR {assessment.total_cash_eur:,.0f}"
    )

    print(
        f"Known-return cash:            "
        f"EUR "
        f"{assessment.known_return_balance_eur:,.0f}"
    )

    print(
        f"Unknown-return cash:          "
        f"EUR "
        f"{assessment.unknown_return_balance_eur:,.0f}"
    )

    print(
        f"Return evidence coverage:     "
        f"{assessment.return_evidence_coverage_pct:.2f}%"
    )

    print(
        f"Assessment status:            "
        f"{assessment.assessment_status}"
    )

    if (
        assessment.blended_annual_return_pct
        is None
    ):
        blended_return_text = "UNKNOWN"
    else:
        blended_return_text = (
            f"{assessment.blended_annual_return_pct:.3f}%"
        )

    print(
        f"Blended annual return:        "
        f"{blended_return_text}"
    )

    if assessment.evidence_requirements:
        print()
        print("EVIDENCE REQUIREMENTS")
        print()

        for requirement in (
            assessment.evidence_requirements
        ):
            print(
                f"  - {requirement}"
            )

    print()
    print("-" * 100)
    print()


def main() -> None:
    mandate = MODEL_COMPANY_MANDATE

    print(
        "TREASURY CASH BASELINE RETURN ANALYSIS"
    )
    print()

    print(
        "A defensible blended return is calculated "
        "only when return evidence covers the entire "
        "cash baseline."
    )

    print()

    print(
        "Known balances are not extrapolated across "
        "cash whose return remains unknown."
    )

    print()

    print("-" * 100)
    print()

    mixed_baseline = CashBaseline(
        baseline_id=(
            "fixture_mixed_cash_baseline"
        ),
        mandate_id=mandate.mandate_id,
        as_of=AS_OF,
        total_cash_eur=5_000_000,
        balances=(
            CashBalance(
                balance_id=(
                    "fixture_operating_cash"
                ),
                label="Operating account",
                balance_type=(
                    "operating_account"
                ),
                balance_eur=1_500_000,
                annual_return_pct=0.0,
                return_evidence_available=True,
                institution="Fixture Bank A",
                source_reference=(
                    "fixture_account_statement"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_savings_cash"
                ),
                label="Savings account",
                balance_type=(
                    "savings_account"
                ),
                balance_eur=1_000_000,
                annual_return_pct=1.20,
                return_evidence_available=True,
                institution="Fixture Bank B",
                source_reference=(
                    "fixture_rate_confirmation"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_term_deposit"
                ),
                label="Short term deposit",
                balance_type="term_deposit",
                balance_eur=1_500_000,
                annual_return_pct=1.50,
                return_evidence_available=True,
                institution="Fixture Bank C",
                source_reference=(
                    "fixture_deposit_confirmation"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_unknown_cash"
                ),
                label="Other corporate cash",
                balance_type="other_cash",
                balance_eur=1_000_000,
                annual_return_pct=None,
                return_evidence_available=False,
                institution="Fixture Bank D",
            ),
        ),
        notes=(
            "Mixed-evidence 8A.2 fixture."
        ),
    )

    print_assessment(
        label=(
            "CASE 1 — INCOMPLETE RETURN EVIDENCE"
        ),
        baseline=mixed_baseline,
    )

    complete_baseline = CashBaseline(
        baseline_id=(
            "fixture_complete_cash_baseline"
        ),
        mandate_id=mandate.mandate_id,
        as_of=AS_OF,
        total_cash_eur=5_000_000,
        balances=(
            CashBalance(
                balance_id=(
                    "fixture_complete_operating"
                ),
                label="Operating account",
                balance_type=(
                    "operating_account"
                ),
                balance_eur=1_500_000,
                annual_return_pct=0.0,
                return_evidence_available=True,
                institution="Fixture Bank A",
                source_reference=(
                    "fixture_account_statement"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_complete_savings"
                ),
                label="Savings account",
                balance_type=(
                    "savings_account"
                ),
                balance_eur=1_000_000,
                annual_return_pct=1.20,
                return_evidence_available=True,
                institution="Fixture Bank B",
                source_reference=(
                    "fixture_rate_confirmation"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_complete_deposit"
                ),
                label="Short term deposit",
                balance_type="term_deposit",
                balance_eur=1_500_000,
                annual_return_pct=1.50,
                return_evidence_available=True,
                institution="Fixture Bank C",
                source_reference=(
                    "fixture_deposit_confirmation"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_complete_other"
                ),
                label="Remunerated corporate cash",
                balance_type="other_cash",
                balance_eur=1_000_000,
                annual_return_pct=0.75,
                return_evidence_available=True,
                institution="Fixture Bank D",
                source_reference=(
                    "fixture_rate_confirmation_d"
                ),
            ),
        ),
        notes=(
            "Complete-evidence 8A.2 fixture."
        ),
    )

    print_assessment(
        label=(
            "CASE 2 — COMPLETE RETURN EVIDENCE"
        ),
        baseline=complete_baseline,
    )

    all_zero_baseline = CashBaseline(
        baseline_id=(
            "fixture_zero_return_baseline"
        ),
        mandate_id=mandate.mandate_id,
        as_of=AS_OF,
        total_cash_eur=5_000_000,
        balances=(
            CashBalance(
                balance_id=(
                    "fixture_zero_return_cash"
                ),
                label="Verified zero-return cash",
                balance_type=(
                    "operating_account"
                ),
                balance_eur=5_000_000,
                annual_return_pct=0.0,
                return_evidence_available=True,
                institution="Fixture Bank",
                source_reference=(
                    "fixture_zero_rate_evidence"
                ),
            ),
        ),
        notes=(
            "Known-zero 8A.2 fixture."
        ),
    )

    print_assessment(
        label=(
            "CASE 3 — VERIFIED ZERO RETURN"
        ),
        baseline=all_zero_baseline,
    )

    print("INTERPRETATION")
    print()

    print(
        "Case 1 must remain UNKNOWN because only "
        "80 percent of treasury cash has return evidence."
    )

    print()

    print(
        "Case 2 has complete evidence and therefore "
        "produces a defensible balance-weighted return."
    )

    print()

    print(
        "Case 3 proves that a verified zero-percent "
        "treasury return remains a valid known economic "
        "baseline rather than being confused with "
        "missing evidence."
    )


if __name__ == "__main__":
    main()