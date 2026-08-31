from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(SRC_DIR),
    )


from treasury_intelligence.analytics.eligibility import (
    evaluate_eligibility,
)
from treasury_intelligence.analytics.positions import (
    build_bank_deposit_position_analysis,
)
from treasury_intelligence.mandates.model_company import (
    MODEL_COMPANY_MANDATE,
)
from treasury_intelligence.sources.addiko import (
    ADDIKO_91_180_DAY_ACCESSIBILITY,
    ADDIKO_91_180_DAY_INSTRUMENT,
    ADDIKO_91_180_DAY_MARKET,
    ADDIKO_91_180_DAY_RATE,
    get_addiko_91_180_day_snapshot,
)


POSITION_SIZES_EUR = (
    100_000.0,
    500_000.0,
    1_000_000.0,
    5_000_000.0,
)


def main() -> None:
    snapshot = get_addiko_91_180_day_snapshot()

    print("ADDIKO CORPORATE EUR TERM DEPOSIT")
    print("=" * 70)
    print(
        f"Instrument: "
        f"{ADDIKO_91_180_DAY_INSTRUMENT.instrument_id}"
    )
    print(
        f"Term: "
        f"{ADDIKO_91_180_DAY_RATE.term_label}"
    )
    print(
        f"Published rate: "
        f"{snapshot.yield_value_pct:.3f}%"
    )
    print(
        f"Quote firmness: "
        f"{snapshot.quote_firmness}"
    )
    print(
        f"Early withdrawal: "
        f"{snapshot.early_exit_possible}"
    )
    print(
        f"Access: "
        f"{ADDIKO_91_180_DAY_ACCESSIBILITY.status}"
    )

    for position_size_eur in POSITION_SIZES_EUR:
        position = (
            build_bank_deposit_position_analysis(
                snapshot=snapshot,
                rate=ADDIKO_91_180_DAY_RATE,
                position_size_eur=position_size_eur,
            )
        )

        eligibility = evaluate_eligibility(
            mandate=MODEL_COMPANY_MANDATE,
            instrument=ADDIKO_91_180_DAY_INSTRUMENT,
            market=ADDIKO_91_180_DAY_MARKET,
            accessibility=(
                ADDIKO_91_180_DAY_ACCESSIBILITY
            ),
            position=position,
        )

        immediate_liquidity_check = next(
            check
            for check in eligibility.checks
            if check.check_name
            == "immediate_liquidity"
        )

        corporate_access_check = next(
            check
            for check in eligibility.checks
            if check.check_name
            == "corporate_access"
        )

        settlement_check = next(
            check
            for check in eligibility.checks
            if check.check_name
            == "settlement"
        )

        print()
        print("-" * 70)

        print(
            f"Position: "
            f"EUR {position_size_eur:,.0f}"
        )

        print(
            f"Entry supported: "
            f"{position.entry_supported}"
        )

        print(
            f"Reference yield: "
            f"{position.reference_yield_pct:.3f}%"
        )

        print(
            f"Executable yield: "
            f"{position.executable_yield_pct}"
        )

        print(
            f"Executable economics known: "
            f"{position.executable_economics_known}"
        )

        print(
            f"Immediate exit supported: "
            f"{position.immediate_exit_supported}"
        )

        print(
            f"Immediate exit coverage: "
            f"{position.immediate_exit_coverage_pct:.1f}%"
        )

        print(
            f"Settlement check: "
            f"{settlement_check.status}"
        )

        print(
            f"Corporate access check: "
            f"{corporate_access_check.status}"
        )

        print(
            f"Immediate liquidity check: "
            f"{immediate_liquidity_check.status}"
        )

        print(
            f"Eligibility: "
            f"{eligibility.overall_status}"
        )


if __name__ == "__main__":
    main()