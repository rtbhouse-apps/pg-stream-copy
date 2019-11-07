# PG Stream Copy
[![Build Status](https://travis-ci.com/rtbhouse-apps/pg-stream-copy.svg?branch=master)](https://travis-ci.com/rtbhouse-apps/pg-stream-copy) [![codecov](https://codecov.io/gh/rtbhouse-apps/pg-stream-copy/branch/master/graph/badge.svg)](https://codecov.io/gh/rtbhouse-apps/pg-stream-copy)

Fast COPY TO postgresql table directly from python by converting input data to bytes and stream to psycopg2 cursor using `COPY <table> FROM STDIN BINARY`

### Usage:
```python
from datetime import date
from psycopg2 import connect
from pg_stream_copy import Schema, WriterEncoder


conn = connect('postgresql://postgres@localhost')
cursor = conn.cursor()
table_name = 'public.example_table'

cursor.execute(f'''
    CREATE TABLE {table_name} (
        _smallint SMALLINT NULL,
        _integer INTEGER NULL,
        _bigint BIGINT NULL,
        _float DOUBLE PRECISION NULL,
        _character_varying CHARACTER VARYING NULL,
        _date DATE NULL
    );
''')
schema = Schema.load_from_table(cursor, table_name)

with WriterEncoder(cursor, table_name, schema) as writer_encoder:
    writer_encoder.append_tuple((2, 3, 4, 2.34, 'foo bar', date(2019, 2, 1)))
    writer_encoder.append_dict({
        '_smallint': 200,
        '_integer': 300,
        '_bigint': 400,
        '_float': 234,
        '_character_varying': 'bar baz',
        '_date': date(2019, 2, 3),
    })

conn.commit()
conn.close()

```

### Supported PostgreSQL types:
* smallint
* integer
* bigint
* double precision
* character varying
* date