#!/bin/bash
# uso: mkimg.sh <saida.dd> <arq1> [arq2 ...]
set -euo pipefail; out="$1"; shift; : > "$out"; truncate -s 1M "$out"
echo "offset,bloco512,bytes,sha256,arquivo" > "$out.manifest.csv"
for f in "$@"; do
  off=$(stat -c %s "$out"); cat "$f" >> "$out"
  echo "$off,$((off/512)),$(stat -c %s "$f"),$(sha256sum "$f"|cut -d' ' -f1),$f" >> "$out.manifest.csv"
  sz=$(stat -c %s "$out"); truncate -s $(( (sz/65536 + 2) * 65536 )) "$out"
done
truncate -s +1M "$out"
