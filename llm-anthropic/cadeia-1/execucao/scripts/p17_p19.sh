set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval/img
# P17
run P17 bash -c 'truncate -s 64M img_c1.img && dd if=../dados/amostra.evtx of=img_c1.img bs=512 seek=2048 conv=notrunc status=none && sha256sum img_c1.img'
# P18
cd ~/aval
run P18 foremost-ng -v -t evtx -i ~/aval/img/img_c1.img -o ~/aval/out/P18
# P19
run P19 bash -c 'c=out/P18/evtx/00002048.evtx; ls -l out/P18/evtx; sha256sum $c; stat -c %s $c dados/amostra.evtx; cmp -n $(stat -c %s dados/amostra.evtx) $c dados/amostra.evtx && echo PREFIXO_OK; ~/aval/venv/bin/python dados/conta_evtx.py $c'
