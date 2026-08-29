from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))


from treasury_intelligence.analytics.risk import (
    count_observations_by_dimension,
    get_aave_eurc_risk_observations,
    get_all_risk_observations,
    get_btf_risk_observations,
    get_ernx_risk_observations,
    get_xeon_risk_observations,
    missing_dimensions,
    observed_dimensions,
)


def format_value(
    observation,
) -> str:
    if observation.value_numeric is not None:
        if observation.unit == "EUR":
            return (
                f"EUR "
                f"{observation.value_numeric:,.0f}"
            )

        if observation.unit is not None:
            return (
                f"{observation.value_numeric:,.2f} "
                f"{observation.unit}"
            )

        return (
            f"{observation.value_numeric:,.2f}"
        )

    if observation.value_text is not None:
        return observation.value_text

    return "UNKNOWN"


def print_instrument(
    label: str,
    observations,
) -> None:
    print(label)
    print()

    for observation in observations:
        print(
            f"{observation.risk_dimension:<24} | "
            f"{observation.observation_type:<24} | "
            f"{format_value(observation)}"
        )

    print()

    observed = observed_dimensions(
        observations
    )

    missing = missing_dimensions(
        observations
    )

    print(
        "Observed dimensions:  "
        + (
            ", ".join(observed)
            if observed
            else "none"
        )
    )

    print(
        "Missing dimensions:   "
        + (
            ", ".join(missing)
            if missing
            else "none"
        )
    )

    print()


def main() -> None:
    aave = get_aave_eurc_risk_observations()

    btf = get_btf_risk_observations()

    xeon = get_xeon_risk_observations()

    ernx = get_ernx_risk_observations()

    all_observations = (
        get_all_risk_observations()
    )

    print("RISK OBSERVATIONS")
    print()

    print(
        "Facts only. No qualitative risk "
        "assessments are produced in 4A."
    )

    print()

    print_instrument(
        "AAVE V3 BASE EURC",
        aave,
    )

    print_instrument(
        "FRENCH BTF",
        btf,
    )

    print_instrument(
        "XEON",
        xeon,
    )

    print_instrument(
        "ERNX",
        ernx,
    )

    print("OBSERVATION COVERAGE")
    print()

    counts = (
        count_observations_by_dimension(
            all_observations
        )
    )

    for dimension, count in counts.items():
        print(
            f"{dimension:<24} "
            f"{count:>3}"
        )

    print()

    print(
        f"Total observations:   "
        f"{len(all_observations)}"
    )

    print()
    print("INTERPRETATION")
    print()

    print(
        "An observation records a sourced fact that may be "
        "relevant to risk."
    )

    print(
        "An observation does not state whether the resulting "
        "risk is low, moderate, high, acceptable, or unacceptable."
    )

    print(
        "Missing dimensions remain explicit and will be handled "
        "during later evidence and assessment work rather than "
        "being silently inferred."
    )


if __name__ == "__main__":
    main()