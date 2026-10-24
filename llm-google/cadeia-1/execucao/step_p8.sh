#!/bin/bash
set -e
exec > /home/revisor/evidencias/audit_f.txt 2>&1
cd /home/revisor/testes
rm -rf output_f
foremost-ng -i test_minimo.img -o output_f
ls -laR output_f
cat output_f/audit.txt
file output_f/png/* || true
