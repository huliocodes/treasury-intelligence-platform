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
        prior_analysis_status="complete",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=True,
        position_liquidity_evidence_sufficient=True,
        execution_cost_evidence_sufficient=True,
        risk_evidence_sufficient=True,
        reusable_analysis_summary=(
            "Completed V1 Franklin analysis uses the generic ETF "
            "position, liquidity, risk, eligibility and return pipeline. "
            "The candidate is recommendation-ready through €2 million "
            "and correctly requires stronger liquidity evidence at "
            "€5 million."
        ),
        evidence_notes=(
            "Franklin reported 2.78% portfolio YTM, 0.15% TER, "
            "0.76-year duration, AA- average credit quality, "
            "80 holdings and approximately €597.73 million AUM.",
            "Modeled defensible return is 2.430% after product and "
            "execution costs.",
            "At €5 million the position is approximately 0.8365% of "
            "fund scale, above the generic 0.50% strong-inference "
            "threshold, so recommendation readiness correctly remains "
            "position-size dependent.",
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
        prior_analysis_status="complete",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=True,
        position_liquidity_evidence_sufficient=True,
        execution_cost_evidence_sufficient=True,
        risk_evidence_sufficient=True,
        reusable_analysis_summary=(
            "DE000BU0E444 is now recommendation-ready through the full "
            "downstream analysis pipeline. The 17 August 2026 auction "
            "yield, EUR 3.0 billion current issue scale, German sovereign "
            "risk evidence, IBKR OTC execution-cost model and position-size "
            "liquidity analysis are integrated."
        ),
        evidence_notes=(
            "At EUR 5 million the position represents approximately "
            "0.1667% of current issue outstanding and receives supported "
            "position-aware liquidity status.",
            "The existing V1 pipeline produces a defensible return of "
            "approximately 2.556% at EUR 5 million with no recommendation "
            "blockers or remaining evidence requirements.",
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
        prior_analysis_status="complete",
        identity_evidence_sufficient=True,
        corporate_access_evidence_sufficient=True,
        current_market_return_evidence_sufficient=True,
        realistic_net_return_evidence_sufficient=True,
        position_liquidity_evidence_sufficient=True,
        execution_cost_evidence_sufficient=True,
        risk_evidence_sufficient=True,
        reusable_analysis_summary=(
            "FR0129704187 is now recommendation-ready through the full "
            "downstream analysis pipeline. The 31 August 2026 auction "
            "yield, EUR 8.135 billion issue scale, French sovereign risk "
            "evidence, IBKR OTC execution-cost model and position-size "
            "liquidity analysis are integrated."
        ),
        evidence_notes=(
            "At EUR 5 million the position represents approximately "
            "0.0615% of issue outstanding and receives supported "
            "position-aware liquidity status.",
            "The existing V1 pipeline produces a defensible return of "
            "approximately 2.760% at EUR 5 million with no recommendation "
            "blockers or remaining evidence requirements.",
        ),
    )