from __future__ import annotations

from dataclasses import dataclass

from treasury_intelligence.analytics.treasury_state import (
    build_treasury_state,
)

from treasury_intelligence.cash_baselines import (
    build_model_company_cash_baseline,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
    CashBaseline,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryPosition,
    TreasuryState,
)


@dataclass(frozen=True)
class ModelCompanyCurrentTreasury:
    state: TreasuryState
    cash_baseline: CashBaseline

    def __post_init__(self) -> None:
        if (
            self.state.mandate_id
            != MODEL_COMPANY_MANDATE.mandate_id
        ):
            raise ValueError(
                "Current treasury state must use the "
                "model-company mandate."
            )

        if (
            self.cash_baseline.mandate_id
            != self.state.mandate_id
        ):
            raise ValueError(
                "Current treasury state and cash baseline "
                "must use the same mandate."
            )

        if (
            self.cash_baseline.as_of
            != self.state.as_of
        ):
            raise ValueError(
                "Current treasury state and cash baseline "
                "must use the same as-of value."
            )

        if (
            abs(
                self.cash_baseline.total_cash_eur
                - self.state.unallocated_capital_eur
            )
            > 0.01
        ):
            raise ValueError(
                "Current cash baseline must reconcile "
                "to unallocated treasury capital."
            )


def build_model_company_current_treasury(
    *,
    as_of: str,
    positions: tuple[
        TreasuryPosition,
        ...
    ] = (),
    cash_balances: tuple[
        CashBalance,
        ...
    ] | None = None,
    notes: str | None = None,
) -> ModelCompanyCurrentTreasury:
    if not as_of:
        raise ValueError(
            "Model-company current treasury requires "
            "an as-of value."
        )

    state = build_treasury_state(
        state_id=(
            "model_company_current_treasury_"
            + as_of.replace("-", "_")
        ),
        mandate=MODEL_COMPANY_MANDATE,
        as_of=as_of,
        positions=positions,
        notes=notes,
    )

    cash_baseline = (
        build_model_company_cash_baseline(
            as_of=as_of,
            total_cash_eur=(
                state.unallocated_capital_eur
            ),
            balances=cash_balances,
        )
    )

    return ModelCompanyCurrentTreasury(
        state=state,
        cash_baseline=cash_baseline,
    )
