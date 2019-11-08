#!/bin/bash

set -e
set -o pipefail

cd "`dirname $0`"
cd ..

export UID
docker-compose down
docker-compose config
docker-compose build
docker-compose run py bash -c "
python --version
python -m venv venv
pip install .[dev]
code=0
mypy . || code=\$?
pycodestyle tests/ pg_stream_copy/ || code=\$?
exit \$code
"
docker-compose down