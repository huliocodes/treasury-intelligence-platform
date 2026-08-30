from __future__ import annotations

from dataclasses import dataclass


IBKR_SOURCE_CHECKED_ON = "2026-08-30"

IBKR_AVAILABLE_COUNTRIES_URL = (
    "https://www.interactivebrokers.com/"
    "en/accounts/open-account-country-list.php"
)

IBKR_EUROPE_BUSINESS_APPLICATION_URL = (
    "https://www.interactivebrokers.com/"
    "en/general/what-you-need-sb.php"
)

IBKR_EUROPE_STOCK_COMMISSIONS_URL = (
    "https://www.interactivebrokers.com/"
    "en/pricing/commissions-stocks.php"
)

IBKR_REQUIRED_MINIMUMS_URL = (
    "https://www.interactivebrokers.com/"
    "en/accounts/required-minimums.php"
)

IBKR_OTHER_FEES_URL = (
    "https://www.interactivebrokers.com/"
    "en/pricing/other-fees.php"
)


@dataclass(frozen=True)
class BrokerAccessEvidence:
    broker: str
    jurisdiction: str
    corporate_account_route_supported: bool
    specific_account_approval_verified: bool
    evidence_date: str
    source_references: tuple[str, ...]
    notes: str | None = None


@dataclass(frozen=True)
class BrokerTradingCostEvidence:
    broker: str
    market_country: str
    pricing_plan: str
    routing_method: str
    monthly_trade_value_limit_eur: float
    commission_pct_of_trade_value: float
    commission_bps: float
    account_minimum_usd: float
    inactivity_fee_usd: float
    evidence_date: str
    source_references: tuple[str, ...]
    notes: str | None = None

    def __post_init__(self) -> None:
        expected_bps = (
            self.commission_pct_of_trade_value
            * 100
        )

        if (
            abs(
                expected_bps
                - self.commission_bps
            )
            > 0.000001
        ):
            raise ValueError(
                "Commission percent and commission "
                "basis points do not reconcile."
            )

        if self.monthly_trade_value_limit_eur <= 0:
            raise ValueError(
                "Monthly trade value limit must be "
                "greater than zero."
            )

        if self.account_minimum_usd < 0:
            raise ValueError(
                "Account minimum cannot be negative."
            )

        if self.inactivity_fee_usd < 0:
            raise ValueError(
                "Inactivity fee cannot be negative."
            )


@dataclass(frozen=True)
class BrokerRecurringAccessCostEvidence:
    broker: str
    jurisdiction: str
    market_country: str
    product_scope: str

    account_minimum_usd: float
    inactivity_fee_usd: float

    platform_fee_pct: float
    recurring_access_cost_pct: float

    generic_custody_fee_identified: bool
    route_specific_exception_identified: bool

    specific_account_terms_verified: bool

    evidence_date: str
    source_references: tuple[str, ...]
    notes: str | None = None

    def __post_init__(self) -> None:
        if self.account_minimum_usd < 0:
            raise ValueError(
                "Account minimum cannot be negative."
            )

        if self.inactivity_fee_usd < 0:
            raise ValueError(
                "Inactivity fee cannot be negative."
            )

        if self.platform_fee_pct < 0:
            raise ValueError(
                "Platform fee cannot be negative."
            )

        if self.recurring_access_cost_pct < 0:
            raise ValueError(
                "Recurring access cost cannot be "
                "negative."
            )

        if (
            self.recurring_access_cost_pct == 0
            and self.generic_custody_fee_identified
        ):
            raise ValueError(
                "Recurring access cost cannot be "
                "modeled as zero when a generic "
                "custody fee has been identified."
            )


IBKR_SLOVENIA_CORPORATE_ACCESS_EVIDENCE = (
    BrokerAccessEvidence(
        broker="Interactive Brokers",
        jurisdiction="Slovenia",
        corporate_account_route_supported=True,
        specific_account_approval_verified=False,
        evidence_date=IBKR_SOURCE_CHECKED_ON,
        source_references=(
            IBKR_AVAILABLE_COUNTRIES_URL,
            IBKR_EUROPE_BUSINESS_APPLICATION_URL,
        ),
        notes=(
            "Interactive Brokers lists Slovenia among "
            "available countries and publishes a "
            "European business-account application "
            "process for companies. This supports the "
            "existence of a corporate brokerage route. "
            "It does not prove approval of any specific "
            "Slovenian d.o.o. or instrument permissions "
            "inside a future account."
        ),
    )
)


IBKR_GERMANY_FIXED_SMARTROUTING_EVIDENCE = (
    BrokerTradingCostEvidence(
        broker="Interactive Brokers",
        market_country="Germany",
        pricing_plan="Fixed",
        routing_method="IB SmartRouting",
        monthly_trade_value_limit_eur=50_000_000,
        commission_pct_of_trade_value=0.05,
        commission_bps=5.0,
        account_minimum_usd=0.0,
        inactivity_fee_usd=0.0,
        evidence_date=IBKR_SOURCE_CHECKED_ON,
        source_references=(
            IBKR_EUROPE_STOCK_COMMISSIONS_URL,
            IBKR_REQUIRED_MINIMUMS_URL,
        ),
        notes=(
            "Public IBKR pricing shows 0.05 percent "
            "of trade value for German stocks and ETFs "
            "under Fixed IB SmartRouting for monthly "
            "trade value up to EUR 50 million. "
            "Organization-account minimum and "
            "inactivity fee are published as zero. "
            "This evidence covers broker-level costs "
            "only and excludes market bid-ask spread, "
            "slippage, market impact, taxes, and any "
            "future entity-specific operational costs."
        ),
    )
)


IBKR_GERMANY_XETRA_ETF_RECURRING_ACCESS_COST_EVIDENCE = (
    BrokerRecurringAccessCostEvidence(
        broker="Interactive Brokers",
        jurisdiction="Slovenia",
        market_country="Germany",
        product_scope=(
            "German/Xetra-listed ETF held through "
            "an IBKR organization-account route"
        ),
        account_minimum_usd=0.0,
        inactivity_fee_usd=0.0,
        platform_fee_pct=0.0,
        recurring_access_cost_pct=0.0,
        generic_custody_fee_identified=False,
        route_specific_exception_identified=False,
        specific_account_terms_verified=False,
        evidence_date=IBKR_SOURCE_CHECKED_ON,
        source_references=(
            IBKR_REQUIRED_MINIMUMS_URL,
            IBKR_EUROPE_STOCK_COMMISSIONS_URL,
            IBKR_OTHER_FEES_URL,
        ),
        notes=(
            "IBKR publicly publishes a USD 0 account "
            "minimum and USD 0 inactivity fee for "
            "organization accounts. Its European "
            "stocks and ETFs pricing states that "
            "there are no platform fees or account "
            "minimums. For Germany Fixed "
            "IB SmartRouting, third-party fees are "
            "listed as none. The current IBKR Other "
            "Fees schedule does not identify a "
            "generic custody fee for German/Xetra "
            "ETFs; the Germany-specific maintenance "
            "fee shown there applies to XETRA-GOLD, "
            "not to ETFs generally. Therefore the "
            "modeled recurring access cost for the "
            "specific IBKR Germany/Xetra ETF route "
            "is zero based on the currently published "
            "fee schedule. This is a route-scoped "
            "research assumption, not a guarantee "
            "that a future specific corporate account "
            "could never have entity-specific or "
            "contract-specific charges. Such account "
            "terms remain an execution-stage "
            "confirmation."
        ),
    )
)