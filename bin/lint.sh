#!/usr/bin/env bash

set -e
set -o pipefail

cd "`dirname $0`/.."

exit_code=0

echo -e "\nRunning black..."
docker compose run --rm --no-deps py poetry run black --check . || exit_code=1

echo -e "\nRunning isort..."
docker compose run --rm --no-deps py poetry run isort -c -q . || exit_code=1

echo -e "\nRunning flake8..."
docker compose run --rm --no-deps py poetry run flake8 || exit_code=1

echo -e "\nRunning mypy..."
docker compose run --rm --no-deps py poetry run mypy . || exit_code=1

echo -e "\nRunning pylint..."
docker compose run --rm --no-deps py poetry run pylint pg_stream_copy tests || exit_code=1

exit $exit_code
