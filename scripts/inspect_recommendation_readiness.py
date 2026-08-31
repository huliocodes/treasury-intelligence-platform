from __future__ import annotations

import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_DIR),
    )


from inspect_universe_position_matrix import (
    POSITION_SIZES_EUR,
    UniverseOpportunity,
    build_opportunity_universe,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)


TARGET_POSITION_SIZE_EUR = 5_000_000.0


@dataclass(frozen=True)
class ReadinessAudit:
    key: str
    label: str

    position_size_eur: float

    candidate_status: str
    eligibility_status: str
    liquidity_status: str
    economics_status: str

    unknown_risk_dimensions: int

    defensible_return_pct: float | None

    blocking_reasons: tuple[str, ...]
    evidence_requirements: tuple[str, ...]

    recommendation_ready: bool

    priority_group: str


def classify_priority(
    candidate: PortfolioCandidateAssessment,
) -> str:
    if candidate.recommendation_ready:
        return "ready"

    if candidate.candidate_status == "needs_evidence":
        return "priority_1"

    if (
        candidate.candidate_status == "blocked"
        and candidate.eligibility_status
        == "ineligible"
    ):
        return "priority_2"

    return "priority_3"


def build_readiness_audit(
    opportunity: UniverseOpportunity,
    candidate: PortfolioCandidateAssessment,
) -> ReadinessAudit:
    return ReadinessAudit(
        key=opportunity.key,
        label=opportunity.label,
        position_size_eur=(
            candidate.position_size_eur
        ),
        candidate_status=(
            candidate.candidate_status
        ),
        eligibility_status=(
            candidate.eligibility_status
        ),
        liquidity_status=(
            candidate.liquidity_position_status
        ),
        economics_status=(
            candidate.economics_status
        ),
        unknown_risk_dimensions=(
            candidate.base_risk_unknown_dimension_count
        ),
        defensible_return_pct=(
            candidate.defensible_return_pct
        ),
        blocking_reasons=(
            candidate.blocking_reasons
        ),
        evidence_requirements=(
            candidate.evidence_requirements
        ),
        recommendation_ready=(
            candidate.recommendation_ready
        ),
        priority_group=classify_priority(
            candidate
        ),
    )


def candidate_at_target_size(
    opportunity: UniverseOpportunity,
) -> PortfolioCandidateAssessment:
    return opportunity.candidate_builder(
        TARGET_POSITION_SIZE_EUR
    )


def format_return(
    audit: ReadinessAudit,
) -> str:
    if audit.defensible_return_pct is None:
        return "-"

    return (
        f"{audit.defensible_return_pct:.3f}%"
    )


def print_priority_1(
    audits: tuple[
        ReadinessAudit,
        ...
    ],
) -> None:
    priority = tuple(
        audit
        for audit in audits
        if audit.priority_group == "priority_1"
    )

    print()
    print("PRIORITY 1 — CLOSEST TO RECOMMENDATION-READY")
    print("=" * 100)

    if not priority:
        print("None")
        return

    for rank, audit in enumerate(
        priority,
        start=1,
    ):
        print()
        print(
            f"{rank}. {audit.label}"
        )
        print("-" * 100)

        print(
            f"Position: "
            f"EUR {audit.position_size_eur:,.0f}"
        )

        print(
            f"Defensible return: "
            f"{format_return(audit)}"
        )

        print(
            f"Eligibility: "
            f"{audit.eligibility_status}"
        )

        print(
            f"Liquidity: "
            f"{audit.liquidity_status}"
        )

        print(
            f"Economics: "
            f"{audit.economics_status}"
        )

        print(
            f"Unknown base risk dimensions: "
            f"{audit.unknown_risk_dimensions}"
        )

        print(
            f"Evidence requirements: "
            f"{len(audit.evidence_requirements)}"
        )

        for requirement in (
            audit.evidence_requirements
        ):
            print(
                f"  - {requirement}"
            )


def print_blocked(
    audits: tuple[
        ReadinessAudit,
        ...
    ],
) -> None:
    blocked = tuple(
        audit
        for audit in audits
        if audit.candidate_status == "blocked"
    )

    print()
    print("CURRENTLY BLOCKED")
    print("=" * 100)

    for audit in blocked:
        print()
        print(audit.label)
        print("-" * 100)

        print(
            f"Position: "
            f"EUR {audit.position_size_eur:,.0f}"
        )

        print(
            f"Defensible return: "
            f"{format_return(audit)}"
        )

        print(
            f"Liquidity: "
            f"{audit.liquidity_status}"
        )

        print(
            f"Blocking reasons: "
            f"{len(audit.blocking_reasons)}"
        )

        for reason in audit.blocking_reasons:
            print(
                f"  - {reason}"
            )


