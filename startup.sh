#!/bin/bash

log_dir="$HOME/jamrecorder/logs/`date +%Y-%m-%d`"
mkdir -p $log_dir

export PATH=$PATH:~/jamrecorder/jamrecorder-server/venv/bin/:~/.nvm/versions/node/v6.12.3/bin/ # Expose flask and node

pushd ~/jamrecorder/jamrecorder-server
./start.sh >> $log_dir/jamrecorder-server.log 2>&1 &

AWS_PROFILE=IoTCommunicator AWS_THING_REGION=us-west-2 AWS_THING_ENDPOINT='aeeoo00izmku2.iot.us-west-2.amazonaws.com' node ~/jamrecorder/iot-communicator/server.js >> $log_dir/iot-communicator-server.log 2>&1 &