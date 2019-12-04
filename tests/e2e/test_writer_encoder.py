from datetime import date
from decimal import Decimal

from pg_stream_copy import Encoder, Schema, Writer, WriterEncoder


def test_writer_encoder(psycopg_cursor):
    psycopg_cursor.execute('''
        CREATE TABLE public.e2e_test_e2e_test_1 (
            _smallint SMALLINT NULL,
            _integer INTEGER NULL,
            _bigint BIGINT NULL,
            _float DOUBLE PRECISION NULL,
            _numeric NUMERIC NULL,
            _character_varying CHARACTER VARYING NULL,
            _text TEXT NULL,
            _date DATE NULL,
            _json JSON NULL,
            _jsonb JSONB NULL
        );
    ''')

    schema = Schema.load_from_table(
        psycopg_cursor,
        "public.e2e_test_e2e_test_1",
    )

    with Writer(psycopg_cursor, "public.e2e_test_e2e_test_1") as writer:
        with Encoder(schema, writer) as encoder:
            encoder.append_tuple(
                (1, 2, 3, 1.23, Decimal("2.2622600000000003164"),
                    "1", "-1", date(2019, 1, 1), '{"value": 1}', b'{"value": -1}')
            )
            encoder.append_tuple(
                (10, 20, 30, 12.3, Decimal("-5.69483"),
                    "10", "-10", date(2019, 1, 2), '{"value": 10}', b'{"value": -10}')
            )

    with WriterEncoder(psycopg_cursor, "public.e2e_test_e2e_test_1", schema) as writer_encoder:
        writer_encoder.append_tuple(
            (2, 3, 4, 2.34, Decimal("7890"),
                "2", "-2", date(2019, 2, 1), '{"value": 2}', b'{"value": -2}')
        )
        writer_encoder.append_tuple(
            (20, 30, 40, 23.4, Decimal("-0"),
                "20", "-20", date(2019, 2, 2), '{"value": 20}', b'{"value": -20}')
        )

    psycopg_cursor.execute("""
        SELECT
            *
        FROM
            public.e2e_test_e2e_test_1
        ORDER BY
            _smallint
    """)

    assert list(psycopg_cursor) == [
        (1, 2, 3, 1.23, Decimal("2.2622600000000003164"), "1", "-1", date(2019, 1, 1), {"value": 1}, {"value": -1}),
        (2, 3, 4, 2.34, Decimal("7890"), "2", "-2", date(2019, 2, 1), {"value": 2}, {"value": -2}),
        (10, 20, 30, 12.3, Decimal("-5.69483"), "10", "-10", date(2019, 1, 2), {"value": 10}, {"value": -10}),
        (20, 30, 40, 23.4, Decimal("-0"), "20", "-20", date(2019, 2, 2), {"value": 20}, {"value": -20}),
    ]
