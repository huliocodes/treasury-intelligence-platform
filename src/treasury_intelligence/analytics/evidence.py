from __future__ import annotations

from treasury_intelligence.models.eligibility import (
    EligibilityResult,
)

from treasury_intelligence.models.evidence import (
    EvidenceGap,
)


def _build_resolution(
    check_name: str,
) -> tuple[str, str, str]:
    if check_name == "immediate_liquidity":
        return (
            "position_liquidity",
            "high",
            (
                "Obtain position-size-specific evidence of "
                "immediate exit liquidity, including executable "
                "bid/ask pricing and available size where applicable."
            ),
        )

    if check_name == "corporate_access":
        return (
            "corporate_accessibility",
            "high",
            (
                "Verify that the exact access route supports a "
                "Slovenian d.o.o. operationally and legally, "
                "including account opening, funding, holding "
                "and withdrawal."
            ),
        )

    if check_name == "settlement":
        return (
            "settlement_terms",
            "medium",
            (
                "Verify the settlement cycle for the exact market "
                "and access route."
            ),
        )

    if check_name == "fx_currency":
        return (
            "currency_exposure",
            "high",
            (
                "Verify the instrument's economic FX exposure "
                "relative to the mandate base currency."
            ),
        )

    if check_name == "target_yield":
        return (
            "yield_economics",
            "medium",
            (
                "Obtain a sufficiently reliable current yield "
                "observation for the proposed position."
            ),
        )

    if check_name == "instrument_type":
        return (
            "instrument_classification",
            "medium",
            (
                "Resolve the instrument classification against "
                "the mandate's permitted instrument types."
            ),
        )

    if check_name == "maximum_single_position":
        return (
            "position_limit",
            "high",
            (
                "Resolve treasury capital or proposed allocation "
                "size needed to test the single-position limit."
            ),
        )

    if check_name == "minimum_useful_allocation":
        return (
            "allocation_size",
            "medium",
            (
                "Resolve the proposed allocation amount against "
                "the mandate minimum."
            ),
        )

    return (
        "other",
        "medium",
        (
            "Obtain evidence sufficient to resolve this "
            "mandate eligibility check."
        ),
    )


def build_evidence_gaps(
    eligibility: EligibilityResult,
) -> tuple[EvidenceGap, ...]:
    gaps: list[EvidenceGap] = []

    for check in eligibility.checks:
        if not check.required:
            continue

        if check.status != "unknown":
            continue

        (
            evidence_type,
            priority,
            resolution_action,
        ) = _build_resolution(
            check.check_name
        )

        required_evidence = (
            check.required_value
            if check.required_value is not None
            else "sufficient evidence to resolve the check"
        )

        gaps.append(
            EvidenceGap(
                evidence_gap_id=(
                    f"{eligibility.result_id}_"
                    f"{check.check_name}"
                ),
                mandate_id=eligibility.mandate_id,
                instrument_id=eligibility.instrument_id,
                market_id=eligibility.market_id,
                access_route_id=(
                    eligibility.access_route_id
                ),
                position_size_eur=(
                    eligibility.position_size_eur
                ),
                check_name=check.check_name,
                evidence_type=evidence_type,
                priority=priority,
                current_status="unknown",
                required_evidence=required_evidence,
                resolution_action=resolution_action,
                blocking=True,
                notes=check.reason,
            )
        )

    return tuple(gaps)