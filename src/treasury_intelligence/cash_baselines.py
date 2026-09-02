from __future__ import annotations

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
    CashBaseline,
)


def build_model_company_cash_baseline(
    as_of: str,
    balances: tuple[CashBalance, ...] | None = None,
) -> CashBaseline:
    if not as_of:
        raise ValueError(
            "Model-company cash baseline requires an "
            "as-of value."
        )

    treasury_capital_eur = (
        MODEL_COMPANY_MANDATE.treasury_capital_eur
    )

    if balances is None:
        balances = (
            CashBalance(
                balance_id=(
                    "model_company_unresolved_"
                    "corporate_cash"
                ),
                label="Unresolved corporate cash",
                balance_type="other_cash",
                balance_eur=treasury_capital_eur,
                annual_return_pct=None,
                return_evidence_available=False,
                institution=None,
                source_reference=None,
                notes=(
                    "Verified account-level cash "
                    "evidence has not yet been supplied. "
                    "The balance is represented without "
                    "inventing a bank, account type, or "
                    "cash return."
                ),
            ),
        )

    total_cash_eur = sum(
        balance.balance_eur
        for balance in balances
    )

    if (
        abs(
            total_cash_eur
            - treasury_capital_eur
        )
        > 0.01
    ):
        raise ValueError(
            "Model-company cash balances must "
            "reconcile exactly to treasury capital."
        )

    return CashBaseline(
        baseline_id=(
            "model_company_current_cash_"
            + as_of.replace("-", "_")
        ),
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        as_of=as_of,
        total_cash_eur=total_cash_eur,
        balances=balances,
        notes=(
            "Current model-company corporate cash "
            "baseline. Supplied balances are treated "
            "as treasury-state inputs rather than "
            "market opportunities."
        ),
    )
