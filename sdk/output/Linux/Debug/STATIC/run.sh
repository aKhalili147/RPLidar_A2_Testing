#!/bin/bash

FILENAME=.
if [ $# -gt 0 ]; then
  FILENAME=$1
fi

./ultra_simple /dev/ttyUSB0 > $FILENAME
python3 test.py $FILENAME