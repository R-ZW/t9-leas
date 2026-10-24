import urllib.request,hashlib
from pathlib import Path
url="https://secure.eicar.org/eicar_com.zip"
path=Path("/tmp/foremost-ng/src/testdata/eicar_com.zip")
try:
    with urllib.request.urlopen(url,timeout=20) as r:
        data=r.read()
        status=r.status
    path.write_bytes(data)
    print("URL",url)
    print("HTTP",status)
    print("BYTES",len(data))
    print("SHA256",hashlib.sha256(data).hexdigest())
except Exception as e:
    print("URL",url)
    print("ERROR",type(e).__name__,str(e)[:200])
