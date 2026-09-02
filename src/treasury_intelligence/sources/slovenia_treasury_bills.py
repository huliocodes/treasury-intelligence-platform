from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SloveniaTreasuryBillState = Literal[
    "scheduled",
    "auctioned",
    "issued",
    "listed",
]


@dataclass(frozen=True)
class SloveniaTreasuryBillAuction:
    designation: str
    maturity_bucket: str

    auction_date: str
    settlement_date: str
    maturity_date: str
    days_to_maturity: int

    denomination_eur: float
    currency: str

    state: SloveniaTreasuryBillState

    auction_yield_pct: float | None = None
    auction_price_pct_of_par: float | None = None
    issued_nominal_eur: float | None = None
    isin: str | None = None
    ljse_listing_date: str | None = None

    source: str = (
        "Republic of Slovenia Ministry of Finance"
    )

    source_url: str = (
        "https://www.gov.si/en/topics/"
        "borrowing-and-state-budget-debt-management/"
    )

    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.designation.strip():
            raise ValueError(
                "designation must not be blank."
            )

        if self.days_to_maturity <= 0:
            raise ValueError(
                "days_to_maturity must be greater "
                "than zero."
            )

        if self.denomination_eur <= 0:
            raise ValueError(
                "denomination_eur must be greater "
                "than zero."
            )

        if self.currency != "EUR":
            raise ValueError(
                "Slovenian Treasury bills are modeled "
                "as EUR instruments."
            )

        if self.state == "scheduled":
            unresolved_fields = (
                self.auction_yield_pct,
                self.auction_price_pct_of_par,
                self.issued_nominal_eur,
                self.isin,
                self.ljse_listing_date,
            )

            if any(
                value is not None
                for value in unresolved_fields
            ):
                raise ValueError(
                    "A scheduled Treasury bill must not "
                    "contain post-auction or post-issue "
                    "facts."
                )

        if (
            self.state
            in (
                "auctioned",
                "issued",
                "listed",
            )
            and self.auction_yield_pct is None
        ):
            raise ValueError(
                "An auctioned or later Treasury bill "
                "requires an auction yield."
            )


@dataclass(frozen=True)
class SloveniaTreasuryBillPrimaryAccessEvidence:
    route_id: str
    investor_entity_type: str
    jurisdiction: str

    legal_persons_supported: bool
    orders_via_primary_dealer: bool
    settlement_days_after_auction: int

    primary_dealers: tuple[str, ...]

    source: str
    source_url: str
    observed_date: str
    notes: str


@dataclass(frozen=True)
class SloveniaTreasuryBillPrimaryCostEvidence:
    provider: str

    primary_subscription_commission_pct: (
        float | None
    )

    provider_custody_pct_per_month: float | None
    kdd_custody_pct_per_month: float | None
    kdd_custody_fixed_eur_per_month: float | None

    kdd_settlement_pct: float | None
    kdd_settlement_min_eur: float | None
    kdd_settlement_max_eur: float | None

    kdd_order_matching_eur: float | None
    kdd_maturity_payment_eur: float | None
    provider_maturity_payment_eur: float | None

    source: str
    source_url: str
    observed_date: str

    notes: str


SLOVENIA_TBILL_PRIMARY_ACCESS = (
    SloveniaTreasuryBillPrimaryAccessEvidence(
        route_id=(
            "slovenia_tbill_primary_dealer"
        ),
        investor_entity_type=(
            "Slovenian d.o.o."
        ),
        jurisdiction="Slovenia",
        legal_persons_supported=True,
        orders_via_primary_dealer=True,
        settlement_days_after_auction=2,
        primary_dealers=(
            "BKS BANK AG, Bančna podružnica",
            "ILIRIKA borzno posredniška hiša d.d.",
            "Jefferies GmbH",
            "Nova Ljubljanska banka d.d.",
            "OTP banka d.d.",
            "Raiffeisen Bank International AG",
            "UniCredit Banka Slovenija d.d.",
        ),
        source=(
            "Republic of Slovenia Ministry of Finance"
        ),
        source_url=(
            "https://www.gov.si/en/topics/"
            "borrowing-and-state-budget-debt-management/"
        ),
        observed_date="2026-09-02",
        notes=(
            "The Ministry of Finance states that "
            "Treasury-bill holders may be legal or "
            "natural persons and investors submit "
            "subscription orders through Treasury-bill "
            "primary dealers. Settlement occurs two "
            "working days after the auction."
        ),
    )
)


