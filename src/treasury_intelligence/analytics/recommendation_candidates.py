from __future__ import annotations

from treasury_intelligence.analytics.universe_candidates import (
    DEFAULT_HOLDING_PERIOD_DAYS,
    build_btf_2027_08_11_universe_candidate,
    build_btf_universe_candidate,
    build_bubill_2027_08_18_universe_candidate,
    build_bubill_universe_candidate,
    build_ernx_universe_candidate,
    build_franklin_euro_short_maturity_universe_candidate,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)

from treasury_intelligence.models.portfolio import (
    PortfolioCandidateAssessment,
)


def build_ernx_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    return build_ernx_universe_candidate(
        position_size_eur=position_size_eur,
        mandate=mandate,
        holding_period_days=holding_period_days,
    )


def build_franklin_euro_short_maturity_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    return (
        build_franklin_euro_short_maturity_universe_candidate(
            position_size_eur=position_size_eur,
            mandate=mandate,
            holding_period_days=holding_period_days,
        )
    )


def build_btf_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    return build_btf_universe_candidate(
        position_size_eur=position_size_eur,
        mandate=mandate,
        holding_period_days=holding_period_days,
    )


def build_btf_2027_08_11_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    return build_btf_2027_08_11_universe_candidate(
        position_size_eur=position_size_eur,
        mandate=mandate,
        holding_period_days=holding_period_days,
    )


def build_bubill_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    return build_bubill_universe_candidate(
        position_size_eur=position_size_eur,
        mandate=mandate,
        holding_period_days=holding_period_days,
    )


def build_bubill_2027_08_18_recommendation_candidate(
    position_size_eur: float,
    mandate: TreasuryMandate = MODEL_COMPANY_MANDATE,
    holding_period_days: int = DEFAULT_HOLDING_PERIOD_DAYS,
) -> PortfolioCandidateAssessment:
    return build_bubill_2027_08_18_universe_candidate(
        position_size_eur=position_size_eur,
        mandate=mandate,
        holding_period_days=holding_period_days,
    )