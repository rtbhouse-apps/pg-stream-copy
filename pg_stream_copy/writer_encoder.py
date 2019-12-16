from typing import Any

from .encoder import Encoder
from .schema import Schema
from .writer import Writer


class WriterEncoder:
    """
    Provides all-in-one access to write functionality
    To use:
        __init__ with cursor, table and schema. See Writer and
            Encoder for details
        call append_* repeatedly
        call close() (or use as context manager)
    """
    writer: Writer
    encoder: Encoder

    def __init__(
        self,
        psycopg2_cursor: Any,
        table: str,
        schema: Schema,
    ):
        self.writer = Writer(
            psycopg2_cursor,
            table,
        )
        self.encoder = Encoder(
            schema,
            self.writer,
        )

    def open(self):
        self.writer.open()
        self.encoder.open()

    def close(self):
        exceptions = []

        try:
            self.encoder.close()
        except Exception as e:
            exceptions.append(e)

        try:
            self.writer.close()
        except Exception as e:
            exceptions.append(e)

        if exceptions:
            raise Exception('Following exceptions were handled during WriterEncoder cleanup: ', exceptions)

    def append_tuple(self, row: tuple):
        self.encoder.append_tuple(row)

    def append_dict(self, row: dict):
        self.encoder.append_dict(row)

    def __enter__(self):
        try:
            self.open()
        except Exception as e:
            self.close()
            raise e
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
