from __future__ import annotations

from treasury_intelligence.analytics.risk import (
    get_aave_eurc_risk_observations,
    get_btf_risk_observations,
    get_ernx_risk_observations,
    get_xeon_risk_observations,
)

from treasury_intelligence.models.risk import (
    RISK_DIMENSIONS,
    RiskObservation,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


ASSESSED_AT = "2026-08-29"


def _observation_ids(
    observations: tuple[RiskObservation, ...],
    risk_dimension: str,
) -> tuple[str, ...]:
    return tuple(
        observation.observation_id
        for observation in observations
        if observation.risk_dimension == risk_dimension
    )


def _unknown_assessment(
    assessment_id: str,
    instrument_id: str,
    market_id: str,
    risk_dimension: str,
    rationale: str,
    supporting_observation_ids: tuple[str, ...] = (),
) -> RiskAssessment:
    return RiskAssessment(
        assessment_id=assessment_id,
        instrument_id=instrument_id,
        market_id=market_id,
        risk_dimension=risk_dimension,
        risk_level="unknown",
        rationale=rationale,
        supporting_observation_ids=supporting_observation_ids,
        assessed_at=ASSESSED_AT,
        evidence_sufficient=False,
    )


def _not_applicable_assessment(
    assessment_id: str,
    instrument_id: str,
    market_id: str,
    risk_dimension: str,
    rationale: str,
) -> RiskAssessment:
    return RiskAssessment(
        assessment_id=assessment_id,
        instrument_id=instrument_id,
        market_id=market_id,
        risk_dimension=risk_dimension,
        risk_level="not_applicable",
        rationale=rationale,
        supporting_observation_ids=(),
        assessed_at=ASSESSED_AT,
        evidence_sufficient=True,
    )


def get_aave_eurc_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = (
        get_aave_eurc_risk_observations()
    )

    instrument_id = observations[0].instrument_id
    market_id = observations[0].market_id

    return (
        _unknown_assessment(
            assessment_id=(
                "aave_base_eurc_principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            rationale=(
                "Current observations do not yet provide "
                "sufficient borrower, collateral, liquidation, "
                "bad-debt, or loss-mechanism evidence for a "
                "qualitative principal/credit assessment."
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "aave_base_eurc_market"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="market",
            rationale=(
                "Current observations establish the market type "
                "but do not yet provide sufficient rate-volatility, "
                "utilization, collateral-market, or stress evidence "
                "for a qualitative market-risk assessment."
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "aave_base_eurc_liquidity"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="liquidity",
            rationale=(
                "Liquidity is position-size dependent. Existing "
                "position analysis contains direct available-"
                "liquidity information, but position-aware "
                "liquidity risk assessment has not yet been "
                "integrated into this layer."
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "aave_base_eurc_currency_asset"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="currency_asset",
            rationale=(
                "The position uses EURC and is modeled as having "
                "EUR economic FX exposure, but the current risk "
                "observations do not yet contain sufficient issuer, "
                "reserve, redemption, convertibility, or historical "
                "depeg evidence to assign a qualitative asset-risk "
                "level."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "currency_asset",
                )
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "aave_base_eurc_structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            rationale=(
                "The observation layer establishes that this is an "
                "onchain overcollateralized lending market. That "
                "identifies relevant protocol, collateral, oracle, "
                "liquidation, and market-structure dependencies, "
                "but current evidence is insufficient to grade the "
                "severity of those dependencies."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "aave_base_eurc_technical"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="technical",
            rationale=(
                "The position depends on Aave V3 smart contracts "
                "and Base blockchain execution. This establishes "
                "that technical failure modes exist, but current "
                "observations do not yet contain sufficient audit, "
                "upgrade-control, oracle, incident-history, or "
                "protocol-security evidence to assign a qualitative "
                "technical-risk level."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "technical",
                )
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "aave_base_eurc_operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "operational_regulatory"
            ),
            rationale=(
                "The full Slovenian d.o.o. operating path from EUR "
                "banking through EURC acquisition, Aave usage, "
                "redemption, accounting, custody, and return to the "
                "corporate bank account has not been verified."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "operational_regulatory",
                )
            ),
        ),
    )


def get_btf_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = get_btf_risk_observations()

    instrument_id = observations[0].instrument_id
    market_id = observations[0].market_id

    return (
        _unknown_assessment(
            assessment_id=(
                "btf_2027_03_10_principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            rationale=(
                "The observation layer identifies the French "
                "Republic as issuer, but issuer identity alone is "
                "not sufficient to assign a defensible qualitative "
                "credit-risk level. Sovereign credit evidence has "
                "not yet been incorporated."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "principal_credit",
                )
            ),
        ),
        RiskAssessment(
            assessment_id=(
                "btf_2027_03_10_market"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="market",
            risk_level="low",
            rationale=(
                "The instrument is a short-dated zero-coupon "
                "Treasury bill maturing on 2027-03-10. Its market "
                "price can change before maturity, but the short "
                "remaining maturity limits interest-rate sensitivity "
                "relative to longer-duration fixed-income "
                "instruments."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "market",
                )
            ),
            assessed_at=ASSESSED_AT,
            evidence_sufficient=True,
        ),
        _unknown_assessment(
            assessment_id=(
                "btf_2027_03_10_liquidity"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="liquidity",
            rationale=(
                "Issue size provides market-scale context but does "
                "not establish executable secondary-market depth "
                "for the treasury's position size."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "liquidity",
                )
            ),
        ),
        RiskAssessment(
            assessment_id=(
                "btf_2027_03_10_currency_asset"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="currency_asset",
            risk_level="very_low",
            rationale=(
                "The instrument is denominated in EUR, matching the "
                "model treasury's EUR base currency. The position "
                "therefore introduces no material conventional "
                "foreign-exchange mismatch."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "currency_asset",
                )
            ),
            assessed_at=ASSESSED_AT,
            evidence_sufficient=True,
        ),
        _unknown_assessment(
            assessment_id=(
                "btf_2027_03_10_structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            rationale=(
                "The current observation set does not yet contain "
                "sufficient custody, brokerage, settlement, or "
                "market-infrastructure evidence for a qualitative "
                "structural/counterparty assessment."
            ),
        ),
        _not_applicable_assessment(
            assessment_id=(
                "btf_2027_03_10_technical"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="technical",
            rationale=(
                "No smart-contract, oracle, blockchain, or "
                "protocol-level technical dependency is modeled for "
                "this conventional sovereign security. Ordinary "
                "brokerage and settlement infrastructure belongs to "
                "the structural or operational dimensions."
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "btf_2027_03_10_operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "operational_regulatory"
            ),
            rationale=(
                "The access route is considered eligible for V1, "
                "but the current risk-observation set does not yet "
                "contain enough execution, custody, accounting, tax, "
                "and operational evidence for a qualitative "
                "assessment."
            ),
        ),
    )


def get_xeon_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = get_xeon_risk_observations()

    instrument_id = observations[0].instrument_id
    market_id = observations[0].market_id

    return (
        _unknown_assessment(
            assessment_id=(
                "xeon_principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            rationale=(
                "The current observation layer does not yet contain "
                "sufficient swap-counterparty, collateral, "
                "substitution-basket, or loss-mechanism evidence "
                "for a principal/credit assessment."
            ),
        ),
        RiskAssessment(
            assessment_id="xeon_market",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="market",
            risk_level="low",
            rationale=(
                "The ETF targets a short-term euro overnight-rate "
                "index. Its rate sensitivity is therefore "
                "substantially shorter than that of conventional "
                "longer-duration bond portfolios, although ETF "
                "pricing and tracking can still vary."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "market",
                )
            ),
            assessed_at=ASSESSED_AT,
            evidence_sufficient=True,
        ),
        _unknown_assessment(
            assessment_id="xeon_liquidity",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="liquidity",
            rationale=(
                "Large fund AUM and observed Xetra turnover provide "
                "market-activity context but do not establish "
                "position-size executable exit depth."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "liquidity",
                )
            ),
        ),
        RiskAssessment(
            assessment_id=(
                "xeon_currency_asset"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="currency_asset",
            risk_level="very_low",
            rationale=(
                "The instrument and its target economic exposure "
                "are EUR-based, matching the model treasury's base "
                "currency and therefore avoiding a material "
                "conventional FX mismatch."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "currency_asset",
                )
            ),
            assessed_at=ASSESSED_AT,
            evidence_sufficient=True,
        ),
        _unknown_assessment(
            assessment_id=(
                "xeon_structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            rationale=(
                "Synthetic swap replication establishes the presence "
                "of swap-counterparty and collateral-structure "
                "dependencies. Current observations do not yet "
                "describe the counterparties, collateral, exposure "
                "limits, reset mechanics, or protections sufficiently "
                "to grade their severity."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
        ),
        _not_applicable_assessment(
            assessment_id="xeon_technical",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="technical",
            rationale=(
                "No smart-contract, oracle, blockchain, or "
                "protocol-level technical dependency is modeled for "
                "this exchange-traded UCITS ETF. Trading, custody, "
                "and settlement infrastructure belongs to other risk "
                "dimensions."
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "xeon_operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "operational_regulatory"
            ),
            rationale=(
                "The V1 corporate brokerage route is considered "
                "accessible, but the current observation layer does "
                "not yet provide sufficient execution, custody, "
                "accounting, tax, or operational evidence for a "
                "qualitative assessment."
            ),
        ),
    )


def get_ernx_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = get_ernx_risk_observations()

    instrument_id = observations[0].instrument_id
    market_id = observations[0].market_id

    return (
        RiskAssessment(
            assessment_id=(
                "ernx_principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            risk_level="low",
            rationale=(
                "The portfolio provides diversified exposure to "
                "short-duration investment-grade credit across 671 "
                "securities. Credit loss and spread deterioration "
                "remain possible, so this is not equivalent to cash "
                "or a direct sovereign Treasury bill."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "principal_credit",
                )
            ),
            assessed_at=ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "A later assessment can become more granular once "
                "rating distribution, sector concentration, issuer "
                "concentration, and default-risk evidence are "
                "ingested."
            ),
        ),
        RiskAssessment(
            assessment_id="ernx_market",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="market",
            risk_level="low",
            rationale=(
                "Observed effective duration of 0.36 years and "
                "weighted average maturity of 0.62 years indicate "
                "limited interest-rate sensitivity relative to "
                "longer-duration bond portfolios. Credit-spread and "
                "market-price movements can still affect value."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "market",
                )
            ),
            assessed_at=ASSESSED_AT,
            evidence_sufficient=True,
        ),
        _unknown_assessment(
            assessment_id="ernx_liquidity",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="liquidity",
            rationale=(
                "Share-class AUM and sampled Xetra turnover provide "
                "product-scale and market-activity context but do not "
                "establish position-size executable exit depth."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "liquidity",
                )
            ),
        ),
        RiskAssessment(
            assessment_id=(
                "ernx_currency_asset"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="currency_asset",
            risk_level="very_low",
            rationale=(
                "The instrument is EUR-denominated, matching the "
                "model treasury's base currency and therefore "
                "avoiding a material conventional FX mismatch."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "currency_asset",
                )
            ),
            assessed_at=ASSESSED_AT,
            evidence_sufficient=True,
        ),
        _unknown_assessment(
            assessment_id=(
                "ernx_structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            rationale=(
                "Physical sampled replication means the fund does "
                "not depend on synthetic swap replication for its "
                "core exposure. However, the current observation "
                "layer does not yet contain sufficient custody, "
                "securities-lending, fund-structure, or "
                "counterparty evidence to grade structural risk."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
        ),
        _not_applicable_assessment(
            assessment_id="ernx_technical",
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="technical",
            rationale=(
                "No smart-contract, oracle, blockchain, or "
                "protocol-level technical dependency is modeled for "
                "this exchange-traded UCITS ETF. Trading, custody, "
                "and settlement infrastructure belongs to other risk "
                "dimensions."
            ),
        ),
        _unknown_assessment(
            assessment_id=(
                "ernx_operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "operational_regulatory"
            ),
            rationale=(
                "The V1 corporate brokerage route is considered "
                "accessible, but the current observation layer does "
                "not yet provide sufficient execution, custody, "
                "accounting, tax, or operational evidence for a "
                "qualitative assessment."
            ),
        ),
    )


def get_all_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    return (
        get_aave_eurc_risk_assessments()
        + get_btf_risk_assessments()
        + get_xeon_risk_assessments()
        + get_ernx_risk_assessments()
    )


def validate_dimension_coverage(
    assessments: tuple[RiskAssessment, ...],
) -> None:
    dimensions = tuple(
        assessment.risk_dimension
        for assessment in assessments
    )

    if len(dimensions) != len(RISK_DIMENSIONS):
        raise ValueError(
            "Expected exactly one assessment for each "
            "risk dimension."
        )

    if set(dimensions) != set(RISK_DIMENSIONS):
        raise ValueError(
            "Risk assessments do not cover exactly the "
            "seven required risk dimensions."
        )