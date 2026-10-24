#!/bin/bash
set -e
exec > /home/revisor/evidencias/install.log 2>&1
cd /home/revisor/foremost-ng/foremost-ng-bb812a22/src
sudo make install
which foremost-ng
ls -lh /usr/local/bin/foremost-ng
