from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List, NamedTuple


class DataType(Enum):
    """
    Postgres DataTypes
    Since PG COPY requires data in exact format (eg. 2 bytes for smallint, 4
        bytes for integer) and python data types don't allow to set length, we
        describe schema that is used to remap types to binary forms
    """
    BOOLEAN = auto()  # boolean
    SMALLINT = auto()  # int
    INTEGER = auto()  # int
    BIGINT = auto()  # int
    DOUBLE_PRECISION = auto()  # float
    NUMERIC = auto()  # Decimal
    CHARACTER_VARYING = auto()  # str
    TEXT = auto()  # str
    DATE = auto()  # datetime.date
    TIMESTAMP = auto()  # datetime.datetime without timezone
    TIMESTAMP_TZ = auto()  # datetime.datetime with timezone
    JSON = auto()  # str, eg. json.dumps({})
    JSONB = auto()  # bytes, eg. bytes(json.dumps({}), 'utf-8')


class ColumnDefinition(NamedTuple):
    name: str
    data_type: DataType


@dataclass
class Schema:
    """
    Internal postgres table schema representation
    """
    columns: List[ColumnDefinition]

    @staticmethod
    def load_from_table(
        psycopg2_cursor: Any,
        table: str,  # Must have table_schema.table_name format
    ) -> Schema:
        """
        Retrives this schema from given table
        """
        table_schema, table_name = table.split(".")

        # Possible need to filter table_catalog
        psycopg2_cursor.execute('''
            SELECT
                column_name, data_type
            FROM
                information_schema.columns
            WHERE
                table_schema = %(table_schema)s AND
                table_name = %(table_name)s
            ORDER BY
                ordinal_position
        ''', {
            'table_schema': table_schema,
            'table_name': table_name,
        })

        columns = [
            ColumnDefinition(
                name=row[0],
                data_type=_pg_data_type_to_py[row[1]]
            )
            for row in psycopg2_cursor
        ]

        if not columns:
            raise Exception("information_schema returned 0 rows for this table. Most likely the table was not found.")

        return Schema(
            columns=columns
        )


_pg_data_type_to_py = {
    'boolean': DataType.BOOLEAN,
    'smallint': DataType.SMALLINT,
    'integer': DataType.INTEGER,
    'bigint': DataType.BIGINT,
    'double precision': DataType.DOUBLE_PRECISION,
    'numeric': DataType.NUMERIC,
    'character varying': DataType.CHARACTER_VARYING,
    'text': DataType.TEXT,
    'date': DataType.DATE,
    'timestamp without time zone': DataType.TIMESTAMP,
    'timestamp with time zone': DataType.TIMESTAMP_TZ,
    'json': DataType.JSON,
    'jsonb': DataType.JSONB,
}
