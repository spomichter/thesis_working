#!/bin/bash

docker run -it \
--privileged \
--network=host \
--ipc=host \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
--env DISPLAY=host.docker.internal:0 \
thesis_image bash