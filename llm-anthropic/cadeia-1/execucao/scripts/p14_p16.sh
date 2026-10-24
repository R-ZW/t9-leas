set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval/dados
# P14
run P14 git clone --depth 1 https://github.com/williballenthin/python-evtx.git pyevtx-repo
run P14 git -C pyevtx-repo rev-parse HEAD
run P14 bash -c 'find pyevtx-repo -name "*.evtx" -printf "%s %p\n" | sort -n'
run P14 bash -c 'f=$(find pyevtx-repo -name "*.evtx" -size +68k -printf "%s %p\n" | sort -n | head -1 | cut -d" " -f2); echo "escolhido: $f"; cp "$f" amostra.evtx && sha256sum amostra.evtx && stat -c %s amostra.evtx'
# P15
run P15 python3 -m venv ~/aval/venv
run P15 ~/aval/venv/bin/pip install python-evtx
run P15 bash -c '~/aval/venv/bin/pip show python-evtx | head -3'
cat > conta_evtx.py <<'EOF'
import sys, Evtx.Evtx as E
with E.Evtx(sys.argv[1]) as log:
    print("registros", sum(1 for _ in log.records()))
EOF
run P15 ~/aval/venv/bin/python conta_evtx.py amostra.evtx
# P16
run P16 bash -c 'od -A d -c -N 8 amostra.evtx; echo "u64@0x18:"; od -A d -t u8 -j 24 -N 8 amostra.evtx; echo "u16@0x2A:"; od -A d -t u2 -j 42 -N 2 amostra.evtx'
