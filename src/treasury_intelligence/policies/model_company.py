from __future__ import annotations

from treasury_intelligence.models.rebalance import (
    RebalancePolicy,
)


MODEL_COMPANY_REBALANCE_POLICY = RebalancePolicy(
    policy_id="si_model_company_rebalance_v1",
    minimum_first_year_net_improvement_bps_of_treasury=5.0,
    notes=(
        "Production V1 rebalance materiality policy for the "
        "Slovenian corporate treasury model company. A proposed "
        "allocation change must produce at least five basis points "
        "of first-year net economic improvement relative to total "
        "treasury capital after additional switching costs. For a "
        "EUR 5 million treasury this corresponds to EUR 2,500 of "
        "first-year net benefit. The threshold is an explicit V1 "
        "governance assumption intended to prevent economically "
        "immaterial portfolio churn; it is not a market-derived "
        "return assumption or an eligibility constraint."
    ),
)
