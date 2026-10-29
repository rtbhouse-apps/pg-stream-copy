#!/usr/bin/env bash

set -e
set -o pipefail

cd "`dirname $0`/.."

exit_code=0

docker compose run --rm --no-deps py uv run black ./
docker compose run --rm --no-deps py uv run isort --atomic ./
