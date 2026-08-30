from __future__ import annotations

from dataclasses import dataclass


CASH_BALANCE_TYPES = (
    "operating_account",
    "savings_account",
    "term_deposit",
    "notice_account",
    "overnight_sweep",
    "broker_cash",
    "other_cash",
)


@dataclass(frozen=True)
class CashBalance:
    balance_id: str
    label: str
    balance_type: str
    balance_eur: float
    annual_return_pct: float | None
    return_evidence_available: bool
    institution: str | None = None
    source_reference: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.balance_id:
            raise ValueError(
                "Cash balance ID is required."
            )

        if not self.label:
            raise ValueError(
                "Cash balance label is required."
            )

        if (
            self.balance_type
            not in CASH_BALANCE_TYPES
        ):
            raise ValueError(
                "Unsupported cash balance type: "
                f"{self.balance_type}"
            )

        if self.balance_eur <= 0:
            raise ValueError(
                "Cash balance must be greater than zero."
            )

        if (
            self.return_evidence_available
            and self.annual_return_pct is None
        ):
            raise ValueError(
                "Annual return is required when return "
                "evidence is available."
            )

        if (
            not self.return_evidence_available
            and self.annual_return_pct is not None
        ):
            raise ValueError(
                "Annual return must remain unknown when "
                "return evidence is unavailable."
            )

        if (
            self.annual_return_pct is not None
            and self.annual_return_pct < 0
        ):
            raise ValueError(
                "Cash baseline annual return cannot be "
                "negative in the current model."
            )


@dataclass(frozen=True)
class CashBaseline:
    baseline_id: str
    mandate_id: str
    as_of: str
    total_cash_eur: float
    balances: tuple[CashBalance, ...]
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.baseline_id:
            raise ValueError(
                "Cash baseline ID is required."
            )

        if not self.mandate_id:
            raise ValueError(
                "Mandate ID is required."
            )

        if not self.as_of:
            raise ValueError(
                "Cash baseline as-of value is required."
            )

        if self.total_cash_eur < 0:
            raise ValueError(
                "Total cash cannot be negative."
            )

        balance_total = sum(
            balance.balance_eur
            for balance in self.balances
        )

        if (
            abs(
                balance_total
                - self.total_cash_eur
            )
            > 0.01
        ):
            raise ValueError(
                "Cash balances must sum exactly to "
                "total cash."
            )

        balance_ids = [
            balance.balance_id
            for balance in self.balances
        ]

        if (
            len(balance_ids)
            != len(set(balance_ids))
        ):
            raise ValueError(
                "Cash balance IDs must be unique."
            )