from __future__ import annotations

from pathlib import Path

from treasury_intelligence.persistence.database import (
    connect_database,
)


SCHEMA_FILE = Path(
    "sql/001_create_market_evidence.sql"
)


def main() -> None:
    sql = SCHEMA_FILE.read_text()

    with connect_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)

    print(
        "Applied database schema:"
    )

    print(
        f"  {SCHEMA_FILE}"
    )


if __name__ == "__main__":
    main()
