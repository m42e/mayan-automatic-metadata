#!/bin/bash

if [ "$1" == "rq" ]; then
    echo "rq mode"
    if [ "$USE_GIT_PLUGINS" == "1" ]; then
      if [ "x${GIT_PLUGINS_URL}x" != "xx" ];then
        rm -rf plugins/*
        git clone --depth 1 ${GIT_PLUGINS_URL} plugins
      else
        echo "No GIT Plugin URL Provided"
      fi
    fi
    rq worker mam -vvv --url $REDIS_URL
fi

if [ "$1" == "mam" ]; then
    echo "mam mode"
    gunicorn service:app -b '0.0.0.0:8000'
fi
