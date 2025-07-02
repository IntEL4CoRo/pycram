#!/bin/bash

source ${PYCRAM_WS}/devel/setup.bash
roscore &
roslaunch --wait rvizweb rvizweb.launch &
roslaunch --wait pycram ik_and_description.launch &

# code-server --auth=none --abs-proxy-base-path=/proxy/8080/ &
code-server --auth=none --abs-proxy-base-path=/user/$JUPYTERHUB_CLIENT_ID/proxy/8080 &
exec "$@"