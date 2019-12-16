from datetime import date, datetime, timezone, timedelta
from decimal import Decimal

from pg_stream_copy import protocol


def test_table():
    assert protocol.build_table_header() + protocol.build_table_trailer() == \
        b'PGCOPY\n\xff\r\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'


def test_row_1():
    assert protocol.build_row_header(6) + protocol.build_row_trailer() == b'\x00\x06'


def test_column_boolean():
    assert protocol.build_boolean(True) == b'\x00\x00\x00\x01\x01'
    assert protocol.build_boolean(False) == b'\x00\x00\x00\x01\x00'


def test_column_smallint():
    assert protocol.build_smallint(1234) == b'\x00\x00\x00\x02\x04\xd2'


def test_column_integer():
    assert protocol.build_integer(71337) == b'\x00\x00\x00\x04\x00\x01\x16\xa9'


def test_column_bigint():
    assert protocol.build_bigint(987654321) == b'\x00\x00\x00\x08\x00\x00\x00\x00\x3a\xde\x68\xb1'


def test_column_null():
    assert protocol.build_null() == b'\xff\xff\xff\xff'


def test_column_numeric():
    assert protocol.build_numeric(Decimal('Infinity')) == \
        b'\x00\x00\x00\x08\x00\x00\x00\x00\xc0\x00\x00\x00'
    assert protocol.build_numeric(Decimal('-Infinity')) == \
        b'\x00\x00\x00\x08\x00\x00\x00\x00\xc0\x00\x00\x00'
    assert protocol.build_numeric(Decimal('NaN')) == \
        b'\x00\x00\x00\x08\x00\x00\x00\x00\xc0\x00\x00\x00'

    assert protocol.build_numeric(Decimal(1)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01'
    assert protocol.build_numeric(Decimal(-1)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x40\x00\x00\x00\x00\x01'
    assert protocol.build_numeric(Decimal(23)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x00\x00\x00\x00\x00\x17'
    assert protocol.build_numeric(Decimal(-23)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x40\x00\x00\x00\x00\x17'
    assert protocol.build_numeric(Decimal(456)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x00\x00\x00\x00\x01\xc8'
    assert protocol.build_numeric(Decimal(-456)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x40\x00\x00\x00\x01\xc8'
    assert protocol.build_numeric(Decimal(7890)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x00\x00\x00\x00\x1e\xd2'
    assert protocol.build_numeric(Decimal(-7890)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x40\x00\x00\x00\x1e\xd2'
    assert protocol.build_numeric(Decimal(1234)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x00\x00\x00\x00\x04\xd2'
    assert protocol.build_numeric(Decimal(-1234)) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x00\x40\x00\x00\x00\x04\xd2'

    assert protocol.build_numeric(Decimal(1234) / Decimal(100)) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x02\x00\x0c\x0d\x48'
    assert protocol.build_numeric(Decimal(-1234) / Decimal(100)) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x40\x00\x00\x02\x00\x0c\x0d\x48'

    assert protocol.build_numeric(Decimal('0')) == \
        b'\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00'
    assert protocol.build_numeric(Decimal('-0')) == \
        b'\x00\x00\x00\x08\x00\x00\x00\x00\x40\x00\x00\x00'

    assert protocol.build_numeric(Decimal('5.7288')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x04\x00\x05\x1c\x78'
    assert protocol.build_numeric(Decimal('2.2622600000000003164')) == \
        b'\x00\x00\x00\x14\x00\x06\x00\x00\x00\x00\x00\x13\x00\x02\x0a\x3e\x17\x70\x00\x00\x00\x03\x06\x68'
    assert protocol.build_numeric(Decimal('5.69483')) == \
        b'\x00\x00\x00\x0e\x00\x03\x00\x00\x00\x00\x00\x05\x00\x05\x1b\x24\x0b\xb8'
    assert protocol.build_numeric(Decimal('152.080')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x03\x00\x98\x03\x20'
    assert protocol.build_numeric(Decimal('44.80428')) == \
        b'\x00\x00\x00\x0e\x00\x03\x00\x00\x00\x00\x00\x05\x00\x2c\x1f\x6a\x1f\x40'
    assert protocol.build_numeric(Decimal('2.53620')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x05\x00\x02\x14\xf2'
    assert protocol.build_numeric(Decimal('6.4965')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x04\x00\x06\x13\x65'
    assert protocol.build_numeric(Decimal('71.78358')) == \
        b'\x00\x00\x00\x0e\x00\x03\x00\x00\x00\x00\x00\x05\x00\x47\x1e\x9b\x1f\x40'
    assert protocol.build_numeric(Decimal('7.4625')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x04\x00\x07\x12\x11'
    assert protocol.build_numeric(Decimal('38.69635')) == \
        b'\x00\x00\x00\x0e\x00\x03\x00\x00\x00\x00\x00\x05\x00\x26\x1b\x33\x13\x88'
    assert protocol.build_numeric(Decimal('5.7288')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x04\x00\x05\x1c\x78'
    assert protocol.build_numeric(Decimal('2.2622600000000003164')) == \
        b'\x00\x00\x00\x14\x00\x06\x00\x00\x00\x00\x00\x13\x00\x02\x0a\x3e\x17\x70\x00\x00\x00\x03\x06\x68'
    assert protocol.build_numeric(Decimal('5.69483')) == \
        b'\x00\x00\x00\x0e\x00\x03\x00\x00\x00\x00\x00\x05\x00\x05\x1b\x24\x0b\xb8'
    assert protocol.build_numeric(Decimal('152.080')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x03\x00\x98\x03\x20'
    assert protocol.build_numeric(Decimal('44.80428')) == \
        b'\x00\x00\x00\x0e\x00\x03\x00\x00\x00\x00\x00\x05\x00\x2c\x1f\x6a\x1f\x40'
    assert protocol.build_numeric(Decimal('2.53620')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x05\x00\x02\x14\xf2'
    assert protocol.build_numeric(Decimal('6.4965')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x04\x00\x06\x13\x65'
    assert protocol.build_numeric(Decimal('71.78358')) == \
        b'\x00\x00\x00\x0e\x00\x03\x00\x00\x00\x00\x00\x05\x00\x47\x1e\x9b\x1f\x40'
    assert protocol.build_numeric(Decimal('7.4625')) == \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x00\x00\x00\x04\x00\x07\x12\x11'
    assert protocol.build_numeric(Decimal('38.69635')) == \
        b'\x00\x00\x00\x0e\x00\x03\x00\x00\x00\x00\x00\x05\x00\x26\x1b\x33\x13\x88'

    assert protocol.build_numeric(Decimal('10000000000000000000000000000000000000000000000000000000000000000')) == \
        b'\x00\x00\x00\x0a\x00\x01\x00\x10\x00\x00\x00\x00\x00\x01'


def test_column_character_varying():
    assert protocol.build_character_varying("wuteuef") == b'\x00\x00\x00\x07wuteuef'


def test_column_text():
    assert protocol.build_text("lorem ipsum") == b'\x00\x00\x00\x0Blorem ipsum'


def test_column_date():
    assert protocol.build_date(date(2019, 1, 1)) == b'\x00\x00\x00\x04\x00\x00\x1b\x1c'


def test_timestamp():
    assert protocol.build_timestamp(datetime(2019, 12, 12, 10, 11, 22, 333444)) == \
        b'\00\x00\x00\x08\x00\x02\x3c\x7d\xbc\x5e\xdd\x04'
    assert protocol.build_timestamp(datetime(1990, 12, 12, 10, 11, 22, 333444)) == \
        b'\00\x00\x00\x08\xff\xfe\xfc\x2b\x0d\x3a\xdd\x04'


def test_timestamp_tz():
    assert protocol.build_timestamp_tz(
        datetime(
            2019, 12, 12, 8, 11, 22, 333444,
            tzinfo=timezone(offset=timedelta(hours=-2))
        )
    ) == b'\00\x00\x00\x08\x00\x02\x3c\x7d\xbc\x5e\xdd\x04'
    assert protocol.build_timestamp_tz(
        datetime(
            1990, 12, 12, 12, 11, 22, 333444,
            tzinfo=timezone(offset=timedelta(hours=2))
        )
    ) == b'\00\x00\x00\x08\xff\xfe\xfc\x2b\x0d\x3a\xdd\x04'


def test_column_json():
    assert protocol.build_json('{"value": 1234}') == b'\x00\x00\x00\x0F{"value": 1234}'


def test_column_jsonb():
    assert protocol.build_jsonb(b'{"value": -4321}') == b'\x00\x00\x00\x11\x01{"value": -4321}'


def test_row_2():
    assert \
        protocol.build_row_header(10) + \
        protocol.build_smallint(1234) + \
        protocol.build_bigint(987654321) + \
        protocol.build_integer(71337) + \
        protocol.build_null() + \
        protocol.build_null() + \
        protocol.build_numeric(Decimal("-12.34")) + \
        protocol.build_character_varying("wuteuef") + \
        protocol.build_text("lorem ipsum") + \
        protocol.build_date(date(2019, 1, 1)) + \
        protocol.build_json('{"value": 1234}') + \
        protocol.build_jsonb(b'{"value": -4321}') + \
        protocol.build_row_trailer() \
        == \
        b'\x00\x0A' \
        b'\x00\x00\x00\x02\x04\xd2' \
        b'\x00\x00\x00\x08\x00\x00\x00\x00' \
        b'\x3a\xde\x68\xb1\x00\x00\x00\x04\x00\x01\x16\xa9' \
        b'\xff\xff\xff\xff' \
        b'\xff\xff\xff\xff' \
        b'\x00\x00\x00\x0c\x00\x02\x00\x00\x40\x00\x00\x02\x00\x0c\x0d\x48' \
        b'\x00\x00\x00\x07wuteuef' \
        b'\x00\x00\x00\x0Blorem ipsum' \
        b'\x00\x00\x00\x04\x00\x00\x1b\x1c' \
        b'\x00\x00\x00\x0F{"value": 1234}' \
        b'\x00\x00\x00\x11\x01{"value": -4321}'
