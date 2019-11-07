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
            _date DATE NULL
        );
    ''')

    schema = Schema.load_from_table(
        psycopg_cursor,
        "public.e2e_test_e2e_test_1",
    )

    with Writer(psycopg_cursor, "public.e2e_test_e2e_test_1") as writer:
        with Encoder(schema, writer) as encoder:
            encoder.append_tuple((1, 2, 3, 1.23, "1", date(2019, 1, 1)))
            encoder.append_tuple((10, 20, 30, 12.3, "10", date(2019, 1, 2)))
            encoder.append_tuple((100, 200, 300, 123, "100", date(2019, 1, 3)))

    with WriterEncoder(psycopg_cursor, "public.e2e_test_e2e_test_1", schema) as writer_encoder:
        writer_encoder.append_tuple((2, 3, 4, 2.34, "2", date(2019, 2, 1)))
        writer_encoder.append_tuple((20, 30, 40, 23.4, "20", date(2019, 2, 2)))
        writer_encoder.append_tuple((200, 300, 400, 234, "200", date(2019, 2, 3)))

    psycopg_cursor.execute("""
        SELECT
            COUNT(*),
            SUM(_smallint),
            SUM(_integer),
            SUM(_bigint),
            SUM(_float),
            STRING_AGG(_character_varying, ' ' ORDER BY _smallint),
            MAX(_date)
        FROM
            public.e2e_test_e2e_test_1
    """)
    row = list(psycopg_cursor)[0]
    assert row == (
        6,
        333,
        555,
        777,
        396.27,
        "1 2 10 20 100 200",
        date(2019, 2, 3)
    )
