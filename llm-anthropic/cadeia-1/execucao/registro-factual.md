# Registro factual da execução – Foremost-NG (commit bb812a22cb06ef87b5a2d877dfb6f40eb12d460d)

Data da execução: 24/10/2026, das 15:47 às 16:00 UTC, no contêiner Docker `t9-claude-c1`, usuário `revisor`.
Este documento só registra fatos observados. Não há juízo sobre os selos F e R.

## Onde estão as evidências

Todos os caminhos são relativos a esta pasta, `execucao/`, que corresponde a `/home/revisor/evidencias` no contêiner.

- `scripts/`: scripts executados. `run.sh` é a função de registro. Os blocos `pXX_pYY.sh` foram copiados como estão; o `sed -i "s/\r$//"` aplicado antes de cada execução só converte o fim de linha.
- `logs/Pn.log`: saída completa, data e código de saída (`exit=`) de cada comando.
- `saidas/audit_Pn.txt`: audit.txt gerado pelo artefato em cada execução.
- `saidas/sha256_manifesto.txt`: SHA-256 de todos os arquivos de entrada, imagens e saídas.
- Fora desta pasta, de propósito: o pacote completo de saídas (`/home/revisor/aval/evidencias_completas.tgz` no contêiner, 364132 bytes, SHA-256 2317b37449130da25a0c433534fef8a6ceafa2ebf6d36a5387b16683d79683c4). Ele não foi copiado para o host porque contém o arquivo de teste EICAR.
- A chave do VirusTotal não aparece em nenhum arquivo: `grep -rlF "$VT_API_KEY"` sobre `evidencias/` e `aval/out` retornou 0 arquivos. Só foi registrado que ela existe e tem 64 caracteres.

## Ambiente (versões observadas)

| Item | Valor observado | Evidência |
|---|---|---|
| Sistema | Ubuntu 24.04.2 LTS (noble), x86_64 | logs/P2.log |
| Recursos | 16 CPUs, 7,6 GiB de RAM, 2 GiB de swap, 951 GB livres | logs/P2.log |
| gcc | gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0; pacote gcc 4:13.2.0-7ubuntu1 | logs/P4.log |
| make | 4.3-4.1build2 | logs/P4.log |
| libssl-dev | 3.0.13-0ubuntu3.5 | logs/P4.log |
| libcurl4-openssl-dev | 8.5.0-2ubuntu10.6 | logs/P4.log |
| gcc-multilib | 4:13.2.0-7ubuntu1 | logs/P13.log |
| clang / llvm-lipo | Ubuntu clang 18.1.3; /usr/lib/llvm-18/bin/llvm-lipo | logs/P13.log |
| file | 5.45 | logs/P13.log |
| Python / venv | 3.12.3; python-evtx 0.8.1 e hexdump 3.3 (pip) | logs/P13.log, P15.log |
| curl | 8.5.0 (OpenSSL/3.0.13) | logs/P13.log |
| Go (fora do roteiro) | go1.22.2 linux/amd64, pacote golang-go do apt | logs/P27b.log |

### Downloads (URL, tamanho, SHA-256)

| Origem | Arquivo | Bytes | SHA-256 |
|---|---|---|---|
| artefato fornecido: /home/revisor/artefato.zip | artefato.zip | 7252858 | 955c770e29893527f789e11afc28dcc6b83d7af4a64f14b416e39f554b388e0a |
| https://github.com/williballenthin/python-evtx.git (commit c0007441657899c39180de10a2be1a0e43dbeaf9) | tests/data/issue_39.evtx, copiado como amostra.evtx | 1052672 | a687d8b81ff56da980c2389a31539a97dfe985dccfc5a288230cbb1b0a853279 |
| mesmo repositório | tests/data/system.evtx, copiado como amostra2.evtx | 1118208 | ccb83cfefc9038017224cd97b800b66e248fe14529649ddf47907e5a2021449e |
| PyPI | python_evtx-0.8.1-py3-none-any.whl | 26725 | 46336b854dbe0a1e75873ae30db5f583c9d2262ff1d21bdb6b1e624ecfa18ddb |
| PyPI | hexdump-3.3.zip | 12658 | d781a43b0c16ace3f9366aade73e8ad3a7bd5137d58f0b45ab2d3f54876f20db |
| https://secure.eicar.org/eicar_com.zip (HTTP 200) | eicar_com.zip | 184 | 2546dcffc5ad854d4ddc64fbf056871cd5a00f2471cb7a5bfd4ac23b6e9eedad |
| Arquivo Ubuntu (apt) | pacotes acima e suas dependências | – | o próprio apt verifica os hashes; as versões estão em logs/P4.log, P13.log e P27b.log |

