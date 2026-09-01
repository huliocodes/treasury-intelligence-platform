from __future__ import annotations

from treasury_intelligence.models.research_triage import (
    ResearchEvidenceState,
)


def build_model_company_research_evidence_states() -> tuple[
    ResearchEvidenceState,
    ...,
]:
    return (
        _slovenia_tz233(),
        _slovenia_sz163(),
        _slovenia_dz125(),
        _icash(),
        _ernx(),
        _franklin_euro_short_maturity(),
        _ishares_eur_government_0_1y(),
        _german_bubill_bu0e436(),
        _german_bubill_bu0e444(),
        _french_btf_mar_2027(),
        _french_btf_aug_2027(),
    )


def _slovenia_tz233() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="slovenia_tbill_tz233",
        prior_analysis_status="none",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=False,
        realistic_net_return_evidence_sufficient=False,
        position_liquidity_evidence_sufficient=False,
        execution_cost_evidence_sufficient=False,
        risk_evidence_sufficient=False,
        reusable_analysis_summary=(
            "Official Slovenian Treasury-bill issuance mechanics and "
            "corporate access are already established."
        ),
        evidence_notes=(
            "Auction is scheduled for 8 September 2026, so current yield "
            "evidence does not yet exist.",
        ),
    )


def _slovenia_sz163() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="slovenia_tbill_sz163",
        prior_analysis_status="none",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=False,
        realistic_net_return_evidence_sufficient=False,
        position_liquidity_evidence_sufficient=False,
        execution_cost_evidence_sufficient=False,
        risk_evidence_sufficient=False,
        reusable_analysis_summary=(
            "Official Slovenian Treasury-bill issuance mechanics and "
            "corporate access are already established."
        ),
        evidence_notes=(
            "Auction is scheduled for 8 September 2026, so current yield "
            "evidence does not yet exist.",
        ),
    )


def _slovenia_dz125() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="slovenia_tbill_dz125",
        prior_analysis_status="none",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=False,
        realistic_net_return_evidence_sufficient=False,
        position_liquidity_evidence_sufficient=False,
        execution_cost_evidence_sufficient=False,
        risk_evidence_sufficient=False,
        reusable_analysis_summary=(
            "Official Slovenian Treasury-bill issuance mechanics and "
            "corporate access are already established."
        ),
        evidence_notes=(
            "Auction is scheduled for 8 September 2026, so current yield "
            "evidence does not yet exist.",
        ),
    )


def _icash() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="icash_ljse",
        prior_analysis_status="none",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=False,
        realistic_net_return_evidence_sufficient=False,
        position_liquidity_evidence_sufficient=False,
        execution_cost_evidence_sufficient=False,
        risk_evidence_sufficient=False,
        reusable_analysis_summary=(
            "Exact LJSE instrument identity and Slovenian corporate "
            "brokerage access were verified in Milestone 13C.3."
        ),
        evidence_notes=(
            "Current fund yield, fees, fund scale, trading liquidity and "
            "€5 million position capacity still require research.",
        ),
    )


def _ernx() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="ernx",
        prior_analysis_status="complete",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=True,
        position_liquidity_evidence_sufficient=True,
        execution_cost_evidence_sufficient=True,
        risk_evidence_sufficient=True,
        reusable_analysis_summary=(
            "Existing V1 ERNX candidate is recommendation-ready through "
            "the full downstream analysis pipeline."
        ),
    )


def _franklin_euro_short_maturity() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="franklin_euro_short_maturity",
        prior_analysis_status="none",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=False,
        position_liquidity_evidence_sufficient=False,
        execution_cost_evidence_sufficient=False,
        risk_evidence_sufficient=False,
        reusable_analysis_summary=(
            "Exact UCITS share class, Xetra listing, corporate access and "
            "recent portfolio yield evidence are already available."
        ),
        evidence_notes=(
            "Recent discovery evidence showed approximately 2.70% YTM, "
            "0.75-year duration and roughly €596 million fund scale.",
            "Full position-size execution and risk analysis remain missing.",
        ),
    )


def _ishares_eur_government_0_1y() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="ishares_eur_government_0_1y",
        prior_analysis_status="none",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=False,
        position_liquidity_evidence_sufficient=False,
        execution_cost_evidence_sufficient=False,
        risk_evidence_sufficient=False,
        reusable_analysis_summary=(
            "Exact UCITS implementation, Xetra access, recent YTM and "
            "fund-scale evidence are already established."
        ),
        evidence_notes=(
            "Discovery evidence showed approximately 2.62% weighted "
            "average YTM and 0.49-year duration.",
            "Full position-size execution and holdings-risk analysis "
            "remain missing.",
        ),
    )


def _german_bubill_bu0e436() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="german_bubill_bu0e436",
        prior_analysis_status="complete",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=True,
        position_liquidity_evidence_sufficient=True,
        execution_cost_evidence_sufficient=True,
        risk_evidence_sufficient=True,
        reusable_analysis_summary=(
            "Existing V1 German Bubill analysis is recommendation-ready "
            "through the full downstream pipeline."
        ),
    )


def _german_bubill_bu0e444() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="german_bubill_bu0e444",
        prior_analysis_status="partial",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=False,
        position_liquidity_evidence_sufficient=False,
        execution_cost_evidence_sufficient=True,
        risk_evidence_sufficient=False,
        reusable_analysis_summary=(
            "The existing German Bubill access route, OTC commission model "
            "and sovereign-bill analytics can be reused."
        ),
        evidence_notes=(
            "The 17 August 2026 auction produced approximately 2.656% "
            "average yield.",
            "Security-specific position liquidity, refreshed sovereign risk "
            "evidence and realistic net return remain incomplete.",
        ),
    )


def _french_btf_mar_2027() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="french_btf_mar_2027",
        prior_analysis_status="complete",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=True,
        position_liquidity_evidence_sufficient=True,
        execution_cost_evidence_sufficient=True,
        risk_evidence_sufficient=True,
        reusable_analysis_summary=(
            "Existing V1 French BTF analysis is recommendation-ready "
            "through the full downstream pipeline."
        ),
    )


def _french_btf_aug_2027() -> ResearchEvidenceState:
    return ResearchEvidenceState(
        opportunity_id="french_btf_aug_2027",
        prior_analysis_status="partial",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=False,
        position_liquidity_evidence_sufficient=False,
        execution_cost_evidence_sufficient=True,
        risk_evidence_sufficient=False,
        reusable_analysis_summary=(
            "The existing French BTF corporate access route, OTC commission "
            "model and sovereign-bill analytics can be reused."
        ),
        evidence_notes=(
            "Exact ISIN FR0129704187 and the 31 August 2026 weighted-average "
            "auction yield of 2.860% are established.",
            "Security-specific liquidity, refreshed sovereign risk evidence "
            "and realistic net return remain incomplete.",
        ),
    )