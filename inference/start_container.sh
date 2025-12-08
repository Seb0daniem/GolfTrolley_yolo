#!/bin/bash

# If camera is not connected, anyway
DEVICE_ARG=""
if [ -e /dev/video0 ]; then
    DEVICE_ARG="--device=/dev/video0:/dev/video0"
fi

t=ultralytics/ultralytics:latest-jetson-jetpack6
sudo docker run -it --ipc=host \
	--runtime=nvidia \
	--gpus all \
	$DEVICE_ARG \
	--network=host \
	-e DISPLAY=$DISPLAY \
	-v /home/daniel/GolfTrolley_yolo:/user \
	-v /temp/.X11-unix:/tmp/.X11-unix \
	-w /user \
	$t \
	bash -c "/user/inference/setup_container.sh && bash"
