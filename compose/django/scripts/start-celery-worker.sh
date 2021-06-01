#!/usr/bin/env bash
/app/wait-for-it.sh ${POSTGRES_HOST:-database}:${POSTGRES_PORT:-5432} -s -t 180 -- \
celery -A demo_app.celery worker --loglevel=${LOG_LEVEL:-debug}
