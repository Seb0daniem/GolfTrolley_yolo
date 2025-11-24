#!/bin/bash
echo "Installing Python deps..."
pip install paho-mqtt

echo "Removing recorded videos..."
rm -r /user/recorded
echo "Done setting up container."
