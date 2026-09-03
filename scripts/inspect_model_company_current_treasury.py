from __future__ import annotations

from treasury_intelligence.current_treasury import (
    build_model_company_current_treasury,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
)

from treasury_intelligence.models.treasury_state import (
    TreasuryPosition,
)


AS_OF = "2026-09-03"


def build_position(
    *,
    position_id: str,
    label: str,
    current_value_eur: float,
) -> TreasuryPosition:
    return TreasuryPosition(
        position_id=position_id,
        instrument_id=(
            position_id + "_instrument"
        ),
        market_id=(
            position_id + "_market"
        ),
        access_route_id=(
            position_id + "_access"
        ),
        label=label,
        current_value_eur=current_value_eur,
    )


def build_cash(
    *,
    balance_id: str,
    label: str,
    balance_eur: float,
    annual_return_pct: float | None = None,
    evidence_available: bool = False,
) -> CashBalance:
    return CashBalance(
        balance_id=balance_id,
        label=label,
        balance_type="operating_account",
        balance_eur=balance_eur,
        annual_return_pct=annual_return_pct,
        return_evidence_available=(
            evidence_available
        ),
        institution=None,
        source_reference=None,
    )


def main() -> None:
    print(
        "MILESTONE 15F — PRODUCTION CURRENT TREASURY INPUT"
    )
    print()

    print(
        "CASE 1 — DEFAULT FULL-CASH CURRENT TREASURY"
    )
    print()

    full_cash = (
        build_model_company_current_treasury(
            as_of=AS_OF,
        )
    )

    print(
        f"Positions:                      "
        f"{len(full_cash.state.positions)}"
    )
    print(
        f"Invested capital:               "
        f"EUR {full_cash.state.invested_capital_eur:,.0f}"
    )
    print(
        f"Residual cash:                  "
        f"EUR {full_cash.state.unallocated_capital_eur:,.0f}"
    )
    print(
        f"Cash balances:                  "
        f"{len(full_cash.cash_baseline.balances)}"
    )

    assert full_cash.state.invested_capital_eur == 0
    assert (
        full_cash.state.unallocated_capital_eur
        == 5_000_000
    )
    assert (
        full_cash.cash_baseline.total_cash_eur
        == 5_000_000
    )

    print()
    print(
        "CASE 2 — MIXED INVESTED + CASH TREASURY"
    )
    print()

    mixed = (
        build_model_company_current_treasury(
            as_of=AS_OF,
            positions=(
                build_position(
                    position_id="current_position_a",
                    label="Current Position A",
                    current_value_eur=2_000_000,
                ),
                build_position(
                    position_id="current_position_b",
                    label="Current Position B",
                    current_value_eur=1_000_000,
                ),
            ),
            cash_balances=(
                build_cash(
                    balance_id="cash_a",
                    label="Corporate Cash A",
                    balance_eur=1_200_000,
                    annual_return_pct=1.0,
                    evidence_available=True,
                ),
                build_cash(
                    balance_id="cash_b",
                    label="Corporate Cash B",
                    balance_eur=800_000,
                    annual_return_pct=None,
                    evidence_available=False,
                ),
            ),
        )
    )

    print(
        f"Positions:                      "
        f"{len(mixed.state.positions)}"
    )
    print(
        f"Invested capital:               "
        f"EUR {mixed.state.invested_capital_eur:,.0f}"
    )
    print(
        f"Residual cash:                  "
        f"EUR {mixed.state.unallocated_capital_eur:,.0f}"
    )
    print(
        f"Cash balances:                  "
        f"{len(mixed.cash_baseline.balances)}"
    )

    assert mixed.state.invested_capital_eur == 3_000_000
    assert (
        mixed.state.unallocated_capital_eur
        == 2_000_000
    )
    assert (
        mixed.cash_baseline.total_cash_eur
        == 2_000_000
    )
    assert len(mixed.state.positions) == 2
    assert len(mixed.cash_baseline.balances) == 2

    print()
    print(
        "CASE 3 — FULLY INVESTED TREASURY"
    )
    print()

    fully_invested = (
        build_model_company_current_treasury(
            as_of=AS_OF,
            positions=(
                build_position(
                    position_id="full_position",
                    label="Full Treasury Position",
                    current_value_eur=5_000_000,
                ),
            ),
        )
    )

    print(
        f"Invested capital:               "
        f"EUR {fully_invested.state.invested_capital_eur:,.0f}"
    )
    print(
        f"Residual cash:                  "
        f"EUR {fully_invested.state.unallocated_capital_eur:,.0f}"
    )
    print(
        f"Cash balances:                  "
        f"{len(fully_invested.cash_baseline.balances)}"
    )

    assert (
        fully_invested.state.invested_capital_eur
        == 5_000_000
    )
    assert (
        fully_invested.state.unallocated_capital_eur
        == 0
    )
    assert (
        fully_invested.cash_baseline.total_cash_eur
        == 0
    )
    assert (
        fully_invested.cash_baseline.balances
        == ()
    )

    print()
    print(
        "CASE 4 — CASH MUST RECONCILE TO RESIDUAL CAPITAL"
    )
    print()

    reconciliation_rejected = False

    try:
        build_model_company_current_treasury(
            as_of=AS_OF,
            positions=(
                build_position(
                    position_id="reconciliation_position",
                    label="Reconciliation Position",
                    current_value_eur=3_000_000,
                ),
            ),
            cash_balances=(
                build_cash(
                    balance_id="wrong_cash",
                    label="Wrong Cash Total",
                    balance_eur=1_500_000,
                ),
            ),
        )
    except ValueError:
        reconciliation_rejected = True

    print(
        f"Non-reconciling input rejected: "
        f"{reconciliation_rejected}"
    )

    assert reconciliation_rejected

    print()
    print(
        "CASE 5 — POSITION VALUES CANNOT EXCEED TREASURY"
    )
    print()

    oversized_rejected = False

    try:
        build_model_company_current_treasury(
            as_of=AS_OF,
            positions=(
                build_position(
                    position_id="oversized_position",
                    label="Oversized Position",
                    current_value_eur=5_000_001,
                ),
            ),
        )
    except ValueError:
        oversized_rejected = True

    print(
        f"Oversized treasury rejected:    "
        f"{oversized_rejected}"
    )

    assert oversized_rejected

    print()
    print(
        "-" * 100
    )
    print()
    print(
        "MILESTONE 15F ASSERTIONS"
    )
    print()
    print(
        "Default full-cash state supported:       yes"
    )
    print(
        "Mixed invested/cash state supported:     yes"
    )
    print(
        "Fully invested state supported:          yes"
    )
    print(
        "Cash/residual reconciliation enforced:   yes"
    )
    print(
        "Mandate capital ceiling enforced:        yes"
    )
    print()
    print(
        "All Milestone 15F current-treasury "
        "input assertions passed."
    )


if __name__ == "__main__":
    main()
