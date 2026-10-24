ROTEIRO DE VERIFICAÇÃO – Foremost-NG (commit bb812a22cb06ef87b5a2d877dfb6f40eb12d460d), selos F e R

Este documento é só o plano. Nada foi executado ainda, e nenhum resultado abaixo foi observado. Os resultados "esperados segundo os autores" vêm do README, do Dockerfile, do Makefile ou do artigo. Quando um passo não está documentado pelos autores, ele aparece marcado como [NÃO DOCUMENTADO] com a justificativa. Uma regra vale para todos os passos: não alterar código-fonte, Makefile nem configuração, e não contornar falhas. Toda falha é registrada e tratada pelo critério do próprio passo.

======================================================================
0. REQUISITOS DO AMBIENTE
======================================================================
O que os autores documentam:
- Sistema "Linux-based" [README.md:3].
- "standard GCC toolchain" [artigo p.6, §4].
- Dependências só no Dockerfile: Ubuntu com gcc, make, git, libssl-dev e libcurl4-openssl-dev [Dockerfile:1-6], sem versões fixas (`ubuntu:latest`).
- Chave da API do VirusTotal, a ser obtida pelo próprio usuário [README.md:93-108].
- Não há requisitos de hardware nem de versões.

O que proponho [NÃO DOCUMENTADO], com justificativa:
- Ubuntu 24.04 em amd64 (x86_64). O gcc-multilib, usado para gerar o ELF de 32 bits em C4, só existe em amd64, e a análise de C3 parte de um host little-endian.
- 2 vCPU e 4 GB de RAM. O programa aloca blocos de leitura de 100 MB [src/main.h:230], e no modo "all" pode ler até max_len, que chega a 600 MB no caso de MP4 [src/state.c:344-346].
- 10 GB de disco livre: cerca de 1,5 GB para dependências, mais clang e llvm, imagens de teste abaixo de 200 MB, e mais 3 GB se evidence2.dd for fornecido (2.845.109.643 bytes, conforme a Fig. 2).
- Internet para apt, pip, git, a API do VirusTotal e downloads de amostras.
- Ponto de partida do contêiner: só sudo, unzip e man. Não há compilador, curl nem python3; isso é instalado em P4 e P13.

Aprovações necessárias antes de executar, porque envolvem download de arquivos ou um recurso externo:
1. Pacotes apt dos repositórios oficiais do Ubuntu (P4 e P13).
2. git clone de python-evtx e `pip install python-evtx` (P14 e P15).
3. Download do arquivo de teste eicar_com.zip (P36).
4. A chave VT_API_KEY, que o usuário ou coordenador define no contêiner por meio próprio. Não vou digitar, ler nem exibir o valor (P35).
5. Envio dos hashes SHA-256 dos arquivos de teste ao VirusTotal (P38, P41 e P43).

Também preciso que o coordenador copie artefato.zip para o contêiner (P3).

Convenção de evidências: tudo fica em ~/aval/evid/Pn.log. A função `run` grava data, comando, saída e código de saída.

======================================================================
1. PREPARAÇÃO (F e R)
======================================================================
P1 – F, R, todas – [NÃO DOCUMENTADO]: é preciso para ter evidência rastreável.
- Diretório: ~
- Comandos:
  mkdir -p ~/aval/{evid,dados,img,out}
  cat > ~/aval/run.sh <<'EOF'
  run(){ id="$1"; shift; log="$HOME/aval/evid/$id.log"; printf '### %s | %s\n' "$(date -Is)" "$*" >> "$log"; "$@" 2>&1 | tee -a "$log"; rc=${PIPESTATUS[0]}; echo "exit=$rc" | tee -a "$log"; return $rc; }
  EOF
  source ~/aval/run.sh
  O `source ~/aval/run.sh` deve ser repetido em toda sessão nova.
- Esperado pelos autores: não se aplica.
- Evidência: ~/aval/run.sh.
- Sucesso: a função existe. Falha ou interrupção: se não for possível gravar em ~, parar tudo.

P2 – F, R, todas – [NÃO DOCUMENTADO]: os autores não descrevem o ambiente, então ele precisa ser registrado.
- Diretório: ~/aval
- Comando: run P2 bash -c 'cat /etc/os-release; uname -m; nproc; free -h; df -h $HOME; id'
- Esperado pelos autores: nada documentado.
- Evidência: evid/P2.log.
- Sucesso: Ubuntu 24.04, x86_64, pelo menos 4 GB de RAM e 10 GB livres.
- Falha: arquitetura diferente de x86_64 ou recursos abaixo disso.
- Interrupção: se não for x86_64, parar e consultar o coordenador.

P3 – F, R, todas – [NÃO DOCUMENTADO]: o README manda descompactar `foremost-ng-<version>.tar.gz` [README.md:27], e esse arquivo não existe para este commit. O artigo manda clonar o repositório [p.6], o que traria a HEAD e não o commit avaliado. Por isso usamos o artefato.zip congelado.
- Diretório: ~/aval, onde o coordenador terá colocado artefato.zip.
- Comandos:
  run P3 sha256sum artefato.zip
  run P3 unzip -z artefato.zip
  run P3 unzip -q artefato.zip -d ~/aval/src-art
  run P3 ls -la ~/aval/src-art/foremost-ng-bb812a22