### Legenda de desvio

- **D0**: procedimento dos autores, sem alteração.
- **D1**: ajuste de ambiente.
- **D2**: passo ou entrada proposta pelo revisor.
- **D3**: teste externo, com dados de terceiros.

Passos marcados [FORA DO ROTEIRO] não estavam no roteiro e têm justificativa própria.

## Tabela de passos

Na coluna de comando, `run Pn` é a função de registro de `scripts/run.sh`. O diretório de trabalho é `~/aval` (= /home/revisor/aval), salvo indicação.

| Passo | Comando exato | Resultado esperado | Resultado observado (trecho; código de saída) | Evidência | Status | Desvio |
|---|---|---|---|---|---|---|
| P1 | `mkdir -p ~/aval/{dados,img,out}`; criação de `scripts/run.sh` | estrutura criada | criada; logs gravados em evidencias/logs | scripts/run.sh | sucesso | D2 |
| P2 | `run P2 bash -c 'cat /etc/os-release; uname -m; nproc; free -h; df -h $HOME; id'` | Ubuntu 24.04, x86_64, ≥4 GB, ≥10 GB | Ubuntu 24.04.2, x86_64, 16 CPU, 7,6 GiB, 951 GB livres; exit=0 | logs/P2.log | sucesso | D2 |
| P3 | `cp /home/revisor/artefato.zip ~/aval/`; `run P3 sha256sum artefato.zip`; `run P3 unzip -z artefato.zip`; `run P3 unzip -q artefato.zip -d ~/aval/src-art`; `run P3 ls -la ...` | SHA-256 955c770e…; comentário bb812a22… | SHA-256 955c770e29893527…388e0a; comentário bb812a22cb06ef87b5a2d877dfb6f40eb12d460d; src/Makefile presente; exit=0 | logs/P3.log | sucesso | D1 (zip fornecido, no lugar do tarball do README ou do clone do artigo) |
| P4 | `run P4 sudo apt-get update`; `run P4 sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev`; `run P4 bash -c 'gcc --version \| head -1; ...; dpkg-query -W ...'` | pacotes instalados (Dockerfile:3-6) | instalados; versões na seção Ambiente; exit=0 | logs/P4.log | sucesso | D0 (fonte: Dockerfile; executado com sudo, fora do docker build) |
| P5 | (em `src-art/foremost-ng-bb812a22`) `run P5 make` | compilação, conforme artigo p.6 | `make: *** No targets specified and no makefile found.  Stop.`; exit=2 | logs/P5.log | falha | D0 |
| P6 | (em `.../src`) `run P6 make`; `run P6 bash -c 'ls -l foremost-ng && ./foremost-ng -V'` | binário foremost-ng | compilou com 2 avisos (`state.c:95` e `state.c:121`: retorno de realpath ignorado); binário de 87200 bytes; `-V` → `1.5.7`; exit=0 | logs/P6.log | sucesso | D0 |
| P7 | `run P7 sudo make install`; `run P7 bash -c 'command -v foremost-ng; ls -l /usr/local/bin/foremost-ng /usr/share/man/man8/foremost-ng.8.gz /usr/local/etc/foremost.conf'` | binário, man page e configuração instalados | os 3 arquivos presentes; exit=0 | logs/P7.log | sucesso | D0 |
| P8 | `run P8 foremost-ng -h`; `run P8 foremost-ng -V`; `run P8 bash -c 'man -P cat foremost-ng \| head -150'` | ajuda, versão 1.5.7 e manual | ajuda com -t, -i, -o, -x e -v; `1.5.7`; manual exibido; exit=0 nos três | logs/P8.log | sucesso | D0 |
| P8b [FORA DO ROTEIRO: o `head -150` de P8 cortou o manual] | `run P8b bash -c "man -P cat foremost-ng \| sed -n 150,400p; man -P cat foremost-ng \| grep -n -i -E \"evtx\|elf\|macho\|script\|virustotal\|VT_API\""` | – | a seção BUILT-IN FORMATS não cita evtx, elf, macho nem script (grep só encontra linhas de -x/VirusTotal); EXAMPLES traz `foremost-ng -x image.dd`; exit=0 | logs/P8b.log | sucesso | D0 |
| P9 | criação de hello.c e teste.sh (scripts/p08_p12.sh); `run P9 gcc -O0 -o hello64 hello.c`; `run P9 bash -c 'ls -l ...; sha256sum ...; ./hello64'` | arquivos de teste | hello64 com 15960 B (1ebdac47…); teste.sh com 85 B (85955797…); imprime `ola foremost-ng`; exit=0 | logs/P9.log | sucesso | D2 |
| P10 | `run P10 bash -c 'truncate -s 16M img_f.img && dd if=../dados/hello64 of=img_f.img bs=512 seek=2048 conv=notrunc status=none && dd if=../dados/teste.sh of=img_f.img bs=512 seek=6144 conv=notrunc status=none && sha256sum img_f.img'` | imagem criada | 35fb96e2…; exit=0 | logs/P10.log | sucesso | D2 |
| P11 | `run P11 foremost-ng -v -i ~/aval/img/img_f.img -o ~/aval/out/P11` | audit.txt e subdiretórios por formato (artigo p.7) | `0: 00002048.elf 12 KB 1048576 N/A`; `1: 00006144.script 85 B 3145728 N/A`; `2 FILES EXTRACTED`; exit=0 | logs/P11.log; saidas/audit_P11.txt | sucesso | D2 (comando do artigo, entrada do revisor) |
| P12 | `run P12 bash -c 'ls -lR out/P11; cat out/P11/audit.txt; cmp out/P11/script/00006144.script dados/teste.sh && echo SCRIPT_IDENTICO; readelf -h -l out/P11/elf/00002048.elf'` | script idêntico; ELF legível | `SCRIPT_IDENTICO`; ELF64 com 12304 B (original 15960); readelf lê o cabeçalho e 13 cabeçalhos de programa; `readelf: Error: Reading 1984 bytes extends past end of file for section headers`; exit=0 | logs/P12.log | sucesso | D2 |
| P13 | `run P13 sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc-multilib clang llvm file python3-venv curl` e verificação de versões | ferramentas instaladas | instaladas; exit=0 | logs/P13.log | sucesso | D1 |
| P14 | `run P14 git clone --depth 1 https://github.com/williballenthin/python-evtx.git pyevtx-repo`; `find ... -name "*.evtx"`; escolha do menor arquivo acima de 68k | amostra .evtx | 6 arquivos .evtx; escolhido issue_39.evtx (1052672 B); exit=0 | logs/P14.log | sucesso | D3 |
| P15 | `run P15 python3 -m venv ~/aval/venv`; `run P15 ~/aval/venv/bin/pip install python-evtx`; `run P15 ~/aval/venv/bin/python conta_evtx.py amostra.evtx` | N > 0 registros | python-evtx 0.8.1; `registros 394`; exit=0 | logs/P15.log | sucesso | D3 |
| P15b [FORA DO ROTEIRO: registrar tamanho e hash dos downloads do pip, como pedido] | `run P15b bash -c "~/aval/venv/bin/pip download --no-deps -d /tmp/pd python-evtx==0.8.1 hexdump==3.3 -q; ..."` | – | tamanhos e hashes na tabela de downloads; exit=0 | logs/P15b.log | sucesso | D3 |
| P16 | `run P16 bash -c 'od -A d -c -N 8 amostra.evtx; od -A d -t u8 -j 24 -N 8 amostra.evtx; od -A d -t u2 -j 42 -N 2 amostra.evtx'` | registro dos campos | assinatura `ElfFile\0`; u64 em 0x18 = 395; u16 em 0x2A = 11; exit=0 | logs/P16.log | sucesso | D2 |
| P17 | `run P17 bash -c 'truncate -s 64M img_c1.img && dd if=../dados/amostra.evtx of=img_c1.img bs=512 seek=2048 conv=notrunc status=none && sha256sum img_c1.img'` | imagem criada | 2257835e…; exit=0 | logs/P17.log | sucesso | D3 |
| P18 | `run P18 foremost-ng -v -t evtx -i ~/aval/img/img_c1.img -o ~/aval/out/P18` | .evtx em evtx/, legível por ferramenta de eventos (artigo p.6) | `0: 00002048.evtx 24 MB 1048576 N/A`; `1 FILES EXTRACTED`; exit=0 | logs/P18.log; saidas/audit_P18.txt | sucesso | D3 |
| P19 | `run P19 bash -c 'c=out/P18/evtx/00002048.evtx; ls -l out/P18/evtx; sha256sum $c; stat -c %s $c dados/amostra.evtx; cmp -n $(stat -c %s dados/amostra.evtx) $c dados/amostra.evtx && echo PREFIXO_OK; ~/aval/venv/bin/python dados/conta_evtx.py $c'` | prefixo idêntico; registros = 394 | extraído com 25886720 B (= 395 × 65536), original 1052672 B; `PREFIXO_OK`; `registros 394`; exit=0 | logs/P19.log | sucesso (parcial pelo critério do roteiro: tamanho diferente do original) | D3 |
| P19b [FORA DO ROTEIRO: a amostra de P14 vem de um relato de bug (issue_39); repetido com um log comum, system.evtx] | amostra2.evtx em img_c1b.img (64 MiB, bloco 2048); `run P19b foremost-ng -t evtx -i ~/aval/img/img_c1b.img -o ~/aval/out/P19b` e a mesma validação | prefixo idêntico; registros iguais | original: 0x18 = 13528, 0x2A = 9, 1601 registros, 1118208 B. Extraído: 66060288 B (do offset 1048576 até o fim da imagem de 64 MiB); `PREFIXO_OK`; `registros 1601`; exit=0 | logs/P19b.log; saidas/audit_P19b.txt | sucesso (parcial: tamanho diferente) | D3 |
| P20 | criação de s_bash.sh, s_py.py, s_ps.ps1, neg_coment.sh e neg_curto.sh (scripts/p20_p23.sh); `run P20 bash -c 'wc -c ...; sha256sum ...'` | positivos ≥32 B; neg_curto <32 B | 106, 75, 84, 66 e 18 B; exit=0 | logs/P20.log | sucesso | D2 |
| P21 | `run P21 bash -c 'truncate -s 16M img_c2.img; for p in "s_bash.sh 2048" "s_py.py 4096" "s_ps.ps1 6144" "neg_coment.sh 8192" "neg_curto.sh 10240"; do set -- $p; dd if=../dados/$1 of=img_c2.img bs=512 seek=$2 conv=notrunc status=none; done; sha256sum img_c2.img'` | imagem criada | 9a1a7ce8…; exit=0 | logs/P21.log | sucesso | D2 |
| P22 | `run P22 foremost-ng -v -t script -i ~/aval/img/img_c2.img -o ~/aval/out/P22` | scripts válidos extraídos; curtos (<32 B) e só com comentários ignorados (artigo p.6) | 4 arquivos: 00002048, 00004096, 00006144 e 00008192.script (66 B, offset 4194304); `4 FILES EXTRACTED`; exit=0 | logs/P22.log; saidas/audit_P22.txt | sucesso (execução) | D2 |
| P23 | `run P23 bash -c 'cd out/P22/script && ls -l; cmp 00002048.script ~/aval/dados/s_bash.sh && echo OK_BASH; cmp ... && echo OK_PY; cmp ... && echo OK_PS; ls 00008192* 00010240* 2>&1; head -1 ...'` | 3 positivos idênticos; 2 negativos ausentes | `OK_BASH`, `OK_PY`, `OK_PS`; o negativo só com comentários (00008192.script) foi extraído; neg_curto ausente; exit=0 | logs/P23.log | falha (o critério "nenhum negativo extraído" não foi atendido) | D2 |
| P24 | `run P24 clang -target x86_64-apple-macos11 -c macho.c -o m_x86_64.o`; idem para arm64 e i386-apple-macos10.12; `run P24 /usr/lib/llvm-18/bin/llvm-lipo -create m_x86_64.o m_arm64.o -output m_fat.o`; `file`, `od` e `sha256sum` | objetos Mach-O thin e fat | `file`: Mach-O 64-bit x86_64 object; arm64 object; i386 object; universal binary com 2 arquiteturas. Magics cf fa ed fe / ce fa ed fe / ca fe ba be; exit=0 | logs/P24.log | sucesso | D2 |
| P25 | `run P25 bash -c 'truncate -s 16M img_c3.img; for p in "m_x86_64.o 2048" "m_arm64.o 4096" "m_i386.o 6144" "m_fat.o 8192"; do ...; done; sha256sum img_c3.img'` | imagem criada | c53823ff…; exit=0 | logs/P25.log | sucesso | D2 |
| P26 | `run P26 foremost-ng -v -t macho -i ~/aval/img/img_c3.img -o ~/aval/out/P26` | Mach-O fat e thin extraídos (artigo p.6) | só `0: 00008192.macho 16 KB 4194304 N/A`; `1 FILES EXTRACTED`; exit=0 | logs/P26.log; saidas/audit_P26.txt | sucesso (execução) | D2 |
| P27 | `run P27 bash -c 'ls -lR out/P26; cd out/P26/macho ...; file *; cmp 00008192.macho ~/aval/dados/m_fat.o && echo FAT_IDENTICO; for b in 00002048 00004096 00006144; do ... || echo "AUSENTE $b"; done'` | fat idêntico; cada thin extraído e reconhecido | `FAT_IDENTICO`; `AUSENTE 00002048`, `AUSENTE 00004096`, `AUSENTE 00006144`; exit=0 | logs/P27.log | falha (nenhum thin extraído) | D2 |
| P27b [FORA DO ROTEIRO: verificar se o resultado thin de P27 se repete com executáveis Mach-O ligados, não só objetos] | `run P27b sudo ... apt-get install -y golang-go`; `GOOS=darwin GOARCH=amd64 go build ...` e `GOARCH=arm64`; imagem img_c3b.img (32 MiB, blocos 2048 e 16384); `run P27b foremost-ng -t macho -i ~/aval/img/img_c3b.img -o ~/aval/out/P27b` | executáveis thin extraídos | `file`: Mach-O 64-bit x86_64 executable (2026240 B) e arm64 executable (2029586 B); foremost-ng: `0 FILES EXTRACTED`; exit=0 | logs/P27b.log; saidas/audit_P27b.txt | falha | D1 (instalação do Go) + D2 |
| P28 | `run P28 gcc -m32 -O0 -o hello32 hello.c`; `run P28 bash -c 'file hello32 hello64; ./hello32; ./hello64; ...'` | ELF32 e ELF64 | ELF 32-bit LSB pie (14940 B) e ELF 64-bit LSB pie (15960 B); ambos imprimem `ola foremost-ng`; exit=0 | logs/P28.log | sucesso | D2 |
| P29 | `run P29 bash -c 'truncate -s 16M img_c4.img; dd ... hello32 ... seek=2048 ...; dd ... hello64 ... seek=6144 ...; sha256sum img_c4.img'` | imagem criada | d233f63f…; exit=0 | logs/P29.log | sucesso | D2 |
| P30 | `run P30 foremost-ng -v -t elf -i ~/aval/img/img_c4.img -o ~/aval/out/P30` | união dos segmentos carregáveis (artigo p.6) | `0: 00002048.elf 12 KB 1048576`; `1: 00006144.elf 12 KB 3145728`; `2 FILES EXTRACTED`; exit=0 | logs/P30.log; saidas/audit_P30.txt | sucesso | D2 |
| P31 | `run P31 bash -c 'cd out/P30/elf && ls -l; file *.elf; readelf -h -l 00002048.elf; readelf -h -l 00006144.elf; cmp -n ... && echo PREF32_OK; cmp -n ... && echo PREF64_OK; chmod +x *.elf; ./00002048.elf; ./00006144.elf; readelf -S 00006144.elf 2>&1 \| head -5'` | readelf lê cabeçalho e segmentos; prefixos idênticos; executam | extraídos com 12296 B (ELF32) e 12304 B (ELF64); `file`: `missing section headers at 14900` / `at 15896`; readelf lê o cabeçalho e os segmentos (Class ELF32 / ELF64); `readelf: Error: Reading 1160 bytes extends past end of file for section headers` (e 1984 bytes no 64-bit); `PREF32_OK`, `PREF64_OK`; os dois imprimem `ola foremost-ng`; exit=0 | logs/P31.log | sucesso | D2 |
| P32 | `run P32 bash -c 'truncate -s 80M disk.img; for p in "amostra.evtx 2048" "hello32 131072" "hello64 135168" "s_bash.sh 139264" "m_fat.o 143360" "m_x86_64.o 147456"; do ...; done; sha256sum disk.img'` | imagem criada | b6dc9b25…; exit=0 | logs/P32.log | sucesso | D3 |
| P33 | `run P33 foremost-ng -v -i ~/aval/img/disk.img -o ~/aval/out/P33` e listagem | todos os parsers; um subdiretório por formato (p.7) | elf/00131072.elf, elf/00135168.elf, evtx/00002048.evtx (24 MB), macho/00143360.macho, script/00139264.script; nenhuma saída para m_x86_64.o (bloco 147456); `5 FILES EXTRACTED`; exit=0 | logs/P33.log; saidas/audit_P33.txt | sucesso | D3 |
| P34 | `run P34 foremost-ng -t evtx,elf,exe -i ~/aval/img/disk.img -o ~/aval/out/P34` e listagem | só os módulos EVTX, ELF e EXE (p.7) | diretórios evtx/ e elf/ apenas; evtx/00002048.evtx, elf/00131072.elf e elf/00135168.elf; `3 FILES EXTRACTED`; exit=0 | logs/P34.log; saidas/audit_P34.txt | sucesso | D3 |
| P35 | `run P35 bash -c 'test -n "${VT_API_KEY:-}" && echo "VT_API_KEY_definida (comprimento ${#VT_API_KEY})" \|\| echo VT_API_KEY_ausente'` | chave definida | `VT_API_KEY_definida (comprimento 64)`; exit=0 | logs/P35.log | sucesso | D0 (README:97-101; chave fornecida pelo ambiente) |
| P36 | `run P36 curl -fsSL -o eicar_com.zip -w "url=%{url_effective} http=%{http_code} bytes=%{size_download}\n" https://secure.eicar.org/eicar_com.zip`; `stat`, `sha256sum` e `unzip -l` | arquivo obtido | http=200, 184 B, 2546dcff…; contém eicar.com (68 B); exit=0 | logs/P36.log | sucesso | D3 |
| P37 | `run P37 bash -c 'truncate -s 16M img_c5.img; dd ... eicar_com.zip ... seek=2048 ...; dd ... hello64 ... seek=6144 ...; sha256sum img_c5.img'` | imagem criada | 48043d6d…; exit=0 | logs/P37.log | sucesso | D3 |
| P38 | `run P38 foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P38` | hash consultado no VT e veredito no audit.txt (p.7; Fig. 2) | `0: 00002048.zip 184 B 1048576 Malicious (62)`; `1: 00006144.elf 12 KB 3145728 Clean (0)`; exit=0 | logs/P38.log; saidas/audit_P38.txt | sucesso | D3 |
| P39 | `run P39 bash -c 'sha256sum out/P38/zip/* out/P38/elf/* dados/eicar_com.zip; cmp ... && echo ZIP_IDENTICO; grep ...'`; após 65 s, para cada hash: `run P39 bash -c "curl -s -H \"x-apikey: \$VT_API_KEY\" -H 'Accept: application/json' https://www.virustotal.com/api/v3/files/<sha256> \| ~/aval/venv/bin/python ~/aval/dados/vt_stats.py"` | veredito coerente com o VT para o hash | ZIP extraído idêntico ao original (`ZIP_IDENTICO`, 2546dcff…). VT para 2546dcff…: `"malicious": 62, "undetected": 5, "type-unsupported": 7, "failure": 1, harmless/suspicious/timeout 0`. ELF extraído (16ab4938…): `erro_api: NotFoundError`. exit=0 | logs/P39.log | sucesso | D3 |
| P40 | `run P40 env -u VT_API_KEY foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P40` | aviso; carving continua; consultas puladas (p.7) | `Error: VT_API_KEY environment variable is not set.` uma vez por arquivo (2×); arquivos extraídos com os mesmos hashes de P38; coluna VT `Clean (0)` nos dois; exit=0 | logs/P40.log; saidas/audit_P40.txt | falha (parcial pelo critério do roteiro: aviso e carving presentes, mas veredito `Clean (0)` registrado) | D2 |
| P41 | (65 s após P40) `run P41 env VT_API_KEY=CHAVE_INVALIDA_TESTE foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P41` | aviso; consultas puladas (p.7) | nenhum aviso; coluna VT `Clean (0)` nos dois, inclusive no ZIP EICAR; arquivos extraídos com os mesmos hashes; exit=0 | logs/P41.log; saidas/audit_P41.txt | falha | D2 |
| P42 | `run P42 bash -c "unzip -l artefato.zip \| grep -i -E \"evidence\|\.dd\$\|\.img\$\|\.raw\$\" \|\| echo NENHUMA_IMAGEM_NO_ARTEFATO; grep -rn -i evidence2 src-art \|\| echo SEM_REFERENCIA; ls -la /home/revisor"` | – (não documentado) | `NENHUMA_IMAGEM_NO_ARTEFATO`; `SEM_REFERENCIA`; exit=0 | logs/P42.log | sucesso (busca feita; dado ausente) | D2 |
| P43 | `./foremost-ng -v -x evidence2.dd` (Fig. 2) | tabela da Fig. 2 | não executado: evidence2.dd indisponível (não está no artefato nem foi encontrada publicamente, e os autores não responderam) | – | bloqueado | – |
| P44 | comparação com a Fig. 2 | 12 arquivos com nomes e offsets da Fig. 2 | não executado (depende de P43) | – | bloqueado | – |
| P45 | (em `.../src`) `run P45 bash -c "grep -n \"needle->type ==\" extract.c; grep -n \"init_builtin(state\" state.c"` | registro da organização do código | extract.c:2630-2690 é uma cadeia if/else com 29 linhas de teste de `needle->type`; state.c:324-396 tem 21 chamadas `init_builtin(state`, 3 delas MACHO; exit=0 | logs/P45.log | sucesso | D2 |
| P46 | cópia dos audit.txt para `saidas/`; `run P46 bash -c "find out dados img -type f ... -exec sha256sum {} + \| sort -k2 > .../saidas/sha256_manifesto.txt; ...; tar czf ~/aval/evidencias_completas.tgz out dados/*.c dados/*.sh dados/*.py dados/*.ps1 && sha256sum ..."` | evidências empacotadas | manifesto com 67 linhas; tgz de 364132 B (2317b374…) mantido no contêiner; exit=0 | logs/P46.log; saidas/ | sucesso | D1 (pacote não copiado para o host porque contém o EICAR) |

