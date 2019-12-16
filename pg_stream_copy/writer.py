from os import fdopen, pipe
from threading import Thread
from typing import Any, List


class Writer:
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

    _pipe_read: Any
    _pipe_write: Any
    _consumer_thread: Thread
    _consumer_thread_exceptions: List[Exception]

    def __init__(
        self,
        psycopg2_cursor: Any,  # Special care required, see class desc.
        table: str,  # With tablespace
    ):
        self._psycopg2_cursor = psycopg2_cursor
        self._table = table

    def open(self):
        _pipe_read, _pipe_write = pipe()
        self._pipe_read = fdopen(_pipe_read, 'rb')
        self._pipe_write = fdopen(_pipe_write, 'wb')

        self._consumer_thread = Thread(target=self._consumer_thread_main)
        self._consumer_thread.start()
        self._consumer_thread_exceptions = []

    def close(self):
        exceptions = []

        try:
            if self._pipe_write is not None:
                self._pipe_write.close()
        except Exception as e:
            exceptions.append(e)

        try:
            if self._consumer_thread is not None:
                self._consumer_thread.join()
        except Exception as e:
            exceptions.append(e)

        exceptions.extend(self._consumer_thread_exceptions)

        if exceptions:
            raise Exception('Following exceptions were handled during Writer cleanup: ', exceptions)

    def append(self, data: bytes):
        self._pipe_write.write(data)

    def _consumer_thread_main(self):
        exceptions = []

        try:
            self._psycopg2_cursor.copy_expert(f"COPY {self._table} FROM STDIN BINARY", self._pipe_read)
        except Exception as e:
            exceptions.append(e)

        try:
            if self._pipe_read is not None:
                self._pipe_read.close()
        except Exception as e:
            exceptions.append(e)

        self._consumer_thread_exceptions.extend(exceptions)

    def __enter__(self):
        try:
            self.open()
        except Exception as e:
            self.close()
            raise e
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
