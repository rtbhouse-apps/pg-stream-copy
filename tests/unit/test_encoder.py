from unittest.mock import Mock

from pg_stream_copy.encoder import Encoder

from . import data


def test_all_1():
    writer = Mock()

    with Encoder(
        data.set_1_schema,
        writer
    ) as encoder:
        writer.append.assert_called_once_with(b'PGCOPY\n\xff\r\n\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        writer.reset_mock()

        encoder.append_tuple(data.set_1_row_tuple)
        writer.append.assert_called_once_with(data.set1_row_binary)
        writer.reset_mock()

        encoder.append_dict(data.set_1_row_dict)
        writer.append.assert_called_once_with(data.set1_row_binary)
        writer.reset_mock()

    writer.append.assert_called_once_with(b'\xff\xff')
    writer.reset_mock()
