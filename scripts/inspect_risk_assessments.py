from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.risk_assessments import (
    get_aave_eurc_risk_assessments,
    get_btf_risk_assessments,
    get_ernx_risk_assessments,
    get_xeon_risk_assessments,
    validate_dimension_coverage,
)


def print_assessments(
    label: str,
    assessments,
) -> None:
    validate_dimension_coverage(
        assessments
    )

    print(label)
    print()

    for assessment in assessments:
        evidence = (
            "sufficient"
            if assessment.evidence_sufficient
            else "insufficient"
        )

        print(
            f"{assessment.risk_dimension:<24} | "
            f"{assessment.risk_level:<14} | "
            f"{evidence}"
        )

        print(
            f"  Rationale: {assessment.rationale}"
        )

        if assessment.supporting_observation_ids:
            print(
                "  Evidence:  "
                + ", ".join(
                    assessment.supporting_observation_ids
                )
            )
        else:
            print(
                "  Evidence:  none"
            )

        print()

    print("-" * 90)
    print()


def main() -> None:
    aave = get_aave_eurc_risk_assessments()
    btf = get_btf_risk_assessments()
    xeon = get_xeon_risk_assessments()
    ernx = get_ernx_risk_assessments()

    print("RISK ASSESSMENTS")
    print()

    print(
        "Qualitative assessments are dimension-specific. "
        "No aggregate risk score is produced."
    )

    print()
    print("-" * 90)
    print()

    print_assessments(
        "AAVE V3 BASE EURC",
        aave,
    )

    print_assessments(
        "FRENCH BTF",
        btf,
    )

    print_assessments(
        "XEON",
        xeon,
    )

    print_assessments(
        "ERNX",
        ernx,
    )

    print("INTERPRETATION")
    print()

    print(
        "very_low / low / moderate / high / very_high "
        "are qualitative dimension-level assessments."
    )

    print(
        "unknown means the current evidence is insufficient "
        "for a defensible qualitative assessment."
    )

    print(
        "not_applicable means the modeled risk mechanism does "
        "not apply to the instrument."
    )

    print(
        "No overall risk score or weighted risk ranking is "
        "calculated."
    )


if __name__ == "__main__":
    main()