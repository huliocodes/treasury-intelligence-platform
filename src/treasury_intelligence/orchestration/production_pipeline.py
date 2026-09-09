from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from prefect import flow, task


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def _run_command(
    command: list[str],
    *,
    environment: dict[str, str] | None = None,
) -> None:
    merged_environment = os.environ.copy()

    if environment:
        merged_environment.update(environment)

    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        env=merged_environment,
        check=True,
    )


@task(
    name="ingest-aft-btf-evidence",
    retries=2,
    retry_delay_seconds=5,
)
def ingest_aft_btf_evidence() -> None:
    _run_command(
        [
            sys.executable,
            "scripts/ingest_aft_btf.py",
        ],
        environment={
            "PYTHONPATH": "src",
        },
    )


@task(
    name="ingest-ecb-estr-evidence",
    retries=2,
    retry_delay_seconds=5,
)
def ingest_ecb_estr_evidence() -> None:
    _run_command(
        [
            sys.executable,
            "scripts/ingest_ecb_estr.py",
        ],
        environment={
            "PYTHONPATH": "src",
        },
    )


@task(
    name="ingest-aave-eurc-evidence",
    retries=2,
    retry_delay_seconds=5,
)
def ingest_aave_eurc_evidence() -> None:
    _run_command(
        [
            sys.executable,
            "scripts/ingest_aave_eurc.py",
        ],
        environment={
            "PYTHONPATH": "src",
        },
    )


@task(
    name="ingest-ernx-evidence",
    retries=2,
    retry_delay_seconds=5,
)
def ingest_ernx_evidence() -> None:
    _run_command(
        [
            sys.executable,
            "scripts/ingest_ernx.py",
        ],
        environment={
            "PYTHONPATH": "src",
        },
    )


@task(
    name="build-dbt-warehouse",
)
def build_dbt_warehouse() -> None:
    _run_command(
        [
            "dbt",
            "build",
            "--project-dir",
            "dbt",
            "--profiles-dir",
            "dbt",
        ],
        environment={
            "DBT_POSTGRES_HOST": "localhost",
        },
    )


@task(
    name="build-production-decision",
)
def build_production_decision() -> None:
    _run_command(
        [
            sys.executable,
            "scripts/inspect_production_5m_recommendation.py",
        ],
        environment={
            "PYTHONPATH": "src",
        },
    )


@flow(
    name="treasury-production-pipeline",
    log_prints=True,
)
def treasury_production_pipeline() -> None:
    ingest_aft_btf_evidence()
    ingest_ecb_estr_evidence()
    ingest_aave_eurc_evidence()
    ingest_ernx_evidence()
    build_dbt_warehouse()
    build_production_decision()


if __name__ == "__main__":
    treasury_production_pipeline()
