#!/usr/bin/env bash

set -e
set -o pipefail

cd "`dirname $0`/.."

docker compose run -it --rm --service-ports -e WAIT_HOSTS=db:5432 py sh -c "/wait && poetry run pytest"
