#!/bin/bash
# uso: monta.sh IMG TAM_MB arquivo:bloco ...  (bloco de 512 B, ordem crescente)
set -e; img=$1; tam=$2; shift 2; rm -f "$img"; truncate -s ${tam}M "$img"
m="$img.manifesto.tsv"; printf "bloco\toffset\tarquivo\tbytes\tsha256\n" > "$m"; fim=0
for p in "$@"; do f=${p%:*}; b=${p##*:}; s=$(stat -c%s "$f")
  [ $((b*512)) -ge $fim ] || { echo "SOBREPOSICAO em $f"; exit 1; }
  dd if="$f" of="$img" bs=512 seek="$b" conv=notrunc status=none; fim=$((b*512+s))
  printf "%s\t%s\t%s\t%s\t%s\n" "$b" $((b*512)) "$f" "$s" "$(sha256sum "$f"|cut -d' ' -f1)" >> "$m"
done; sha256sum "$img" >> "$m"
