import os

os.makedirs("/tmp/teste_c4", exist_ok=True)
img_path = "/tmp/teste_c4/c4_elf.img"

with open("/bin/true", "rb") as f:
    elf_data = f.read()

with open(img_path, "wb") as f:
    f.write(b"\x00" * 1024)
    f.write(elf_data)
    f.write(b"\x00" * 1024)

print(f"Created {img_path} with size {os.path.getsize(img_path)} bytes (ELF size: {len(elf_data)})")
