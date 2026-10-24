import os

os.makedirs("/tmp/teste_f", exist_ok=True)
img_path = "/tmp/teste_f/test_f.img"

png_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa74e\xdf\x00\x00\x00\x00IEND\xaeB`\x82"
script_data = b"#!/bin/bash\n# Minimal functional test\necho \"Foremost-NG is functional\"\nexit 0\n"

with open(img_path, "wb") as f:
    f.write(b"\x00" * 1024)
    f.write(script_data)
    f.write(b"\x00" * 2048)
    f.write(png_data)
    f.write(b"\x00" * 1024)

print(f"Created {img_path} with size {os.path.getsize(img_path)} bytes")