- Esperado: o SHA-256 é 955c770e29893527f789e11afc28dcc6b83d7af4a64f14b416e39f554b388e0a, o comentário do zip é bb812a22cb06ef87b5a2d877dfb6f40eb12d460d e existe src/Makefile.
- Evidência: evid/P3.log.
- Sucesso: hash e commit conferem. Falha: divergência.
- Interrupção: se o hash divergir, parar tudo.

P4 – F, R, todas – Documentado só no Dockerfile [Dockerfile:3-6]. O README não lista dependências para Linux.
- Diretório: ~/aval
- Comandos:
  run P4 sudo apt-get update
  run P4 sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev
  run P4 bash -c 'gcc --version | head -1; make --version | head -1; dpkg-query -W gcc make libssl-dev libcurl4-openssl-dev'
- Esperado pelos autores: pacotes instalados. Nenhuma versão é especificada.
- Evidência: evid/P4.log, com as versões instaladas.
- Sucesso: código de saída 0 e versões registradas. Falha: erro do apt.
- Interrupção: se a instalação falhar, parar tudo.

P5 – F, todas – Documentado no artigo [p.6, §4: `cd foremost-ng`, `make`]. É um teste de conformidade do procedimento do artigo.
- Diretório: ~/aval/src-art/foremost-ng-bb812a22
- Comando: run P5 make
- Esperado pelos autores: compilação. Pelo índice, não há Makefile na raiz, então prevejo o erro "no makefile found".
- Evidência: evid/P5.log.
- Sucesso: compila. Falha: erro de make, que fica registrado como divergência entre o artigo e o README.
- Interrupção: não interrompe; seguir para P6.

P6 – F, R, todas – Documentado [README.md:28 e 33: `cd .../src`, `make`].
- Diretório: ~/aval/src-art/foremost-ng-bb812a22/src
- Comandos:
  run P6 make
  run P6 bash -c 'ls -l foremost-ng && ./foremost-ng -V'
- Esperado pelos autores: um binário `foremost-ng`.
- Evidência: evid/P6.log, com os avisos do compilador.
- Sucesso: make sai com 0, o binário existe e `-V` imprime 1.5.7.
- Falha: make sai com código diferente de 0 ou o binário não é gerado.
- Interrupção: se P6 falhar, parar F e R sem corrigir o código. F e R ficam não verificados por falha de compilação.

P7 – F, R, todas – Documentado [README.md:34: `sudo make install`; Makefile:107-118].
- Diretório: o mesmo de P6.
- Comandos:
  run P7 sudo make install
  run P7 bash -c 'command -v foremost-ng; ls -l /usr/local/bin/foremost-ng /usr/share/man/man8/foremost-ng.8.gz /usr/local/etc/foremost.conf'
- Esperado pelos autores: binário em /usr/local/bin, man page em /usr/share/man/man8 e configuração em /usr/local/etc.
- Evidência: evid/P7.log.
- Sucesso: os três arquivos existem. Falha: algum deles falta.
- Interrupção: se o binário ou o foremost.conf faltarem, parar. Sem configuração o programa aborta [src/config.c:225-229 e src/main.c:222-224].

======================================================================
2. TESTE MÍNIMO – SELO F
======================================================================
Os autores não fornecem um exemplo mínimo com dados. Essa lacuna documental continua valendo, seja qual for o resultado da execução.

P8 – F – Documentado [README.md:79 `man foremost-ng`; artigo p.7; opções em src/main.c:92-112].
- Diretório: ~/aval
- Comandos:
  run P8 foremost-ng -h
  run P8 foremost-ng -V
  run P8 bash -c 'man -P cat foremost-ng | head -150'
- Esperado pelos autores: a ajuda com as opções -t, -i, -o e -x, a versão 1.5.7 (que também aparece na Fig. 2) e a página de manual.
- Evidência: evid/P8.log.
- Sucesso: ajuda e versão impressas, e o manual exibido.
- Falha: travamento ou saída vazia. Se faltar só o manual, conta como falha documental, não funcional.
- Interrupção: se `-h` travar, parar F e R.

P9 – F – [NÃO DOCUMENTADO]: os autores não fornecem dados, e é preciso uma entrada com conteúdo conhecido para comparar.
- Diretório: ~/aval/dados
- Comandos:
  cat > hello.c <<'EOF'
  #include <stdio.h>
  int main(void){ puts("ola foremost-ng"); return 0; }
  EOF
  run P9 gcc -O0 -o hello64 hello.c
  printf '#!/bin/bash\n# script de teste do avaliador\nfor i in 1 2 3; do\n  echo "linha $i"\ndone\n' > teste.sh
  run P9 bash -c 'ls -l hello64 teste.sh; sha256sum hello64 teste.sh; ./hello64'
- Esperado pelos autores: não se aplica.
- Evidência: evid/P9.log, com os hashes.
- Sucesso: os arquivos são criados e o programa imprime "ola foremost-ng".
- Falha ou interrupção: se o gcc falhar, parar, porque o ambiente fica inválido.

