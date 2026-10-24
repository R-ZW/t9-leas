from Evtx.Evtx import Evtx
from pathlib import Path
paths=[
Path("/tmp/foremost-ng/src/testdata/issue_38.evtx"),
Path("/temp/output/c1/evtx/00000008.evtx"),
Path("/tmp/foremost-ng/src/testdata/security.evtx"),
Path("/temp/output/c1/evtx/00000256.evtx"),
]
for p in paths:
    try:
        with Evtx(str(p)) as log:
            n=sum(1 for _ in log.records())
        print(p, "bytes",p.stat().st_size,"records",n)
    except Exception as e:
        print(p,"ERROR",type(e).__name__,str(e)[:160])
