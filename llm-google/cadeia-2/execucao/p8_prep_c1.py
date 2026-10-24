import struct
import os

os.makedirs("/tmp/teste_c1", exist_ok=True)
img_path = "/tmp/teste_c1/c1_evtx.img"

chunk_count = 1
# Header: 4096 bytes
header = bytearray(4096)
header[0:8] = b"ElfFile\x00\x00"
# chunk_count at offset 0x18 (little endian 32-bit int)
struct.pack_into("<I", header, 0x18, chunk_count)

# Chunk: 65536 - 4096 bytes (or if chunk is 65536, file is 4096 header + chunks)
# But Foremost-NG extract_evtx does: full_size = chunk_count * 65536
# So if chunk_count = 1, full_size = 65536 bytes total.
chunk_data = bytearray(65536 - 4096)
chunk_data[0:8] = b"ElfChnk\x00"

evtx_data = header + chunk_data

with open(img_path, "wb") as f:
    f.write(b"\x55" * 512) # prefix padding
    f.write(evtx_data)
    f.write(b"\xAA" * 512) # suffix padding

print(f"Created {img_path} with size {os.path.getsize(img_path)} bytes")
