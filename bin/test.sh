#!/usr/bin/env bash

set -e
set -o pipefail

cd "`dirname $0`/.."

docker compose run -it --rm --service-ports py sh -c "/wait && poetry run pytest"
