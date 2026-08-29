from __future__ import annotations

from collections import Counter

from treasury_intelligence.models.risk import (
    RISK_DIMENSIONS,
    RiskObservation,
)

from treasury_intelligence.sources.aave import (
    AAVE_V3_BASE_EURC_INSTRUMENT,
    AAVE_V3_BASE_EURC_MARKET,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_MARKET,
)

from treasury_intelligence.sources.ishares import (
    ERNX_INSTRUMENT,
    ERNX_MARKET,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_INSTRUMENT,
    XEON_MARKET,
)


def get_aave_eurc_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        RiskObservation(
            observation_id=(
                "aave_base_eurc_asset_type"
            ),
            instrument_id=(
                AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
            ),
            market_id=(
                AAVE_V3_BASE_EURC_MARKET.market_id
            ),
            observed_at="2026-08-29",
            risk_dimension="currency_asset",
            observation_type="asset_type",
            value_text="EURC stablecoin",
            evidence_level="observed",
            source="Aave / Circle",
            source_url=(
                "https://app.aave.com/"
            ),
            notes=(
                "The supplied asset is EURC. Economic FX "
                "exposure is modeled separately as EUR, while "
                "stablecoin-specific redemption, issuer, and "
                "depeg considerations belong in the risk layer."
            ),
        ),
        RiskObservation(
            observation_id=(
                "aave_base_eurc_market_structure"
            ),
            instrument_id=(
                AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
            ),
            market_id=(
                AAVE_V3_BASE_EURC_MARKET.market_id
            ),
            observed_at="2026-08-29",
            risk_dimension="structural_counterparty",
            observation_type="market_structure",
            value_text=(
                "Onchain overcollateralized lending market"
            ),
            evidence_level="observed",
            source="Aave",
            source_url=(
                "https://app.aave.com/"
            ),
            notes=(
                "Return is generated through lending activity "
                "inside the Aave V3 protocol rather than through "
                "a conventional bank deposit or security."
            ),
        ),
        RiskObservation(
            observation_id=(
                "aave_base_eurc_technical_structure"
            ),
            instrument_id=(
                AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
            ),
            market_id=(
                AAVE_V3_BASE_EURC_MARKET.market_id
            ),
            observed_at="2026-08-29",
            risk_dimension="technical",
            observation_type="execution_environment",
            value_text=(
                "Aave V3 smart contracts on Base"
            ),
            evidence_level="observed",
            source="Aave",
            source_url=(
                "https://app.aave.com/"
            ),
            notes=(
                "The position depends on smart-contract and "
                "blockchain execution rather than traditional "
                "securities settlement infrastructure."
            ),
        ),
        RiskObservation(
            observation_id=(
                "aave_base_eurc_corporate_access_status"
            ),
            instrument_id=(
                AAVE_V3_BASE_EURC_INSTRUMENT.instrument_id
            ),
            market_id=(
                AAVE_V3_BASE_EURC_MARKET.market_id
            ),
            observed_at="2026-08-29",
            risk_dimension="operational_regulatory",
            observation_type="corporate_access_status",
            value_text=(
                "Corporate operational access unverified"
            ),
            evidence_level="observed",
            source="Treasury Intelligence research",
            notes=(
                "Technical access has been demonstrated, but the "
                "full Slovenian d.o.o. EUR bank -> EURC -> Aave "
                "-> EUR -> bank operating path has not yet been "
                "verified."
            ),
        ),
    )