P10 – F – [NÃO DOCUMENTADO]: é preciso montar uma "disk.img" com deslocamentos conhecidos.
- Diretório: ~/aval/img
- Comando: run P10 bash -c 'truncate -s 16M img_f.img && dd if=../dados/hello64 of=img_f.img bs=512 seek=2048 conv=notrunc status=none && dd if=../dados/teste.sh of=img_f.img bs=512 seek=6144 conv=notrunc status=none && sha256sum img_f.img'
- Posições: o ELF fica no deslocamento 1048576 (bloco 2048) e o script no deslocamento 3145728 (bloco 6144).
- Evidência: evid/P10.log.
- Sucesso: imagem criada. Interrupção: se falhar, parar F.

P11 – F – Documentado, no formato do exemplo [artigo p.7, §4.1: `foremost-ng -i disk.img -o <dir>`].
- Diretório: ~/aval
- Comando: run P11 foremost-ng -v -i ~/aval/img/img_f.img -o ~/aval/out/P11
- Esperado pelos autores [p.7, §4.1-4.2 e Fig. 2]:
  - todos os parsers são executados;
  - um subdiretório por formato;
  - audit.txt com as colunas ID, Name (bs=512), Size, Offset, Comment e VT.
- Evidência: evid/P11.log e out/P11/.
- Sucesso: código de saída 0, audit.txt existe e lista pelo menos elf/00002048.elf (offset 1048576) e script/00006144.script (offset 3145728).
- Falha: travamento, audit.txt ausente ou um dos dois arquivos ausente.
- Interrupção: se houver segfault ou aborto, parar F e R.

P12 – F – [NÃO DOCUMENTADO]: é preciso conferir a integridade do que foi recuperado.
- Diretório: ~/aval
- Comando: run P12 bash -c 'ls -lR out/P11; cat out/P11/audit.txt; cmp out/P11/script/00006144.script dados/teste.sh && echo SCRIPT_IDENTICO; readelf -h -l out/P11/elf/00002048.elf'
- Evidência: evid/P12.log.
- Sucesso: o script é idêntico ao original e o readelf lê o cabeçalho e os segmentos do ELF.
- Falha: o conteúdo difere ou o readelf dá erro no cabeçalho.
- Interrupção: nenhuma.

======================================================================
3. SELO R – PREPARAÇÃO COMUM
======================================================================
P13 – R, C1 a C5 – [NÃO DOCUMENTADO]: os autores não indicam ferramentas para gerar dados nem para validar o que foi extraído, e a tabela de reivindicações exige validar com ferramentas próprias de cada formato.
- Diretório: ~/aval
- Comandos:
  run P13 sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc-multilib clang llvm file python3-venv curl
  run P13 bash -c 'clang --version | head -1; ls /usr/lib/llvm-*/bin/llvm-lipo; file --version | head -1; python3 --version; curl --version | head -1'
- Evidência: evid/P13.log.
- Sucesso: tudo instalado.
- Falha ou interrupção: se faltar o gcc-multilib, C4 fica sem o caso de 32 bits; se faltar clang ou llvm, C3 é interrompida. Registrar e seguir com o resto.

======================================================================
4. SELO R – BLOCO C1 (EVTX)
======================================================================
Fonte: artigo p.6, §3, e p.7, §4.1. Resultado esperado [reivindicacoes.md:7]: um .evtx extraído e legível por uma ferramenta de análise de eventos.

P14 – R, C1 – [NÃO DOCUMENTADO]: o artigo cita o DFTT [p.7] sem indicar amostra EVTX, então é preciso um .evtx real. Exige aprovação de download.
- Diretório: ~/aval/dados
- Comandos:
  run P14 git clone --depth 1 https://github.com/williballenthin/python-evtx.git pyevtx-repo
  run P14 bash -c 'find pyevtx-repo -name "*.evtx" -printf "%s %p\n" | sort -n'
  run P14 bash -c 'f=$(find pyevtx-repo -name "*.evtx" -size +68k -printf "%s %p\n" | sort -n | head -1 | cut -d" " -f2); cp "$f" amostra.evtx && sha256sum amostra.evtx && stat -c %s amostra.evtx'
- Evidência: evid/P14.log, com o hash e o tamanho.
- Sucesso: amostra.evtx criada.
- Interrupção: se não houver .evtx, interromper C1 como "dado de teste indisponível" e pedir outra fonte ao coordenador.

P15 – R, C1 – [NÃO DOCUMENTADO]: o artigo fala em "standard event log tools" sem nomear nenhuma; uso python-evtx. Exige aprovação de download.
- Diretório: ~/aval/dados
- Comandos:
  run P15 python3 -m venv ~/aval/venv
  run P15 ~/aval/venv/bin/pip install python-evtx
  cat > conta_evtx.py <<'EOF'
  import sys, Evtx.Evtx as E
  with E.Evtx(sys.argv[1]) as log:
      print("registros", sum(1 for _ in log.records()))
  EOF
  run P15 ~/aval/venv/bin/python conta_evtx.py amostra.evtx
- Evidência: evid/P15.log, com o número N de registros do original.
- Sucesso: N > 0.
- Interrupção: se a ferramenta não ler o original, interromper C1 por problema do validador, não do artefato.

