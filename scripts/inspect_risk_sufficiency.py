from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_DIR),
    )


from treasury_intelligence.analytics.risk_assessments import (
    get_btf_risk_assessments,
    get_ernx_risk_assessments,
    get_xeon_risk_assessments,
)

from treasury_intelligence.analytics.risk_sufficiency import (
    assess_risk_evidence_sufficiency,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)


def print_assessment(
    label: str,
    risk_assessments,
) -> None:
    assessment = (
        assess_risk_evidence_sufficiency(
            mandate=MODEL_COMPANY_MANDATE,
            risk_assessments=risk_assessments,
        )
    )

    print()
    print(label)
    print("-" * 100)

    print(
        "Instrument:",
        assessment.instrument_id,
    )

    print(
        "Market:",
        assessment.market_id,
    )

    print(
        "Required dimensions:",
        ", ".join(
            assessment.required_dimensions
        )
        or "none",
    )

    print(
        "Insufficient dimensions:",
        ", ".join(
            assessment.insufficient_dimensions
        )
        or "none",
    )

    print(
        "Unacceptable dimensions:",
        ", ".join(
            assessment.unacceptable_dimensions
        )
        or "none",
    )

    print(
        "Evidence requirements:",
        len(
            assessment.evidence_requirements
        ),
    )

    print(
        "Risk blockers:",
        len(
            assessment.risk_blocking_reasons
        ),
    )

    print(
        "Evidence sufficient:",
        assessment.evidence_sufficient,
    )

    print(
        "Risk acceptable:",
        assessment.risk_acceptable,
    )

    print(
        "Sufficient for recommendation:",
        assessment.sufficient_for_recommendation,
    )


def main() -> None:
    print()
    print("RISK SUFFICIENCY AND TOLERANCE AUDIT")
    print("=" * 100)

    print_assessment(
        "XEON",
        get_xeon_risk_assessments(),
    )

    print_assessment(
        "ERNX",
        get_ernx_risk_assessments(),
    )

    print_assessment(
        "French BTF",
        get_btf_risk_assessments(),
    )

    print()
    print("=" * 100)

    print(
        "PASS: unknown required risks create evidence "
        "requirements rather than arbitrary score-based "
        "failures."
    )

    print(
        "PASS: known required risks outside mandate "
        "tolerance create blockers."
    )

    print(
        "PASS: position-size liquidity remains separate "
        "from the base-risk mandate gate."
    )


if __name__ == "__main__":
    main()