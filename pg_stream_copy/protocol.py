from datetime import date
from struct import pack

# https://www.postgresql.org/docs/10/sql-copy.html - Binary Format section

pg_null = pack('>I', 0xFFFFFFFF)
pg_date_epoch = date(2000, 1, 1)  # https://www.postgresql.org/message-id/d34l6e%24284h%241%40news.hub.org


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


def build_smallint(value: int) -> bytes:
    return _build_value(pack('>h', value))


def build_integer(value: int) -> bytes:
    return _build_value(pack('>i', value))


def build_bigint(value: int) -> bytes:
    return _build_value(pack('>q', value))


def build_double_precision(value: float) -> bytes:
    return _build_value(pack('>d', value))


def build_character_varying(value: str) -> bytes:
    return _build_value(bytes(value, 'utf-8'))


def build_date(day: date) -> bytes:
    days = (day - pg_date_epoch).days
    return build_integer(days)
