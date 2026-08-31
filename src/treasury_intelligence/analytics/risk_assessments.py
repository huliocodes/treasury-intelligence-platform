from __future__ import annotations

from treasury_intelligence.analytics.btf_risk_evidence import (
    get_btf_recommendation_risk_observations,
)

from treasury_intelligence.analytics.ernx_risk_evidence import (
    get_ernx_recommendation_risk_observations,
)

from treasury_intelligence.analytics.risk import (
    get_aave_eurc_risk_observations,
    get_btf_risk_observations,
    get_ernx_risk_observations,
    get_xeon_risk_observations,
)

from treasury_intelligence.analytics.xeon_risk_evidence import (
    get_xeon_recommendation_risk_observations,
)

from treasury_intelligence.models.risk import (
    RISK_DIMENSIONS,
    RiskObservation,
)

from treasury_intelligence.models.risk_assessments import (
    RiskAssessment,
)


ASSESSED_AT = "2026-08-29"
ERNX_ASSESSED_AT = "2026-08-31"
XEON_ASSESSED_AT = "2026-08-31"
BTF_ASSESSED_AT = "2026-08-31"


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
    observations = (
        get_btf_risk_observations()
        + get_btf_recommendation_risk_observations()
    )

    instrument_id = observations[0].instrument_id
    market_id = observations[0].market_id

    return (
        RiskAssessment(
            assessment_id=(
                "btf_2027_03_10_principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            risk_level="low",
            rationale=(
                "The security is a direct short-term "
                "obligation of the French Republic. "
                "France remains strongly investment-grade: "
                "Fitch affirmed its A+ sovereign rating "
                "with a Stable Outlook on 28 August 2026, "
                "while AFT reports a broader set of major "
                "agency sovereign ratings spanning A+ "
                "through the AA and AAA ranges. Sovereign "
                "default and fiscal deterioration are "
                "therefore remote but not negligible, "
                "particularly given weaker fiscal metrics "
                "and negative outlooks at some agencies. "
                "This supports a low rather than very-low "
                "principal/credit risk classification."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "principal_credit",
                )
            ),
            assessed_at=BTF_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Low does not mean equivalent to insured "
                "cash or a risk-free asset. The assessment "
                "reflects strong investment-grade French "
                "sovereign credit quality together with "
                "non-zero fiscal, political, downgrade, "
                "and sovereign-default risk."
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
        RiskAssessment(
            assessment_id=(
                "btf_2027_03_10_structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            risk_level="low",
            rationale=(
                "The position is a direct French Republic "
                "Treasury bill rather than a fund share, "
                "structured product, derivative claim, "
                "tokenized wrapper, or lending-protocol "
                "position. It therefore avoids material "
                "investment-wrapper and derivative-"
                "counterparty dependencies. Residual "
                "broker, custodian, depository, settlement, "
                "and administrative dependencies remain, "
                "so structural risk is low rather than "
                "not applicable or negligible."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
            assessed_at=BTF_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "This assessment does not assert that "
                "settlement infrastructure cannot fail. "
                "It reflects the comparatively simple "
                "direct-sovereign-security structure and "
                "separates ordinary custody and brokerage "
                "operations from the issuer's credit risk."
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
        RiskAssessment(
            assessment_id=(
                "btf_2027_03_10_operational_regulatory"
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
                "is segregated, fully paid customer "
                "securities are held through designated "
                "depositories and custodians for clients' "
                "benefit, and customer securities and "
                "money are reconciled daily. These controls "
                "provide sufficient recommendation-stage "
                "evidence for a low operational and "
                "regulatory risk assessment while ordinary "
                "broker, custody, settlement, account-"
                "configuration, and administrative risks "
                "remain."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "operational_regulatory",
                )
            ),
            assessed_at=BTF_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Company-specific accounting, tax "
                "treatment, internal authorization, final "
                "account setup, and instrument permissions "
                "remain execution-stage checks unless a "
                "specific restriction is discovered."
            ),
        ),
    )


def get_xeon_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = (
        get_xeon_risk_observations()
        + get_xeon_recommendation_risk_observations()
    )

    instrument_id = observations[0].instrument_id
    market_id = observations[0].market_id

    return (
        RiskAssessment(
            assessment_id=(
                "xeon_principal_credit"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension="principal_credit",
            risk_level="moderate",
            rationale=(
                "XEON obtains its target exposure through "
                "indirect swap replication rather than by "
                "directly holding an overnight deposit. DWS "
                "states that Xtrackers UCITS ETFs may have "
                "up to 10% net counterparty exposure to a "
                "single counterparty under UCITS limits and "
                "that default of an OTC derivative "
                "counterparty in an indirectly replicated ETF "
                "can lead to fund liquidation and investor "
                "losses of up to 10% of NAV through that "
                "counterparty-default mechanism. Collateral "
                "and regulatory exposure limits mitigate this "
                "risk but do not eliminate principal-loss "
                "potential."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "principal_credit",
                )
            ),
            assessed_at=XEON_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Moderate is a mandate classification, not "
                "an estimate of expected loss. The documented "
                "maximum counterparty exposure and default-loss "
                "mechanism are materially less compatible with "
                "a very-high-capital-preservation treasury "
                "mandate than the low-risk structures accepted "
                "by the current V1 policy."
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
        RiskAssessment(
            assessment_id=(
                "xeon_structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            risk_level="moderate",
            rationale=(
                "XEON is a Luxembourg UCITS ETF using "
                "indirect swap replication with a named "
                "fund custodian. Its structure therefore "
                "depends on one or more swap counterparties "
                "performing derivative obligations. UCITS "
                "counterparty-exposure limits and EMIR "
                "collateral exchange mitigate this dependency, "
                "but DWS explicitly states that counterparty "
                "failure can cause losses, dealing suspension, "
                "or liquidation of an indirectly replicated "
                "ETF. These protections reduce but do not "
                "remove the structural dependency."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
            assessed_at=XEON_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "The assessment is moderate rather than high "
                "because the structure is a regulated UCITS "
                "fund with counterparty limits, collateral "
                "risk-mitigation requirements, and an "
                "identified custodian. It is not classified "
                "low because a derivative-counterparty default "
                "is a documented principal-loss and fund-"
                "continuity mechanism."
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
        RiskAssessment(
            assessment_id=(
                "xeon_operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "operational_regulatory"
            ),
            risk_level="low",
            rationale=(
                "The modeled route uses a conventional "
                "regulated corporate brokerage and UCITS "
                "custody structure. IBKR Ireland states that "
                "client money is segregated, fully paid "
                "securities are held through depositories and "
                "custodians for clients' benefit, and client "
                "money and securities are reconciled daily. "
                "XEON also has an identified Luxembourg fund "
                "custodian. This is sufficient recommendation-"
                "stage evidence for a low operational and "
                "regulatory risk assessment while ordinary "
                "broker, custodian, settlement, onboarding, "
                "and administrative risks remain."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "operational_regulatory",
                )
            ),
            assessed_at=XEON_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Company-specific tax treatment, accounting, "
                "internal authorization, final account setup, "
                "and account permissions remain execution-stage "
                "checks unless a specific restriction is "
                "discovered."
            ),
        ),
    )


def get_ernx_risk_assessments(
) -> tuple[RiskAssessment, ...]:
    observations = (
        get_ernx_risk_observations()
        + get_ernx_recommendation_risk_observations()
    )

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
            assessed_at=ERNX_ASSESSED_AT,
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
                "Observed effective duration of approximately "
                "0.36 years and weighted average maturity of "
                "approximately 0.62 years indicate limited "
                "interest-rate sensitivity relative to longer-"
                "duration bond portfolios. Credit-spread and "
                "market-price movements can still affect value."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "market",
                )
            ),
            assessed_at=ERNX_ASSESSED_AT,
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
            assessed_at=ERNX_ASSESSED_AT,
            evidence_sufficient=True,
        ),
        RiskAssessment(
            assessment_id=(
                "ernx_structural_counterparty"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "structural_counterparty"
            ),
            risk_level="low",
            rationale=(
                "ERNX is a physically replicated Irish UCITS ETF "
                "with State Street Custodial Services (Ireland) "
                "Limited identified as custodian. Securities lending "
                "introduces borrower and collateral dependencies, "
                "but BlackRock reports average securities on loan "
                "of 4.25% of AUM, a maximum of 6.67%, and "
                "collateralisation of 106.09% for the year ending "
                "30 June 2026. These controls and the limited "
                "reported lending exposure support a low, rather "
                "than negligible, structural/counterparty risk "
                "assessment."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "structural_counterparty",
                )
            ),
            assessed_at=ERNX_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Low does not mean risk-free. Custodian failure, "
                "service-provider failure, securities-lending "
                "borrower default, collateral shortfall, or other "
                "fund-structure failures can still cause loss."
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
        RiskAssessment(
            assessment_id=(
                "ernx_operational_regulatory"
            ),
            instrument_id=instrument_id,
            market_id=market_id,
            risk_dimension=(
                "operational_regulatory"
            ),
            risk_level="low",
            rationale=(
                "The modeled route uses a conventional regulated "
                "corporate brokerage and UCITS custody structure. "
                "IBKR Ireland states that client money is segregated, "
                "fully paid client securities are held at "
                "depositories and custodians for clients' benefit, "
                "and client money and securities are reconciled "
                "daily. Together with the identified UCITS fund "
                "custodian, this provides sufficient V1 evidence "
                "that the core custody and operational path is "
                "controlled, while ordinary broker, custodian, "
                "settlement, onboarding, and administrative risks "
                "remain."
            ),
            supporting_observation_ids=(
                _observation_ids(
                    observations,
                    "operational_regulatory",
                )
            ),
            assessed_at=ERNX_ASSESSED_AT,
            evidence_sufficient=True,
            notes=(
                "Company-specific accounting, tax treatment, "
                "internal authorization, and final account setup "
                "remain execution-stage checks unless a specific "
                "restriction is discovered. They are not treated "
                "as evidence that the instrument itself is "
                "unrecommendable at portfolio-analysis stage."
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