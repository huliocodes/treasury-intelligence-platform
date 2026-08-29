from datetime import date
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.bonds import (
    zero_coupon_annualized_yield,
)

from treasury_intelligence.analytics.eligibility import (
    evaluate_eligibility,
)

from treasury_intelligence.analytics.evidence import (
    build_evidence_gaps,
)

from treasury_intelligence.analytics.positions import (
    build_aave_position_analysis,
    build_btf_position_analysis,
    build_ernx_position_analysis,
    build_xeon_position_analysis,
)

from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)

from treasury_intelligence.sources.aave import (
    AAVE_V3_BASE_EURC_ACCESSIBILITY,
    AAVE_V3_BASE_EURC_INSTRUMENT,
    AAVE_V3_BASE_EURC_MARKET,
    fetch_aave_v3_base_eurc,
)

from treasury_intelligence.sources.ecb import (
    fetch_recent_estr,
)

from treasury_intelligence.sources.france import (
    BTF_2027_03_10,
    BTF_2027_03_10_ACCESSIBILITY,
    BTF_2027_03_10_MARKET,
    get_btf_2027_03_10_market_observation,
    get_btf_2027_03_10_snapshot,
)

from treasury_intelligence.sources.ishares import (
    ERNX_ACCESSIBILITY,
    ERNX_INSTRUMENT,
    ERNX_MARKET,
    get_ernx_snapshot,
)

from treasury_intelligence.sources.xtrackers import (
    XEON_ACCESSIBILITY,
    XEON_INSTRUMENT,
    XEON_MARKET,
    build_xeon_snapshot,
)


POSITION_SIZE_EUR = 5_000_000


def print_gaps(
    label: str,
    eligibility,
) -> None:
    gaps = build_evidence_gaps(
        eligibility
    )

    print(label)
    print(
        f"Eligibility:          "
        f"{eligibility.overall_status}"
    )

    if not gaps:
        print("Blocking evidence gaps: none")
        print()
        return

    print(
        f"Blocking evidence gaps: "
        f"{len(gaps)}"
    )

    for gap in gaps:
        print()
        print(
            f"  Check:              "
            f"{gap.check_name}"
        )

        print(
            f"  Evidence type:      "
            f"{gap.evidence_type}"
        )

        print(
            f"  Priority:           "
            f"{gap.priority}"
        )

        print(
            f"  Required evidence:  "
            f"{gap.required_evidence}"
        )

        print(
            f"  Next action:        "
            f"{gap.resolution_action}"
        )

    print()


def main() -> None:
    mandate = MODEL_COMPANY_MANDATE

    aave_observation = fetch_aave_v3_base_eurc()

    estr = fetch_recent_estr(limit=1)[-1]

    xeon_snapshot = build_xeon_snapshot(
        estr_rate_pct=estr.rate_pct,
        estr_reference_date=estr.reference_date,
    )

    ernx_snapshot = get_ernx_snapshot()

    btf_snapshot = get_btf_2027_03_10_snapshot()

    btf_market = (
        get_btf_2027_03_10_market_observation()
    )

    settlement_date = date(2026, 8, 31)

    maturity_date = date.fromisoformat(
        BTF_2027_03_10.maturity_date
    )

    btf_market_yield = zero_coupon_annualized_yield(
        price_pct_of_par=btf_market.price_pct_of_par,
        settlement_date=settlement_date,
        maturity_date=maturity_date,
    )

    print("EVIDENCE GAPS")
    print()
    print(
        f"Position size:        "
        f"EUR {POSITION_SIZE_EUR:,.0f}"
    )
    print()

    aave_position = build_aave_position_analysis(
        observation=aave_observation,
        position_size_eur=POSITION_SIZE_EUR,
    )

    aave_eligibility = evaluate_eligibility(
        mandate=mandate,
        instrument=AAVE_V3_BASE_EURC_INSTRUMENT,
        market=AAVE_V3_BASE_EURC_MARKET,
        accessibility=(
            AAVE_V3_BASE_EURC_ACCESSIBILITY
        ),
        position=aave_position,
    )

    print_gaps(
        "AAVE EURC",
        aave_eligibility,
    )

    btf_position = build_btf_position_analysis(
        snapshot=btf_snapshot,
        market_observation=btf_market,
        position_size_eur=POSITION_SIZE_EUR,
        market_derived_yield_pct=btf_market_yield,
    )

    btf_eligibility = evaluate_eligibility(
        mandate=mandate,
        instrument=BTF_2027_03_10,
        market=BTF_2027_03_10_MARKET,
        accessibility=(
            BTF_2027_03_10_ACCESSIBILITY
        ),
        position=btf_position,
    )

    print_gaps(
        "FRENCH BTF",
        btf_eligibility,
    )

    xeon_position = build_xeon_position_analysis(
        snapshot=xeon_snapshot,
        position_size_eur=POSITION_SIZE_EUR,
    )

    xeon_eligibility = evaluate_eligibility(
        mandate=mandate,
        instrument=XEON_INSTRUMENT,
        market=XEON_MARKET,
        accessibility=XEON_ACCESSIBILITY,
        position=xeon_position,
    )

    print_gaps(
        "XEON",
        xeon_eligibility,
    )

    ernx_position = build_ernx_position_analysis(
        snapshot=ernx_snapshot,
        position_size_eur=POSITION_SIZE_EUR,
    )

    ernx_eligibility = evaluate_eligibility(
        mandate=mandate,
        instrument=ERNX_INSTRUMENT,
        market=ERNX_MARKET,
        accessibility=ERNX_ACCESSIBILITY,
        position=ernx_position,
    )

    print_gaps(
        "ERNX",
        ernx_eligibility,
    )


if __name__ == "__main__":
    main()