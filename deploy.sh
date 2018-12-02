#!/bin/bash

scp -r ./iot-communicator/[\!.]* pi@raspberrypi.local:~/jamrecorder/iot-communicator
scp -r ./jamrecorder-server/[\!.]* pi@raspberrypi.local:~/jamrecorder/jamrecorder-server
