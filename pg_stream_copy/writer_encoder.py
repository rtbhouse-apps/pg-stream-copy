from contextlib import AbstractContextManager
from types import TracebackType
from typing import Any, Optional

from .encoder import Encoder
from .schema import Schema
from .writer import Writer


class WriterEncoder(AbstractContextManager["WriterEncoder"]):
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
        super().__init__()

        self.writer = Writer(
            psycopg2_cursor,
            table,
        )
        self.encoder = Encoder(
            schema,
            self.writer,
        )

    def open(self) -> None:
        self.writer.open()
        self.encoder.open()

    def close(self) -> None:
        exceptions: list[Exception] = []

        try:
            self.encoder.close()
        except Exception as exc:
            exceptions.append(exc)

        try:
            self.writer.close()
        except Exception as exc:
            exceptions.append(exc)

        if exceptions:
            raise Exception("Following exceptions were handled during WriterEncoder cleanup: ", exceptions)

    def append_tuple(self, row: tuple[Any, ...]) -> None:
        self.encoder.append_tuple(row)

    def append_dict(self, row: dict[str, Any]) -> None:
        self.encoder.append_dict(row)

    def __enter__(self) -> "WriterEncoder":
        try:
            self.open()
        except Exception as exc:
            self.close()
            raise exc

        return self

    def __exit__(
        self,
        __exc_type: Optional[type[BaseException]],
        __exc_value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    ) -> None:
        self.close()
