from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Any, Optional

from .protocol import (
    build_bigint,
    build_boolean,
    build_character_varying,
    build_date,
    build_double_precision,
    build_integer,
    build_json,
    build_jsonb,
    build_null,
    build_numeric,
    build_row_header,
    build_row_trailer,
    build_smallint,
    build_table_header,
    build_table_trailer,
    build_text,
    build_timestamp,
    build_timestamp_tz,
)
from .schema import DataType, Schema
from .writer import Writer


class Encoder(AbstractContextManager["Encoder"]):
    """
    Provides access to Writer with row-level access by either tuples or
    dicts. Allows to easily append rows to postgres without taking care of
    underlying representation.

    To use:
        - initialize
        - call open()
        - call append_tuple(...) / append_dict(...) repeatedly
        - call close() to finalize
    """

    _schema: Schema
    _writer: Writer

    def __init__(
        self,
        schema: Schema,
        writer: Writer,
    ):
        super().__init__()

        self._schema = schema
        self._writer = writer

    def open(self) -> None:
        self._append_table_header()

    def close(self) -> None:
        self._append_table_trailer()

    def append_tuple(self, row: tuple[Any, ...]) -> None:
        assert len(self._schema.columns) == len(row)
        self._writer.append(self._build_row(row))

    def append_dict(self, row: dict[str, Any]) -> None:
        self.append_tuple(tuple(row[column.name] for column in self._schema.columns))

    def _append_table_header(self) -> None:
        self._writer.append(build_table_header())

    def _append_table_trailer(self) -> None:
        self._writer.append(build_table_trailer())

    def _build_row(self, row: tuple[Any, ...]) -> bytes:
        chunks_row = [self._build_cell(column.data_type, value) for column, value in zip(self._schema.columns, row)]
        return b"".join(
            [
                build_row_header(len(self._schema.columns)),
                *chunks_row,
                build_row_trailer(),
            ]
        )

    def _build_cell(
        self,
        data_type: DataType,
        value: Any,
    ) -> bytes:
        if value is None:
            return build_null()

        return _data_type_protocol_build[data_type](value)

    def __enter__(self) -> "Encoder":
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


_data_type_protocol_build: dict[DataType, Callable[[Any], bytes]] = {
    DataType.BOOLEAN: build_boolean,
    DataType.SMALLINT: build_smallint,
    DataType.INTEGER: build_integer,
    DataType.BIGINT: build_bigint,
    DataType.DOUBLE_PRECISION: build_double_precision,
    DataType.NUMERIC: build_numeric,
    DataType.CHARACTER_VARYING: build_character_varying,
    DataType.TEXT: build_text,
    DataType.DATE: build_date,
    DataType.TIMESTAMP: build_timestamp,
    DataType.TIMESTAMP_TZ: build_timestamp_tz,
    DataType.JSON: build_json,
    DataType.JSONB: build_jsonb,
}
