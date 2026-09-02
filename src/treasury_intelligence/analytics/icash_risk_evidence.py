from __future__ import annotations

from treasury_intelligence.models.risk import (
    RiskObservation,
)

from treasury_intelligence.sources.icash import (
    ICASH_INSTRUMENT,
    ICASH_MARKET,
)


ICASH_INTERCAPITAL_SOURCE_URL = (
    "https://intercapitaletf.hr/"
)

ICASH_LJSE_SOURCE_URL = (
    "https://ljse.si/en/papir-311/310"
    "?isin=HRICAMFEUMM1"
)


def get_icash_recommendation_risk_observations(
) -> tuple[RiskObservation, ...]:
    instrument_id = ICASH_INSTRUMENT.instrument_id
    market_id = ICASH_MARKET.market_id

    return (
        RiskObservation(
            observation_id="icash_portfolio_btf_weight",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="principal_credit",
            observation_type="government_bill_weight",
            value_numeric=84.49,
            unit="pct_nav",
            evidence_level="published",
            source="InterCapital Asset Management",
            source_url=ICASH_INTERCAPITAL_SOURCE_URL,
            notes=(
                "Approximately 84.49% of net assets were "
                "reported in short French Treasury bills."
            ),
        ),
        RiskObservation(
            observation_id="icash_portfolio_deposit_weight",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="principal_credit",
            observation_type="bank_deposit_weight",
            value_numeric=15.57,
            unit="pct_nav",
            evidence_level="published",
            source="InterCapital Asset Management",
            source_url=ICASH_INTERCAPITAL_SOURCE_URL,
            notes=(
                "Approximately 15.57% of net assets were "
                "reported in deposits at OTP and PBZ."
            ),
        ),
        RiskObservation(
            observation_id="icash_short_maturity_profile",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-28",
            risk_dimension="market",
            observation_type="money_market_maturity_profile",
            value_text=(
                "WAM 1.98, WAL 2.02, with no reported "
                "assets beyond 180 days"
            ),
            evidence_level="published",
            source="InterCapital Asset Management",
            source_url=ICASH_INTERCAPITAL_SOURCE_URL,
            notes=(
                "The very short maturity profile materially "
                "limits conventional interest-rate exposure."
            ),
        ),
        RiskObservation(
            observation_id="icash_fund_aum",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="liquidity",
            observation_type="fund_aum",
            value_numeric=36_520_000.0,
            unit="EUR",
            evidence_level="published",
            source="InterCapital Asset Management",
            source_url=ICASH_INTERCAPITAL_SOURCE_URL,
            notes=(
                "Fund scale is used by the position-aware "
                "ETF liquidity layer. Scale does not itself "
                "prove executable secondary-market depth."
            ),
        ),
        RiskObservation(
            observation_id="icash_market_maker_quote_size",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="liquidity",
            observation_type=(
                "minimum_market_maker_quote_obligation"
            ),
            value_numeric=30.0,
            unit="shares",
            evidence_level="published",
            source="Ljubljana Stock Exchange",
            source_url=ICASH_LJSE_SOURCE_URL,
            notes=(
                "The minimum quote obligation is evidence of "
                "market-making infrastructure, not evidence "
                "of large position-size executable depth."
            ),
        ),
        RiskObservation(
            observation_id="icash_eur_exposure",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-08-31",
            risk_dimension="currency_asset",
            observation_type="fund_currency",
            value_text="EUR",
            evidence_level="published",
            source="InterCapital Asset Management",
            source_url=ICASH_INTERCAPITAL_SOURCE_URL,
        ),
        RiskObservation(
            observation_id="icash_ucits_structure",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="structural_counterparty",
            observation_type="regulated_fund_structure",
            value_text="Croatian UCITS ETF",
            evidence_level="published",
            source="InterCapital Asset Management",
            source_url=ICASH_INTERCAPITAL_SOURCE_URL,
        ),
        RiskObservation(
            observation_id="icash_depositary",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="structural_counterparty",
            observation_type="fund_depositary",
            value_text="OTP banka",
            evidence_level="published",
            source="InterCapital Asset Management",
            source_url=ICASH_INTERCAPITAL_SOURCE_URL,
            notes=(
                "Depositary and other counterparties remain "
                "structural dependencies despite the UCITS "
                "framework."
            ),
        ),
        RiskObservation(
            observation_id="icash_ljse_listing",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="operational_regulatory",
            observation_type="regulated_exchange_listing",
            value_text="Ljubljana Stock Exchange",
            evidence_level="published",
            source="Ljubljana Stock Exchange",
            source_url=ICASH_LJSE_SOURCE_URL,
        ),
        RiskObservation(
            observation_id="icash_slovenian_corporate_route",
            instrument_id=instrument_id,
            market_id=market_id,
            observed_at="2026-09-02",
            risk_dimension="operational_regulatory",
            observation_type="corporate_brokerage_route",
            value_text=(
                "Slovenian legal-person brokerage route "
                "through an LJSE member"
            ),
            evidence_level="supported_route",
            source="LJSE / Slovenian broker evidence",
            source_url=ICASH_LJSE_SOURCE_URL,
        ),
    )
