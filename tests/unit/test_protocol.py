from datetime import date

from pg_stream_copy import protocol


def test_table():
    assert protocol.build_table_header() + protocol.build_table_trailer() == b'PGCOPY\n\xff\r\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'


def test_row_1():
    assert protocol.build_row_header(6) + protocol.build_row_trailer() == b'\x00\x06'


def test_column_smallint():
    assert protocol.build_smallint(1234) == b'\x00\x00\x00\x02\x04\xd2'


def test_column_integer():
    assert protocol.build_integer(71337) == b'\x00\x00\x00\x04\x00\x01\x16\xa9'


def test_column_bigint():
    assert protocol.build_bigint(987654321) == b'\x00\x00\x00\x08\x00\x00\x00\x00:\xdeh\xb1'


def test_column_null():
    assert protocol.build_null() == b'\xff\xff\xff\xff'


def test_column_character_varying():
    assert protocol.build_character_varying("wuteuef") == b'\x00\x00\x00\x07wuteuef'


def test_column_date():
    assert protocol.build_date(date(2019, 1, 1)) == b'\x00\x00\x00\x04\x00\x00\x1b\x1c'


def test_row_2():
    assert \
        protocol.build_row_header(7) + \
        protocol.build_smallint(1234) + \
        protocol.build_bigint(987654321) + \
        protocol.build_integer(71337) + \
        protocol.build_null() + \
        protocol.build_null() + \
        protocol.build_character_varying("wuteuef") + \
        protocol.build_date(date(2019, 1, 1)) + \
        protocol.build_row_trailer() \
        == \
        b'\x00\x07' \
        b'\x00\x00\x00\x02\x04\xd2' \
        b'\x00\x00\x00\x08\x00\x00\x00\x00' \
        b':\xdeh\xb1\x00\x00\x00\x04\x00\x01\x16\xa9' \
        b'\xff\xff\xff\xff' \
        b'\xff\xff\xff\xff' \
        b'\x00\x00\x00\x07wuteuef' \
        b'\x00\x00\x00\x04\x00\x00\x1b\x1c'
