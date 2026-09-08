from __future__ import annotations

import os

import psycopg
from psycopg import Connection


def get_database_url() -> str:
    database_url = os.environ.get(
        "DATABASE_URL"
    )

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is required."
        )

    return database_url


def connect_database() -> Connection:
    return psycopg.connect(
        get_database_url()
    )
