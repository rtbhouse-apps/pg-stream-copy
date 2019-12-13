from __future__ import annotations

from typing import Any, Callable, Dict

from . import protocol
from .schema import DataType, Schema
from .writer import Writer


class Encoder:
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
        self._schema = schema
        self._writer = writer

    def open(self):
        self._append_table_header()

    def close(self):
        self._append_table_trailer()

    def append_tuple(self, row: tuple):
        assert len(self._schema.columns) == len(row)
        self._writer.append(
            self._build_row(row)
        )

    def append_dict(self, row: dict):
        self.append_tuple(tuple(row[column.name] for column in self._schema.columns))

    def _append_table_header(self):
        self._writer.append(
            protocol.build_table_header()
        )

    def _append_table_trailer(self):
        self._writer.append(
            protocol.build_table_trailer()
        )

    def _build_row(
        self,
        row: tuple
    ) -> bytes:
        chunks_row = [
            self._build_cell(column.data_type, value)
            for column, value in zip(self._schema.columns, row)
        ]
        return b''.join([
            protocol.build_row_header(len(self._schema.columns)),
            *chunks_row,
            protocol.build_row_trailer(),
        ])

    def _build_cell(
        self,
        data_type: DataType,
        value: Any,
    ) -> bytes:
        if value is None:
            return protocol.build_null()

        return _data_type_protocol_build[data_type](value)

    def __enter__(self):
        try:
            self.open()
        except Exception as e:
            self.close()
            raise e
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


_data_type_protocol_build: Dict[DataType, Callable[[Any], bytes]] = {
    DataType.BOOLEAN: protocol.build_boolean,
    DataType.SMALLINT: protocol.build_smallint,
    DataType.INTEGER: protocol.build_integer,
    DataType.BIGINT: protocol.build_bigint,
    DataType.DOUBLE_PRECISION: protocol.build_double_precision,
    DataType.NUMERIC: protocol.build_numeric,
    DataType.CHARACTER_VARYING: protocol.build_character_varying,
    DataType.TEXT: protocol.build_text,
    DataType.DATE: protocol.build_date,
    DataType.TIMESTAMP: protocol.build_timestamp,
    DataType.TIMESTAMP_TZ: protocol.build_timestamp_tz,
    DataType.JSON: protocol.build_json,
    DataType.JSONB: protocol.build_jsonb,
}
