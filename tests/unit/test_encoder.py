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
        writer.append.assert_called_once_with(
            b'\x00\x06\x00\x00\x00\x02\x11E\x00\x00\x00\x04\x12A\xf2\xd0\x00\x00\x00\x08%4\xa1>'
            b'\xb3U\xf7\xee\x00\x00\x00\x08@(\xae\x14z\xe1G\xae\x00\x00\x00\x11'
            b'lorem ipsum dolor\x00\x00\x00\x04\x00\x00\x02k'
        )
        writer.reset_mock()

        encoder.append_dict(data.set_1_row_dict)
        writer.append.assert_called_once_with(
            b'\x00\x06\x00\x00\x00\x02\x11E\x00\x00\x00\x04\x12A\xf2\xd0\x00\x00\x00\x08%4\xa1>'
            b'\xb3U\xf7\xee\x00\x00\x00\x08@(\xae\x14z\xe1G\xae\x00\x00\x00\x11'
            b'lorem ipsum dolor\x00\x00\x00\x04\x00\x00\x02k'
        )
        writer.reset_mock()

    writer.append.assert_called_once_with(b'\xff\xff')
    writer.reset_mock()
