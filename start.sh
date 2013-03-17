#!/bin/bash
# see scripts/debian-init.d for production deployments

cd `dirname $0`
export PYTHONPATH=`dirname $0`
twistd -n cyclone -p 11000 -l 127.0.0.1 \
       -r deck.web.Application -c deck.conf $*
