import hashlib,json,os,urllib.request,urllib.error
root="/tmp/foremost-ng/src/carved-files/elf"
for name in ("00006144.elf","00006400.elf"):
    data=open(root+"/"+name,"rb").read()
    digest=hashlib.sha256(data).hexdigest()
    req=urllib.request.Request("https://www.virustotal.com/api/v3/files/"+digest,headers={"x-apikey":os.environ["VT_API_KEY"],"Accept":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=20) as resp:
            body=json.load(resp)
            stats=body.get("data",{}).get("attributes",{}).get("last_analysis_stats")
            print(name,digest,"HTTP",resp.status,"stats",stats)
    except urllib.error.HTTPError as e:
        print(name,digest,"HTTP",e.code)
    except Exception as e:
        print(name,digest,type(e).__name__,str(e)[:160])
