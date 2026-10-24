#!/bin/bash
set -e
exec > /home/revisor/evidencias/audit_c3_macho.txt 2>&1
cd /home/revisor/testes
rm -rf output_macho
foremost-ng -t macho -i macho_sample.raw -o output_macho
ls -laR output_macho
cat output_macho/audit.txt
for f in output_macho/macho/*; do
    echo "=== Arquivo $f ==="
    ls -lh "$f"
    file "$f"
done
