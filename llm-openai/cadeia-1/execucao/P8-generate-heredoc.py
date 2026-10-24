from pathlib import Path
import hashlib, struct
root=Path("/tmp/foremost-ng/src")
td=root/"testdata"
td.mkdir(exist_ok=True)
image=bytearray(5*1024*1024)
manifest=[]
def add(name,data,offset):
    (td/name).write_bytes(data)
    image[offset:offset+len(data)]=data
    manifest.append((name,offset,len(data),hashlib.sha256(data).hexdigest()))
evtx1=Path("/tmp/python-evtx/tests/data/issue_38.evtx").read_bytes()
evtx2=Path("/tmp/python-evtx/tests/data/security.evtx").read_bytes()
add("issue_38.evtx",evtx1,4096)
add("security.evtx",evtx2,131072)
ident=b"\x7fELF"+bytes([1,1,1])+bytes(9)
eh32=struct.pack("<16sHHIIIIIHHHHHH",ident,2,3,1,0x8048000,52,0,0,52,32,1,40,0,0)
ph32=struct.pack("<IIIIIIII",1,0,0x8048000,0x8048000,128,128,5,4096)
elf32=(eh32+ph32).ljust(128,b"\x00")
add("sample32.elf",elf32,3145728)
add("sample64.elf",Path("/bin/true").read_bytes(),3276800)
bash=b"#!/bin/bash\necho recovered-bash-script\n"
py=b"#!/usr/bin/env python3\nprint(\"recovered-python-script\")\n"
ps=b"#!/usr/bin/env pwsh\nWrite-Output recovered-powershell-script\n"
comment=b"#!/bin/bash\n# only a comment with a long enough line to exceed 32 bytes\n"
add("sample-bash.script",bash,3407872)
add("sample-python.script",py,3416064)
add("sample-powershell.script",ps,3424256)
add("only-comments.script",comment,3432448)
m32header=struct.pack("<IiiIIII",0xfeedface,7,3,2,1,56,0)
m32segment=struct.pack("<II16sIIIIIIII",1,56,b"__TEXT".ljust(16,b"\x00"),0x1000,128,0,128,5,5,0,0)
thin32=(m32header+m32segment).ljust(128,b"\x00")
m64header=struct.pack("<IiiIIIII",0xfeedfacf,0x01000007,3,2,1,72,0,0)
m64segment=struct.pack("<II16sQQQQIIII",0x19,72,b"__TEXT".ljust(16,b"\x00"),0x100000000,160,0,160,5,5,0,0)
thin64=(m64header+m64segment).ljust(160,b"\x00")
fat=struct.pack(">IIiiIII",0xcafebabe,1,7,3,32,128,0)+bytes(4)+thin32
add("thin32.macho",thin32,4194304)
add("thin64.macho",thin64,4202496)
add("fat.macho",fat,4210688)
(root/"disk.img").write_bytes(image)
(root/"memory.dump").write_bytes(image)
with open("/home/revisor/evidencias/P8-input-manifest.txt","w") as f:
    f.write("origin EVTX: https://github.com/williballenthin/python-evtx.git @ c0007441657899c39180de10a2be1a0e43dbeaf9\n")
    f.write("origin ELF64: Ubuntu container /bin/true; others: reviewer-generated with Python\n")
    for name,offset,size,digest in manifest:
        f.write(f"{name}\toffset={offset}\tsize={size}\tsha256={digest}\n")
    for name in ("disk.img","memory.dump"):
        data=(root/name).read_bytes()
        f.write(f"{name}\tsize={len(data)}\tsha256={hashlib.sha256(data).hexdigest()}\n")
print((root/"disk.img").stat().st_size)
for row in manifest: print(*row)