def get_btf_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        RiskObservation(
            observation_id=(
                "btf_2027_03_10_issuer"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observed_at="2026-08-24",
            risk_dimension="principal_credit",
            observation_type="issuer",
            value_text="French Republic",
            evidence_level="published",
            source="Agence France Trésor",
            source_url=(
                "https://www.aft.gouv.fr/"
            ),
            notes=(
                "The instrument is a short-term sovereign "
                "obligation issued by the French Republic."
            ),
        ),
        RiskObservation(
            observation_id=(
                "btf_2027_03_10_structure"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observed_at="2026-08-24",
            risk_dimension="market",
            observation_type="instrument_structure",
            value_text=(
                "Zero-coupon discount Treasury bill"
            ),
            evidence_level="published",
            source="Agence France Trésor",
            source_url=(
                "https://www.aft.gouv.fr/"
            ),
            notes=(
                "The bill is purchased below par and redeemed "
                "at par at maturity."
            ),
        ),
        RiskObservation(
            observation_id=(
                "btf_2027_03_10_maturity"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observed_at="2026-08-24",
            risk_dimension="market",
            observation_type="maturity_date",
            value_text="2027-03-10",
            evidence_level="published",
            source="Agence France Trésor",
            source_url=(
                "https://www.aft.gouv.fr/"
            ),
            notes=(
                "Market-price exposure before maturity is "
                "distinct from redemption at par at maturity."
            ),
        ),
        RiskObservation(
            observation_id=(
                "btf_2027_03_10_issue_outstanding"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observed_at="2026-08-24",
            risk_dimension="liquidity",
            observation_type="issue_outstanding",
            value_numeric=2_323_000_000,
            unit="EUR",
            evidence_level="published",
            source="Agence France Trésor",
            source_url=(
                "https://www.aft.gouv.fr/"
            ),
            notes=(
                "Issue outstanding provides market-scale context "
                "but does not establish immediate secondary-market "
                "exit depth."
            ),
        ),
        RiskObservation(
            observation_id=(
                "btf_2027_03_10_currency"
            ),
            instrument_id=(
                BTF_2027_03_10.instrument_id
            ),
            market_id=(
                BTF_2027_03_10_MARKET.market_id
            ),
            observed_at="2026-08-24",
            risk_dimension="currency_asset",
            observation_type="denomination_currency",
            value_text="EUR",
            evidence_level="published",
            source="Agence France Trésor",
            source_url=(
                "https://www.aft.gouv.fr/"
            ),
        ),
    )


def get_xeon_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        RiskObservation(
            observation_id="xeon_replication_method",
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-29",
            risk_dimension="structural_counterparty",
            observation_type="replication_method",
            value_text="Synthetic swap replication",
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=(
                "https://etf.dws.com/"
            ),
            notes=(
                "The ETF obtains its target exposure through a "
                "synthetic swap structure rather than direct "
                "physical replication of overnight deposits."
            ),
        ),
        RiskObservation(
            observation_id="xeon_reference_index",
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-29",
            risk_dimension="market",
            observation_type="reference_index",
            value_text=(
                "Solactive €STR +8.5 Daily Total Return Index"
            ),
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=(
                "https://etf.dws.com/"
            ),
            notes=(
                "The ETF's economic return is linked to a "
                "short-term euro overnight-rate benchmark."
            ),
        ),
        RiskObservation(
            observation_id="xeon_currency",
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-29",
            risk_dimension="currency_asset",
            observation_type="denomination_currency",
            value_text="EUR",
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=(
                "https://etf.dws.com/"
            ),
        ),
        RiskObservation(
            observation_id="xeon_fund_aum",
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-29",
            risk_dimension="liquidity",
            observation_type="fund_aum",
            value_numeric=22_210_000_000,
            unit="EUR",
            evidence_level="published",
            source="DWS Xtrackers",
            source_url=(
                "https://etf.dws.com/"
            ),
            notes=(
                "Fund AUM provides scale context. It is not "
                "equivalent to secondary-market executable depth."
            ),
        ),
        RiskObservation(
            observation_id="xeon_xetra_daily_turnover",
            instrument_id=(
                XEON_INSTRUMENT.instrument_id
            ),
            market_id=XEON_MARKET.market_id,
            observed_at="2026-08-27",
            risk_dimension="liquidity",
            observation_type="daily_turnover",
            value_numeric=19_360_381,
            unit="EUR",
            evidence_level="market_observed",
            source="MarketScreener",
            source_url=(
                "https://www.marketscreener.com/quote/etf/"
                "XTRACKERS-II-EUR-OVERNIGH-576012/quotes/"
            ),
            notes=(
                "Observed Xetra turnover is market-activity "
                "evidence only and does not prove immediate "
                "position-size executable depth."
            ),
        ),
    )


def get_ernx_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        RiskObservation(
            observation_id="ernx_credit_exposure",
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-26",
            risk_dimension="principal_credit",
            observation_type="yield_source",
            value_text=(
                "Investment-grade short-duration credit"
            ),
            evidence_level="published",
            source="iShares",
            source_url=(
                "https://www.ishares.com/"
            ),
            notes=(
                "Unlike sovereign bills or overnight-rate "
                "exposure, return includes short-duration "
                "investment-grade credit exposure."
            ),
        ),
        RiskObservation(
            observation_id="ernx_replication_method",
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-26",
            risk_dimension="structural_counterparty",
            observation_type="replication_method",
            value_text="Physical sampled replication",
            evidence_level="published",
            source="iShares",
            source_url=(
                "https://www.ishares.com/"
            ),
        ),
        RiskObservation(
            observation_id="ernx_effective_duration",
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-26",
            risk_dimension="market",
            observation_type="effective_duration",
            value_numeric=0.36,
            unit="years",
            evidence_level="published",
            source="iShares",
            source_url=(
                "https://www.ishares.com/"
            ),
            notes=(
                "Effective duration is an observable interest-rate "
                "sensitivity measure, not a qualitative risk rating."
            ),
        ),
        RiskObservation(
            observation_id="ernx_average_maturity",
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-26",
            risk_dimension="market",
            observation_type="weighted_average_maturity",
            value_numeric=0.62,
            unit="years",
            evidence_level="published",
            source="iShares",
            source_url=(
                "https://www.ishares.com/"
            ),
        ),
        RiskObservation(
            observation_id="ernx_holdings_count",
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-26",
            risk_dimension="principal_credit",
            observation_type="holdings_count",
            value_numeric=671,
            unit="securities",
            evidence_level="published",
            source="iShares",
            source_url=(
                "https://www.ishares.com/"
            ),
            notes=(
                "Holdings count provides diversification context "
                "but does not by itself establish credit quality "
                "or loss probability."
            ),
        ),
        RiskObservation(
            observation_id="ernx_currency",
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-26",
            risk_dimension="currency_asset",
            observation_type="denomination_currency",
            value_text="EUR",
            evidence_level="published",
            source="iShares",
            source_url=(
                "https://www.ishares.com/"
            ),
        ),
        RiskObservation(
            observation_id="ernx_share_class_aum",
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-26",
            risk_dimension="liquidity",
            observation_type="share_class_aum",
            value_numeric=2_793_000_000,
            unit="EUR",
            evidence_level="published",
            source="iShares",
            source_url=(
                "https://www.ishares.com/"
            ),
            notes=(
                "Share-class AUM provides product scale context "
                "but is not the same as secondary-market "
                "executable liquidity."
            ),
        ),
        RiskObservation(
            observation_id="ernx_xetra_daily_turnover",
            instrument_id=(
                ERNX_INSTRUMENT.instrument_id
            ),
            market_id=ERNX_MARKET.market_id,
            observed_at="2026-08-21",
            risk_dimension="liquidity",
            observation_type="daily_turnover",
            value_numeric=1_485_729,
            unit="EUR",
            evidence_level="market_observed",
            source="MarketScreener",
            source_url=(
                "https://www.marketscreener.com/quote/etf/"
                "ISHARES-ULTRASHORT-BOND-U-137131876/"
            ),
            notes=(
                "Observed Xetra turnover is market-activity "
                "evidence only and does not prove immediate "
                "position-size executable depth."
            ),
        ),
    )


def get_all_risk_observations(
) -> tuple[RiskObservation, ...]:
    return (
        get_aave_eurc_risk_observations()
        + get_btf_risk_observations()
        + get_xeon_risk_observations()
        + get_ernx_risk_observations()
    )


def count_observations_by_dimension(
    observations: tuple[RiskObservation, ...],
) -> dict[str, int]:
    counts = Counter(
        observation.risk_dimension
        for observation in observations
    )

    return {
        dimension: counts.get(
            dimension,
            0,
        )
        for dimension in RISK_DIMENSIONS
    }


def observed_dimensions(
    observations: tuple[RiskObservation, ...],
) -> tuple[str, ...]:
    observed = {
        observation.risk_dimension
        for observation in observations
    }

    return tuple(
        dimension
        for dimension in RISK_DIMENSIONS
        if dimension in observed
    )


def missing_dimensions(
    observations: tuple[RiskObservation, ...],
) -> tuple[str, ...]:
    observed = set(
        observed_dimensions(
            observations
        )
    )

    return tuple(
        dimension
        for dimension in RISK_DIMENSIONS
        if dimension not in observed
    )