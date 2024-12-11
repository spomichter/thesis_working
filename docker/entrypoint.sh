#!/bin/bash

set -e

source /opt/ros/humble/setup.bash
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
# source /home/ros/dev_ws/install/setup.bash
# source /home/ros/ws_moveit2/install/setup.bash

echo "Provided arguments: $@"

exec $@