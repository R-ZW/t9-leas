#!/usr/bin/env python3
# [FORA DO ROTEIRO] Validador EVTX usando a API do python-evtx 0.8.1
# (o script de console evtx_dump instalado pelo pip falha com
#  "ModuleNotFoundError: No module named 'scripts'").
# Uso: valida_evtx.py ARQUIVO.evtx
# Saida: campos do cabecalho, numero de chunks lidos, numero de registros
# renderizados em XML e numero de erros de renderizacao.
import sys
import Evtx.Evtx as evtx

path = sys.argv[1]
erros = 0
regs = 0
with evtx.Evtx(path) as log:
    fh = log.get_file_header()
    print("magic_ok=%s" % fh.check_magic())
    print("header_chunk_count=%d" % fh.chunk_count())
    print("header_next_record_number=%d" % fh.next_record_number())
    print("header_verify=%s" % fh.verify())
    chunks = 0
    for ch in fh.chunks():
        chunks += 1
    print("chunks_iterados=%d" % chunks)
    for rec in log.records():
        try:
            x = rec.xml()
            if "<Event " in x:
                regs += 1
        except Exception as e:  # registra e segue
            erros += 1
            if erros <= 3:
                print("erro_registro: %r" % (e,))
print("registros_xml=%d" % regs)
print("erros_render=%d" % erros)
