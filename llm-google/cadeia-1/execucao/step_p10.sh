#!/bin/bash
set -e
exec > /home/revisor/evidencias/audit_c1_evtx.txt 2>&1
cd /home/revisor/testes
rm -rf output_evtx
foremost-ng -t evtx -i evtx_sample.raw -o output_evtx
ls -laR output_evtx
cat output_evtx/audit.txt
file output_evtx/evtx/* || true
ls -lh output_evtx/evtx/