ILIRIKA_SLOVENIA_TBILL_PRIMARY_COSTS = (
    SloveniaTreasuryBillPrimaryCostEvidence(
        provider="ILIRIKA d.d.",
        primary_subscription_commission_pct=None,
        provider_custody_pct_per_month=0.0008,
        kdd_custody_pct_per_month=0.00107,
        kdd_custody_fixed_eur_per_month=0.40,
        kdd_settlement_pct=0.037,
        kdd_settlement_min_eur=5.00,
        kdd_settlement_max_eur=30.79,
        kdd_order_matching_eur=0.25,
        kdd_maturity_payment_eur=0.31,
        provider_maturity_payment_eur=15.00,
        source="ILIRIKA d.d.",
        source_url=(
            "https://www.ilirika.si/en/news/"
            "vpis-zakladnih-menic-na-"
            "primarni-izdaji-september-2026"
        ),
        observed_date="2026-09-02",
        notes=(
            "ILIRIKA published these expected costs for "
            "the September 2026 Republic of Slovenia "
            "Treasury-bill primary auction. The page "
            "does not identify a separate investor-paid "
            "primary-subscription brokerage commission, "
            "so such a commission is deliberately left "
            "unknown rather than assumed zero."
        ),
    )
)


NLB_SLOVENIA_TBILL_PRIMARY_SUBSCRIPTION_FREE = (
    SloveniaTreasuryBillPrimaryCostEvidence(
        provider="NLB d.d.",
        primary_subscription_commission_pct=0.0,
        provider_custody_pct_per_month=None,
        kdd_custody_pct_per_month=None,
        kdd_custody_fixed_eur_per_month=None,
        kdd_settlement_pct=None,
        kdd_settlement_min_eur=None,
        kdd_settlement_max_eur=None,
        kdd_order_matching_eur=None,
        kdd_maturity_payment_eur=None,
        provider_maturity_payment_eur=None,
        source="NLB d.d.",
        source_url=(
            "https://www.nlb.si/podjetja/"
            "nalozbe-in-depoziti/vrednostni-papirji/"
            "zakladne-menice"
        ),
        observed_date="2026-09-02",
        notes=(
            "NLB explicitly states that mediation for "
            "primary Treasury-bill subscription is free "
            "because NLB receives compensation from the "
            "Republic of Slovenia. Other custody, KDD, "
            "account and lifecycle costs are not "
            "established by this evidence object and are "
            "therefore represented as unknown rather than "
            "zero. This is not a complete all-in NLB "
            "cost schedule."
        ),
    )
)


TZ233 = SloveniaTreasuryBillAuction(
    designation="TZ233",
    maturity_bucket="3_month",
    auction_date="2026-09-08",
    settlement_date="2026-09-10",
    maturity_date="2026-12-10",
    days_to_maturity=91,
    denomination_eur=1_000.0,
    currency="EUR",
    state="scheduled",
    notes=(
        "Scheduled September 2026 three-month "
        "Treasury-bill auction. No September auction "
        "yield, auction price, issued amount, ISIN or "
        "LJSE listing is assumed before those facts "
        "are officially published."
    ),
)


SZ163 = SloveniaTreasuryBillAuction(
    designation="SZ163",
    maturity_bucket="6_month",
    auction_date="2026-09-08",
    settlement_date="2026-09-10",
    maturity_date="2027-03-11",
    days_to_maturity=182,
    denomination_eur=1_000.0,
    currency="EUR",
    state="scheduled",
    notes=(
        "Scheduled September 2026 six-month "
        "Treasury-bill auction. No September auction "
        "yield, auction price, issued amount, ISIN or "
        "LJSE listing is assumed before those facts "
        "are officially published."
    ),
)


DZ125 = SloveniaTreasuryBillAuction(
    designation="DZ125",
    maturity_bucket="12_month",
    auction_date="2026-09-08",
    settlement_date="2026-09-10",
    maturity_date="2027-09-09",
    days_to_maturity=364,
    denomination_eur=1_000.0,
    currency="EUR",
    state="scheduled",
    notes=(
        "Scheduled September 2026 twelve-month "
        "Treasury-bill auction. No September auction "
        "yield, auction price, issued amount, ISIN or "
        "LJSE listing is assumed before those facts "
        "are officially published."
    ),
)


LATEST_PREDECESSOR_YIELDS_PCT = {
    "TZ232": 2.20,
    "SZ162": 2.45,
    "DZ124": 2.64,
}


def get_september_2026_scheduled_auctions(
) -> tuple[
    SloveniaTreasuryBillAuction,
    ...,
]:
    return (
        TZ233,
        SZ163,
        DZ125,
    )
