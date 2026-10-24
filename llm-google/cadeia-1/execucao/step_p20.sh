#!/bin/bash
exec > /home/revisor/evidencias/figura2_reproduction.txt 2>&1
cd /home/revisor/foremost-ng/foremost-ng-bb812a22/src
echo "=== Tentativa de execucao do comando da Figura 2 ==="
echo "Comando: ./foremost-ng -v -x evidence2.dd"
if [ -f evidence2.dd ]; then
    ./foremost-ng -v -x evidence2.dd
else
    ./foremost-ng -v -x evidence2.dd || true
    echo "FALHA Factual: O arquivo evidence2.dd nao existe no diretorio ou artefato, inviabilizando a reproducao da Figura 2."
fi