P16 – R, C1 – [NÃO DOCUMENTADO]: documenta o risco da análise anterior (o campo lido em 0x18 contra o número de chunks em 0x2A). É só registro.
- Diretório: ~/aval/dados
- Comando: run P16 bash -c 'od -A d -c -N 8 amostra.evtx; od -A d -t u8 -j 24 -N 8 amostra.evtx; od -A d -t u2 -j 42 -N 2 amostra.evtx'
- Evidência: evid/P16.log.
- Critério: nenhum de sucesso ou falha.

P17 – R, C1 – [NÃO DOCUMENTADO]: é preciso montar a imagem.
- Diretório: ~/aval/img
- Comando: run P17 bash -c 'truncate -s 64M img_c1.img && dd if=../dados/amostra.evtx of=img_c1.img bs=512 seek=2048 conv=notrunc status=none && sha256sum img_c1.img'
- Se a amostra tiver mais de 48 MiB, usar tamanho de imagem igual ao da amostra mais 16 MiB.
- Sucesso: imagem criada.

P18 – R, C1 – Documentado [opção -t: artigo p.7, §4.1; identificador "evtx": src/state.c:688].
- Diretório: ~/aval
- Comando: run P18 foremost-ng -v -t evtx -i ~/aval/img/img_c1.img -o ~/aval/out/P18
- Esperado pelos autores: um arquivo em evtx/ legível por ferramentas de eventos [p.6].
- Evidência: evid/P18.log e out/P18/.
- Sucesso: código de saída 0 e evtx/00002048.evtx listado com offset 1048576.
- Falha: nenhum .evtx gerado. Interrupção: em caso de travamento.

P19 – R, C1 – [NÃO DOCUMENTADO]: validação.
- Diretório: ~/aval
- Comando: run P19 bash -c 'c=out/P18/evtx/00002048.evtx; ls -l out/P18/evtx; sha256sum $c; stat -c %s $c dados/amostra.evtx; cmp -n $(stat -c %s dados/amostra.evtx) $c dados/amostra.evtx && echo PREFIXO_OK; ~/aval/venv/bin/python dados/conta_evtx.py $c'
- Sucesso: o arquivo começa com os mesmos bytes do original e o número de registros é igual a N.
- Sucesso parcial: legível, mas com tamanho diferente do original; registrar a diferença.
- Falha: arquivo ausente, erro de leitura ou menos de N registros.

======================================================================
5. SELO R – BLOCO C2 (SCRIPTS)
======================================================================
Fonte: artigo p.6, §3. Resultado esperado [reivindicacoes.md:8]: script extraído com a linha do interpretador e o corpo legível.

P20 – R, C2 – [NÃO DOCUMENTADO]: dados com casos positivos e negativos para testar o mínimo de 32 bytes e a exigência de algo além de comentários.
- Diretório: ~/aval/dados
- Comandos:
  printf '#!/bin/bash\n# backup\nfor f in /etc/hostname /etc/os-release; do\n  cp "$f" /tmp/ && echo "copiado $f"\ndone\n' > s_bash.sh
  printf '#!/usr/bin/env python3\nimport os\nfor k in sorted(os.environ):\n    print(k)\n' > s_py.py
  printf '#!/usr/bin/env pwsh\nGet-ChildItem -Path . | ForEach-Object { Write-Output $_.Name }\n' > s_ps.ps1
  printf '#!/bin/sh\n# apenas comentario linha 1\n# apenas comentario linha 2\n' > neg_coment.sh
  printf '#!/bin/sh\necho oi\n' > neg_curto.sh
  run P20 bash -c 'wc -c s_bash.sh s_py.py s_ps.ps1 neg_coment.sh neg_curto.sh; sha256sum s_* neg_*'
- Sucesso: os três positivos têm pelo menos 32 bytes e neg_curto.sh tem menos de 32.

P21 – R, C2 – [NÃO DOCUMENTADO]: montagem da imagem.
- Diretório: ~/aval/img
- Comando: run P21 bash -c 'truncate -s 16M img_c2.img; for p in "s_bash.sh 2048" "s_py.py 4096" "s_ps.ps1 6144" "neg_coment.sh 8192" "neg_curto.sh 10240"; do set -- $p; dd if=../dados/$1 of=img_c2.img bs=512 seek=$2 conv=notrunc status=none; done; sha256sum img_c2.img'

P22 – R, C2 – Documentado [-t: p.7; identificador "script": src/state.c:695].
- Diretório: ~/aval
- Comando: run P22 foremost-ng -v -t script -i ~/aval/img/img_c2.img -o ~/aval/out/P22
- Esperado pelos autores: os scripts extraídos com a linha do interpretador, ignorando os que têm menos de 32 bytes ou só comentários [p.6]. O artigo dá como exemplo o nome `00000002.sh` [p.7], mas a Fig. 2 mostra `.script`.

P23 – R, C2 – [NÃO DOCUMENTADO]: validação.
- Comando: run P23 bash -c 'cd out/P22/script && ls -l; cmp 00002048.script ~/aval/dados/s_bash.sh && echo OK_BASH; cmp 00004096.script ~/aval/dados/s_py.py && echo OK_PY; cmp 00006144.script ~/aval/dados/s_ps.ps1 && echo OK_PS; ls 00008192* 00010240* 2>&1'
- Sucesso: os três positivos são idênticos aos originais e os dois negativos não aparecem.
- Falha: algum positivo falta ou difere, ou algum negativo é extraído.
- A diferença entre as extensões .sh e .script é registrada só como divergência documental.

