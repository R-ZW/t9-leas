#!/bin/bash
echo "=== P18: Busca de evidence2.dd no sistema de arquivos do container ===" > /home/revisor/evidencias/18_find_evidence2.log
FOUND=$(find / -name "evidence2.dd" 2>/dev/null)
if [ -n "$FOUND" ]; then
    echo "Arquivo localizado em: $FOUND" >> /home/revisor/evidencias/18_find_evidence2.log
    ls -lh "$FOUND" >> /home/revisor/evidencias/18_find_evidence2.log
else
    echo "FATO OBSERVADO: Arquivo evidence2.dd NAO ENCONTRADO no sistema de arquivos." >> /home/revisor/evidencias/18_find_evidence2.log
fi
cat /home/revisor/evidencias/18_find_evidence2.log
