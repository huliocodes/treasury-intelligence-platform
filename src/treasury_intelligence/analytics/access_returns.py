from __future__ import annotations

from dataclasses import replace

from treasury_intelligence.sources.ibkr import (
    BrokerRecurringAccessCostEvidence,
)


XEON_ACCESS_FEE_COMPONENT_ID = (
    "xeon_access_fee"
)


def apply_xeon_access_cost_evidence(
    components: tuple,
    access_cost_evidence: BrokerRecurringAccessCostEvidence,
) -> tuple:
    if not components:
        raise ValueError(
            "Return components are required."
        )

    matching_components = tuple(
        component
        for component in components
        if getattr(
            component,
            "component_id",
            None,
        )
        == XEON_ACCESS_FEE_COMPONENT_ID
    )

    if len(matching_components) != 1:
        raise ValueError(
            "Exactly one XEON access-fee "
            "component is required."
        )

    if (
        access_cost_evidence
        .generic_custody_fee_identified
    ):
        raise ValueError(
            "Cannot apply zero recurring access "
            "cost when a generic custody fee has "
            "been identified for the route."
        )

    source_reference = None

    if access_cost_evidence.source_references:
        source_reference = (
            access_cost_evidence
            .source_references[0]
        )

    enriched_components = []

    for component in components:
        if (
            component.component_id
            != XEON_ACCESS_FEE_COMPONENT_ID
        ):
            enriched_components.append(
                component
            )
            continue

        enriched_component = replace(
            component,
            label=(
                "Published recurring IBKR access "
                "cost for Germany/Xetra ETF route"
            ),
            status="published",
            basis="annualized_pct",
            value=(
                access_cost_evidence
                .recurring_access_cost_pct
            ),
            source="Interactive Brokers",
            source_url=source_reference,
            notes=(
                "IBKR public pricing supports a "
                "zero recurring access-cost "
                "assumption for the modeled "
                "organization-account "
                "Germany/Xetra ETF route: account "
                "minimum and inactivity fee are "
                "published as zero, platform fees "
                "are stated as absent, and no "
                "generic German/Xetra ETF custody "
                "fee is identified in the current "
                "published Other Fees schedule. "
                "This does not represent approval "
                "or contractual confirmation for "
                "a specific future Slovenian "
                "d.o.o. account. Specific-account "
                "terms remain an execution-stage "
                "confirmation."
            ),
        )

        enriched_components.append(
            enriched_component
        )

    return tuple(
        enriched_components
    )