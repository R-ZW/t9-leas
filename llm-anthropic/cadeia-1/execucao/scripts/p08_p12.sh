set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval
# P8
run P8 foremost-ng -h
run P8 foremost-ng -V
run P8 bash -c 'man -P cat foremost-ng | head -150'
# P9
cd ~/aval/dados
cat > hello.c <<'EOF'
#include <stdio.h>
int main(void){ puts("ola foremost-ng"); return 0; }
EOF
run P9 gcc -O0 -o hello64 hello.c
printf '#!/bin/bash\n# script de teste do avaliador\nfor i in 1 2 3; do\n  echo "linha $i"\ndone\n' > teste.sh
run P9 bash -c 'ls -l hello64 teste.sh; sha256sum hello64 teste.sh; ./hello64'
# P10
cd ~/aval/img
run P10 bash -c 'truncate -s 16M img_f.img && dd if=../dados/hello64 of=img_f.img bs=512 seek=2048 conv=notrunc status=none && dd if=../dados/teste.sh of=img_f.img bs=512 seek=6144 conv=notrunc status=none && sha256sum img_f.img'
# P11
cd ~/aval
run P11 foremost-ng -v -i ~/aval/img/img_f.img -o ~/aval/out/P11
# P12
run P12 bash -c 'ls -lR out/P11; cat out/P11/audit.txt; cmp out/P11/script/00006144.script dados/teste.sh && echo SCRIPT_IDENTICO; readelf -h -l out/P11/elf/00002048.elf'
