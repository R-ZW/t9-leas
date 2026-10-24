import os

os.makedirs("/tmp/teste_c2", exist_ok=True)
img_path = "/tmp/teste_c2/c2_script.img"

bash_script = b"#!/bin/bash\n# Production incident response script\necho \"Running IR triage on Linux\"\nuname -a\nexit 0\n"
python_script = b"#!/usr/bin/env python3\n# Python malware analyzer\nimport hashlib\nprint(\"Analyzing SHA256 checksums\")\n"
pwsh_script = b"#!/usr/bin/env pwsh\n# PowerShell IR script\nWrite-Output \"PowerShell Core Execution\"\n"
dummy_comment_script = b"#!/bin/sh\n# Only comments\n# Another comment\n"

with open(img_path, "wb") as f:
    f.write(b"\x00" * 512)
    f.write(bash_script)
    f.write(b"\x00" * 1024)
    f.write(python_script)
    f.write(b"\x00" * 1024)
    f.write(pwsh_script)
    f.write(b"\x00" * 1024)
    f.write(dummy_comment_script) # Should be discarded by foremost-ng
    f.write(b"\x00" * 512)

print(f"Created {img_path} with size {os.path.getsize(img_path)} bytes")
