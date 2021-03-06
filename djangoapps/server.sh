#!/bin/bash

ROOT=`pwd`
name=django
prefix=quizy

socket=/tmp/$prefix-$name.sock 
pidfile=$ROOT/logs/run/$name.pid 
errlog=$ROOT/logs/$name.error.log
python=$WORKON_HOME/$prefix/bin/python

cd $ROOT
case "$1" in
    "start")
        uwsgi --chdir=$ROOT --module=root.wsgi \
            --env DJANGO_SETTINGS_MODULE=root.settings_prod \
            --master --pidfile=$pidfile \
            --socket=$socket --processes=5 --harakiri=120 --post-buffering=1 \
            --max-requests=4000 --vacuum --home=$WORKON_HOME/$prefix \
            --daemonize=$errlog
        chmod o+w $socket
        ;;
    "stop")
        kill -9 `cat $pidfile`
        ;;
    "restart")
        ./server.sh stop
        ./server.sh start
        ;;
    *) 
        echo "Usage: ./server.sh {start|stop|restart}"
        ;;
esac
