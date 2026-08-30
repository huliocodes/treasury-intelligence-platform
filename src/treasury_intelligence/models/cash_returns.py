from __future__ import annotations

from dataclasses import dataclass


CASH_RETURN_ASSESSMENT_STATUSES = (
    "complete",
    "incomplete",
    "not_applicable",
)


@dataclass(frozen=True)
class CashBaselineReturnAssessment:
    assessment_id: str
    baseline_id: str
    total_cash_eur: float
    known_return_balance_eur: float
    unknown_return_balance_eur: float
    return_evidence_coverage_pct: float
    blended_annual_return_pct: float | None
    assessment_status: str
    evidence_requirements: tuple[str, ...]
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.assessment_id:
            raise ValueError(
                "Cash return assessment ID is required."
            )

        if not self.baseline_id:
            raise ValueError(
                "Cash baseline ID is required."
            )

        if self.total_cash_eur < 0:
            raise ValueError(
                "Total cash cannot be negative."
            )

        if self.known_return_balance_eur < 0:
            raise ValueError(
                "Known-return balance cannot be negative."
            )

        if self.unknown_return_balance_eur < 0:
            raise ValueError(
                "Unknown-return balance cannot be negative."
            )

        reconciled_total = (
            self.known_return_balance_eur
            + self.unknown_return_balance_eur
        )

        if (
            abs(
                reconciled_total
                - self.total_cash_eur
            )
            > 0.01
        ):
            raise ValueError(
                "Known and unknown return balances must "
                "reconcile to total cash."
            )

        if not (
            0.0
            <= self.return_evidence_coverage_pct
            <= 100.0
        ):
            raise ValueError(
                "Return evidence coverage must be "
                "between 0 and 100 percent."
            )

        if (
            self.assessment_status
            not in CASH_RETURN_ASSESSMENT_STATUSES
        ):
            raise ValueError(
                "Unsupported cash return assessment status: "
                f"{self.assessment_status}"
            )

        if self.assessment_status == "complete":
            if self.total_cash_eur <= 0:
                raise ValueError(
                    "Complete cash return assessment "
                    "requires positive total cash."
                )

            if (
                self.return_evidence_coverage_pct
                < 100.0
            ):
                raise ValueError(
                    "Complete cash return assessment "
                    "requires 100 percent evidence coverage."
                )

            if (
                self.blended_annual_return_pct
                is None
            ):
                raise ValueError(
                    "Complete cash return assessment "
                    "requires a blended annual return."
                )

            if self.evidence_requirements:
                raise ValueError(
                    "Complete cash return assessment "
                    "cannot contain evidence requirements."
                )

        if self.assessment_status == "incomplete":
            if (
                self.blended_annual_return_pct
                is not None
            ):
                raise ValueError(
                    "Incomplete cash return assessment "
                    "must keep blended return unknown."
                )

            if not self.evidence_requirements:
                raise ValueError(
                    "Incomplete cash return assessment "
                    "requires evidence requirements."
                )

        if self.assessment_status == "not_applicable":
            if self.total_cash_eur != 0:
                raise ValueError(
                    "Not-applicable cash return assessment "
                    "requires zero total cash."
                )

            if (
                self.blended_annual_return_pct
                is not None
            ):
                raise ValueError(
                    "Not-applicable cash return assessment "
                    "must not contain a blended return."
                )