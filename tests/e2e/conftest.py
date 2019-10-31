import psycopg2
import pytest


@pytest.fixture
def psycopg2_rollback_cursor_10():
    yield from _psycopg2_rollback_cursor("postgres10")


@pytest.fixture
def psycopg2_rollback_cursor_11():
    yield from _psycopg2_rollback_cursor("postgres11")


@pytest.fixture
def psycopg2_rollback_cursor_12():
    yield from _psycopg2_rollback_cursor("postgres12")


def _psycopg2_rollback_cursor(host: str):
    psycopg2_connection = psycopg2.connect(f"postgresql://postgres:postgres@{host}/postgres")
    psycopg2_cursor = psycopg2_connection.cursor()
    yield psycopg2_cursor
    psycopg2_connection.rollback()
    psycopg2_connection.close()
