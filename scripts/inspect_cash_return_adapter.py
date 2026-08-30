from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.cash_returns import (
    build_cash_baseline_return_assessment,
    build_unallocated_return_input,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
    CashBaseline,
)


AS_OF = "2026-08-30"


def print_adapter_result(
    label: str,
    baseline: CashBaseline,
) -> None:
    assessment = (
        build_cash_baseline_return_assessment(
            assessment_id=(
                f"{baseline.baseline_id}_return"
            ),
            baseline=baseline,
        )
    )

    review_input = (
        build_unallocated_return_input(
            assessment=assessment,
            notes=(
                "Review-layer unallocated return "
                "derived from cash-baseline economics."
            ),
        )
    )

    print(label)
    print()

    print(
        f"Assessment status:            "
        f"{assessment.assessment_status}"
    )

    print(
        f"Evidence coverage:            "
        f"{assessment.return_evidence_coverage_pct:.2f}%"
    )

    if (
        assessment.blended_annual_return_pct
        is None
    ):
        assessment_return_text = "UNKNOWN"
    else:
        assessment_return_text = (
            f"{assessment.blended_annual_return_pct:.3f}%"
        )

    print(
        f"Assessment return:            "
        f"{assessment_return_text}"
    )

    print(
        f"Review evidence available:    "
        f"{review_input.evidence_available}"
    )

    if review_input.annual_return_pct is None:
        review_return_text = "UNKNOWN"
    else:
        review_return_text = (
            f"{review_input.annual_return_pct:.3f}%"
        )

    print(
        f"Review annual return:         "
        f"{review_return_text}"
    )

    print(
        f"Source reference:             "
        f"{review_input.source_reference}"
    )

    print()
    print("-" * 100)
    print()


def main() -> None:
    mandate = MODEL_COMPANY_MANDATE

    print(
        "CASH BASELINE TO REVIEW RETURN ADAPTER"
    )
    print()

    print(
        "The adapter exposes a numeric unallocated "
        "treasury return only when the underlying "
        "cash-baseline return assessment is complete."
    )

    print()

    print("-" * 100)
    print()

    incomplete_baseline = CashBaseline(
        baseline_id=(
            "fixture_adapter_incomplete"
        ),
        mandate_id=mandate.mandate_id,
        as_of=AS_OF,
        total_cash_eur=5_000_000,
        balances=(
            CashBalance(
                balance_id=(
                    "fixture_known_cash"
                ),
                label="Known-return cash",
                balance_type=(
                    "savings_account"
                ),
                balance_eur=4_000_000,
                annual_return_pct=1.0,
                return_evidence_available=True,
                institution="Fixture Bank A",
                source_reference=(
                    "fixture_known_rate"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_unknown_cash"
                ),
                label="Unknown-return cash",
                balance_type="other_cash",
                balance_eur=1_000_000,
                annual_return_pct=None,
                return_evidence_available=False,
                institution="Fixture Bank B",
            ),
        ),
    )

    print_adapter_result(
        label=(
            "CASE 1 — INCOMPLETE CASH ECONOMICS"
        ),
        baseline=incomplete_baseline,
    )

    complete_baseline = CashBaseline(
        baseline_id=(
            "fixture_adapter_complete"
        ),
        mandate_id=mandate.mandate_id,
        as_of=AS_OF,
        total_cash_eur=5_000_000,
        balances=(
            CashBalance(
                balance_id=(
                    "fixture_complete_a"
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
                    "fixture_statement_a"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_complete_b"
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
                    "fixture_rate_b"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_complete_c"
                ),
                label="Short term deposit",
                balance_type="term_deposit",
                balance_eur=1_500_000,
                annual_return_pct=1.50,
                return_evidence_available=True,
                institution="Fixture Bank C",
                source_reference=(
                    "fixture_rate_c"
                ),
            ),
            CashBalance(
                balance_id=(
                    "fixture_complete_d"
                ),
                label="Remunerated cash",
                balance_type="other_cash",
                balance_eur=1_000_000,
                annual_return_pct=0.75,
                return_evidence_available=True,
                institution="Fixture Bank D",
                source_reference=(
                    "fixture_rate_d"
                ),
            ),
        ),
    )

    print_adapter_result(
        label=(
            "CASE 2 — COMPLETE CASH ECONOMICS"
        ),
        baseline=complete_baseline,
    )

    zero_baseline = CashBaseline(
        baseline_id=(
            "fixture_adapter_zero"
        ),
        mandate_id=mandate.mandate_id,
        as_of=AS_OF,
        total_cash_eur=5_000_000,
        balances=(
            CashBalance(
                balance_id=(
                    "fixture_verified_zero"
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
                    "fixture_zero_rate"
                ),
            ),
        ),
    )

    print_adapter_result(
        label=(
            "CASE 3 — VERIFIED ZERO CASH RETURN"
        ),
        baseline=zero_baseline,
    )

    print("INTERPRETATION")
    print()

    print(
        "Incomplete cash economics cross into the "
        "review layer as UNKNOWN with evidence false."
    )

    print()

    print(
        "Complete cash economics cross into the "
        "review layer with their defensible blended "
        "annual return."
    )

    print()

    print(
        "A verified zero-percent return crosses the "
        "same boundary as 0.000 percent with evidence "
        "true, preserving the distinction between "
        "zero and missing evidence."
    )


if __name__ == "__main__":
    main()