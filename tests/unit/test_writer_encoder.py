from pg_stream_copy.writer_encoder import WriterEncoder

from . import data
from .mocks import MockPsycopg2CopyExpert


def test_all_1():
    psycopg2_cursor = MockPsycopg2CopyExpert()

    with WriterEncoder(
        psycopg2_cursor,
        "test_table",
        data.set_1_schema
    ) as write_encoder:
        write_encoder.append_tuple(data.set_1_row_tuple)
        write_encoder.append_dict(data.set_1_row_dict)

    assert psycopg2_cursor.query == 'COPY test_table FROM STDIN BINARY'
    assert psycopg2_cursor.data == \
        b'PGCOPY\n\xff\r\n\x00\x00\x00\x00\x00\x00\x00\x00\x00' + \
        data.set1_row_binary + \
        data.set1_row_binary + \
        b'\xff\xff'
