from __future__ import annotations

from collections.abc import Iterator
from os import environ

import pytest
from psycopg2 import connect  # type: ignore
from psycopg2._psycopg import cursor  # pylint: disable=no-name-in-module


@pytest.fixture
def psycopg_cursor() -> Iterator[cursor]:
    db_dsn = environ.get("DB_DSN", "postgresql://postgres@localhost:5432/e2e_db")
    psycopg2_connection = connect(db_dsn)
    psycopg2_cursor = psycopg2_connection.cursor()

    yield psycopg2_cursor

    psycopg2_connection.rollback()
    psycopg2_connection.close()
