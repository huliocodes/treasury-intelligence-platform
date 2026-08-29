from __future__ import annotations

from treasury_intelligence.models.economics import (
    EconomicsEvidenceAssessment,
    EconomicsEvidenceGap,
)

from treasury_intelligence.models.returns import (
    ReturnAnalysis,
    ReturnComponent,
)


def _gap_priority(
    component: ReturnComponent,
) -> str:
    if component.component_type in (
        "entry_execution_cost",
        "exit_execution_cost",
        "slippage_price_impact",
        "liquidity_cost",
    ):
        return "high"

    if component.component_type in (
        "access_fee",
        "fx_hedging_cost",
        "tax_cost",
        "network_cost",
        "operational_cost",
    ):
        return "high"

    return "medium"


def _required_evidence(
    component: ReturnComponent,
) -> str:
    if (
        component.component_type
        == "slippage_price_impact"
    ):
        return (
            "Position-size-specific executable spread, "
            "slippage, or market-impact evidence for the "
            "modeled entry and exit transaction."
        )

    if (
        component.component_type
        in (
            "entry_execution_cost",
            "exit_execution_cost",
        )
    ):
        return (
            "Execution-cost evidence applicable to the "
            "actual venue, access route, order size, and "
            "pricing plan."
        )

    if (
        component.component_type
        == "access_fee"
    ):
        return (
            "Confirmed corporate account pricing covering "
            "custody, platform, account, and other recurring "
            "access costs applicable to the actual execution "
            "route."
        )

    if (
        component.component_type
        == "network_cost"
    ):
        return (
            "Observed or reliably estimated network "
            "transaction cost for the required execution "
            "path."
        )

    if (
        component.component_type
        == "fx_hedging_cost"
    ):
        return (
            "Position-specific FX conversion or hedging "
            "cost applicable to the treasury execution path."
        )

    if (
        component.component_type
        == "tax_cost"
    ):
        return (
            "Applicable tax treatment and position-specific "
            "tax cost required for the modeled treasury "
            "entity."
        )

    return (
        "Sufficient evidence to quantify this return-cost "
        "component for the modeled position and execution "
        "route."
    )


def _resolution_action(
    component: ReturnComponent,
) -> str:
    if (
        component.component_type
        == "slippage_price_impact"
    ):
        return (
            "Obtain a firm or execution-grade bid/ask and "
            "available size for the modeled position, or "
            "obtain broker execution-cost analysis sufficient "
            "to estimate round-trip spread and market impact."
        )

    if (
        component.component_type
        in (
            "entry_execution_cost",
            "exit_execution_cost",
        )
    ):
        return (
            "Confirm the actual broker pricing plan and "
            "calculate the commission and venue costs for "
            "the modeled order."
        )

    if (
        component.component_type
        == "access_fee"
    ):
        return (
            "Confirm the exact corporate brokerage account "
            "fee schedule, including custody and any recurring "
            "organization-account charges."
        )

    if (
        component.component_type
        == "network_cost"
    ):
        return (
            "Observe the transaction path and estimate the "
            "required network fees using current execution "
            "conditions."
        )

    if (
        component.component_type
        == "fx_hedging_cost"
    ):
        return (
            "Obtain an executable or institutionally "
            "representative FX conversion or hedging quote."
        )

    if (
        component.component_type
        == "tax_cost"
    ):
        return (
            "Determine applicable entity-specific tax "
            "treatment before incorporating tax into net "
            "treasury return."
        )

    return (
        "Obtain evidence sufficient to replace this unknown "
        "component with an observed, published, executable, "
        "model-derived, estimated, or known-zero value."
    )


def _build_gap(
    analysis: ReturnAnalysis,
    component: ReturnComponent,
) -> EconomicsEvidenceGap:
    return EconomicsEvidenceGap(
        evidence_gap_id=(
            f"{analysis.analysis_id}_"
            f"{component.component_id}_gap"
        ),
        return_analysis_id=(
            analysis.analysis_id
        ),
        instrument_id=(
            analysis.instrument_id
        ),
        market_id=(
            analysis.market_id
        ),
        access_route_id=(
            analysis.access_route_id
        ),
        position_size_eur=(
            analysis.position_size_eur
        ),
        holding_period_days=(
            analysis.holding_period_days
        ),
        component_id=(
            component.component_id
        ),
        component_type=(
            component.component_type
        ),
        component_label=(
            component.label
        ),
        component_basis=(
            component.basis
        ),
        current_status=(
            component.status
        ),
        priority=(
            _gap_priority(
                component
            )
        ),
        blocking=True,
        required_evidence=(
            _required_evidence(
                component
            )
        ),
        resolution_action=(
            _resolution_action(
                component
            )
        ),
        notes=(
            "This component blocks a complete realistic "
            "expected return because its economic value "
            "is currently unknown."
        ),
    )


def build_economics_evidence_assessment(
    analysis: ReturnAnalysis,
) -> EconomicsEvidenceAssessment:
    gaps = tuple(
        _build_gap(
            analysis=analysis,
            component=component,
        )
        for component in analysis.components
        if (
            component.component_type
            != "reference_yield"
            and component.status == "unknown"
        )
    )

    blocking_gap_count = len(
        tuple(
            gap
            for gap in gaps
            if gap.blocking
        )
    )

    if (
        analysis.economics_complete
        and blocking_gap_count > 0
    ):
        raise ValueError(
            "Return analysis claims complete economics "
            "while unknown blocking components remain."
        )

    if (
        not analysis.economics_complete
        and blocking_gap_count == 0
    ):
        raise ValueError(
            "Return analysis is incomplete but no unknown "
            "blocking cost component explains why."
        )

    if analysis.economics_complete:
        economics_status = "complete"

        strongest_supported_claim = (
            "The modeled return economics are complete "
            "for the included components, position size, "
            "holding period, and access route."
        )
    else:
        economics_status = "incomplete"

        strongest_supported_claim = (
            "A return after currently known costs can be "
            "calculated, but realistic expected return "
            "cannot yet be established because one or more "
            "required cost components remain unknown."
        )

    return EconomicsEvidenceAssessment(
        assessment_id=(
            f"{analysis.analysis_id}_"
            "economics_evidence"
        ),
        return_analysis_id=(
            analysis.analysis_id
        ),
        instrument_id=(
            analysis.instrument_id
        ),
        market_id=(
            analysis.market_id
        ),
        access_route_id=(
            analysis.access_route_id
        ),
        position_size_eur=(
            analysis.position_size_eur
        ),
        holding_period_days=(
            analysis.holding_period_days
        ),
        economics_status=(
            economics_status
        ),
        realistic_expected_return_available=(
            analysis.realistic_expected_return_pct
            is not None
        ),
        blocking_gap_count=(
            blocking_gap_count
        ),
        evidence_gaps=gaps,
        strongest_supported_claim=(
            strongest_supported_claim
        ),
        notes=(
            "Only explicit unknown components already "
            "included in ReturnAnalysis are converted into "
            "economics evidence gaps. Missing components "
            "are not invented automatically."
        ),
    )