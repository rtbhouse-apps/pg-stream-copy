from pg_stream_copy import Schema, WriterEncoder
from pg_stream_copy.schema import ColumnDefinition, DataType
import pytest


def test_exceptions(psycopg_cursor):
    psycopg_cursor.execute('''
        CREATE TABLE public.test_exceptions (
            _column1 INTEGER NULL,
            _column2 INTEGER NULL,
            _column3 INTEGER NULL
        );
    ''')

    schema = Schema(columns=[
        ColumnDefinition("_column1", DataType.INTEGER),
        # Invalid schema - missing _column2, _column3
    ])

    with pytest.raises(Exception):
        with WriterEncoder(psycopg_cursor, "public.test_exceptions", schema) as writer_encoder:
            writer_encoder.append_dict({
                "_column1": 0
            })
