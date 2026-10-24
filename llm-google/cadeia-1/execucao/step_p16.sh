#!/bin/bash
set -e
exec > /home/revisor/evidencias/audit_c4_elf.txt 2>&1
cd /home/revisor/testes
rm -rf output_elf
foremost-ng -t elf -i elf_sample.raw -o output_elf
ls -laR output_elf
cat output_elf/audit.txt
for f in output_elf/elf/*; do
    echo "=== Executando file em $f ==="
    file "$f"
    echo "=== Executando readelf -h em $f ==="
    readelf -h "$f"
    echo "=== Executando readelf -l em $f ==="
    readelf -l "$f"
    echo "=== Execucao direta do ELF extraido ==="
    chmod +x "$f"
    "$f" || echo "Exit code: $?"
done
