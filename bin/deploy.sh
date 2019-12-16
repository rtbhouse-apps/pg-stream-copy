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
  py bash -c "
python -m venv venv
pip install \
  setuptools==42.0.2 \
  twine==3.1.1 \
  wheel==0.33.6
python setup.py build sdist bdist_wheel
twine upload \
  --username \${TWINE_USERNAME:-__token__} \
  --password \${TWINE_PASSWORD} \
  --verbose \
  dist/*
"
