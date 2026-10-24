#!/bin/bash
set -e
exec > /home/revisor/evidencias/cli_help_version.txt 2>&1
echo "=== foremost-ng -V ==="
foremost-ng -V
echo "=== foremost-ng -h ==="
foremost-ng -h || true
