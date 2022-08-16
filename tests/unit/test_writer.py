from io import BufferedReader
from unittest.mock import MagicMock, Mock

from pg_stream_copy.writer import Writer


def test_all_1() -> None:
    buffer = bytearray()

    def copy_expert_mock(query: str, data_: BufferedReader) -> None:
        assert query == "COPY test_table FROM STDIN BINARY"
        buffer.extend(data_.read())

    psycopg2_cursor = MagicMock()
    copy_export_mock = psycopg2_cursor.copy_expert = Mock(
        side_effect=copy_expert_mock,
    )

    with Writer(psycopg2_cursor, "test_table") as writer:
        writer.append(b"\x01\x02")
        writer.append(b"\x03\x04")

    copy_export_mock.assert_called_once()
    assert buffer == b"\x01\x02\x03\x04"
