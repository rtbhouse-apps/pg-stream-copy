from datetime import date

from pg_stream_copy import ColumnDefinition, DataType, Schema

set_1_schema = Schema([
    ColumnDefinition('SMALLINT', DataType.SMALLINT),
    ColumnDefinition('INTEGER', DataType.INTEGER),
    ColumnDefinition('BIGINT', DataType.BIGINT),
    ColumnDefinition('DOUBLE_PRECISION', DataType.DOUBLE_PRECISION),
    ColumnDefinition('CHARACTER_VARYING', DataType.CHARACTER_VARYING),
    ColumnDefinition('DATE', DataType.DATE),
])
set_1_row_tuple = (0x1145, 0x1241f2d0, 0x2534a13eb355f7ee, 12.34, "lorem ipsum dolor", date(2001, 9, 11))
set_1_row_dict = {
    'SMALLINT': 0x1145,
    'INTEGER': 0x1241f2d0,
    'BIGINT': 0x2534a13eb355f7ee,
    'DOUBLE_PRECISION': 12.34,
    'CHARACTER_VARYING': "lorem ipsum dolor",
    'DATE': date(2001, 9, 11),
}
