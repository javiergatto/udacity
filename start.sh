#!/bin/bash

export TERM=xterm

. start-server.sh

. start-app.sh

tail -f /dev/null
