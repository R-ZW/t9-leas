#!/bin/bash
set -e
exec > /home/revisor/evidencias/script_sample_spec.txt 2>&1
cd /home/revisor/testes

python3 -c '
s1 = b"#!/bin/bash\n# Script de teste forense\necho \"Executando rotina forense Bash\"\nexit 0\n\x00"
s2 = b"#!/usr/bin/env python3\n# Test script\nimport sys\nprint(\"Executando rotina forense Python\")\n\x00"
# Script inválido (só comentários):
s_invalid = b"#!/bin/sh\n# Apenas comentario\n# Outro comentario\n\x00"

with open("script_sample.raw", "wb") as f:
    f.write(b"\x90" * 1024)
    f.write(s1)
    f.write(b"\x90" * 1024)
    f.write(s_invalid)
    f.write(b"\x90" * 1024)
    f.write(s2)
    f.write(b"\x90" * 1024)
'
ls -lh script_sample.raw
sha256sum script_sample.raw