## Observações por reivindicação (apenas fatos)

### C1 – EVTX
- Amostra 1 (issue_39.evtx, 1052672 B, 394 registros):
  - O cabeçalho tem 395 no deslocamento 0x18 e 11 no deslocamento 0x2A (P16).
  - Com `-t evtx`, o artefato gerou `evtx/00002048.evtx` no offset 1048576, com 25886720 B, que é 395 × 65536 (P18 e P19).
  - Os primeiros 1052672 bytes do arquivo extraído são idênticos ao original.
  - O python-evtx 0.8.1 leu 394 registros no arquivo extraído, o mesmo número do original.
- Amostra 2 (system.evtx, 1118208 B, 1601 registros, 13528 em 0x18, 9 em 0x2A):
  - O arquivo extraído tem 66060288 B, que vai do offset 1048576 até o fim da imagem de 64 MiB.
  - O prefixo é idêntico ao original, e o python-evtx leu 1601 registros (P19b).
- Na imagem combinada, o EVTX foi extraído nos dois modos: padrão (P33) e `-t evtx,elf,exe` (P34).

### C2 – Scripts
- Os scripts bash (106 B), python (75 B) e pwsh (84 B) foram extraídos byte a byte, com a linha `#!` preservada, como `.script` nos offsets 1048576, 2097152 e 3145728 (P22 e P23).
- O script de 18 B não foi extraído.
- O script de 66 B formado só pela linha `#!/bin/sh` e duas linhas de comentário foi extraído (`00008192.script`).
- A extensão gerada é `.script`. O artigo usa `00000002.sh` como exemplo na p.7, e a Fig. 2 mostra `.script`.

