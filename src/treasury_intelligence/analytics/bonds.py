from __future__ import annotations

from datetime import date


def zero_coupon_annualized_yield(
    price_pct_of_par: float,
    settlement_date: date,
    maturity_date: date,
) -> float:
    if price_pct_of_par <= 0:
        raise ValueError(
            "price_pct_of_par must be greater than zero"
        )

    days_to_maturity = (
        maturity_date - settlement_date
    ).days

    if days_to_maturity <= 0:
        raise ValueError(
            "maturity_date must be after settlement_date"
        )

    price_fraction = price_pct_of_par / 100

    annualized_yield = (
        (1 / price_fraction)
        ** (365 / days_to_maturity)
        - 1
    )

    return annualized_yield * 100