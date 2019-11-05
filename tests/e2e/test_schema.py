from pg_stream_copy import ColumnDefinition, DataType, Schema


def test_from_table_schema_1_10(psycopg2_rollback_cursor_10):
    _test_from_table_schema_1(psycopg2_rollback_cursor_10)


def test_from_table_schema_1_11(psycopg2_rollback_cursor_11):
    _test_from_table_schema_1(psycopg2_rollback_cursor_11)


def test_from_table_schema_1_12(psycopg2_rollback_cursor_12):
    _test_from_table_schema_1(psycopg2_rollback_cursor_12)


def _test_from_table_schema_1(psycopg2_rollback_cursor):
    psycopg2_rollback_cursor.execute('''
        CREATE TABLE public.test_schema_test_from_table_schema_1 (
            _smallint SMALLINT NULL,
            _integer INTEGER NULL,
            _bigint BIGINT NULL,
            _double_precision DOUBLE PRECISION NULL,
            _character_varying CHARACTER VARYING NULL,
            _date DATE NULL
        )
    ''')

    schema = Schema.load_from_table(
        psycopg2_rollback_cursor,
        "public.test_schema_test_from_table_schema_1",
    )

    assert schema == Schema(columns=[
        ColumnDefinition('_smallint', DataType.SMALLINT),
        ColumnDefinition('_integer', DataType.INTEGER),
        ColumnDefinition('_bigint', DataType.BIGINT),
        ColumnDefinition('_double_precision', DataType.DOUBLE_PRECISION),
        ColumnDefinition('_character_varying', DataType.CHARACTER_VARYING),
        ColumnDefinition('_date', DataType.DATE),
    ])
