from pg_stream_copy.writer import Writer

from .mocks import MockPsycopg2CopyExpert


def test_all_1():
    psycopg2_cursor = MockPsycopg2CopyExpert()
    with Writer(
        psycopg2_cursor,
        'test_table'
    ) as writer:
        writer.append(b'\x01\x02')
        writer.append(b'\x03\x04')

    assert psycopg2_cursor.query == 'COPY test_table FROM STDIN BINARY'
    assert psycopg2_cursor.data == b'\x01\x02\x03\x04'
