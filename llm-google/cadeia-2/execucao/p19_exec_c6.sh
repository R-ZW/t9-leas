#!/bin/bash
echo "=== P19: Tentativa de execucao do experimento da Figura 2 (foremost-ng -v -x evidence2.dd) ===" > /home/revisor/evidencias/19_exec_c6_fig2.log
if [ -f "/home/revisor/evidence2.dd" ]; then
    cd /home/revisor
    foremost-ng -v -x evidence2.dd 2>&1 | tee -a /home/revisor/evidencias/19_exec_c6_fig2.log
    cp output/audit.txt /home/revisor/evidencias/19_audit_fig2.txt 2>/dev/null || true
else
    cd /home/revisor
    foremost-ng -v -x evidence2.dd 2>&1 | tee -a /home/revisor/evidencias/19_exec_c6_fig2.log
    echo "STATUS: BLOQUEADO / FALHA - O arquivo evidence2.dd nao existe no diretorio ou sistema." >> /home/revisor/evidencias/19_exec_c6_fig2.log
fi
cat /home/revisor/evidencias/19_exec_c6_fig2.log
