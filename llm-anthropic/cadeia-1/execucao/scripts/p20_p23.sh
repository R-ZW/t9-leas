set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval/dados
# P20
printf '#!/bin/bash\n# backup\nfor f in /etc/hostname /etc/os-release; do\n  cp "$f" /tmp/ && echo "copiado $f"\ndone\n' > s_bash.sh
printf '#!/usr/bin/env python3\nimport os\nfor k in sorted(os.environ):\n    print(k)\n' > s_py.py
printf '#!/usr/bin/env pwsh\nGet-ChildItem -Path . | ForEach-Object { Write-Output $_.Name }\n' > s_ps.ps1
printf '#!/bin/sh\n# apenas comentario linha 1\n# apenas comentario linha 2\n' > neg_coment.sh
printf '#!/bin/sh\necho oi\n' > neg_curto.sh
run P20 bash -c 'wc -c s_bash.sh s_py.py s_ps.ps1 neg_coment.sh neg_curto.sh; sha256sum s_* neg_*'
# P21
cd ~/aval/img
run P21 bash -c 'truncate -s 16M img_c2.img; for p in "s_bash.sh 2048" "s_py.py 4096" "s_ps.ps1 6144" "neg_coment.sh 8192" "neg_curto.sh 10240"; do set -- $p; dd if=../dados/$1 of=img_c2.img bs=512 seek=$2 conv=notrunc status=none; done; sha256sum img_c2.img'
# P22
cd ~/aval
run P22 foremost-ng -v -t script -i ~/aval/img/img_c2.img -o ~/aval/out/P22
# P23
run P23 bash -c 'cd out/P22/script && ls -l; cmp 00002048.script ~/aval/dados/s_bash.sh && echo OK_BASH; cmp 00004096.script ~/aval/dados/s_py.py && echo OK_PY; cmp 00006144.script ~/aval/dados/s_ps.ps1 && echo OK_PS; ls 00008192* 00010240* 2>&1; head -1 00002048.script 00004096.script 00006144.script'