### C3 – Mach-O
- O universal (fat, 17032 B) foi extraído e é idêntico ao original (`FAT_IDENTICO`, P27).
- Os objetos thin x86_64, arm64 (magic cf fa ed fe) e i386 (ce fa ed fe) não geraram nenhum arquivo (P26 e P27).
- Executáveis thin ligados (Go, darwin/amd64 e darwin/arm64, cerca de 2 MB cada, reconhecidos pelo `file`) também não geraram arquivo: `0 FILES EXTRACTED` (P27b).
- Na imagem combinada, foi extraído só o fat; o thin x86_64 não (P33).

### C4 – ELF
- ELF32 (14940 B) e ELF64 (15960 B) foram extraídos como `.elf` com 12296 B e 12304 B (P30 e P31).
- O readelf leu o cabeçalho ELF e todos os cabeçalhos de programa, com a classe correta. Também informou que a tabela de seções fica além do fim do arquivo, e o `file` relatou "missing section headers".
- Os arquivos extraídos são prefixos idênticos dos originais e executaram com a saída esperada (`ola foremost-ng`).
- O ELF também foi extraído nos modos padrão e `-t evtx,elf,exe` (P33 e P34) e no teste mínimo (P11).

### C5 – VirusTotal
- Com uma chave válida (P38):
  - o ZIP EICAR extraído (idêntico ao original, SHA-256 2546dcff…) recebeu no audit.txt o rótulo `Malicious (62)`;
  - a consulta independente à API v3 pelo mesmo hash retornou `malicious: 62` (P39);
  - o ELF extraído (16ab4938…) recebeu `Clean (0)`, e a API retornou `NotFoundError` para esse hash.