======================================================================
6. SELO R – BLOCO C3 (MACH-O FAT E THIN)
======================================================================
Fonte: artigo p.6, §3. Resultado esperado [reivindicacoes.md:9]: binário Mach-O extraído e reconhecível. Este bloco testa diretamente a previsão da análise de que o caso thin falha.

P24 – R, C3 – [NÃO DOCUMENTADO]: não há amostras Mach-O. Sem o SDK da Apple não dá para gerar executável ligado, só objetos Mach-O; essa limitação fica registrada.
- Diretório: ~/aval/dados
- Comandos:
  printf 'int soma(int a,int b){return a+b;}\nint main(void){return soma(2,3);}\n' > macho.c
  run P24 clang -target x86_64-apple-macos11 -c macho.c -o m_x86_64.o
  run P24 clang -target arm64-apple-macos11 -c macho.c -o m_arm64.o
  run P24 clang -target i386-apple-macos10.12 -c macho.c -o m_i386.o
  LIPO=$(ls /usr/lib/llvm-*/bin/llvm-lipo | head -1); run P24 "$LIPO" -create m_x86_64.o m_arm64.o -output m_fat.o
  run P24 bash -c 'file m_*.o; for f in m_*.o; do od -A x -t x1 -N 4 $f; done; sha256sum m_*.o'
- Esperado (formato): os thin de 64 bits começam com cf fa ed fe, o de 32 bits com ce fa ed fe e o fat com ca fe ba be.
- Interrupção: se o i386 falhar, seguir só com 64 bits e fat e registrar. Se o lipo falhar, o caso fat fica não testado.

P25 – R, C3 – [NÃO DOCUMENTADO]: montagem da imagem.
- Diretório: ~/aval/img
- Comando: run P25 bash -c 'truncate -s 16M img_c3.img; for p in "m_x86_64.o 2048" "m_arm64.o 4096" "m_i386.o 6144" "m_fat.o 8192"; do set -- $p; [ -f ../dados/$1 ] && dd if=../dados/$1 of=img_c3.img bs=512 seek=$2 conv=notrunc status=none; done; sha256sum img_c3.img'

P26 – R, C3 – Documentado [-t; identificador "macho": src/state.c:672].
- Comando: run P26 foremost-ng -v -t macho -i ~/aval/img/img_c3.img -o ~/aval/out/P26
- Esperado pelos autores: os Mach-O fat e thin escritos por inteiro [p.6].

P27 – R, C3 – [NÃO DOCUMENTADO]: validação.
- Comando: run P27 bash -c 'cd out/P26/macho && ls -l; file *; cmp 00008192.macho ~/aval/dados/m_fat.o && echo FAT_IDENTICO; for b in 00002048 00004096 00006144; do [ -f $b.macho ] && /usr/lib/llvm-*/bin/llvm-objdump --macho --private-headers $b.macho | head -20 || echo "AUSENTE $b"; done'
- Sucesso: o fat é idêntico ao original e cada thin gera um .macho que `file` e `llvm-objdump` reconhecem.
- Falha: algum thin ausente (o que a análise prevê) ou o fat ausente ou diferente.
- Se o fat funcionar e o thin falhar, C3 conta como não reproduzida, porque a reivindicação cobre os dois.

======================================================================
7. SELO R – BLOCO C4 (ELF DE 32 E 64 BITS)
======================================================================
Fonte: artigo p.6, §3, e p.7, §4.1. Resultado esperado [reivindicacoes.md:10]: um .elf estruturalmente legível por analisador ELF.

P28 – R, C4 – [NÃO DOCUMENTADO]: é preciso um ELF32 e um ELF64 conhecidos.
- Diretório: ~/aval/dados
- Comandos:
  run P28 gcc -m32 -O0 -o hello32 hello.c
  run P28 bash -c 'file hello32 hello64; ./hello32; ./hello64; sha256sum hello32 hello64'
- Interrupção: se o -m32 falhar, testar só 64 bits e registrar C4 como parcial.

P29 – R, C4 – [NÃO DOCUMENTADO]: montagem da imagem.
- Diretório: ~/aval/img
- Comando: run P29 bash -c 'truncate -s 16M img_c4.img; dd if=../dados/hello32 of=img_c4.img bs=512 seek=2048 conv=notrunc status=none; dd if=../dados/hello64 of=img_c4.img bs=512 seek=6144 conv=notrunc status=none; sha256sum img_c4.img'

P30 – R, C4 – Documentado [`-t elf`: p.7, §4.1].
- Comando: run P30 foremost-ng -v -t elf -i ~/aval/img/img_c4.img -o ~/aval/out/P30
- Esperado pelos autores: a união dos segmentos carregáveis, com "layout executável correto" [p.6].

