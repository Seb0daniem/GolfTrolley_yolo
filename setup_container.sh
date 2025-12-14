#!/bin/bash
echo "Installing Python deps..."
pip3 install paho-mqtt
pip3 install board
pip3 install adafruit-circuitpython-pca9685
pip3 install Jetson.GPIO

echo "Removing recorded videos..."
find /user/recorded -mindepth 1 ! -name ".gitkeep" -delete
echo "Done setting up container."
