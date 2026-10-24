#!/bin/bash
set -e
exec > /home/revisor/evidencias/build.log 2>&1
cd /home/revisor/foremost-ng/foremost-ng-bb812a22/src
make clean
make
ls -lh foremost-ng
file foremost-ng