P31 – R, C4 – [NÃO DOCUMENTADO]: validação. Executar os ELF extraídos é seguro, porque foram compilados por nós.
- Comando: run P31 bash -c 'cd out/P30/elf && ls -l; file *.elf; readelf -h -l 00002048.elf; readelf -h -l 00006144.elf; cmp -n $(stat -c %s 00002048.elf) 00002048.elf ~/aval/dados/hello32 && echo PREF32_OK; cmp -n $(stat -c %s 00006144.elf) 00006144.elf ~/aval/dados/hello64 && echo PREF64_OK; chmod +x *.elf; ./00002048.elf; ./00006144.elf; readelf -S 00006144.elf 2>&1 | head -5'
- Sucesso: os dois arquivos existem, a classe 32 ou 64 está correta, o readelf lê cabeçalho e segmentos, os prefixos coincidem com os originais e ambos imprimem "ola foremost-ng".
- Falha: arquivo ausente, classe errada ou erro no cabeçalho ou nos segmentos.
- A falta da tabela de seções é registrada como divergência da afirmação do artigo sobre "symbol information", não como falha de C4.

======================================================================
8. SELO R – EXEMPLOS COMBINADOS DO ARTIGO (C1, C2, C3, C4)
======================================================================
P32 – R, C1 a C4 – [NÃO DOCUMENTADO]: o "disk.img" do artigo não é fornecido.
- Diretório: ~/aval/img
- Comando: run P32 bash -c 'truncate -s 80M disk.img; for p in "amostra.evtx 2048" "hello32 131072" "hello64 135168" "s_bash.sh 139264" "m_fat.o 143360" "m_x86_64.o 147456"; do set -- $p; dd if=../dados/$1 of=disk.img bs=512 seek=$2 conv=notrunc status=none; done; sha256sum disk.img'
- Isso pressupõe que amostra.evtx tenha menos de 60 MiB.

P33 – F, R, C1 a C4 – Documentado [modo padrão: p.7, §4.1].
- Diretório: ~/aval
- Comando: run P33 foremost-ng -v -i ~/aval/img/disk.img -o ~/aval/out/P33
- Esperado pelos autores: todos os parsers inspecionam a imagem, com um subdiretório por formato.
- Sucesso: evtx/, elf/ (2 arquivos), script/ e macho/ presentes, e o audit.txt coerente com os offsets usados.
- Falha: algum formato ausente, a ser comparado com os blocos C1 a C4.

P34 – R, C1 e C4 – Documentado [sintaxe exata da p.7: `foremost-ng -t evtx,elf,exe -i disk.img -o ...`].
- Comando: run P34 foremost-ng -t evtx,elf,exe -i ~/aval/img/disk.img -o ~/aval/out/P34
- Esperado pelos autores: só os módulos EVTX, ELF e EXE rodam.
- Sucesso: só aparecem os subdiretórios evtx/ e elf/ (e exe/ se houver algo), sem script/ nem macho/.
- Falha: tipos fora do filtro ou evtx/elf ausentes.

======================================================================
9. SELO R – BLOCO C5 (VIRUSTOTAL)
======================================================================
Fonte: artigo p.3, p.7 §4.1 e Fig. 2; README.md:89-108. Resultado esperado [reivindicacoes.md:11]: a consulta associada ao hash do arquivo extraído, com o resultado registrado; sem chave, aviso e carving sem consulta. A API gratuita permite cerca de 4 consultas por minuto, e o programa não controla esse ritmo. Por isso as imagens deste bloco têm só 2 arquivos e as execuções ficam a pelo menos 60 s uma da outra.

P35 – R, C5 – Documentado [README.md:95-107: criar conta, obter a chave e exportar VT_API_KEY]. Executado pelo humano: não crio conta nem manipulo a chave.
- Diretório: ~/aval
- Comando (meu, sem exibir o valor): run P35 bash -c 'test -n "$VT_API_KEY" && echo VT_API_KEY_definida || echo VT_API_KEY_ausente'
- Sucesso: "definida".
- Interrupção: se ausente, interromper P38 e P39 (C5 fica sem o ramo positivo por falta de recurso externo) e seguir com P40 e P41.

P36 – R, C5 – [NÃO DOCUMENTADO]: é preciso um arquivo cujo hash o VT conheça com certeza e que o programa extraia byte a byte. O ZIP de teste EICAR é inofensivo e padronizado. Exige aprovação de download.
- Diretório: ~/aval/dados
- Comandos:
  run P36 curl -fsSLo eicar_com.zip https://secure.eicar.org/eicar_com.zip
  run P36 sha256sum eicar_com.zip
- Interrupção: se o download falhar, o ramo positivo fica inconclusivo. Não enviar arquivos ao VT, porque isso seria publicação.

P37 – R, C5 – [NÃO DOCUMENTADO]: montagem da imagem.
- Diretório: ~/aval/img
- Comando: run P37 bash -c 'truncate -s 16M img_c5.img; dd if=../dados/eicar_com.zip of=img_c5.img bs=512 seek=2048 conv=notrunc status=none; dd if=../dados/hello64 of=img_c5.img bs=512 seek=6144 conv=notrunc status=none; sha256sum img_c5.img'

P38 – R, C5 – Documentado [`-x` com chave: p.7, §4.1; README.md:91].
- Diretório: ~/aval
- Comando: run P38 foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P38
- Esperado pelos autores: hash calculado para cada arquivo, consulta à API e audit.txt anotado com o veredito. A Fig. 2 mostra o formato "Malicious (2)" / "Clean (0)".

