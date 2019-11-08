from datetime import date

from pg_stream_copy import ColumnDefinition, DataType, Schema

set_1_schema = Schema([
    ColumnDefinition('SMALLINT', DataType.SMALLINT),
    ColumnDefinition('INTEGER', DataType.INTEGER),
    ColumnDefinition('BIGINT', DataType.BIGINT),
    ColumnDefinition('DOUBLE_PRECISION', DataType.DOUBLE_PRECISION),
    ColumnDefinition('CHARACTER_VARYING', DataType.CHARACTER_VARYING),
    ColumnDefinition('TEXT', DataType.TEXT),
    ColumnDefinition('DATE', DataType.DATE),
    ColumnDefinition('JSON', DataType.JSON),
    ColumnDefinition('JSONB', DataType.JSONB),
])
set_1_row_tuple = (
    0x1145,
    0x1241f2d0,
    0x2534a13eb355f7ee,
    12.34,
    "lorem ipsum dolor",
    "sit amet, consectetur",
    date(2001, 9, 11),
    '{"value": 1234}',
    b'{"value": -4321}'
)
set_1_row_dict = {
    'SMALLINT': 0x1145,
    'INTEGER': 0x1241f2d0,
    'BIGINT': 0x2534a13eb355f7ee,
    'DOUBLE_PRECISION': 12.34,
    'CHARACTER_VARYING': "lorem ipsum dolor",
    'TEXT': "sit amet, consectetur",
    'DATE': date(2001, 9, 11),
    'JSON': '{"value": 1234}',
    'JSONB': b'{"value": -4321}',
}

set1_row_binary = b'\x00\x09' \
    b'\x00\x00\x00\x02\x11E' \
    b'\x00\x00\x00\x04\x12A\xf2' \
    b'\xd0\x00\x00\x00\x08%4\xa1>\xb3U\xf7\xee' \
    b'\x00\x00\x00\x08@(\xae\x14z\xe1G\xae' \
    b'\x00\x00\x00\x11lorem ipsum dolor' \
    b'\x00\x00\x00\x15sit amet, consectetur' \
    b'\x00\x00\x00\x04\x00\x00\x02k' \
    b'\x00\x00\x00\x0F{"value": 1234}' \
    b'\x00\x00\x00\x11\x01{"value": -4321}'
