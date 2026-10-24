set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval/dados
# P28
run P28 gcc -m32 -O0 -o hello32 hello.c
run P28 bash -c 'file hello32 hello64; ./hello32; ./hello64; stat -c "%n %s" hello32 hello64; sha256sum hello32 hello64'
# P29
cd ~/aval/img
run P29 bash -c 'truncate -s 16M img_c4.img; dd if=../dados/hello32 of=img_c4.img bs=512 seek=2048 conv=notrunc status=none; dd if=../dados/hello64 of=img_c4.img bs=512 seek=6144 conv=notrunc status=none; sha256sum img_c4.img'
# P30
cd ~/aval
run P30 foremost-ng -v -t elf -i ~/aval/img/img_c4.img -o ~/aval/out/P30
# P31
run P31 bash -c 'cd out/P30/elf && ls -l; file *.elf; readelf -h -l 00002048.elf; readelf -h -l 00006144.elf; cmp -n $(stat -c %s 00002048.elf) 00002048.elf ~/aval/dados/hello32 && echo PREF32_OK; cmp -n $(stat -c %s 00006144.elf) 00006144.elf ~/aval/dados/hello64 && echo PREF64_OK; chmod +x *.elf; ./00002048.elf; ./00006144.elf; readelf -S 00006144.elf 2>&1 | head -5'
