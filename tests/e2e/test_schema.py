from pg_stream_copy import ColumnDefinition, DataType, Schema


def test_from_table_schema(psycopg_cursor):
    psycopg_cursor.execute('''
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
        psycopg_cursor,
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
