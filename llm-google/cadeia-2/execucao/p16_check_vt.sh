#!/bin/bash
if [ -n "$VT_API_KEY" ]; then
    echo "VT_API_KEY esta definida e nao-vazia (mascarada: <VT_API_KEY>)" > /home/revisor/evidencias/16_vt_key_status.txt
else
    echo "AVISO: VT_API_KEY nao configurada no ambiente" > /home/revisor/evidencias/16_vt_key_status.txt
fi
cat /home/revisor/evidencias/16_vt_key_status.txt
