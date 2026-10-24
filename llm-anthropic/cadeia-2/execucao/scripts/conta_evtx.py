# [FORA DO ROTEIRO] substitui o evtx_dump quebrado do python-evtx 0.8.1
# uso: python conta_evtx.py <arquivo.evtx> ...
# imprime: arquivo, chunks declarados no cabeçalho, registros lidos, registros com XML válido, erro (se houver)
import sys
import Evtx.Evtx as evtx

for path in sys.argv[1:]:
    total = xml_ok = 0
    erro = ""
    try:
        with evtx.Evtx(path) as log:
            fh = log.get_file_header()
            chunks = fh.chunk_count()
            for rec in log.records():
                total += 1
                try:
                    x = rec.xml()
                    if "<Event " in x:
                        xml_ok += 1
                except Exception as e:  # registro individual ilegível
                    erro = "registro: %r" % e
    except Exception as e:
        chunks = "?"
        erro = "arquivo: %r" % e
    print("%s chunks=%s registros=%d xml_ok=%d erro=%s" % (path, chunks, total, xml_ok, erro or "-"))
