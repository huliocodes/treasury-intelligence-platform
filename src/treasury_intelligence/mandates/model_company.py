from __future__ import annotations

from treasury_intelligence.models.mandates import (
    TreasuryMandate,
)


MODEL_COMPANY_MANDATE = TreasuryMandate(
    mandate_id="si_model_company_v1",
    name="Slovenian Corporate Treasury Model Company V1",

    base_currency="EUR",
    treasury_capital_eur=5_000_000,

    minimum_useful_allocation_eur=100_000,
    maximum_single_position_pct=100.0,

    target_yield_pct=3.0,
    target_yield_is_hard_constraint=False,

    capital_preservation_priority="very_high",
    liquidity_requirement="high",

    allowed_currencies=("EUR",),
    maximum_unhedged_fx_exposure_pct=0.0,

    minimum_immediate_liquidity_coverage_pct=100.0,
    maximum_settlement_days=2,

    allowed_instrument_types=None,

    require_verified_corporate_access=True,
    allowed_accessibility_statuses=(
        "eligible_v1",
    ),

    review_frequency_days=30,

    notes=(
        "Model mandate for a Slovenian d.o.o. with approximately "
        "EUR 5 million of excess treasury capital. Target yield is "
        "approximately 3% but is not a hard eligibility constraint. "
        "Primary objectives are capital preservation, EUR exposure "
        "and high liquidity. The mandate does not require the entire "
        "treasury to be allocated to one opportunity."
    ),
)