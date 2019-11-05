from os import environ
import psycopg2
import pytest


@pytest.fixture
def psycopg_cursor():
    psycopg2_connection = psycopg2.connect(environ['DB_DSN'])
    psycopg2_cursor = psycopg2_connection.cursor()

    yield psycopg2_cursor

    psycopg2_connection.rollback()
    psycopg2_connection.close()
