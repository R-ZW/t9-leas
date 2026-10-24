#!/bin/bash
mkdir -p /tmp/teste_c5
cd /tmp/teste_c5
foremost-ng -v -x -t elf -i /tmp/teste_c4/c4_elf.img -o /tmp/teste_c5/output_c5 2>&1 | tee /home/revisor/evidencias/17_exec_c5.log
cat /tmp/teste_c5/output_c5/audit.txt >> /home/revisor/evidencias/17_exec_c5.log
cp /tmp/teste_c5/output_c5/audit.txt /home/revisor/evidencias/17_audit_c5.txt
echo "EXIT_CODE: $?" >> /home/revisor/evidencias/17_exec_c5.log
