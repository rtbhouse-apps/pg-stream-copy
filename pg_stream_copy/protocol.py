from datetime import date, datetime, timezone
from decimal import Decimal
from struct import pack
from typing import List, Tuple, cast

# https://www.postgresql.org/docs/10/sql-copy.html - Binary Format section

pg_null = pack('>I', 0xFFFFFFFF)
pg_date_epoch = date(2000, 1, 1)
pg_timestamp_epoch = datetime(2000, 1, 1).timestamp()
pg_timestamp_tz_epoch = datetime(2000, 1, 1, tzinfo=timezone.utc).timestamp()


################################################################################
# table level
################################################################################
def build_table_header() -> bytes:
    return b"PGCOPY\n\377\r\n\0" + pack('>I', 0) + pack('>I', 0)


def build_table_trailer() -> bytes:
    return pack('>H', 0xFFFF)


################################################################################
# row level
################################################################################
def build_row_header(columns_count: int) -> bytes:
    return pack('>H', columns_count)


def build_row_trailer() -> bytes:
    return b''


################################################################################
# cell level
################################################################################
def _build_value(value: bytes) -> bytes:
    return pack('>I', len(value)) + value


def build_null() -> bytes:
    return pg_null


def build_boolean(value: bool) -> bytes:
    return _build_value(pack('>?', value))


def build_smallint(value: int) -> bytes:
    return _build_value(pack('>h', value))


def build_integer(value: int) -> bytes:
    return _build_value(pack('>i', value))


def build_bigint(value: int) -> bytes:
    return _build_value(pack('>q', value))


def build_double_precision(value: float) -> bytes:
    return _build_value(pack('>d', value))


def build_numeric(value: Decimal) -> bytes:
    value_tuple = value.as_tuple()

    if not isinstance(value_tuple.exponent, int):
        return _build_value(pack(
            f'>hhHH',
            0,
            0,
            0xC000,
            0,
        ))

    # RPad digits so exponent is dividable 4
    exponent = value_tuple.exponent
    digits = list(value_tuple.digits)
    digits += [0] * (exponent % 4)
    exponent -= (exponent % 4)
    exponent //= 4

    # LPad digits, so they are grouped by 4
    digits = [0] * (-len(digits) % 4) + digits

    # Group into 4-element tuples
    digits_groups = [
        cast(Tuple[int, int, int, int], tuple(digits[index * 4:(index + 1) * 4]))
        for index in range(0, len(digits) // 4)
    ]

    # Convert 4-element tuples into
    def digits_group_to_pg_digit(digits_group: Tuple[int, int, int, int]) -> int:
        pg_digit = 0
        for exponent, digit in enumerate(reversed(digits_group)):
            pg_digit += digit * 10 ** exponent
        return pg_digit

    pg_digits = [digits_group_to_pg_digit(digits_group) for digits_group in digits_groups]

    # Cut R-zeros, convert each cut zero to +1 exponent
    def pg_digits_rtrim(pg_digits: List[int]) -> Tuple[List[int], int]:
        for index, pg_digit in enumerate(reversed(pg_digits)):
            if pg_digit == 0:
                continue

            if index == 0:
                return (pg_digits, 0)
            else:
                return (pg_digits[:-index], index)

        return ([], len(pg_digits))

    (pg_digits, pg_digits_trimmed) = pg_digits_rtrim(pg_digits)
    exponent += pg_digits_trimmed

    # https://www.postgresql.org/message-id/16572.1091489720@sss.pgh.pa.us
    return _build_value(pack(
        f'>hhHH{len(pg_digits)}H',
        len(pg_digits),
        exponent + len(pg_digits) - 1,
        0x4000 if value_tuple.sign else 0x0000,
        -value_tuple.exponent,
        *pg_digits
    ))


def build_character_varying(value: str) -> bytes:
    return _build_value(bytes(value, 'utf-8'))


def build_text(value: str) -> bytes:
    return build_character_varying(value)


def build_date(day: date) -> bytes:
    days = (day - pg_date_epoch).days
    return build_integer(days)


def build_timestamp(value: datetime):
    if value.tzinfo is not None:
        raise Exception('datatime with timezone cannot be used for timestamp field')

    timestamp_ms = int((value.timestamp() - pg_timestamp_epoch) * 1_000_000)
    return _build_value(pack('>q', timestamp_ms))


def build_timestamp_tz(value: datetime):
    if value.tzinfo is None:
        raise Exception('datatime without timezone cannot be used for timestamptz field')

    timestamp_ms = int((value.timestamp() - pg_timestamp_tz_epoch) * 1_000_000)
    return _build_value(pack('>q', timestamp_ms))


def build_json(value: str) -> bytes:
    return build_character_varying(value)


def build_jsonb(value: bytes) -> bytes:
    return _build_value(pack('>B', 1) + value)
