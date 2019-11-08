#!/bin/bash

set -e
set -o pipefail

cd "`dirname $0`"
cd ..

export UID
docker-compose down
docker-compose config
docker-compose build
docker-compose run \
  -e TWINE_USERNAME=${TWINE_USERNAME} \
  -e TWINE_PASSWORD=${TWINE_PASSWORD} \
  dev bash -c "
python -m venv venv
pip install twine
python setup.py sdist
twine upload \
  --username \${TWINE_USERNAME:-__token__} \
  --password \${TWINE_PASSWORD} \
  --verbose \
  dist/*
"