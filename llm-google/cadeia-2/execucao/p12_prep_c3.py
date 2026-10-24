import struct
import os

os.makedirs("/tmp/teste_c3", exist_ok=True)
img_path = "/tmp/teste_c3/c3_macho.img"

# 1. Thin Mach-O 64-bit LE
# magic: 0xfeedfacf -> in LE: 0xcf, 0xfa, 0xed, 0xfe
# Header is 32 bytes:
# magic(4), cputype(4), cpusubtype(4), filetype(4), ncmds(4), sizeofcmds(4), flags(4), reserved(4)
thin_magic = struct.pack("<I", 0xfeedfacf)
thin_hdr = thin_magic + struct.pack("<IIIIIII", 0x01000007, 3, 2, 1, 72, 0, 0)
# LC_SEGMENT_64: cmd=0x19 (4), cmdsize=72 (4), segname 16s, vmaddr (8), vmsize (8), fileoff (8), filesize (8), maxprot (4), initprot (4), nsects (4), flags (4)
# fileoff = 0, filesize = 4096
thin_lc = struct.pack("<II16sQQQQIIII", 0x19, 72, b"__TEXT\x00", 0, 4096, 0, 4096, 7, 5, 0, 0)
thin_payload = b"\x90" * (4096 - len(thin_hdr) - len(thin_lc))
thin_macho = thin_hdr + thin_lc + thin_payload

# 2. FAT Mach-O (universal)
# magic: 0xcafebabe (Big Endian)
# nfat_arch = 1 (Big Endian)
# fat_arch entry (20 bytes, all Big Endian):
# cputype (4), cpusubtype (4), offset (4), size (4), align (4)
fat_magic = struct.pack(">I", 0xcafebabe)
fat_hdr = fat_magic + struct.pack(">I", 1)
# arch offset = 4096, arch size = 4096 -> total end = 8192
fat_arch = struct.pack(">IIIII", 0x01000007, 3, 4096, 4096, 12)
fat_data = bytearray(8192)
fat_data[0:len(fat_hdr)] = fat_hdr
fat_data[len(fat_hdr):len(fat_hdr)+len(fat_arch)] = fat_arch
# put a thin macho inside the fat slice at 4096
fat_data[4096:4096+len(thin_macho)] = thin_macho

with open(img_path, "wb") as f:
    f.write(b"\x00" * 512)
    f.write(thin_macho)
    f.write(b"\x00" * 1024)
    f.write(fat_data)
    f.write(b"\x00" * 512)

print(f"Created {img_path} with size {os.path.getsize(img_path)} bytes")
