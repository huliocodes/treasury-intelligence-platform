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
    total_cash_eur: float | None = None,
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

    if total_cash_eur is None:
        total_cash_eur = treasury_capital_eur

    if total_cash_eur < 0:
        raise ValueError(
            "Model-company cash baseline cannot contain "
            "negative cash."
        )

    if (
        total_cash_eur
        - treasury_capital_eur
        > 0.01
    ):
        raise ValueError(
            "Model-company cash baseline cannot exceed "
            "mandate treasury capital."
        )

    if balances is None:
        if total_cash_eur == 0:
            balances = ()

        else:
            balances = (
                CashBalance(
                    balance_id=(
                        "model_company_unresolved_"
                        "corporate_cash"
                    ),
                    label="Unresolved corporate cash",
                    balance_type="other_cash",
                    balance_eur=total_cash_eur,
                    annual_return_pct=None,
                    return_evidence_available=False,
                    institution=None,
                    source_reference=None,
                    notes=(
                        "Verified account-level cash "
                        "evidence has not yet been supplied. "
                        "The current unallocated treasury "
                        "balance is represented without "
                        "inventing a bank, account type, or "
                        "cash return."
                    ),
                ),
            )

    supplied_balance_total_eur = sum(
        balance.balance_eur
        for balance in balances
    )

    if (
        abs(
            supplied_balance_total_eur
            - total_cash_eur
        )
        > 0.01
    ):
        raise ValueError(
            "Model-company cash balances must reconcile "
            "exactly to the requested current cash total."
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
            "Current model-company unallocated corporate "
            "cash baseline. The baseline represents the "
            "cash portion of the current treasury state, "
            "which may be all, part, or none of mandate "
            "treasury capital."
        ),
    )
