#!/bin/bash
set -e
exec > /home/revisor/evidencias/macho_sample_spec.txt 2>&1
cd /home/revisor/testes

python3 -c '
import struct

# 1. Mach-O thin 64-bit LE (magic 0xCFFAEDFE)
# Header: magic (4), cputype (4), cpusubtype (4), filetype (4), ncmds (4), sizeofcmds (4), flags (4), reserved (4) = 32 bytes
# Load command LC_SEGMENT_64 (0x19): cmd (4), cmdsize (4), segname (16), vmaddr (8), vmsize (8), fileoff (8), filesize (8), maxprot (4), initprot (4), nsects (4), flags (4) = 72 bytes
# Let fileoff = 0, filesize = 2048 bytes
magic_thin64 = struct.pack("<I", 0xCFFAEDFE)
hdr_thin64 = magic_thin64 + struct.pack("<IIIIIII", 0x01000007, 3, 2, 1, 72, 0, 0)
lc_seg64 = struct.pack("<II16sQQQQIIII", 0x19, 72, b"__TEXT\x00"*2, 0x1000, 2048, 0, 2048, 7, 7, 0, 0)
macho64_blob = hdr_thin64 + lc_seg64 + b"\x90" * (2048 - len(hdr_thin64) - len(lc_seg64))

# 2. Mach-O Fat Universal (magic 0xCAFEBABE, Big Endian)
# Header: magic(4), nfat_arch(4)
# fat_arch: cputype(4), cpusubtype(4), offset(4), size(4), align(4) = 20 bytes
# arch1: offset 4096, size 1024 -> max_end = 5120 bytes
magic_fat = struct.pack(">II", 0xCAFEBABE, 1)
arch1 = struct.pack(">IIIII", 7, 3, 4096, 1024, 12)
fat_blob = bytearray(b"\x00" * 5120)
fat_blob[0:8] = magic_fat
fat_blob[8:28] = arch1
fat_blob[4096:5120] = b"\x7FELF_MOCK_DATA" * 64

with open("macho_sample.raw", "wb") as f:
    f.write(b"\x11" * 2048)  # padding
    f.write(macho64_blob)     # thin 64-bit at offset 2048
    f.write(b"\x22" * 2048)  # padding
    f.write(fat_blob)         # fat universal
    f.write(b"\x33" * 2048)  # padding
'
ls -lh macho_sample.raw
sha256sum macho_sample.raw
