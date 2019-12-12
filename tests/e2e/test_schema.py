import pytest

from pg_stream_copy import ColumnDefinition, DataType, Schema


def test_from_table_schema(psycopg_cursor):
    psycopg_cursor.execute('''
        CREATE TABLE public.test_schema_test_from_table_schema_1 (
            _boolean BOOLEAN NULL,
            _smallint SMALLINT NULL,
            _integer INTEGER NULL,
            _bigint BIGINT NULL,
            _double_precision DOUBLE PRECISION NULL,
            _numeric NUMERIC NULL,
            _character_varying CHARACTER VARYING NULL,
            _text TEXT NULL,
            _date DATE NULL,
            _timestamp timestamp NULL,
            _timestamp_tz timestamp with time zone NULL,
            _json JSON NULL,
            _jsonb JSONB NULL
        )
    ''')

    schema = Schema.load_from_table(
        psycopg_cursor,
        "public.test_schema_test_from_table_schema_1",
    )

    assert schema == Schema(columns=[
        ColumnDefinition('_boolean', DataType.BOOLEAN),
        ColumnDefinition('_smallint', DataType.SMALLINT),
        ColumnDefinition('_integer', DataType.INTEGER),
        ColumnDefinition('_bigint', DataType.BIGINT),
        ColumnDefinition('_double_precision', DataType.DOUBLE_PRECISION),
        ColumnDefinition('_numeric', DataType.NUMERIC),
        ColumnDefinition('_character_varying', DataType.CHARACTER_VARYING),
        ColumnDefinition('_text', DataType.TEXT),
        ColumnDefinition('_date', DataType.DATE),
        ColumnDefinition('_timestamp', DataType.TIMESTAMP),
        ColumnDefinition('_timestamp_tz', DataType.TIMESTAMP_TZ),
        ColumnDefinition('_json', DataType.JSON),
        ColumnDefinition('_jsonb', DataType.JSONB),
    ])


def test_from_table_schema_invalid(psycopg_cursor):
    with pytest.raises(Exception):
        Schema.load_from_table(
            psycopg_cursor,
            "public.test_from_table_schema_invalid",
        )
