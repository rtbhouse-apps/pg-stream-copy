from contextlib import AbstractContextManager
from os import fdopen, pipe
from threading import Thread
from types import TracebackType
from typing import Any, BinaryIO, Optional


class Writer(AbstractContextManager["Writer"]):
    """
    Provides piped, buffered access to PG COPY binary stream.
    To use:
        __init__, providing table and cursor to execute PG COPY on. Please note,
            the cursor will be shared with worker thread until close() is called.
        Call open() to initialize.
        Call append() to write data to the pipe. Please note there will be some
            cost for write() syscall, so it is advised to batch the data in
            chunks
        When all is written - call close() to finalize the transfer. It is not
            allowed to use object after close() was called
        Don't forget to call commit() on connection :D
    """

    _psycopg2_cursor: Any
    _table: str

    _pipe_read: Optional[BinaryIO]
    _pipe_write: Optional[BinaryIO]
    _consumer_thread: Optional[Thread]
    _consumer_thread_exceptions: list[Exception]

    def __init__(
        self,
        psycopg2_cursor: Any,  # Special care required, see class desc.
        table: str,  # With tablespace
    ):
        super().__init__()

        self._psycopg2_cursor = psycopg2_cursor
        self._table = table

        self._pipe_read = None
        self._pipe_write = None
        self._consumer_thread = None
        self._consumer_thread_exceptions = []

    def open(self) -> None:
        assert self._pipe_read is None
        assert self._pipe_write is None
        _pipe_read, _pipe_write = pipe()
        self._pipe_read = fdopen(_pipe_read, "rb")
        self._pipe_write = fdopen(_pipe_write, "wb")

        assert self._consumer_thread is None
        self._consumer_thread = Thread(target=self._consumer_thread_main)
        self._consumer_thread.start()
        self._consumer_thread_exceptions = []

    def close(self) -> None:
        exceptions: list[Exception] = []

        try:
            if self._pipe_write is not None:
                self._pipe_write.close()
                self._pipe_write = None
        except Exception as exc:
            exceptions.append(exc)

        try:
            if self._consumer_thread is not None:
                self._consumer_thread.join()
                self._consumer_thread = None
        except Exception as exc:
            exceptions.append(exc)

        # self._pipe_read closed inside thread

        exceptions.extend(self._consumer_thread_exceptions)

        if exceptions:
            raise Exception("Following exceptions were handled during Writer cleanup: ", exceptions)

    def append(self, data: bytes) -> None:
        assert self._pipe_write is not None, "Writer must be opened/entered before appending data"
        self._pipe_write.write(data)

    def _consumer_thread_main(self) -> None:
        assert self._pipe_read is not None

        exceptions: list[Exception] = []

        try:
            self._psycopg2_cursor.copy_expert(f"COPY {self._table} FROM STDIN BINARY", self._pipe_read)
        except Exception as exc:
            exceptions.append(exc)

        try:
            self._pipe_read.close()
            self._pipe_read = None
        except Exception as exc:
            exceptions.append(exc)

        self._consumer_thread_exceptions.extend(exceptions)

    def __enter__(self) -> "Writer":
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
