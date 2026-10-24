from pathlib import Path
import struct
base = Path("/home/revisor/artefato-extraido/foremost-ng-bb812a22/src")
out = Path("/home/revisor/evidencias")
segname = b"__TEXT" + bytes(10)
thin32_header = struct.pack("<IIIIIII", 0xFEEDFACE, 7, 3, 2, 1, 56, 0)
thin32_segment = struct.pack("<II16sIIIIIIII", 1, 56, segname, 0, 16, 84, 16, 5, 5, 0, 0)
thin32 = thin32_header + thin32_segment + bytes([0x90]) * 16
thin64_header = struct.pack("<IIIIIIII", 0xFEEDFACF, 0x01000007, 3, 2, 1, 72, 0, 0)
thin64_segment = struct.pack("<II16sQQQQIIII", 0x19, 72, segname, 0, 16, 104, 16, 5, 5, 0, 0)
thin64 = thin64_header + thin64_segment + bytes([0x90]) * 16
fat_header = struct.pack(">II", 0xCAFEBABE, 1)
fat_arch = struct.pack(">IIIII", 7, 3, 28, len(thin32), 0)
fat = fat_header + fat_arch + thin32
for name, data in [("macho-fat.dd", fat), ("macho-thin32.dd", thin32), ("macho-thin64.dd", thin64)]:
    (base / name).write_bytes(data)
    (out / name).write_bytes(data)
    print(name, len(data))
