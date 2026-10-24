set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval
# P35 (nao imprime o valor)
run P35 bash -c 'test -n "${VT_API_KEY:-}" && echo "VT_API_KEY_definida (comprimento ${#VT_API_KEY})" || echo VT_API_KEY_ausente'
# P36
cd ~/aval/dados
run P36 curl -fsSL -o eicar_com.zip -w "url=%{url_effective} http=%{http_code} bytes=%{size_download}\n" https://secure.eicar.org/eicar_com.zip
run P36 bash -c 'stat -c "%n %s" eicar_com.zip; sha256sum eicar_com.zip; unzip -l eicar_com.zip'
# P37
cd ~/aval/img
run P37 bash -c 'truncate -s 16M img_c5.img; dd if=../dados/eicar_com.zip of=img_c5.img bs=512 seek=2048 conv=notrunc status=none; dd if=../dados/hello64 of=img_c5.img bs=512 seek=6144 conv=notrunc status=none; sha256sum img_c5.img'
# P38
cd ~/aval
run P38 foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P38
