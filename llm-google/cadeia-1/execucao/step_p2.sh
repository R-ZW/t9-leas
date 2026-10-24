#!/bin/bash
set -e
exec > /home/revisor/evidencias/apt_install.log 2>&1
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev python3
gcc --version
make --version
