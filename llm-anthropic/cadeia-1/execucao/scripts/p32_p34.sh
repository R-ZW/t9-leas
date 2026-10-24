set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval/img
# P32
run P32 bash -c 'truncate -s 80M disk.img; for p in "amostra.evtx 2048" "hello32 131072" "hello64 135168" "s_bash.sh 139264" "m_fat.o 143360" "m_x86_64.o 147456"; do set -- $p; dd if=../dados/$1 of=disk.img bs=512 seek=$2 conv=notrunc status=none; done; sha256sum disk.img'
# P33
cd ~/aval
run P33 foremost-ng -v -i ~/aval/img/disk.img -o ~/aval/out/P33
run P33 bash -c 'find out/P33 -type f | sort; grep -E "^ +[0-9]+:|FILES|=" out/P33/audit.txt'
# P34 (sintaxe do artigo p.7)
run P34 foremost-ng -t evtx,elf,exe -i ~/aval/img/disk.img -o ~/aval/out/P34
run P34 bash -c 'find out/P34 -type f | sort; ls out/P34; grep -E "^ +[0-9]+:|FILES|=" out/P34/audit.txt'
