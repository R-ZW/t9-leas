import hashlib,json,os,urllib.request,urllib.error
path="/tmp/foremost-ng/src/carved-eicar/zip/00000008.zip"
digest=hashlib.sha256(open(path,"rb").read()).hexdigest()
req=urllib.request.Request("https://www.virustotal.com/api/v3/files/"+digest,headers={"x-apikey":os.environ["VT_API_KEY"],"Accept":"application/json"})
try:
    with urllib.request.urlopen(req,timeout=20) as resp:
        body=json.load(resp)
        print("HASH",digest,"HTTP",resp.status,"STATS",body.get("data",{}).get("attributes",{}).get("last_analysis_stats"))
except urllib.error.HTTPError as e:
    print("HASH",digest,"HTTP",e.code)
