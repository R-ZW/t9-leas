#!/bin/bash
set -e
exec > /home/revisor/evidencias/test_minimo_created.txt 2>&1
mkdir -p /home/revisor/testes
cd /home/revisor/testes

python3 -c '
# Imagem sintética com padding e um PNG válido embutido
png_data = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"
    b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)
with open("test_minimo.img", "wb") as f:
    f.write(b"\x00" * 1024 * 1024) # 1 MB padding
    f.write(png_data)
    f.write(b"\x00" * 1024 * 512)  # 512 KB padding
'
ls -lh test_minimo.img
sha256sum test_minimo.img
