import os, sys, urllib.request, json
key = os.environ.get("VT_API_KEY", "")
if not key:
    print("VT_API_KEY is not set!")
    exit(1)
hash_val = sys.argv[1] if len(sys.argv) > 1 else "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"
url = f"https://www.virustotal.com/api/v3/files/{hash_val}"
req = urllib.request.Request(url, headers={"x-apikey": key, "Accept": "application/json"})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats")
        print("HTTP Status:", resp.status)
        print("last_analysis_stats:", json.dumps(stats))
except Exception as e:
    print("Error:", e)
