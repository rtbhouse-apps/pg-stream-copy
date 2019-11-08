#!/bin/bash

set -e
set -o pipefail

cd "`dirname $0`"
cd ..

export UID
export PG_VERSION=${PG_VERSION:-"12"}
export PYTHON_VERSION=${PYTHON_VERSION:-"3.8"}

echo "starting tests for POSTGRESQL ${PG_VERSION} and PYTHON ${PYTHON_VERSION}"

docker-compose down
docker-compose config
docker-compose up -d db
docker-compose build
docker-compose run db psql --version
docker-compose run py bash -c "
python -m venv venv
python --version
pip install .[dev,e2e]
pytest --cov=pg_stream_copy tests/
"
docker-compose down