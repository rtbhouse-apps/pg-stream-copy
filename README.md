# PG Stream Copy
[![Build Status](https://travis-ci.com/rtbhouse-apps/pg-stream-copy.svg?branch=master)](https://travis-ci.com/rtbhouse-apps/pg-stream-copy)
[![codecov](https://codecov.io/gh/rtbhouse-apps/pg-stream-copy/branch/master/graph/badge.svg)](https://codecov.io/gh/rtbhouse-apps/pg-stream-copy)
[![PyPI](https://img.shields.io/pypi/v/pg-stream-copy)](https://pypi.org/project/pg-stream-copy/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pg-stream-copy)](https://pypi.org/project/pg-stream-copy/)

Fast COPY TO postgresql table directly from python by converting input data to bytes and stream to psycopg2 cursor using `COPY <table> FROM STDIN BINARY`

### Benchmark:
The test with 1 mln rows of different column types on docker environment gave results:
* ~21.5s for `pg_stream_copy`
* ~54s for `psycopg2.extras.execute_values`

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
        _numeric NUMERIC NULL,
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
        '_numeric': Decimal("-12.34")
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
* numeric
* character varying
* text
* date
* json
* jsonb


### Development:
```bash
# prepare env
docker-compose run py bash
python -m venv venv
pip install -e .[dev,e2e]
# run tests
pytest tests/
```
If you need to test different PostgreSQL and Python version, you can use env vars:
```bash
PYTHON_VERSION=3.7 PG_VERSION=10 docker-compose build
PYTHON_VERSION=3.7 PG_VERSION=10 docker-compose run py ...
```
or use CI script:
```bash
PG_VERSION=11 PYTHON_VERSION=3.7 ./bin/tests.sh
```
currently pg_stream_copy is supporting Python 3.7 and 3.8 and PostgreSQL v10, v11, v12
