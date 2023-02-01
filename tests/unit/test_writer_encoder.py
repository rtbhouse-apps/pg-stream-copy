from io import BufferedReader
from unittest.mock import MagicMock, Mock

from pg_stream_copy.writer_encoder import WriterEncoder

from . import data


def test_all_1() -> None:
    buffer = bytearray()

    def copy_expert_mock(query: str, data_: BufferedReader) -> None:
        assert query == "COPY test_table FROM STDIN BINARY"
        buffer.extend(data_.read())

    psycopg2_cursor = MagicMock()
    copy_export_mock = psycopg2_cursor.copy_expert = Mock(
        side_effect=copy_expert_mock,
    )

    with WriterEncoder(psycopg2_cursor, "test_table", data.SET1_SCHEMA) as write_encoder:
        write_encoder.append_tuple(data.SET1_ROW_TUPLE)
        write_encoder.append_dict(data.SET1_ROW_DICT)

    copy_export_mock.assert_called_once()
    assert buffer == (
        b"PGCOPY\n\xff\r\n\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        + data.SET1_ROW_BINARY
        + data.SET1_ROW_BINARY
        + b"\xff\xff"
    )
