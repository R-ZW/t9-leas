from pathlib import Path
import hashlib
import json
import os
import urllib.error
import urllib.request
path = Path("/home/revisor/evidencias/P15-C5-recuperado.elf")
digest = hashlib.sha256(path.read_bytes()).hexdigest()
url = "https://www.virustotal.com/api/v3/files/" + digest
request = urllib.request.Request(url, headers={"x-apikey": os.environ["VT_API_KEY"], "Accept": "application/json"})
print("sha256", digest)
try:
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
        print("http_status", response.status)
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        print("malicious", stats.get("malicious"))
        print("undetected", stats.get("undetected"))
except urllib.error.HTTPError as error:
    print("http_status", error.code)
except urllib.error.URLError as error:
    print("url_error", type(error.reason).__name__)
