#!/bin/bash

docker run -it \
--user ros \
--privileged \
-p 10000:10000 \
-v /tmp/.X11-unix:/tmp/.X11-unix:rw \
--env DISPLAY=host.docker.internal:0 \
thesis_image bash
