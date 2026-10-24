#!/bin/bash
set -e
exec > /home/revisor/evidencias/audit_c2_script.txt 2>&1
cd /home/revisor/testes
rm -rf output_script
foremost-ng -t script -i script_sample.raw -o output_script
ls -laR output_script
cat output_script/audit.txt
for f in output_script/script/*; do
    echo "=== Conteudo de $f ==="
    cat "$f"
    echo ""
    file "$f"
done
