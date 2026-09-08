from __future__ import annotations

import os
from datetime import datetime, time, timezone

import psycopg

from treasury_intelligence.analytics.universe_candidates import (
    analyze_opportunity_universe_at_position_size,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.persistence.opportunity_snapshots import (
    load_latest_opportunity_snapshot,
)

from treasury_intelligence.sources.aave import (
    load_latest_aave_reserve_observation,
)

from treasury_intelligence.sources.ecb import (
    load_latest_estr_observation,
)

from treasury_intelligence.sources.france import (
    get_btf_2027_03_10_snapshot,
)


AS_OF = "2026-09-08"

REPORT_INSTRUMENT_IDS = (
    "fr_btf_2027_08_11",
    "fr_btf_2027_03_10",
    "ernx",
    "xeon",
    "aave_v3_base_eurc",
)


def _first_reason(candidate) -> str:
    if candidate.blocking_reasons:
        return candidate.blocking_reasons[0]

    if candidate.evidence_requirements:
        return candidate.evidence_requirements[0]

    return "No unresolved production requirement."


def _annual_return_eur(candidate) -> float | None:
    if candidate.defensible_return_pct is None:
        return None

    return (
        candidate.position_size_eur
        * candidate.defensible_return_pct
        / 100.0
    )


def _format_return(value: float | None) -> str:
    if value is None:
        return "unknown"

    return f"{value:.3f}%"


def _format_annual_return(value: float | None) -> str:
    if value is None:
        return "unknown"

    return f"EUR {value:,.0f}"


def main() -> None:
    database_url = os.environ.get(
        "DATABASE_URL"
    )

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is required."
        )

    warehouse_as_of = datetime.combine(
        datetime.fromisoformat(AS_OF).date(),
        time.max,
        tzinfo=timezone.utc,
    )

    with psycopg.connect(
        database_url
    ) as connection:
        btf_snapshot = (
            load_latest_opportunity_snapshot(
                connection=connection,
                structural_snapshot=(
                    get_btf_2027_03_10_snapshot()
                ),
            )
        )

        estr_observation = (
            load_latest_estr_observation(
                connection=connection,
                as_of=warehouse_as_of,
            )
        )

        aave_observation = (
            load_latest_aave_reserve_observation(
                connection=connection,
                as_of=warehouse_as_of,
            )
        )

    candidates = (
        analyze_opportunity_universe_at_position_size(
            position_size_eur=(
                MODEL_COMPANY_MANDATE
                .treasury_capital_eur
            ),
            mandate=MODEL_COMPANY_MANDATE,
            estr_observation=estr_observation,
            btf_2027_03_10_snapshot=(
                btf_snapshot
            ),
            aave_observation=(
                aave_observation
            ),
            as_of=AS_OF,
        )
    )

    if len(candidates) != 14:
        raise RuntimeError(
            "Expected 14 canonical production "
            f"candidates, found {len(candidates)}."
        )

    indexed = {
        candidate.instrument_id: candidate
        for candidate in candidates
    }

    missing = [
        instrument_id
        for instrument_id
        in REPORT_INSTRUMENT_IDS
        if instrument_id not in indexed
    ]

    if missing:
        raise RuntimeError(
            "Daily report instruments missing from "
            "canonical universe: "
            + ", ".join(missing)
        )

    report_candidates = tuple(
        indexed[instrument_id]
        for instrument_id
        in REPORT_INSTRUMENT_IDS
    )

    ranked = tuple(
        sorted(
            report_candidates,
            key=lambda candidate: (
                candidate.defensible_return_pct
                is None,
                -(
                    candidate.defensible_return_pct
                    or 0.0
                ),
                candidate.label,
            ),
        )
    )

    recommendation_ready = tuple(
        candidate
        for candidate in report_candidates
        if candidate.recommendation_ready
    )

    ranked_ready = tuple(
        candidate
        for candidate in ranked
        if candidate.recommendation_ready
    )

    best_current = next(
        (
            candidate
            for candidate in ranked
            if (
                candidate.defensible_return_pct
                is not None
            )
        ),
        None,
    )

    best_production_ready = (
        ranked_ready[0]
        if ranked_ready
        else None
    )

    print(
        "TREASURY INTELLIGENCE REPORT"
    )
    print("=" * 72)
    print()

    print(
        f"As of:                {AS_OF}"
    )
    print(
        "Treasury capital:     "
        f"EUR "
        f"{MODEL_COMPANY_MANDATE.treasury_capital_eur:,.0f}"
    )
    print(
        "Base currency:        "
        f"{MODEL_COMPANY_MANDATE.base_currency}"
    )
    print()

    print(
        "CURRENT PRODUCTION ACTION"
    )
    print("-" * 72)

    if best_production_ready is None:
        print(
            "Action:               hold unallocated"
        )
        print(
            "Authorized allocation: EUR 0"
        )
        print(
            "Reason:               no shortlisted "
            "opportunity currently passes every "
            "production readiness gate."
        )
    else:
        print(
            "Action:               candidate available "
            "for approval"
        )
        print(
            "Candidate:            "
            f"{best_production_ready.label}"
        )
        print(
            "Defensible return:    "
            f"{_format_return(best_production_ready.defensible_return_pct)}"
        )

    print()
    print(
        "CURRENT OPPORTUNITY RANKING"
    )
    print("-" * 72)
    print()

    for rank, candidate in enumerate(
        ranked,
        start=1,
    ):
        annual_return = (
            _annual_return_eur(
                candidate
            )
        )

        print(
            f"{rank}. {candidate.label}"
        )
        print(
            "   Instrument:        "
            f"{candidate.instrument_id}"
        )
        print(
            "   Defensible return: "
            f"{_format_return(candidate.defensible_return_pct)}"
        )
        print(
            "   Annual return:     "
            f"{_format_annual_return(annual_return)}"
        )
        print(
            "   Status:            "
            f"{candidate.candidate_status}"
        )
        print(
            "   Eligibility:       "
            f"{candidate.eligibility_status}"
        )
        print(
            "   Liquidity:         "
            f"{candidate.liquidity_position_status}"
        )
        print(
            "   Economics:         "
            f"{candidate.economics_status}"
        )
        print(
            "   Production ready:  "
            f"{candidate.recommendation_ready}"
        )
        print(
            "   Main gap:          "
            f"{_first_reason(candidate)}"
        )
        print()

    print(
        "BEST CURRENT CANDIDATE"
    )
    print("-" * 72)

    if best_current is None:
        print(
            "No shortlisted candidate has a "
            "defensible return."
        )
    else:
        print(
            "Candidate:            "
            f"{best_current.label}"
        )
        print(
            "Defensible return:    "
            f"{_format_return(best_current.defensible_return_pct)}"
        )
        print(
            "Annual return at "
            f"EUR {best_current.position_size_eur:,.0f}: "
            f"{_format_annual_return(_annual_return_eur(best_current))}"
        )
        print(
            "Production status:    "
            f"{best_current.candidate_status}"
        )

        if best_current.recommendation_ready:
            print(
                "Interpretation:       highest-return "
                "recommendation-ready opportunity in "
                "the report shortlist."
            )
        else:
            print(
                "Interpretation:       highest-return "
                "currently analyzed opportunity in the "
                "report shortlist, but not yet cleared "
                "for production recommendation."
            )

            print(
                "Outstanding item:    "
                f"{_first_reason(best_current)}"
            )

    print()
    print(
        "PRODUCTION-READY SHORTLIST"
    )
    print("-" * 72)

    if recommendation_ready:
        for candidate in ranked_ready:
            print(
                f"- {candidate.label}: "
                f"{_format_return(candidate.defensible_return_pct)}"
            )
    else:
        print(
            "None."
        )

    print()
    print(
        "REPORT INTERPRETATION"
    )
    print("-" * 72)
    print(
        "Ranking is based on the existing defensible "
        "return produced by the canonical treasury "
        "candidate model."
    )
    print(
        "Ranking does not override eligibility, risk, "
        "liquidity, economics, freshness, approval, or "
        "execution gates."
    )
    print(
        "A high-ranked needs-evidence candidate is an "
        "analytical opportunity, not an authorized "
        "allocation."
    )

    print()
    print("=" * 72)
    print(
        "DAILY TREASURY REPORT COMPLETE"
    )


if __name__ == "__main__":
    main()
