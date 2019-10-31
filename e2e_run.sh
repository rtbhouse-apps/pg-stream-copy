#!/bin/bash

docker-compose -f e2e.docker-compose.yaml up \
    --abort-on-container-exit \
    --exit-code-from e2e
