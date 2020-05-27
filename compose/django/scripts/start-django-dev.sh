#!/usr/bin/env bash
/app/wait-for-it.sh ${POSTGRES_HOST:-database}:${POSTGRES_PORT:-5432} -s -t 180 -- \
python /app/src/manage.py runserver 0.0.0.0:${DJANGO_RUNSERVER_PORT:-8100} -v3
