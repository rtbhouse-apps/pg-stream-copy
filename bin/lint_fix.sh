#!/usr/bin/env bash

set -e
set -o pipefail

cd "`dirname $0`/.."

exit_code=0

docker compose run --rm --no-deps py poetry run black ./
docker compose run --rm --no-deps py poetry run isort --atomic ./
