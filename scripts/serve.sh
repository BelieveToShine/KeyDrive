#!/bin/sh
# start the local preview server on :5931 if it is not already answering (it dies between turns)
cd "$(dirname "$0")/.." || exit 1
curl -s -o /dev/null http://localhost:5931/index.html && exit 0
setsid nohup python3 -m http.server 5931 >/dev/null 2>&1 &
sleep 1
