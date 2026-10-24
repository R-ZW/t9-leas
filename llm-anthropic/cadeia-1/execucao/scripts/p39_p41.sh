set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval
# P39: hashes e conferencia independente na API do VT (consulta por hash; a chave nao e impressa)
run P39 bash -c 'sha256sum out/P38/zip/* out/P38/elf/* dados/eicar_com.zip; cmp out/P38/zip/00002048.zip dados/eicar_com.zip && echo ZIP_IDENTICO; grep -E "^ +[0-9]+:" out/P38/audit.txt'
sleep 65
cat > ~/aval/dados/vt_stats.py <<'EOF'
import json, sys
d = json.load(sys.stdin)
if "error" in d:
    print("erro_api:", d["error"].get("code"))
else:
    a = d["data"]["attributes"]
    print("sha256:", a.get("sha256"))
    print("last_analysis_stats:", json.dumps(a.get("last_analysis_stats"), sort_keys=True))
EOF
for h in $(sha256sum out/P38/zip/00002048.zip out/P38/elf/00006144.elf | cut -d" " -f1); do
  run P39 bash -c "curl -s -H \"x-apikey: \$VT_API_KEY\" -H 'Accept: application/json' https://www.virustotal.com/api/v3/files/$h | ~/aval/venv/bin/python ~/aval/dados/vt_stats.py"
done
# P40: sem chave
run P40 env -u VT_API_KEY foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P40
run P40 bash -c 'sha256sum out/P40/zip/* out/P40/elf/*; grep -E "^ +[0-9]+:" out/P40/audit.txt'
sleep 65
# P41: chave invalida
run P41 env VT_API_KEY=CHAVE_INVALIDA_TESTE foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P41
run P41 bash -c 'sha256sum out/P41/zip/* out/P41/elf/*; grep -E "^ +[0-9]+:" out/P41/audit.txt'
