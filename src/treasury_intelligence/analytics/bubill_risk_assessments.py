from __future__ import annotations

from collections.abc import Callable

from treasury_intelligence.analytics.bubill_risk_evidence import (
    get_bubill_2027_08_18_recommendation_risk_observations,
    get_bubill_recommendation_risk_observations,
)

from treasury_intelligence.models.opportunities import (
    Instrument,
    Market,
)

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)

from treasury_intelligence.sources.germany import (
    BUBILL_2027_07_14,
    BUBILL_2027_07_14_MARKET,
    BUBILL_2027_08_18,
    BUBILL_2027_08_18_MARKET,
)


BUBILL_ASSESSED_AT = "2026-09-01"


def _observation_ids(
    observations: tuple[RiskObservation, ...],
    risk_dimension: str,
) -> tuple[str, ...]:
    return tuple(
        observation.observation_id
        for observation in observations
        if observation.risk_dimension
        == risk_dimension
    )


def _build_bubill_risk_assessments(
    *,
    instrument: Instrument,
    market: Market,
    observation_builder: Callable[
        [],
        tuple[RiskObservation, ...],
    ],
    assessment_id_prefix: str,
    maturity_date_text: str,
) -> tuple[RiskAssessment, ...]:
    observations = observation_builder()

    instrument_id = instrument.instrument_id
    market_id = market.market_id

    return (
        RiskAssessment(
            assessment_id=(
                f"{assessment_id_prefix}_"
                "principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            risk_level="low",
            rationale=(
                "The security is a direct short-term "
                "obligation of the Federal Republic "
                "of Germany. The German Finance Agency "
                "currently reports AAA or Aaa long-term "
                "ratings with stable outlooks across "
                "Fitch, DBRS Morningstar, Standard & "
                "Poor's, Moody's, Scope and KBRA. "
                "This represents exceptionally strong "
                "sovereign credit quality. Sovereign "
                "default, fiscal deterioration and "
                "rating migration nevertheless remain "
                "non-zero risks, so the classification "
                "is low rather than very_low."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "principal_credit",
                )
            ),
            assessed_at=BUBILL_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "The qualitative risk scale deliberately "
                "does not equate an AAA/Aaa rating with "
                "zero or negligible sovereign credit "
                "risk."
            ),
        ),
        RiskAssessment(
            assessment_id=(
                f"{assessment_id_prefix}_market"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="market",
            risk_level="low",
            rationale=(
                f"{instrument.isin} is a short-dated "
                "zero-coupon German Treasury discount "
                f"paper maturing on {maturity_date_text}. "
                "Its secondary-market price can change "
                "before maturity, but its short remaining "
                "term limits interest-rate sensitivity "
                "relative to longer-duration fixed-income "
                "securities."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "market",
                )
            ),
            assessed_at=BUBILL_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                f"{assessment_id_prefix}_liquidity"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="liquidity",
            risk_level="unknown",
            rationale=(
                "Base liquidity remains intentionally "
                "ungraded because liquidity is "
                "position-size dependent. Position "
                "analysis separately evaluates current "
                "issue scale relative to the requested "
                "allocation size."
            ),
            supporting_observation_ids=(),
            assessed_at=BUBILL_ASSESSED_AT,
            evidence_sufficient=False,
            notes=(
                "Liquidity is excluded from the current "
                "base-risk mandate gate because the "
                "position-aware liquidity layer handles "
                "this dimension."
            ),
        ),
        RiskAssessment(
            assessment_id=(
                f"{assessment_id_prefix}_"
                "currency_asset"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="currency_asset",
            risk_level="very_low",
            rationale=(
                "The instrument is issued and traded "
                "in EUR, matching the model treasury's "
                "EUR base currency. The position "
                "therefore introduces no material "
                "conventional foreign-exchange mismatch."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "currency_asset",
                )
            ),
            assessed_at=BUBILL_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                f"{assessment_id_prefix}_"
                "structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            risk_level="low",
            rationale=(
                "The position is a direct Federal "
                "Republic of Germany Treasury discount "
                "paper rather than a fund share, "
                "structured product, derivative claim, "
                "tokenized wrapper or lending-protocol "
                "position. It therefore avoids material "
                "investment-wrapper and derivative-"
                "counterparty dependencies. Residual "
                "broker, custodian, depository, "
                "settlement and administrative "
                "dependencies remain, so structural "
                "risk is low rather than negligible "
                "or not applicable."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
            assessed_at=BUBILL_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "This assessment does not assert that "
                "brokerage or settlement infrastructure "
                "cannot fail. It reflects the simple "
                "direct-sovereign-security structure."
            ),
        ),
        RiskAssessment(
            assessment_id=(
                f"{assessment_id_prefix}_technical"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="technical",
            risk_level="not_applicable",
            rationale=(
                "No smart-contract, oracle, blockchain "
                "or protocol-level technical dependency "
                "is modeled for this conventional "
                "sovereign security. Ordinary brokerage "
                "and settlement infrastructure belongs "
                "to the structural or operational risk "
                "dimensions."
            ),
            supporting_observation_ids=(),
            assessed_at=BUBILL_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                f"{assessment_id_prefix}_"
                "operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "operational_regulatory"
            ),
            risk_level="low",
            rationale=(
                "The modeled route uses a conventional "
                "regulated corporate brokerage to hold "
                "a conventional sovereign security. "
                "IBKR Ireland states that client money "
                "is segregated, fully paid client "
                "securities are held through designated "
                "depositories and custodians for "
                "clients' benefit, and client money "
                "and securities are reconciled daily. "
                "These controls provide sufficient "
                "recommendation-stage evidence for a "
                "low operational and regulatory risk "
                "assessment while ordinary broker, "
                "custody, settlement, account-"
                "configuration and administrative "
                "risks remain."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "operational_regulatory",
                )
            ),
            assessed_at=BUBILL_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Company-specific accounting, tax "
                "treatment, internal authorization, "
                "final account setup and instrument "
                "permissions remain execution-stage "
                "checks unless a specific restriction "
                "is discovered."
            ),
        ),
    )


def get_bubill_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    return _build_bubill_risk_assessments(
        instrument=BUBILL_2027_07_14,
        market=BUBILL_2027_07_14_MARKET,
        observation_builder=(
            get_bubill_recommendation_risk_observations
        ),
        assessment_id_prefix=(
            "de_bubill_2027_07_14"
        ),
        maturity_date_text="14 July 2027",
    )


def get_bubill_2027_08_18_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    return _build_bubill_risk_assessments(
        instrument=BUBILL_2027_08_18,
        market=BUBILL_2027_08_18_MARKET,
        observation_builder=(
            get_bubill_2027_08_18_recommendation_risk_observations
        ),
        assessment_id_prefix=(
            "de_bubill_2027_08_18"
        ),
        maturity_date_text="18 August 2027",
    )