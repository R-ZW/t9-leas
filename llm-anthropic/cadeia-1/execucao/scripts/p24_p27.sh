set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval/dados
# P24
printf 'int soma(int a,int b){return a+b;}\nint main(void){return soma(2,3);}\n' > macho.c
run P24 clang -target x86_64-apple-macos11 -c macho.c -o m_x86_64.o
run P24 clang -target arm64-apple-macos11 -c macho.c -o m_arm64.o
run P24 clang -target i386-apple-macos10.12 -c macho.c -o m_i386.o
LIPO=$(ls /usr/lib/llvm-*/bin/llvm-lipo | head -1)
run P24 "$LIPO" -create m_x86_64.o m_arm64.o -output m_fat.o
run P24 bash -c 'file m_*.o; for f in m_*.o; do echo $f; od -A x -t x1 -N 4 $f; done; stat -c "%n %s" m_*.o; sha256sum m_*.o'
# P25
cd ~/aval/img
run P25 bash -c 'truncate -s 16M img_c3.img; for p in "m_x86_64.o 2048" "m_arm64.o 4096" "m_i386.o 6144" "m_fat.o 8192"; do set -- $p; [ -f ../dados/$1 ] && dd if=../dados/$1 of=img_c3.img bs=512 seek=$2 conv=notrunc status=none; done; sha256sum img_c3.img'
# P26
cd ~/aval
run P26 foremost-ng -v -t macho -i ~/aval/img/img_c3.img -o ~/aval/out/P26
# P27
run P27 bash -c 'ls -lR out/P26; cd out/P26/macho 2>/dev/null || { echo "SEM_DIRETORIO_MACHO"; exit 0; }; file *; cmp 00008192.macho ~/aval/dados/m_fat.o && echo FAT_IDENTICO; for b in 00002048 00004096 00006144; do if [ -f $b.macho ]; then /usr/lib/llvm-18/bin/llvm-objdump --macho --private-headers $b.macho | head -20; else echo "AUSENTE $b"; fi; done'
