from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BankDepositRate:
    bank: str
    product: str
    investor_type: str
    currency: str

    term_label: str
    min_term_days: int
    max_term_days: int | None

    annual_rate_pct: float
    rate_type: str

    price_status: str
    quote_firmness: str

    minimum_amount_eur: float | None
    maximum_amount_eur: float | None

    fixed_rate: bool
    negotiated: bool
    early_withdrawal: bool

    effective_date: str
    source: str
    source_url: str

    notes: str | None = None


@dataclass(frozen=True)
class BankDepositPositionInterpretation:
    position_size_eur: float
    published_rate_pct: float
    minimum_amount_supported: bool
    maximum_amount_supported: bool | None
    published_rate_is_executable: bool
    executable_rate_pct: float | None
    quote_required: bool


def interpret_bank_deposit_position(
    rate: BankDepositRate,
    position_size_eur: float,
) -> BankDepositPositionInterpretation:
    if position_size_eur <= 0:
        raise ValueError(
            "position_size_eur must be greater than zero"
        )

    if rate.minimum_amount_eur is None:
        minimum_amount_supported = True
    else:
        minimum_amount_supported = (
            position_size_eur >= rate.minimum_amount_eur
        )

    if rate.maximum_amount_eur is None:
        maximum_amount_supported = None
    else:
        maximum_amount_supported = (
            position_size_eur <= rate.maximum_amount_eur
        )

    published_rate_is_executable = (
        rate.price_status == "published"
        and rate.quote_firmness == "firm"
        and not rate.negotiated
    )

    executable_rate_pct = (
        rate.annual_rate_pct
        if published_rate_is_executable
        else None
    )

    quote_required = (
        not published_rate_is_executable
    )

    return BankDepositPositionInterpretation(
        position_size_eur=position_size_eur,
        published_rate_pct=rate.annual_rate_pct,
        minimum_amount_supported=minimum_amount_supported,
        maximum_amount_supported=maximum_amount_supported,
        published_rate_is_executable=(
            published_rate_is_executable
        ),
        executable_rate_pct=executable_rate_pct,
        quote_required=quote_required,
    )