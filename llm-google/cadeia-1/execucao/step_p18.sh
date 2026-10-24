#!/bin/bash
set -e
exec > /home/revisor/evidencias/audit_c5_vt.txt 2>&1
cd /home/revisor/testes
rm -rf output_vt_key
foremost-ng -x -t elf -i elf_sample.raw -o output_vt_key
ls -laR output_vt_key
cat output_vt_key/audit.txt
