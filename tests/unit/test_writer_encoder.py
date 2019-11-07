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
        b'PGCOPY\n\xff\r\n\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        \
        b'\x00\x06' \
        b'\x00\x00\x00\x02\x11E' \
        b'\x00\x00\x00\x04\x12A\xf2\xd0' \
        b'\x00\x00\x00\x08%4\xa1>\xb3U\xf7\xee' \
        b'\x00\x00\x00\x08@(\xae\x14z\xe1G\xae' \
        b'\x00\x00\x00\x11lorem ipsum dolor' \
        b'\x00\x00\x00\x04\x00\x00\x02k' \
        \
        b'\x00\x06' \
        b'\x00\x00\x00\x02\x11E' \
        b'\x00\x00\x00\x04\x12A\xf2\xd0' \
        b'\x00\x00\x00\x08%4\xa1>\xb3U\xf7\xee' \
        b'\x00\x00\x00\x08@(\xae\x14z\xe1G\xae' \
        b'\x00\x00\x00\x11lorem ipsum dolor' \
        b'\x00\x00\x00\x04\x00\x00\x02k' \
        \
        b'\xff\xff'
