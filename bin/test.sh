#!/usr/bin/env bash

set -e
set -o pipefail

cd "`dirname $0`/.."

docker compose run --rm py pytest
