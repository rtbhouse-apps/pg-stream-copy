from unittest.mock import MagicMock, Mock

from pg_stream_copy.encoder import Encoder

from . import data


def test_all_1() -> None:
    writer = MagicMock()
    append_mock = writer.append = Mock()

    with Encoder(data.set_1_schema, writer) as encoder:
        append_mock.assert_called_once_with(b"PGCOPY\n\xff\r\n\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        writer.reset_mock()

        encoder.append_tuple(data.set_1_row_tuple)
        append_mock.assert_called_once_with(data.set1_row_binary)
        writer.reset_mock()

        encoder.append_dict(data.set_1_row_dict)
        append_mock.assert_called_once_with(data.set1_row_binary)
        writer.reset_mock()

    append_mock.assert_called_once_with(b"\xff\xff")
    writer.reset_mock()
