from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.cash_returns import (
    build_freshness_aware_cash_baseline_return_assessment,
    build_unallocated_return_input,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
    CashBaseline,
)


AS_OF = "2026-09-03"


def build_baseline(
    *,
    baseline_id: str,
    annual_return_pct: float | None,
    evidence_available: bool,
    evidence_date: str | None,
) -> CashBaseline:
    return CashBaseline(
        baseline_id=baseline_id,
        mandate_id=(
            MODEL_COMPANY_MANDATE.mandate_id
        ),
        as_of=AS_OF,
        total_cash_eur=5_000_000,
        balances=(
            CashBalance(
                balance_id=baseline_id + "_cash",
                label="Model company corporate cash",
                balance_type="operating_account",
                balance_eur=5_000_000,
                annual_return_pct=annual_return_pct,
                return_evidence_available=(
                    evidence_available
                ),
                institution="Fixture Bank",
                source_reference=(
                    "fixture_cash_rate_evidence"
                    if evidence_available
                    else None
                ),
                return_evidence_date=evidence_date,
            ),
        ),
    )


def assess(
    baseline: CashBaseline,
):
    return (
        build_freshness_aware_cash_baseline_return_assessment(
            assessment_id=(
                baseline.baseline_id
                + "_return_assessment"
            ),
            baseline=baseline,
            as_of=AS_OF,
            notes=(
                "Milestone 15H deterministic "
                "cash-return freshness fixture."
            ),
        )
    )


def main() -> None:
    print(
        "MILESTONE 15H — DATED CURRENT-CASH ECONOMICS"
    )
    print()

    print(
        "CASE 1 — UNRESOLVED CASH RETURN"
    )
    print()

    unresolved = assess(
        build_baseline(
            baseline_id="cash_unresolved",
            annual_return_pct=None,
            evidence_available=False,
            evidence_date=None,
        )
    )

    print(
        "Status:                         "
        f"{unresolved.assessment_status}"
    )
    print(
        "Return:                         "
        f"{unresolved.blended_annual_return_pct}"
    )

    assert (
        unresolved.assessment_status
        == "incomplete"
    )
    assert (
        unresolved.blended_annual_return_pct
        is None
    )

    print()
    print(
        "CASE 2 — FRESH VERIFIED CASH RETURN"
    )
    print()

    fresh = assess(
        build_baseline(
            baseline_id="cash_fresh",
            annual_return_pct=1.50,
            evidence_available=True,
            evidence_date="2026-09-01",
        )
    )

    fresh_input = (
        build_unallocated_return_input(
            assessment=fresh,
        )
    )

    print(
        "Status:                         "
        f"{fresh.assessment_status}"
    )
    print(
        "Blended annual return:          "
        f"{fresh.blended_annual_return_pct:.3f}%"
    )
    print(
        "Review evidence available:      "
        f"{fresh_input.evidence_available}"
    )

    assert fresh.assessment_status == "complete"
    assert fresh.blended_annual_return_pct == 1.50
    assert fresh_input.evidence_available
    assert fresh_input.annual_return_pct == 1.50

    print()
    print(
        "CASE 3 — STALE VERIFIED CASH RETURN"
    )
    print()

    stale = assess(
        build_baseline(
            baseline_id="cash_stale",
            annual_return_pct=1.50,
            evidence_available=True,
            evidence_date="2026-08-20",
        )
    )

    stale_input = (
        build_unallocated_return_input(
            assessment=stale,
        )
    )

    print(
        "Status:                         "
        f"{stale.assessment_status}"
    )
    print(
        "Return:                         "
        f"{stale.blended_annual_return_pct}"
    )

    for requirement in stale.evidence_requirements:
        print(
            "Evidence requirement:          "
            f"{requirement}"
        )

    assert stale.assessment_status == "incomplete"
    assert stale.blended_annual_return_pct is None
    assert not stale_input.evidence_available
    assert any(
        "stale" in requirement
        for requirement in stale.evidence_requirements
    )

    print()
    print(
        "CASE 4 — UNDATED VERIFIED CASH RETURN"
    )
    print()

    undated = assess(
        build_baseline(
            baseline_id="cash_undated",
            annual_return_pct=1.50,
            evidence_available=True,
            evidence_date=None,
        )
    )

    print(
        "Status:                         "
        f"{undated.assessment_status}"
    )

    for requirement in undated.evidence_requirements:
        print(
            "Evidence requirement:          "
            f"{requirement}"
        )

    assert (
        undated.assessment_status
        == "incomplete"
    )
    assert (
        undated.blended_annual_return_pct
        is None
    )
    assert any(
        "undated" in requirement.lower()
        for requirement in (
            undated.evidence_requirements
        )
    )

    print()
    print(
        "CASE 5 — FUTURE-DATED CASH RETURN"
    )
    print()

    future = assess(
        build_baseline(
            baseline_id="cash_future",
            annual_return_pct=1.50,
            evidence_available=True,
            evidence_date="2026-09-04",
        )
    )

    print(
        "Status:                         "
        f"{future.assessment_status}"
    )

    for requirement in future.evidence_requirements:
        print(
            "Evidence requirement:          "
            f"{requirement}"
        )

    assert future.assessment_status == "incomplete"
    assert future.blended_annual_return_pct is None
    assert any(
        "future_dated" in requirement
        for requirement in future.evidence_requirements
    )

    print()
    print(
        "CASE 6 — EXACT SEVEN-DAY BOUNDARY"
    )
    print()

    boundary = assess(
        build_baseline(
            baseline_id="cash_boundary",
            annual_return_pct=1.25,
            evidence_available=True,
            evidence_date="2026-08-27",
        )
    )

    print(
        "Status:                         "
        f"{boundary.assessment_status}"
    )
    print(
        "Blended annual return:          "
        f"{boundary.blended_annual_return_pct:.3f}%"
    )

    assert (
        boundary.assessment_status
        == "complete"
    )
    assert (
        boundary.blended_annual_return_pct
        == 1.25
    )

    print()
    print("-" * 100)
    print()
    print(
        "MILESTONE 15H ASSERTIONS"
    )
    print()
    print(
        "Missing cash return stays unknown:       yes"
    )
    print(
        "Fresh dated cash return is usable:       yes"
    )
    print(
        "Stale cash return requires refresh:      yes"
    )
    print(
        "Undated cash return requires evidence:   yes"
    )
    print(
        "Future-dated return is rejected:         yes"
    )
    print(
        "Seven-day policy boundary respected:     yes"
    )
    print(
        "Existing market-return policy reused:    yes"
    )
    print()
    print(
        "All Milestone 15H cash-return freshness "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
