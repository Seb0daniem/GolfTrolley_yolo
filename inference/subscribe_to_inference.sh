#!/bin/bash
echo "Subscribing to 'inference_metadata'..."
mosquitto_sub -h localhost -p 1883 -t inference_metadata
