#!/bin/bash
set -e
exec > /home/revisor/evidencias/vt_nokey_err.txt 2>&1
cd /home/revisor/testes
rm -rf output_vt_nokey
# Executa sem a chave de API
VT_API_KEY="" foremost-ng -x -t elf -i elf_sample.raw -o output_vt_nokey || true
ls -laR output_vt_nokey
cat output_vt_nokey/audit.txt
