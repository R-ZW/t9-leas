#!/usr/bin/env python3
# [FORA DO ROTEIRO / conferencia do revisor] Consulta o VirusTotal (API v3)
# somente por hash. A chave e lida de VT_API_KEY e nunca e impressa.
# Uso: vt_consulta.py HASH [HASH ...]   (pausa de 16 s entre consultas: limite 4/min)
import json, os, sys, time, urllib.request, urllib.error, datetime

key = os.environ.get("VT_API_KEY", "")
if not key:
    print("VT_API_KEY ausente"); sys.exit(2)
for i, h in enumerate(sys.argv[1:]):
    if i:
        time.sleep(16)
    req = urllib.request.Request("https://www.virustotal.com/api/v3/files/" + h,
                                 headers={"x-apikey": key, "Accept": "application/json"})
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        a = d["data"]["attributes"]
        st = a.get("last_analysis_stats", {})
        print("%s\t%s\tHTTP 200\tmalicious=%s\tsuspicious=%s\tundetected=%s\tharmless=%s\tnome=%s" % (
            ts, h, st.get("malicious"), st.get("suspicious"), st.get("undetected"),
            st.get("harmless"), a.get("meaningful_name")))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            code = json.loads(body).get("error", {}).get("code")
        except Exception:
            code = body[:80]
        print("%s\t%s\tHTTP %d\t%s" % (ts, h, e.code, code))
