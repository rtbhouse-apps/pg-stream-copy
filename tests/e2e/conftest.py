from os import environ
import psycopg2
import pytest


@pytest.fixture
def psycopg_cursor():
    db_dsn = environ.get('DB_DSN', 'postgresql://postgres@localhost:5432/e2e_db')
    psycopg2_connection = psycopg2.connect(db_dsn)
    psycopg2_cursor = psycopg2_connection.cursor()

    yield psycopg2_cursor

    psycopg2_connection.rollback()
    psycopg2_connection.close()
