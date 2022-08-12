from unittest.mock import MagicMock, Mock

from pg_stream_copy.writer import Writer


def test_all_1() -> None:
    psycopg2_cursor = MagicMock()
    copy_export_mock = psycopg2_cursor.copy_expert = Mock(
        return_value=None,
    )

    with Writer(psycopg2_cursor, "test_table") as writer:
        writer.append(b"\x01\x02")
        writer.append(b"\x03\x04")

    copy_export_mock.assert_called_once_with(
        "COPY test_table FROM STDIN BINARY",
        b"\x01\x02\x03\x04",
    )
