from __future__ import annotations

from treasury_intelligence.models.evidence_refresh_capabilities import (
    EvidenceRefreshCapabilityAssessment,
)


MODEL_COMPANY_EVIDENCE_REFRESH_CAPABILITIES = (
    EvidenceRefreshCapabilityAssessment(
        source_reference=(
            "ernx_xetra_2026_08_21_market_activity"
        ),
        capability="manual",
        notes=(
            "ERNX market-liquidity evidence currently "
            "depends on delayed public MarketScreener "
            "evidence. No production refresh adapter "
            "exists."
        ),
    ),
    EvidenceRefreshCapabilityAssessment(
        source_reference=(
            "fr_btf_2027_03_10_auction_2026-08-24"
        ),
        capability="manual",
        notes=(
            "Agence France Tresor publishes exact "
            "security auction evidence, but repeated "
            "HTTP validation showed nondeterministic "
            "Cloudflare access. The source is suitable "
            "for analyst verification but is not treated "
            "as an automatic production adapter."
        ),
    ),
    EvidenceRefreshCapabilityAssessment(
        source_reference=(
            "de_bubill_2027_07_14_auction_2026-08-24"
        ),
        capability="manual",
        notes=(
            "German Finance Agency auction evidence is "
            "currently maintained as researched source "
            "evidence. No production refresh adapter "
            "exists."
        ),
    ),
    EvidenceRefreshCapabilityAssessment(
        source_reference=(
            "de_bubill_2027_08_18_auction_2026-08-17"
        ),
        capability="manual",
        notes=(
            "German Finance Agency auction evidence is "
            "currently maintained as researched source "
            "evidence. No production refresh adapter "
            "exists."
        ),
    ),
)


def get_model_company_refresh_capability(
    *,
    source_reference: str,
) -> EvidenceRefreshCapabilityAssessment | None:
    matches = tuple(
        assessment
        for assessment
        in MODEL_COMPANY_EVIDENCE_REFRESH_CAPABILITIES
        if assessment.source_reference == source_reference
    )

    if len(matches) > 1:
        raise ValueError(
            "Duplicate refresh capability for "
            f"{source_reference}."
        )

    if not matches:
        return None

    return matches[0]
