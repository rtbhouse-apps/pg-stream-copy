from unittest.mock import MagicMock, Mock

from pg_stream_copy.encoder import Encoder

from . import data


def test_all_1() -> None:
    writer = MagicMock()
    append_mock = writer.append = Mock()

    with Encoder(data.SET1_SCHEMA, writer) as encoder:
        append_mock.assert_called_once_with(b"PGCOPY\n\xff\r\n\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        writer.reset_mock()

        encoder.append_tuple(data.SET1_ROW_TUPLE)
        append_mock.assert_called_once_with(data.SET1_ROW_BINARY)
        writer.reset_mock()

        encoder.append_dict(data.SET1_ROW_DICT)
        append_mock.assert_called_once_with(data.SET1_ROW_BINARY)
        writer.reset_mock()

    append_mock.assert_called_once_with(b"\xff\xff")
    writer.reset_mock()
