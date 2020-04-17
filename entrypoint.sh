#!/bin/bash

if [ "$1" == "rq" ]; then
    echo "rq mode"
    rq worker mam -vvv --url $REDIS_URL
fi

if [ "$1" == "mam" ]; then
    echo "mam mode"
    gunicorn service:app -b '0.0.0.0:8000'
fi
