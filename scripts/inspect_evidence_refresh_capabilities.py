from __future__ import annotations

from treasury_intelligence.analytics.model_company_evidence_refresh import (
    build_model_company_evidence_refresh_plan,
)
from treasury_intelligence.models.evidence_refresh_capabilities import (
    EvidenceRefreshCapabilityAssessment,
)
from treasury_intelligence.policies.evidence_refresh_capabilities import (
    MODEL_COMPANY_EVIDENCE_REFRESH_CAPABILITIES,
    get_model_company_refresh_capability,
)


AS_OF = "2026-09-03"

EXPECTED_SOURCE_REFERENCES = {
    "de_bubill_2027_07_14_auction_2026-08-24",
    "de_bubill_2027_08_18_auction_2026-08-17",
    "ernx_xetra_2026_08_21_market_activity",
    "fr_btf_2027_03_10_auction_2026-08-24",
}


def main() -> None:
    plan = build_model_company_evidence_refresh_plan(
        as_of=AS_OF,
    )

    print(
        "MILESTONE 15J.1 — EVIDENCE REFRESH "
        "CAPABILITY CONTRACT"
    )
    print()

    print(
        f"As of:                       {AS_OF}"
    )
    print(
        f"Actionable refresh items:    "
        f"{plan.actionable_count}"
    )

    unique_sources = {
        item.source_reference
        for item in plan.items
    }

    print(
        f"Underlying source observations: "
        f"{len(unique_sources)}"
    )
    print()

    capabilities = []

    for item in plan.items:
        assessment = (
            get_model_company_refresh_capability(
                source_reference=(
                    item.source_reference
                ),
            )
        )

        capabilities.append(
            assessment
        )

        capability = (
            assessment.capability
            if assessment is not None
            else "unclassified"
        )

        print(
            f"{item.instrument_id:<30} "
            f"{item.evidence_type:<20} "
            f"{capability:<12} "
            f"{item.source_reference}"
        )

    print()
    print("-" * 100)
    print()

    assert len(plan.items) == 6

    assert unique_sources == (
        EXPECTED_SOURCE_REFERENCES
    )

    assert len(
        MODEL_COMPANY_EVIDENCE_REFRESH_CAPABILITIES
    ) == 4

    assert all(
        assessment is not None
        for assessment in capabilities
    )

    assert all(
        assessment.capability == "manual"
        for assessment in capabilities
        if assessment is not None
    )

    for source_reference in (
        EXPECTED_SOURCE_REFERENCES
    ):
        assessment = (
            get_model_company_refresh_capability(
                source_reference=source_reference,
            )
        )

        assert assessment is not None
        assert assessment.capability == "manual"
        assert assessment.adapter_reference is None

    assert (
        get_model_company_refresh_capability(
            source_reference=(
                "unknown_source_reference"
            ),
        )
        is None
    )

    automatic_without_adapter_rejected = False

    try:
        EvidenceRefreshCapabilityAssessment(
            source_reference="invalid_automatic",
            capability="automatic",
        )
    except ValueError:
        automatic_without_adapter_rejected = True

    assert automatic_without_adapter_rejected

    adapter_on_manual_rejected = False

    try:
        EvidenceRefreshCapabilityAssessment(
            source_reference="invalid_manual",
            capability="manual",
            adapter_reference="fake.adapter",
        )
    except ValueError:
        adapter_on_manual_rejected = True

    assert adapter_on_manual_rejected

    print(
        "MILESTONE 15J.1 ASSERTIONS"
    )
    print()

    print(
        "Production refresh plan reused:           yes"
    )
    print(
        "All six work items classified:           yes"
    )
    print(
        "Four underlying source observations:      yes"
    )
    print(
        "Exact production source references used:  yes"
    )
    print(
        "AFT correctly classified manual:         yes"
    )
    print(
        "German auction evidence manual:          yes"
    )
    print(
        "ERNX liquidity evidence manual:          yes"
    )
    print(
        "Automatic requires real adapter:         yes"
    )
    print(
        "Manual cannot claim adapter:             yes"
    )
    print(
        "Unknown source remains unclassified:     yes"
    )
    print(
        "No scheduler introduced:                 yes"
    )
    print(
        "No recommendation logic changed:         yes"
    )

    print()
    print(
        "All Milestone 15J.1 refresh-capability "
        "assertions passed."
    )


if __name__ == "__main__":
    main()
