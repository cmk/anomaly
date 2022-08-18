#!/bin/bash

echo "Running anomaly.py"
sudo PYTHONPATH=/home/cmk/.local/lib/python3.9/site-packages:$PYTHONPATH /usr/bin/python3 /home/cmk/Documents/anomaly/anomaly.py & > /home/cmk/Desktop/log.txt 2>&1

