from __future__ import annotations

from prefect.schedules import Cron

from treasury_intelligence.orchestration.production_pipeline import (
    treasury_production_pipeline,
)


DEPLOYMENT_NAME = "treasury-production-weekday"

PRODUCTION_SCHEDULE = Cron(
    "0 7 * * 1-5",
    timezone="Europe/Ljubljana",
    slug="weekday-morning",
)


def build_production_deployment():
    """
    Build the production deployment configuration.

    The deployment is intentionally registered as paused.
    Registering it demonstrates the production scheduling
    contract without causing automatic runs on the local
    development machine.
    """

    return treasury_production_pipeline.to_deployment(
        name=DEPLOYMENT_NAME,
        description=(
            "Refresh official treasury market evidence, "
            "build the dbt warehouse, and run the "
            "warehouse-backed production decision."
        ),
        tags=[
            "treasury",
            "production",
            "warehouse",
        ],
        schedule=PRODUCTION_SCHEDULE,
        paused=True,
    )


def main() -> None:
    deployment = build_production_deployment()

    deployment_id = deployment.apply()

    print("PREFECT PRODUCTION DEPLOYMENT")
    print()
    print(
        f"Deployment name: {DEPLOYMENT_NAME}"
    )
    print(
        "Schedule:        0 7 * * 1-5"
    )
    print(
        "Timezone:        Europe/Ljubljana"
    )
    print(
        "State:           paused"
    )
    print(
        f"Deployment ID:   {deployment_id}"
    )
    print()
    print(
        "No local runner was started."
    )
    print(
        "No automatic flow runs will execute while "
        "the deployment remains paused."
    )


if __name__ == "__main__":
    main()
