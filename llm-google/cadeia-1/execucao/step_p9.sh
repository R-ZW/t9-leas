#!/bin/bash
set -e
exec > /home/revisor/evidencias/evtx_sample_spec.txt 2>&1
cd /home/revisor/testes

python3 -c '
import struct

# Chunks de 64 KiB (65536 bytes)
# Header EVTX:
# 0x00..0x07: "ElfFile\0"
# 0x18..0x1B: chunk_count = 2 (little endian) -> 128 KiB total
chunk_size = 65536
chunk_count = 2
total_size = chunk_size * chunk_count

evtx_data = bytearray(b"\x00" * total_size)
evtx_data[0:8] = b"ElfFile\x00\x00"
evtx_data[0x18:0x1C] = struct.pack("<I", chunk_count)
# Coloca marcador no final do chunk 1 e chunk 2
evtx_data[65530:65536] = b"CHUNK1"
evtx_data[total_size-6:total_size] = b"CHUNK2"

with open("evtx_sample.raw", "wb") as f:
    f.write(b"\xAA" * 4096)  # padding antes (offset 4096)
    f.write(evtx_data)
    f.write(b"\xBB" * 4096)  # padding depois
'
ls -lh evtx_sample.raw
sha256sum evtx_sample.raw
