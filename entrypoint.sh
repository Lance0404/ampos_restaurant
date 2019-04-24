#!/bin/bash
set -e

if [ "$1" = 'celery' ] && [ "$2" = 'worker' ]; then
    # exec newrelic-admin run-program "$@"
    exec "$@"
elif [ "$1" = 'celery' ] && [ "$2" = 'beat' ]; then
    # exec newrelic-admin run-program "$@"
    exec "$@"
elif [ "$1" = 'web' ]; then
    # exec newrelic-admin run-program "$@"
    exec "$@"
else
    exec "$@"
fi
