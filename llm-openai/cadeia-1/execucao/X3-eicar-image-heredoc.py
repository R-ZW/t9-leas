from pathlib import Path
import hashlib
root=Path("/tmp/foremost-ng/src")
data=(root/"testdata/eicar_com.zip").read_bytes()
image=bytearray(1024*1024)
image[4096:4096+len(data)]=data
path=root/"eicar.img"
path.write_bytes(image)
print("INPUT_BYTES",len(data),"OFFSET",4096)
print("IMAGE_BYTES",len(image),"IMAGE_SHA256",hashlib.sha256(image).hexdigest())
