from __future__ import annotations

from dataclasses import dataclass


IBKR_FIXED_INCOME_SOURCE_CHECKED_ON = "2026-08-31"


@dataclass(frozen=True)
class EuropeOtcBondCommissionEvidence:
    broker: str
    market_scope: str
    currency: str

    first_tier_limit_eur: float
    first_tier_commission_bps: float
    additional_commission_bps: float

    recurring_access_cost_pct: float

    source_references: tuple[str, ...]
    notes: str | None = None


IBKR_EUROPE_OTC_BOND_EVIDENCE = (
    EuropeOtcBondCommissionEvidence(
        broker="Interactive Brokers",
        market_scope="Europe OTC - All Bonds",
        currency="EUR",
        first_tier_limit_eur=10_000.0,
        first_tier_commission_bps=10.0,
        additional_commission_bps=2.5,
        recurring_access_cost_pct=0.0,
        source_references=(
            "https://www.interactivebrokers.com/"
            "en/pricing/commissions-bonds.php",
            "https://www.interactivebrokers.com/"
            "en/accounts/required-minimums.php",
        ),
        notes=(
            "Published Europe OTC bond commissions are "
            "tiered: the first EUR 10,000 of trade value "
            "is charged at 10 bps and additional trade "
            "value is charged at 2.5 bps. IBKR publishes "
            "zero account minimums and inactivity fees "
            "for organization accounts. Optional services, "
            "market data, transfers, taxes, and any "
            "instrument-specific external charges are not "
            "asserted to be zero by this evidence."
        ),
    )
)
