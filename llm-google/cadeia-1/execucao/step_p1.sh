#!/bin/bash
set -e
exec > /home/revisor/evidencias/env_info.txt 2>&1
uname -a
cat /etc/os-release
if [ -n "$VT_API_KEY" ]; then
    echo "VT_API_KEY: presente (mascarada: <VT_API_KEY>)"
else
    echo "VT_API_KEY: ausente"
fi
