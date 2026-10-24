#!/bin/bash
set -e
exec > /home/revisor/evidencias/elf_target_info.txt 2>&1
cd /home/revisor/testes

echo 'int main(int argc, char** argv) { return 42; }' | gcc -x c - -O2 -o elf_target
ls -lh elf_target
file elf_target
readelf -h elf_target
readelf -l elf_target

python3 -c '
with open("elf_target", "rb") as f:
    elf_data = f.read()

with open("elf_sample.raw", "wb") as f:
    f.write(b"\xCC" * 8192) # padding 8192 bytes
    f.write(elf_data)
    f.write(b"\xDD" * 8192)
'
ls -lh elf_sample.raw
sha256sum elf_sample.raw
