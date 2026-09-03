from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.analytics.cash_returns import (
    build_freshness_aware_cash_baseline_return_assessment,
    build_unallocated_return_input,
)

from treasury_intelligence.analytics.universe_candidates import (
    analyze_opportunity_universe_at_position_size,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.cash_baselines import (
    CashBalance,
    CashBaseline,
)


AS_OF = "2026-09-03"
TREASURY_CAPITAL_EUR = 10_000_000.0
CURRENT_CASH_RETURN_PCT = 1.25


def main() -> None:
    print(
        "=== MILESTONE 15N — ARBITRARY COMPANY INPUT PROOF ==="
    )
    print()

    mandate = replace(
        MODEL_COMPANY_MANDATE,
        mandate_id="acceptance_company_10m",
        name="Acceptance company EUR 10M treasury",
        treasury_capital_eur=TREASURY_CAPITAL_EUR,
    )

    cash_balance = CashBalance(
        balance_id="acceptance_company_operating_cash",
        label="Acceptance company operating cash",
        balance_type="operating_account",
        balance_eur=TREASURY_CAPITAL_EUR,
        annual_return_pct=CURRENT_CASH_RETURN_PCT,
        return_evidence_available=True,
        institution="Acceptance Fixture Bank",
        source_reference=(
            "acceptance_company_supplied_cash_rate_"
            "2026_09_03"
        ),
        return_evidence_date=AS_OF,
        notes=(
            "Deterministic acceptance fixture proving that "
            "cash economics are not coupled to the model "
            "company's EUR 5M treasury size or 0% cash rate."
        ),
    )

    cash_baseline = CashBaseline(
        baseline_id=(
            "acceptance_company_current_cash_2026_09_03"
        ),
        mandate_id=mandate.mandate_id,
        as_of=AS_OF,
        total_cash_eur=TREASURY_CAPITAL_EUR,
        balances=(cash_balance,),
        notes=(
            "Generic cash baseline for a non-model-company "
            "EUR 10M treasury acceptance fixture."
        ),
    )

    cash_return_assessment = (
        build_freshness_aware_cash_baseline_return_assessment(
            assessment_id=(
                "acceptance_company_cash_return_2026_09_03"
            ),
            baseline=cash_baseline,
            as_of=AS_OF,
            notes=(
                "Freshness-aware assessment of supplied "
                "1.25% current cash economics."
            ),
        )
    )

    current_unallocated_return = (
        build_unallocated_return_input(
            assessment=cash_return_assessment,
            notes=(
                "Current return input for the arbitrary "
                "company acceptance fixture."
            ),
        )
    )

    candidates = (
        analyze_opportunity_universe_at_position_size(
            position_size_eur=TREASURY_CAPITAL_EUR,
            mandate=mandate,
            as_of=AS_OF,
        )
    )

    recommendation_ready = tuple(
        candidate
        for candidate in candidates
        if candidate.candidate_status
        == "recommendation_ready"
    )

    needs_evidence = tuple(
        candidate
        for candidate in candidates
        if candidate.candidate_status
        == "needs_evidence"
    )

    blocked = tuple(
        candidate
        for candidate in candidates
        if candidate.candidate_status == "blocked"
    )

    analyzed_position_sizes = {
        candidate.position_size_eur
        for candidate in candidates
    }

    current_annual_return_eur = (
        TREASURY_CAPITAL_EUR
        * CURRENT_CASH_RETURN_PCT
        / 100
    )

    print(
        f"Mandate ID:                 "
        f"{mandate.mandate_id}"
    )
    print(
        "Treasury capital:           "
        f"EUR {mandate.treasury_capital_eur:,.2f}"
    )
    print(
        "Current cash balance:       "
        f"EUR {cash_baseline.total_cash_eur:,.2f}"
    )
    print(
        "Current cash return:        "
        f"{cash_return_assessment.blended_annual_return_pct:.3f}%"
    )
    print(
        "Current annual return:      "
        f"EUR {current_annual_return_eur:,.2f}"
    )
    print(
        "Cash evidence status:       "
        f"{cash_return_assessment.assessment_status}"
    )
    print(
        "Cash return evidence:       "
        f"{current_unallocated_return.evidence_available}"
    )
    print()

    print(
        f"Production universe:        "
        f"{len(candidates)}"
    )
    print(
        "Recommendation-ready:      "
        f"{len(recommendation_ready)}"
    )
    print(
        f"Needs evidence:             "
        f"{len(needs_evidence)}"
    )
    print(
        f"Blocked:                    "
        f"{len(blocked)}"
    )
    print(
        "Analyzed position sizes:    "
        + ", ".join(
            f"EUR {value:,.2f}"
            for value in sorted(
                analyzed_position_sizes
            )
        )
    )
    print()

    if recommendation_ready:
        best_ready = max(
            recommendation_ready,
            key=lambda candidate: (
                candidate.defensible_return_pct
                if candidate.defensible_return_pct
                is not None
                else float("-inf")
            ),
        )

        print(
            "Best ready candidate:      "
            f"{best_ready.label}"
        )
        print(
            "Best defensible return:    "
            f"{best_ready.defensible_return_pct:.3f}%"
        )
    else:
        print(
            "Best ready candidate:      "
            "NONE — evidence/capacity does not support "
            "a recommendation-ready EUR 10M position."
        )

    print()

    assert (
        mandate.treasury_capital_eur
        == TREASURY_CAPITAL_EUR
    )
    assert (
        mandate.mandate_id
        != MODEL_COMPANY_MANDATE.mandate_id
    )

    assert cash_baseline.mandate_id == mandate.mandate_id
    assert (
        cash_baseline.total_cash_eur
        == TREASURY_CAPITAL_EUR
    )

    assert (
        cash_return_assessment.assessment_status
        == "complete"
    )
    assert (
        cash_return_assessment.blended_annual_return_pct
        == CURRENT_CASH_RETURN_PCT
    )
    assert (
        cash_return_assessment.known_return_balance_eur
        == TREASURY_CAPITAL_EUR
    )
    assert (
        cash_return_assessment.unknown_return_balance_eur
        == 0.0
    )
    assert (
        cash_return_assessment.return_evidence_coverage_pct
        == 100.0
    )

    assert (
        current_unallocated_return.evidence_available
        is True
    )
    assert (
        current_unallocated_return.annual_return_pct
        == CURRENT_CASH_RETURN_PCT
    )

    assert (
        abs(
            current_annual_return_eur
            - 125_000.0
        )
        < 0.01
    )

    assert len(candidates) == 14

    assert (
        len(recommendation_ready)
        + len(needs_evidence)
        + len(blocked)
        == len(candidates)
    )

    assert analyzed_position_sizes == {
        TREASURY_CAPITAL_EUR
    }

    for candidate in candidates:
        assert (
            candidate.mandate_id
            == mandate.mandate_id
        )
        assert (
            candidate.position_size_eur
            == mandate.treasury_capital_eur
        )

    assert all(
        candidate.recommendation_ready
        for candidate in recommendation_ready
    )

    assert all(
        not candidate.recommendation_ready
        for candidate in (
            *needs_evidence,
            *blocked,
        )
    )

    print(
        "EUR 5M treasury capital is not a hidden "
        "analytical constant:                  yes"
    )
    print(
        "0% current cash return is not a hidden "
        "analytical constant:                  yes"
    )
    print(
        "Generic cash baseline accepts EUR 10M: yes"
    )
    print(
        "Production universe analyzed at EUR 10M: yes"
    )
    print()
    print(
        "All Milestone 15N arbitrary-company input "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
