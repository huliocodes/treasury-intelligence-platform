from __future__ import annotations

from treasury_intelligence.analytics.universe_candidates import (
    analyze_opportunity_universe_at_position_size,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)


AS_OF = "2026-09-03"


def main() -> None:
    candidates = (
        analyze_opportunity_universe_at_position_size(
            position_size_eur=(
                MODEL_COMPANY_MANDATE
                .treasury_capital_eur
            ),
            mandate=MODEL_COMPANY_MANDATE,
            as_of=AS_OF,
        )
    )

    assert len(candidates) == 14

    candidate_map = {
        candidate.label: candidate
        for candidate in candidates
    }

    ready = tuple(
        candidate
        for candidate in candidates
        if candidate.recommendation_ready
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
        if candidate.candidate_status
        == "blocked"
    )

    print(
        "MILESTONE 15G.2 — FRESHNESS-GATED "
        "PRODUCTION UNIVERSE"
    )
    print()
    print(
        f"Total:                 {len(candidates)}"
    )
    print(
        f"Recommendation-ready:  {len(ready)}"
    )
    print(
        f"Needs evidence:        {len(needs_evidence)}"
    )
    print(
        f"Blocked:               {len(blocked)}"
    )
    print()

    for candidate in candidates:
        print(
            f"{candidate.label:32} "
            f"{candidate.candidate_status}"
        )

        for requirement in (
            candidate.evidence_requirements
        ):
            if requirement.startswith(
                "Refresh required:"
            ):
                print(
                    f"  - {requirement}"
                )

    assert len(ready) == 1
    assert len(needs_evidence) == 8
    assert len(blocked) == 5

    assert ready[0].label == (
        "French BTF Aug 2027"
    )

    expected_stale_types = {
        "ERNX": (
            "market_liquidity",
        ),
        "French BTF Mar 2027": (
            "market_return",
        ),
        "German Bubill Jul 2027": (
            "market_return",
            "market_liquidity",
        ),
        "German Bubill Aug 2027": (
            "market_return",
            "market_liquidity",
        ),
    }

    for label, evidence_types in (
        expected_stale_types.items()
    ):
        candidate = candidate_map[label]

        assert (
            candidate.candidate_status
            == "needs_evidence"
        )

        refresh_requirements = tuple(
            requirement
            for requirement
            in candidate.evidence_requirements
            if requirement.startswith(
                "Refresh required:"
            )
        )

        for evidence_type in evidence_types:
            assert any(
                evidence_type in requirement
                for requirement
                in refresh_requirements
            )

    btf_aug = candidate_map[
        "French BTF Aug 2027"
    ]

    assert btf_aug.recommendation_ready

    assert not any(
        requirement.startswith(
            "Refresh required:"
        )
        for requirement
        in btf_aug.evidence_requirements
    )

    print()
    print(
        "Freshness-valid winner: "
        f"{btf_aug.label}"
    )
    print()
    print(
        "All Milestone 15G.2 freshness-gating "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