def print_cross_universe_evidence(
    audits: tuple[
        ReadinessAudit,
        ...
    ],
) -> None:
    evidence_counter = Counter(
        requirement
        for audit in audits
        for requirement in (
            audit.evidence_requirements
        )
    )

    print()
    print("CROSS-UNIVERSE EVIDENCE LEVERAGE")
    print("=" * 100)

    for requirement, count in (
        evidence_counter.most_common()
    ):
        print()
        print(
            f"{count} opportunities"
        )

        print(
            f"  {requirement}"
        )


def print_readiness_table(
    audits: tuple[
        ReadinessAudit,
        ...
    ],
) -> None:
    print()
    print("EUR 5M RECOMMENDATION-READINESS TABLE")
    print("=" * 118)

    print(
        f"{'Opportunity':<22}"
        f"{'Return':>10}"
        f"{'Eligibility':>16}"
        f"{'Liquidity':>16}"
        f"{'Economics':>14}"
        f"{'Risk ?':>10}"
        f"{'Evidence':>12}"
        f"{'Blockers':>10}"
    )

    print("-" * 118)

    for audit in audits:
        print(
            f"{audit.label:<22}"
            f"{format_return(audit):>10}"
            f"{audit.eligibility_status:>16}"
            f"{audit.liquidity_status:>16}"
            f"{audit.economics_status:>14}"
            f"{audit.unknown_risk_dimensions:>10}"
            f"{len(audit.evidence_requirements):>12}"
            f"{len(audit.blocking_reasons):>10}"
        )

    print("=" * 118)


def print_accessibility_status(
    audits: tuple[
        ReadinessAudit,
        ...
    ],
) -> None:
    modeled_eligible = tuple(
        audit
        for audit in audits
        if audit.eligibility_status != "ineligible"
    )

    print()
    print("ACCESSIBILITY STATUS")
    print("=" * 100)

    print(
        "The following opportunities currently satisfy "
        "or survive the modeled V1 corporate-access "
        "eligibility analysis:"
    )

    print()

    for audit in modeled_eligible:
        print(
            f"  - {audit.label}"
        )

    print()

    print(
        "V1 accessibility is based on the supported "
        "corporate access route and known instrument / "
        "market availability. An exact live order ticket "
        "from the model company is not required before "
        "portfolio analysis."
    )

    print(
        "Account-specific permissions, onboarding, and "
        "operational checks remain execution-stage tasks. "
        "A known legal, product, jurisdictional, or broker "
        "restriction would still override this modeled "
        "accessibility conclusion."
    )


def print_summary(
    audits: tuple[
        ReadinessAudit,
        ...
    ],
) -> None:
    print()
    print("READINESS SUMMARY")
    print("=" * 100)

    print(
        "Universe opportunities:",
        len(audits),
    )

    print(
        "Diagnostic position sizes available:",
        len(POSITION_SIZES_EUR),
    )

    print(
        "Target readiness audit size:",
        f"EUR {TARGET_POSITION_SIZE_EUR:,.0f}",
    )

    print(
        "Recommendation-ready:",
        sum(
            audit.recommendation_ready
            for audit in audits
        ),
    )

    print(
        "Needs evidence:",
        sum(
            audit.candidate_status
            == "needs_evidence"
            for audit in audits
        ),
    )

    print(
        "Blocked:",
        sum(
            audit.candidate_status
            == "blocked"
            for audit in audits
        ),
    )

    print()

    print(
        "Interpretation: this audit prioritizes evidence "
        "work. It does not rank investments and it does "
        "not allocate treasury capital."
    )


def main() -> None:
    opportunities, aave_observation = (
        build_opportunity_universe()
    )

    audits = tuple(
        build_readiness_audit(
            opportunity=opportunity,
            candidate=candidate_at_target_size(
                opportunity
            ),
        )
        for opportunity in opportunities
    )

    print()
    print("RECOMMENDATION-READINESS EVIDENCE AUDIT")
    print("=" * 100)

    print(
        "Mandate:",
        MODEL_MANDATE_DESCRIPTION,
    )

    print(
        "Aave observation:",
        aave_observation.observed_at.isoformat(),
    )

    print_readiness_table(
        audits
    )

    print_priority_1(
        audits
    )

    print_blocked(
        audits
    )

    print_cross_universe_evidence(
        audits
    )

    print_accessibility_status(
        audits
    )

    print_summary(
        audits
    )


MODEL_MANDATE_DESCRIPTION = (
    "Slovenian d.o.o. / EUR 5M / high liquidity / "
    "0% unhedged FX / very high capital preservation"
)


if __name__ == "__main__":
    main()
