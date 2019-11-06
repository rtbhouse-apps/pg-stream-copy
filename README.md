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

schema = Schema.load_from_table(cursor, table_name)
with WriterEncoder(cursor, table_name, schema) as writer_encoder:
    writer_encoder.append_tuple((2, 3, 4, 2.34, "2", date(2019, 2, 1)))
    writer_encoder.append_dict({
        'col1': 200,
        'col2': 300,
        'col3': 400,
        'col4': 234,
        'col5': '200',
        'col6': date(2019, 2, 3),
    })

cursor.commit()
conn.close()

```

More detailed example in tests: https://github.com/rtbhouse-apps/pg-stream-copy/blob/master/tests/e2e/test_e2e.py

### Supported PostgreSQL types:
* smallint
* integer
* bigint
* double precision
* character varying
* date