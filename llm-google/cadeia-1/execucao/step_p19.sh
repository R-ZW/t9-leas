#!/bin/bash
set -e
exec > /home/revisor/evidencias/evidence2_find.txt 2>&1
echo "=== Buscando evidence2.dd no sistema ==="
find / -name "evidence2.dd" 2>/dev/null || true
echo "=== Buscando qualquer arquivo .dd ==="
find /home/revisor -name "*.dd" 2>/dev/null || true
find /pacote -name "*.dd" 2>/dev/null || true
