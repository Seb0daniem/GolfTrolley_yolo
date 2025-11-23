#!/bin/bash

t=ultralytics/ultralytics:latest-jetson-jetpack6
sudo docker run -it --ipc=host \
	--runtime=nvidia \
	--gpus all \
	--device=/dev/video0:/dev/video0 \
	-e DISPLAY=$DISPLAY \
	-v /home/daniel/GolfTrolley_yolo:/user \
	-v /temp/.X11-unix:/tmp/.X11-unix \
	-w /user \
	$t \
	bash -c "/user/inference/setup_container.sh && bash"