P39 – R, C5 – [NÃO DOCUMENTADO]: é preciso associar o hash ao veredito.
- Comando: run P39 bash -c 'sha256sum out/P38/zip/* out/P38/elf/* dados/eicar_com.zip; cat out/P38/audit.txt'
- O humano consulta os hashes no site do VirusTotal e compara com o que foi registrado.
- Sucesso: o ZIP extraído aparece com "Malicious (n)", n > 0, coerente com o VT para aquele hash. O ELF tem um rótulo; espero "Clean (0)" porque o hash é desconhecido, o que não discrimina nada.
- Falha: coluna "N/A" ou "Clean (-1)", que indica falha de parse; "Clean (0)" para um hash que o VT marca como malicioso; ou erros do curl.
- Inconclusivo: se o hash do ZIP extraído diferir do original e for desconhecido do VT.

P40 – R, C5 – Documentado [p.7: sem chave, aviso e consultas puladas].
- Comando: run P40 env -u VT_API_KEY foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P40
- Sucesso: aviso emitido, os mesmos arquivos extraídos (hashes iguais aos de P38) e a coluna VT sem veredito.
- Falha parcial (prevista pela análise): aviso repetido por arquivo com rótulo "Clean (0)", o que diverge de "pular as consultas".
- Falha: o carving não acontece.

P41 – R, C5 – Documentado [p.7: chave inválida, aviso e consultas puladas]. Executar pelo menos 60 s depois de P38.
- Comando: run P41 env VT_API_KEY=CHAVE_INVALIDA_TESTE foremost-ng -v -x -t zip,elf -i ~/aval/img/img_c5.img -o ~/aval/out/P41
- Sucesso: aviso emitido e arquivos extraídos.
- Falha: nenhum aviso e veredito "Clean (0)" registrado.

======================================================================
10. SELO R – BLOCO C6 (FIGURA 2)
======================================================================
Fonte: artigo p.7, §4.2, e p.8, Fig. 2. Critério [reivindicacoes.md:21]: os mesmos arquivos e offsets; as contagens do VT não precisam coincidir.

P42 – R, C6 – [NÃO DOCUMENTADO]: o README não trata do assunto, então é preciso confirmar que o dado não existe.
- Diretório: ~/aval
- Comando: run P42 bash -c 'unzip -l artefato.zip | grep -i -E "evidence|\.dd$|\.img$|\.raw$" || echo NENHUMA_IMAGEM_NO_ARTEFATO; grep -rn -i evidence2 src-art || echo SEM_REFERENCIA'
- Esperado pelos autores: nada documentado.
- Interrupção: se o arquivo estiver ausente, C6 é NÃO REPRODUZÍVEL. Não substituir por outra imagem; pedir ao coordenador que solicite o arquivo aos autores.

P43 – R, C6 – Documentado, mas condicional: só se o coordenador fornecer evidence2.dd com 2.845.109.643 bytes [comando exato da Fig. 2: `./foremost-ng -v -x evidence2.dd`, executado a partir de src/].
- Diretório: ~/aval/src-art/foremost-ng-bb812a22/src, com evidence2.dd copiado para ali e sem um output/ preexistente.
- Comandos:
  run P43 bash -c 'stat -c %s evidence2.dd; sha256sum evidence2.dd'
  run P43 ./foremost-ng -v -x evidence2.dd
- Esperado pelos autores: a tabela da Fig. 2. Exige a chave do P35. Com 12 consultas, o limite da API pode afetar a coluna VT, o que não pesa no critério.

P44 – R, C6 – [NÃO DOCUMENTADO]: comparação.
- Comando: run P44 cat output/audit.txt
- Comparar com a Fig. 2, nome e offset:
  00004352.elf/2228224
  00004820.elf/2467840
  00005108.elf/2615296
  00005492.script/2811904
  00399884.exe/204740608
  00405060.exe/207390720
  00414932.exe/212445184
  00428728.exe/219508736
  00442520.exe/226570240
  00447356.exe/229046272
  01786101.zip/914484119
  01787042.zip/914965615
- Sucesso: os 12 arquivos aparecem com os mesmos nomes e offsets, e os tamanhos batem com a figura.
- Falha: algum arquivo ausente ou com offset diferente.

======================================================================
11. C7 (ARQUITETURA) – FORA DA REGRA DE R, SÓ INSPEÇÃO
======================================================================
P45 – R, C7 – [NÃO DOCUMENTADO]: o artigo não traz experimento para esta reivindicação.
- Diretório: ~/aval/src-art/foremost-ng-bb812a22/src
- Comando: run P45 bash -c 'grep -n "needle->type ==" extract.c; grep -n "init_builtin(state" state.c'
- Esperado pelos autores: um despachante central e parsers com interface uniforme [p.2-3, Fig. 1].
- Registro: confirmar se, para adicionar um parser, é preciso alterar extract_file.
- Critério: não pesa nas decisões.

P46 – F e R – [NÃO DOCUMENTADO]: empacota as evidências.
- Diretório: ~/aval
- Comando: run P46 bash -c 'tar czf evidencias.tgz evid out && sha256sum evidencias.tgz'
- Atenção: out/ contém o ZIP EICAR, que antivírus do host podem sinalizar.