- Sem VT_API_KEY (P40): `Error: VT_API_KEY environment variable is not set.` apareceu uma vez por arquivo, o carving foi concluído com os mesmos hashes e a coluna VT registrou `Clean (0)` nos dois arquivos.
- Com uma chave inválida (P41): não houve aviso, o carving foi concluído e a coluna VT registrou `Clean (0)` nos dois arquivos, inclusive no EICAR.
- Nenhuma execução gerou um arquivo `recovery.log`; o que se gerou foi audit.txt.
- O hash não aparece no audit.txt (saidas/audit_P38.txt).

### C6 – Exemplo da Figura 2
- A imagem evidence2.dd não existe no artefato.zip nem é citada em nenhum arquivo do código (P42).
- Segundo a coordenação, ela não foi encontrada publicamente e os autores não responderam.
- O comando da Fig. 2 não foi executado e a comparação com a figura não foi feita (P43 e P44 bloqueados).

### Outros fatos registrados (procedimento e documentação)
- O `make` na raiz do repositório, como descrito no artigo (p.6), falhou com exit=2 (P5).
- O `make` em `src/`, como no README, compilou com 2 avisos (P6).
- O manual instalado não cita os formatos evtx, elf, macho nem script na seção BUILT-IN FORMATS (P8b).
- A instalação colocou a configuração em /usr/local/etc/foremost.conf, e todas as execuções a usaram (linha `Configuration file:` dos audit.txt).
