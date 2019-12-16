from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from pg_stream_copy import ColumnDefinition, DataType, Schema

set_1_schema = Schema([
    ColumnDefinition('BOOLEAN', DataType.BOOLEAN),
    ColumnDefinition('SMALLINT', DataType.SMALLINT),
    ColumnDefinition('INTEGER', DataType.INTEGER),
    ColumnDefinition('BIGINT', DataType.BIGINT),
    ColumnDefinition('DOUBLE_PRECISION', DataType.DOUBLE_PRECISION),
    ColumnDefinition('NUMERIC', DataType.NUMERIC),
    ColumnDefinition('CHARACTER_VARYING', DataType.CHARACTER_VARYING),
    ColumnDefinition('TEXT', DataType.TEXT),
    ColumnDefinition('DATE', DataType.DATE),
    ColumnDefinition('TIMESTAMP', DataType.TIMESTAMP),
    ColumnDefinition('TIMESTAMP_TZ', DataType.TIMESTAMP_TZ),
    ColumnDefinition('JSON', DataType.JSON),
    ColumnDefinition('JSONB', DataType.JSONB),
])
set_1_row_tuple = (
    False,
    0x1145,
    0x1241f2d0,
    0x2534a13eb355f7ee,
    12.34,
    Decimal("-12.34"),
    "lorem ipsum dolor",
    "sit amet, consectetur",
    date(2001, 9, 11),
    datetime(2019, 12, 12, 10, 11, 22, 333444),
    datetime(2019, 12, 12, 8, 11, 22, 333444, tzinfo=timezone(offset=timedelta(hours=-2))),
    '{"value": 1234}',
    b'{"value": -4321}'
)
set_1_row_dict = {
    'BOOLEAN': False,
    'SMALLINT': 0x1145,
    'INTEGER': 0x1241f2d0,
    'BIGINT': 0x2534a13eb355f7ee,
    'DOUBLE_PRECISION': 12.34,
    'NUMERIC': Decimal("-12.34"),
    'CHARACTER_VARYING': "lorem ipsum dolor",
    'TEXT': "sit amet, consectetur",
    'DATE': date(2001, 9, 11),
    'TIMESTAMP': datetime(2019, 12, 12, 10, 11, 22, 333444),
    'TIMESTAMP_TZ': datetime(2019, 12, 12, 8, 11, 22, 333444, tzinfo=timezone(offset=timedelta(hours=-2))),
    'JSON': '{"value": 1234}',
    'JSONB': b'{"value": -4321}',
}

set1_row_binary = (
    b'\x00\x0d'
    b'\x00\x00\x00\x01\x00'
    b'\x00\x00\x00\x02\x11\x45'
    b'\x00\x00\x00\x04\x12\x41\xf2'
    b'\xd0\x00\x00\x00\x08\x25\x34\xa1\x3e\xb3\x55\xf7\xee'
    b'\x00\x00\x00\x08\x40\x28\xae\x14\x7a\xe1\x47\xae'
    b'\x00\x00\x00\x0c\x00\x02\x00\x00\x40\x00\x00\x02\x00\x0c\x0d\x48'
    b'\x00\x00\x00\x11lorem ipsum dolor'
    b'\x00\x00\x00\x15sit amet, consectetur'
    b'\x00\x00\x00\x04\x00\x00\x02\x6b'
    b'\00\x00\x00\x08\x00\x02\x3c\x7d\xbc\x5e\xdd\x04'
    b'\00\x00\x00\x08\x00\x02\x3c\x7d\xbc\x5e\xdd\x04'
    b'\x00\x00\x00\x0F{"value": 1234}'
    b'\x00\x00\x00\x11\x01{"value": -4321}'
)
