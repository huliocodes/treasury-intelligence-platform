from __future__ import annotations

from treasury_intelligence.models.cash_baselines import (
    CashBaseline,
)

from treasury_intelligence.models.cash_returns import (
    CashBaselineReturnAssessment,
)

from treasury_intelligence.models.economic_comparisons import (
    UnallocatedReturnInput,
)


def build_cash_baseline_return_assessment(
    assessment_id: str,
    baseline: CashBaseline,
    notes: str | None = None,
) -> CashBaselineReturnAssessment:
    if not assessment_id:
        raise ValueError(
            "Cash return assessment ID is required."
        )

    if baseline.total_cash_eur == 0:
        return CashBaselineReturnAssessment(
            assessment_id=assessment_id,
            baseline_id=baseline.baseline_id,
            total_cash_eur=0.0,
            known_return_balance_eur=0.0,
            unknown_return_balance_eur=0.0,
            return_evidence_coverage_pct=100.0,
            blended_annual_return_pct=None,
            assessment_status="not_applicable",
            evidence_requirements=(),
            notes=notes,
        )

    known_balances = tuple(
        balance
        for balance in baseline.balances
        if balance.return_evidence_available
    )

    unknown_balances = tuple(
        balance
        for balance in baseline.balances
        if not balance.return_evidence_available
    )

    known_return_balance_eur = sum(
        balance.balance_eur
        for balance in known_balances
    )

    unknown_return_balance_eur = sum(
        balance.balance_eur
        for balance in unknown_balances
    )

    return_evidence_coverage_pct = (
        known_return_balance_eur
        / baseline.total_cash_eur
        * 100
    )

    if unknown_balances:
        evidence_requirements = tuple(
            (
                f"Return evidence unavailable for "
                f"{balance.label} "
                f"(EUR {balance.balance_eur:,.2f})."
            )
            for balance in unknown_balances
        )

        return CashBaselineReturnAssessment(
            assessment_id=assessment_id,
            baseline_id=baseline.baseline_id,
            total_cash_eur=baseline.total_cash_eur,
            known_return_balance_eur=(
                known_return_balance_eur
            ),
            unknown_return_balance_eur=(
                unknown_return_balance_eur
            ),
            return_evidence_coverage_pct=(
                return_evidence_coverage_pct
            ),
            blended_annual_return_pct=None,
            assessment_status="incomplete",
            evidence_requirements=(
                evidence_requirements
            ),
            notes=notes,
        )

    weighted_return_numerator = sum(
        (
            balance.balance_eur
            * balance.annual_return_pct
        )
        for balance in known_balances
        if balance.annual_return_pct is not None
    )

    blended_annual_return_pct = (
        weighted_return_numerator
        / baseline.total_cash_eur
    )

    return CashBaselineReturnAssessment(
        assessment_id=assessment_id,
        baseline_id=baseline.baseline_id,
        total_cash_eur=baseline.total_cash_eur,
        known_return_balance_eur=(
            known_return_balance_eur
        ),
        unknown_return_balance_eur=0.0,
        return_evidence_coverage_pct=100.0,
        blended_annual_return_pct=(
            blended_annual_return_pct
        ),
        assessment_status="complete",
        evidence_requirements=(),
        notes=notes,
    )


def build_unallocated_return_input(
    assessment: CashBaselineReturnAssessment,
    notes: str | None = None,
) -> UnallocatedReturnInput:
    if assessment.assessment_status == "complete":
        return UnallocatedReturnInput(
            annual_return_pct=(
                assessment.blended_annual_return_pct
            ),
            evidence_available=True,
            source_reference=(
                assessment.assessment_id
            ),
            notes=notes,
        )

    return UnallocatedReturnInput(
        annual_return_pct=None,
        evidence_available=False,
        source_reference=(
            assessment.assessment_id
        ),
        notes=notes,
    )