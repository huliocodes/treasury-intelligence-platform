#!/usr/bin/env bash

set -u

echo "========================================"
echo "TREASURY INTELLIGENCE PLATFORM"
echo "END-TO-END DATA ENGINEERING DEMO"
echo "========================================"
echo

failed=0

project_root="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/.." \
    && pwd
)"

cd "$project_root" || {
    echo "FAILED: cannot enter project root."
    failed=1
}

echo "=== 1. ENVIRONMENT ==="

if [ -f .venv/Scripts/activate ]; then
    source .venv/Scripts/activate
else
    echo "FAILED: .venv/Scripts/activate not found."
    failed=1
fi

if [ -f .env ]; then
    set -a
    source .env
    set +a
else
    echo "FAILED: .env not found."
    failed=1
fi

export DBT_POSTGRES_HOST=localhost
export PYTHONPATH=src

python --version

echo
echo "=== 2. POSTGRES ==="

docker compose up -d postgres

if [ $? -ne 0 ]; then
    echo "FAILED: docker compose up"
    failed=1
fi

docker compose ps

echo
echo "=== 3. DATABASE SCHEMA ==="

if [ "$failed" -eq 0 ]; then
    python scripts/apply_database_schema.py

    if [ $? -ne 0 ]; then
        echo "FAILED: database schema application"
        failed=1
    else
        echo "Database schema: PASS"
    fi
else
    echo "SKIPPED"
fi

echo
echo "=== 4. PREFECT API CHECK ==="

python - <<'PY'
import sys

import httpx

url = "http://127.0.0.1:4200/api/health"

try:
    response = httpx.get(
        url,
        timeout=5,
    )
    response.raise_for_status()
except Exception as exc:
    print(
        "FAILED: Prefect server is not reachable at "
        "http://127.0.0.1:4200"
    )
    print(
        "Start it in another terminal with:"
    )
    print(
        "  source .venv/Scripts/activate"
    )
    print(
        "  prefect server start"
    )
    print()
    print(exc)
    sys.exit(1)

print("Prefect API: PASS")
PY

if [ $? -ne 0 ]; then
    failed=1
fi

echo
echo "=== 5. ORCHESTRATED PIPELINE ==="

if [ "$failed" -eq 0 ]; then
    python \
        -m treasury_intelligence.orchestration.production_pipeline

    if [ $? -ne 0 ]; then
        echo "FAILED: Prefect production pipeline"
        failed=1
    else
        echo "Prefect production pipeline: PASS"
    fi
else
    echo "SKIPPED"
fi

echo
echo "=== 6. LATEST WAREHOUSE EVIDENCE ==="

if [ "$failed" -eq 0 ]; then
    python - <<'PY'
import os
import psycopg

with psycopg.connect(
    os.environ["DATABASE_URL"]
) as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                instrument_id,
                evidence_type,
                measure,
                observed_date,
                numeric_value,
                unit,
                source_name
            FROM analytics_marts.latest_market_evidence
            ORDER BY
                instrument_id,
                evidence_type,
                measure
            """
        )

        rows = cursor.fetchall()

        print(
            f"Latest evidence series: {len(rows)}"
        )

        for row in rows:
            print(row)
PY

    if [ $? -ne 0 ]; then
        echo "FAILED: warehouse evidence query"
        failed=1
    fi
else
    echo "SKIPPED"
fi

echo
echo "=== 7. FINAL REPOSITORY STATE ==="

git status -sb

echo
if [ "$failed" -eq 0 ]; then
    echo "========================================"
    echo "SHOWCASE DEMO COMPLETE"
    echo "========================================"
else
    echo "========================================"
    echo "SHOWCASE DEMO FAILED"
    echo "REVIEW THE OUTPUT ABOVE"
    echo "========================================"
fi

exit "$failed"
