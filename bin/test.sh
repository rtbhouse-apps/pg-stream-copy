#!/usr/bin/env bash

set -e
set -o pipefail

cd "`dirname $0`/.."

docker compose run --rm --service-ports py pytest
