from datetime import date

from pg_stream_copy import Encoder, Schema, Writer, WriterEncoder


def test_writer_encoder(psycopg_cursor):
    psycopg_cursor.execute('''
        CREATE TABLE public.e2e_test_e2e_test_1 (
            _smallint SMALLINT NULL,
            _integer INTEGER NULL,
            _bigint BIGINT NULL,
            _float DOUBLE PRECISION NULL,
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

    rows = [
        (1, 2, 3, 1.23, "1", "-1", date(2019, 1, 1), '{"value": 1}', b'{"value": -1}'),
        (10, 20, 30, 12.3, "10", "-10", date(2019, 1, 2), '{"value": 10}', b'{"value": -10}'),
        (100, 200, 300, 123, "100", "-100", date(2019, 1, 3), '{"value": 100}', b'{"value": -100}'),

        (2, 3, 4, 2.34, "2", "-2", date(2019, 2, 1), '{"value": 2}', b'{"value": -2}'),
        (20, 30, 40, 23.4, "20", "-20", date(2019, 2, 2), '{"value": 20}', b'{"value": -20}'),
        (200, 300, 400, 234, "200", "-200", date(2019, 2, 3), '{"value": 200}', b'{"value": -200}')
    ]

    with Writer(psycopg_cursor, "public.e2e_test_e2e_test_1") as writer:
        with Encoder(schema, writer) as encoder:
            encoder.append_tuple(rows[0])
            encoder.append_tuple(rows[1])
            encoder.append_tuple(rows[2])

    with WriterEncoder(psycopg_cursor, "public.e2e_test_e2e_test_1", schema) as writer_encoder:
        writer_encoder.append_tuple(rows[3])
        writer_encoder.append_tuple(rows[4])
        writer_encoder.append_tuple(rows[5])

    psycopg_cursor.execute("""
        SELECT
            *
        FROM
            public.e2e_test_e2e_test_1
        ORDER BY
            _smallint
    """)

    assert list(psycopg_cursor) == rows
