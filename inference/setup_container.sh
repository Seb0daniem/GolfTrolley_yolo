#!/bin/bash
echo "Installing Python deps..."
pip install paho-mqtt

echo "Removing recorded videos..."
find /user/recorded -mindepth 1 ! -name ".gitkeep" -delete
echo "Done setting up container."