======================================================================
12. TEMPO ESTIMADO
======================================================================
- Preparação, P1 a P7: 15 a 25 min, dominados pelo apt.
- F, P8 a P12: 10 a 15 min.
- Ferramentas, P13: 10 a 15 min (clang e llvm somam cerca de 1 GB).
- C1, P14 a P19: 20 a 30 min.
- C2, P20 a P23: 10 min.
- C3, P24 a P27: 15 a 20 min.
- C4, P28 a P31: 10 min.
- Combinados, P32 a P34: 10 min.
- C5, P35 a P41: 20 a 30 min, incluindo as esperas de rate limit e a conferência humana.
- C6, P42: 2 min. Mais 30 a 60 min se evidence2.dd for fornecido (P43 e P44).
- C7 e empacotamento, P45 e P46: 5 min.
- Total: cerca de 2h30 a 3h30 sem C6; cerca de 3h30 a 4h30 com C6.

======================================================================
13. TABELA DE PASSOS
======================================================================
| ID | Selo | Reiv. | Documentado? | Objetivo | Interrompe se |
|---|---|---|---|---|---|
| P1 | F,R | todas | ND | Estrutura e função run | não houver gravação em ~ |
| P2 | F,R | todas | ND | Registrar ambiente | arquitetura não for x86_64 |
| P3 | F,R | todas | ND (substitui o tarball) | Obter e conferir artefato.zip | hash divergir |
| P4 | F,R | todas | Dockerfile:3-6 | Dependências apt | apt falhar |
| P5 | F | todas | artigo p.6 | `make` na raiz (conformidade) | não interrompe |
| P6 | F,R | todas | README:28,33 | Compilar em src/ | make falhar |
| P7 | F,R | todas | README:34 | `sudo make install` | binário ou conf faltar |
| P8 | F | – | README:79; p.7 | -h, -V, man | -h travar |
| P9 | F | – | ND | Criar ELF64 e script de teste | gcc falhar |
| P10 | F | – | ND | Montar img_f.img | falha de dd |
| P11 | F | – | p.7 §4.1 | Execução mínima -i/-o | travamento |
| P12 | F | – | ND | Validar saídas mínimas | – |
| P13 | R | C1-C5 | ND | Ferramentas de geração e validação | parcial por bloco |
| P14 | R | C1 | ND | Obter amostra EVTX | sem amostra |
| P15 | R | C1 | ND | python-evtx; contar registros | original ilegível |
| P16 | R | C1 | ND | Registrar campos 0x18/0x2A | – |
| P17 | R | C1 | ND | Montar img_c1.img | – |
| P18 | R | C1 | p.7 (-t) | Carving -t evtx | travamento |
| P19 | R | C1 | ND | Validar EVTX extraído | – |
| P20 | R | C2 | ND | Scripts positivos e negativos | – |
| P21 | R | C2 | ND | Montar img_c2.img | – |
| P22 | R | C2 | p.7 (-t) | Carving -t script | travamento |
| P23 | R | C2 | ND | Validar scripts | – |
| P24 | R | C3 | ND | Gerar Mach-O thin e fat | clang/lipo faltar |
| P25 | R | C3 | ND | Montar img_c3.img | – |
| P26 | R | C3 | p.7 (-t) | Carving -t macho | travamento |
| P27 | R | C3 | ND | Validar Mach-O | – |
| P28 | R | C4 | ND | Gerar ELF32 e ELF64 | -m32 falhar (parcial) |
| P29 | R | C4 | ND | Montar img_c4.img | – |
| P30 | R | C4 | p.7 §4.1 | Carving -t elf | travamento |
| P31 | R | C4 | ND | Validar ELF (readelf, cmp, executar) | – |
| P32 | R | C1-C4 | ND | Montar disk.img combinada | – |
| P33 | F,R | C1-C4 | p.7 §4.1 | Modo padrão | travamento |
| P34 | R | C1,C4 | p.7 §4.1 | `-t evtx,elf,exe` exato | travamento |
| P35 | R | C5 | README:95-107 (humano) | Chave VT presente | chave ausente (ramo positivo) |
| P36 | R | C5 | ND | Obter eicar_com.zip | download falhar (inconclusivo) |
| P37 | R | C5 | ND | Montar img_c5.img | – |
| P38 | R | C5 | p.7 §4.1; README:91 | -x com chave | sem chave |
| P39 | R | C5 | ND | Hash e veredito; conferência humana | – |
| P40 | R | C5 | p.7 | -x sem chave | – |
| P41 | R | C5 | p.7 | -x com chave inválida | – |
| P42 | R | C6 | ND | Procurar evidence2.dd | ausente: C6 não reproduzível |
| P43 | R | C6 | Fig. 2 (condicional) | `./foremost-ng -v -x evidence2.dd` | dado não fornecido |
| P44 | R | C6 | ND | Comparar com a Fig. 2 | – |
| P45 | R | C7 | ND | Inspeção do despachante | não pesa |
| P46 | F,R | – | ND | Empacotar evidências | – |

ND = [NÃO DOCUMENTADO]. Nenhum passo deste roteiro foi executado.