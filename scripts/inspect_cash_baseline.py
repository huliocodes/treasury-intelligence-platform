from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
    CashBaseline,
)


AS_OF = "2026-08-30"


def print_baseline(
    label: str,
    baseline: CashBaseline,
) -> None:
    print(label)
    print()

    print(
        f"Baseline ID:                  "
        f"{baseline.baseline_id}"
    )

    print(
        f"Mandate:                      "
        f"{baseline.mandate_id}"
    )

    print(
        f"As of:                        "
        f"{baseline.as_of}"
    )

    print(
        f"Total cash:                   "
        f"EUR {baseline.total_cash_eur:,.0f}"
    )

    print(
        f"Balance count:                "
        f"{len(baseline.balances)}"
    )

    print()
    print("BALANCES")
    print()

    for balance in baseline.balances:
        allocation_pct = (
            balance.balance_eur
            / baseline.total_cash_eur
            * 100
        )

        if balance.annual_return_pct is None:
            return_text = "UNKNOWN"
        else:
            return_text = (
                f"{balance.annual_return_pct:.3f}%"
            )

        print(
            f"  {balance.label:<24} "
            f"EUR {balance.balance_eur:>12,.0f} | "
            f"{allocation_pct:>6.2f}% | "
            f"{return_text:>8}"
        )

        print(
            f"    Type:                     "
            f"{balance.balance_type}"
        )

        print(
            f"    Return evidence:          "
            f"{balance.return_evidence_available}"
        )

        if balance.institution:
            print(
                f"    Institution:              "
                f"{balance.institution}"
            )

        if balance.source_reference:
            print(
                f"    Source reference:         "
                f"{balance.source_reference}"
            )

        print()

    print("-" * 100)
    print()


def main() -> None:
    mandate = MODEL_COMPANY_MANDATE

    print("TREASURY CASH BASELINE MODEL")
    print()

    print(
        "The cash baseline represents where currently "
        "unallocated treasury capital actually sits."
    )

    print()

    print(
        "A known zero return and an unknown return are "
        "different evidence states."
    )

    print()

    print("-" * 100)
    print()

    known_zero = CashBalance(
        balance_id="fixture_operating_cash",
        label="Operating account",
        balance_type="operating_account",
        balance_eur=1_500_000,
        annual_return_pct=0.0,
        return_evidence_available=True,
        institution="Fixture Bank A",
        source_reference=(
            "fixture_account_statement"
        ),
        notes=(
            "Deterministic 8A.1 fixture demonstrating "
            "a known zero cash return."
        ),
    )

    known_savings = CashBalance(
        balance_id="fixture_savings_cash",
        label="Savings account",
        balance_type="savings_account",
        balance_eur=1_000_000,
        annual_return_pct=1.20,
        return_evidence_available=True,
        institution="Fixture Bank B",
        source_reference=(
            "fixture_rate_confirmation"
        ),
        notes=(
            "Deterministic 8A.1 fixture demonstrating "
            "a known positive cash return."
        ),
    )

    known_deposit = CashBalance(
        balance_id="fixture_term_deposit",
        label="Short term deposit",
        balance_type="term_deposit",
        balance_eur=1_500_000,
        annual_return_pct=1.50,
        return_evidence_available=True,
        institution="Fixture Bank C",
        source_reference=(
            "fixture_deposit_confirmation"
        ),
        notes=(
            "Deterministic 8A.1 fixture demonstrating "
            "a known deposit return."
        ),
    )

    unknown_cash = CashBalance(
        balance_id="fixture_unknown_cash",
        label="Other corporate cash",
        balance_type="other_cash",
        balance_eur=1_000_000,
        annual_return_pct=None,
        return_evidence_available=False,
        institution="Fixture Bank D",
        source_reference=None,
        notes=(
            "Deterministic 8A.1 fixture demonstrating "
            "an unresolved cash return."
        ),
    )

    mixed_baseline = CashBaseline(
        baseline_id=(
            "fixture_mixed_cash_baseline"
        ),
        mandate_id=mandate.mandate_id,
        as_of=AS_OF,
        total_cash_eur=(
            mandate.treasury_capital_eur
        ),
        balances=(
            known_zero,
            known_savings,
            known_deposit,
            unknown_cash,
        ),
        notes=(
            "Deterministic 8A.1 model-company "
            "cash-baseline fixture."
        ),
    )

    print_baseline(
        label=(
            "CASE 1 — MIXED CASH BASELINE"
        ),
        baseline=mixed_baseline,
    )

    print(
        "CASE 2 — KNOWN ZERO RETURN IS VALID"
    )
    print()

    zero_return_balance = CashBalance(
        balance_id="fixture_known_zero",
        label="Known zero account",
        balance_type="operating_account",
        balance_eur=100_000,
        annual_return_pct=0.0,
        return_evidence_available=True,
    )

    print(
        f"Annual return:                "
        f"{zero_return_balance.annual_return_pct:.3f}%"
    )

    print(
        f"Evidence available:           "
        f"{zero_return_balance.return_evidence_available}"
    )

    print()

    print("-" * 100)
    print()

    print(
        "CASE 3 — UNKNOWN RETURN MUST REMAIN UNKNOWN"
    )
    print()

    try:
        CashBalance(
            balance_id=(
                "fixture_invalid_unknown"
            ),
            label="Invalid unknown account",
            balance_type="operating_account",
            balance_eur=100_000,
            annual_return_pct=0.0,
            return_evidence_available=False,
        )

    except ValueError as exc:
        print(
            "Balance rejected by gate:      True"
        )

        print(
            f"Reason:                        "
            f"{exc}"
        )

    else:
        raise AssertionError(
            "Unknown-return cash balance unexpectedly "
            "accepted a numeric return."
        )

    print()

    print("-" * 100)
    print()

    print(
        "CASE 4 — BALANCES MUST RECONCILE "
        "TO TOTAL CASH"
    )
    print()

    try:
        CashBaseline(
            baseline_id=(
                "fixture_invalid_total"
            ),
            mandate_id=(
                mandate.mandate_id
            ),
            as_of=AS_OF,
            total_cash_eur=5_000_000,
            balances=(
                known_zero,
                known_savings,
            ),
        )

    except ValueError as exc:
        print(
            "Baseline rejected by gate:     True"
        )

        print(
            f"Reason:                        "
            f"{exc}"
        )

    else:
        raise AssertionError(
            "Non-reconciling cash baseline "
            "unexpectedly passed validation."
        )

    print()

    print("-" * 100)
    print()

    print("INTERPRETATION")
    print()

    print(
        "The baseline records factual current cash "
        "balances and their return-evidence state."
    )

    print(
        "It does not yet calculate a blended return."
    )

    print(
        "A balance earning a verified zero percent "
        "is explicitly different from a balance whose "
        "return is unknown."
    )

    print(
        "The next analytical layer can therefore refuse "
        "to calculate a defensible blended treasury "
        "return whenever economically relevant balance "
        "evidence remains unresolved."
    )


if __name__ == "__main__":
    main()