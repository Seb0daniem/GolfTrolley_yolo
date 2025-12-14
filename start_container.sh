sudo docker run -it --ipc=host \
  --privileged \
  --runtime=nvidia \
  --gpus all \
  --network=host \
  -e DISPLAY=$DISPLAY \
  -v /home/daniel/GolfTrolley_yolo:/user \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -w /user \
  ultralytics/ultralytics:latest-jetson-jetpack6 \
  bash -c "/user/setup_container.sh && bash"
