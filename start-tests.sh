#!/usr/bin/env bash
/app/src/wait-for-it.sh ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432} -s -t 180 -- \
pytest
