#!/bin/bash

docker run -dt \
--user ros \
--runtime=nvidia \
--gpus all \
--privileged \
-p 10000:10000 \
-p 5901:5901 \
-p 6901:6901 \
dim_img bash
