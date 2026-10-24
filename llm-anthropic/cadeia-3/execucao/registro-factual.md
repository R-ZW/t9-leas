# Registro factual da execução: Foremost-NG (commit bb812a22cb06ef87b5a2d877dfb6f40eb12d460d)

Execução feita em 24/10/2026, das 15:46 às 16:02 UTC, no contêiner `t9-claude-c3`. Os comandos rodaram com `docker exec t9-claude-c3 bash -lc '<comando>'`, como usuário `revisor`.

Variáveis usadas nos comandos:
- `EV=/home/revisor/evidencias`, que é esta pasta (D:\Lab-artefatos\t9-trabalho\claude-c3\execucao);
- `AV=/home/revisor/aval`, `T=$AV/testes`, `O=$AV/out`, `SRC=$AV/foremost-ng-bb812a22/src`.

O roteiro seguido é o da etapa anterior (passos P1–P34). Os passos não previstos estão marcados [FORA DO ROTEIRO]. Este documento não decide selos.

Classificação dos desvios:
- D0: procedimento dos autores, sem alteração.
- D1: ajuste de ambiente.
- D2: passo ou entrada proposta pelo revisor.
- D3: teste externo, com dados de terceiros.

## 1. Ambiente observado

| Item | Valor observado | Evidência |
|---|---|---|
| SO | Ubuntu 24.04.2 LTS (noble), kernel 6.18.33.2-microsoft-standard-WSL2, x86_64 | P1_ambiente.txt |
| Recursos | 16 vCPU, 7,6 GiB de RAM, 951 GB livres | P1_ambiente.txt |
| Estado inicial | sudo, unzip e man-db instalados; sem gcc, make, git, curl, file e python3 | P1_ambiente.txt |
| Dependências dos autores (Dockerfile:5) | gcc 13.3.0 (pacote 4:13.2.0-7ubuntu1), make 4.3, git 2.43.0, libssl-dev 3.0.13-0ubuntu3.5, libcurl4-openssl-dev 8.5.0-2ubuntu10.6 | P2_versoes.txt |
| Validadores (D1) | file 5.45, xxd 9.1, binutils/readelf 2.42, gcc-multilib 13.2, clang/llvm/lld 18.1.3 (llvm-lipo-18, ld64.lld-18), python3 3.12.3, python-evtx 0.8.1 (venv) | P8_versoes.txt |
| Artefato | /home/revisor/artefato.zip, SHA-256 955c770e…8e0a, comentário bb812a22cb06ef87b5a2d877dfb6f40eb12d460d | P3_zip.txt |
| Binário compilado | src/foremost-ng com 87.200 bytes, SHA-256 c479c4c4…a5a6, instalado em /usr/local/bin | P6_install.log |
| Chave do VirusTotal | presente no ambiente (64 caracteres); o valor não foi impresso. Nenhum arquivo de evidência contém a chave (grep -rlF retornou 0 arquivos) | verificação final |

Downloads de terceiros (D3):

| Item | URL | Tamanho | SHA-256 |
|---|---|---|---|
| DFTT nº 11 | https://prdownloads.sourceforge.net/dftt/11-carve-fat.zip?download | 11.596.213 B | 0c5e850a29f5811a4861a8d75404f7c45ab1b4526981414c7f86d223d5a71b67 |
| Imagem extraída do zip DFTT nº 11 | — | 64.979.456 B | 83585232e908529286f1ff04c43b4d858604875c733183a9e3b44a07ff818d26 |
| python-evtx (clone --depth 1, commit c0007441657899c39180de10a2be1a0e43dbeaf9), tests/data/system.evtx | https://github.com/williballenthin/python-evtx | 1.118.208 B | ccb83cfefc9038017224cd97b800b66e248fe14529649ddf47907e5a2021449e |
| python-evtx, tests/data/security.evtx | mesmo repositório | 2.166.784 B | 5f29a03cf8c1b4bfbd82c4074ccc81ecfe85d7ee15375afc352ed5025c9a4d8d |
| EICAR | https://secure.eicar.org/eicar.com | 68 B | 275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f |
| Clone do repositório dos autores | https://github.com/cristianzsh/foremost-ng.git | — | HEAD inicial 09ad68b398ded9d7b68043c07028850284fcc318 |

Sobre a imagem DFTT: o MD5 0069813c892a462f88dc6d376624f7d9 confere com o publicado na página do DFTT. Sobre o clone: o HEAD inicial ficou 2 commits à frente; depois de `git checkout` para bb812a22, o conteúdo é igual ao do zip, exceto pelos fins de linha (o zip tem CRLF e o clone tem LF).

Scripts auxiliares do revisor, salvos nesta pasta: `monta.sh` (monta imagens), `valida_evtx.py` (validador EVTX) e `vt_consulta.py` (consulta ao VT só por hash). Os hashes de todas as evidências estão em `SHA256SUMS_evidencias.txt`.

## 2. Passos executados

Status possíveis: sucesso, falha, inconclusivo, bloqueado, não executado. Nas colunas de resultado, "rc" é o código de saída do comando.

| Passo | Comando exato (núcleo) | Resultado esperado | Resultado observado (trecho, rc) | Evidência | Status | Desvio |
|---|---|---|---|---|---|---|
| P1 | `{ date -u; uname -a; cat /etc/os-release; nproc; free -h; df -h $HOME; …; command -v gcc make git curl file python3; } > $EV/P1_ambiente.txt` | Ubuntu 24.04 x86_64 | Ubuntu 24.04.2, x86_64. rc=1 só porque `command -v` não achou ferramentas que ainda não estavam instaladas | P1_ambiente.txt | sucesso | D2 |
| P2 | `sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev` | pacotes instalados (Dockerfile:3-5) | rc=0; os 5 pacotes com status "ii" | P2_apt.log, P2_versoes.txt | sucesso | D0 (comando do Dockerfile, rodado fora do docker build; o README não lista dependências para Linux) |
| P3-A | `sha256sum artefato.zip; unzip -z artefato.zip; unzip -q artefato.zip -d $AV; sha256sum README.md src/Makefile …` | hash 955c770e… e commit bb812a22; README ff3414f0…; Makefile ce9da14a… | os três hashes conferem; unzip rc=0; existe só src/Makefile, nenhum Makefile na raiz | P3_zip.txt | sucesso | D1 |
| P3-B | `git clone https://github.com/cristianzsh/foremost-ng.git; git checkout bb812a22…; diff -r --strip-trailing-cr` | HEAD = bb812a22 | clone rc=0; HEAD inicial 09ad68b; checkout rc=0; "IDENTICO ao zip (exceto fins de linha CR)" | P3_clone.log | sucesso | D0 (clone) + D1 (checkout) |
| P4 | `cd $AV/foremost-ng-bb812a22 && make`, repetido na raiz do clone | compilação (artigo, p.6: "cd foremost-ng / make") | `make: *** No targets specified and no makefile found.  Stop.` rc=2, nos dois diretórios | P4_make_raiz.log | falha | D0 |
| P5 | `cd $SRC && make` | binário foremost-ng (README:28,33) | rc=0; 2 avisos `-Wunused-result` (realpath, state.c:95 e 121); binário de 87.200 B | P5_make.log | sucesso | D0 |
| P6 | `cd $SRC && sudo make install` | binário disponível no sistema (artigo, p.7) | rc=0; /usr/local/bin/foremost-ng, /usr/share/man/man8/foremost-ng.8.gz e /usr/local/etc/foremost.conf instalados | P6_install.log | sucesso | D0 |
| P7 | (Dockerfile) | — | não há Docker dentro do contêiner; os passos do Dockerfile foram reproduzidos em P2, P5 e P6 | — | não executado | — |
| P8 | `sudo apt-get install -y file xxd binutils gcc-multilib clang llvm lld python3 python3-venv ca-certificates curl; python3 -m venv $AV/venv; $AV/venv/bin/pip install python-evtx` | validadores instalados | apt rc=0; pip rc=0 (python-evtx 0.8.1). Os nomes são llvm-lipo-18 e ld64.lld-18, sem versão sem sufixo | P8_valid.log, P8_versoes.txt | sucesso | D1 |
| P9 | criação e autoteste de `monta.sh` | gera a imagem e o manifesto e detecta sobreposição | imagem e manifesto corretos; sobreposição detectada (rc=1, como esperado) | monta.sh | sucesso | D2 |
| P10 | `foremost-ng; foremost-ng -h; foremost-ng -V` | ajuda e versão 1.5.7 | ajuda com -t, -i, -o, -x e -v; -V imprime "1.5.7"; rc=0 nos três | P10_uso.txt | sucesso | D0 |
| P11 | `man foremost-ng \| col -b` | página de manual | rc=0, 196 linhas, com seção EXAMPLES (por exemplo `foremost-ng -x image.dd`). A lista "BUILT-IN FORMATS" não menciona evtx, elf, macho nem script | P11_man.txt | sucesso | D0 |
| P12 | `foremost-ng -i $T/dftt/11-carve-fat/11-carve-fat.dd -o $O/F_dftt` | pasta por formato, arquivos NNNNNNNN.ext e audit.txt (artigo §4.1-4.2) | rc=0, cerca de 1,3 s; "14 FILES EXTRACTED". Contra o gabarito do DFTT: 10 dos 15 arquivos com MD5 idêntico (3 JPG, GIF, MOV, 2 PDF, 2 WMV, ZIP); haxor2.jpg (corrompido de propósito) não foi extraído; DOC, XLS, PPT e WAV foram extraídos com tamanho diferente (o PPT de 11.264 B saiu com 7.212.032 B) | P12_run.log, P12_audit.txt, P12_comparacao.tsv, P12_gabarito.tsv, P12_file_md5.txt, P12_fonte.txt | sucesso | D3 (fonte citada pelos autores, artigo p.7; imagem escolhida pelo revisor) |
| P13 | cópia de system.evtx e security.evtx (python-evtx) para e1.evtx e e2.evtx; `evtx_dump e1.evtx` | originais legíveis | `evtx_dump` rc=1: `ModuleNotFoundError: No module named 'scripts'`. [FORA DO ROTEIRO] validação refeita com `valida_evtx.py` (API do Evtx): e1 com 9 chunks no cabeçalho e 1.601 registros; e2 com 26 chunks e 2.261 registros; 0 erros | P13_fonte.txt, P13_ref.txt, valida_evtx.py | sucesso (na 2ª tentativa) | D3 + D2 |
| P14 | `monta.sh img_A.dd 64 e1.evtx:2048`; `monta.sh img_B.dd 64 e1.evtx:2048 e2.evtx:4232` | manifestos | gerados | P14_img_A/B.manifesto.tsv | sucesso | D2/D3 |
| P15 | `foremost-ng -v -t evtx -i img_A.dd -o $O/C1_A` (idem para B) | `00002048.evtx`; em B também `00004232.evtx` | rc=0. A: `00002048.evtx` com 66.060.288 B. B: `00002048.evtx` com 1.118.208 B e `00004232.evtx` com 64.942.080 B | P15_A.log, P15_B.log, P15_*_audit.txt | sucesso | D3 |
| P16 | `cmp -n`, `xxd`, `valida_evtx.py` em cada arquivo extraído | legível, com a mesma contagem de registros | todos começam com "ElfFile"; prefixo idêntico ao original; 1.601 / 1.601 / 2.261 registros, 0 erros. Tamanhos: A = 66.060.288 (original 1.118.208); B1 = 1.118.208 (arquivo idêntico); B2 = 64.942.080 (original 2.166.784) | P16_valida.txt | sucesso (legibilidade); tamanho diferente do original em 2 de 3 | D3 |
| P17 | criação de s1.sh, s2.py, s3.ps1, n1.sh (só comentários, 46 B) e n2.sh (17 B); `monta.sh img_c2.dd 8 …` | manifesto | gerado | P17_amostras.txt, P17_img_c2.manifesto.tsv | sucesso | D2 |
| P18 | `foremost-ng -v -t script -i img_c2.dd -o $O/C2` | 3 positivos e 0 negativos | rc=0; "4 FILES EXTRACTED": 00000100, 00000200, 00000300 e 00000400 (.script); 00000500 não foi extraído | P18.log, P18_audit.txt | falha (n1.sh, só com comentários, foi extraído) | D2 |
| P19 | `cmp` entre cada arquivo extraído e o original; `head -1` | positivos idênticos, com shebang | s1, s2 e s3 idênticos (linhas 1: `#!/bin/bash`, `#!/usr/bin/env python3`, `#!/usr/bin/env pwsh`); n1 também idêntico; n2 ausente | P19.txt | ver P18 | D2 |
| P20 | `clang -target {x86_64,arm64,i386}-apple-macos… -c h.c`; `llvm-lipo-18 -create`; `ld64.lld-18 … -e _main` | fat, thin de 32 bits e thin de 64 bits | objetos t64.o, t64a.o, t32.o e fat.o gerados. Executável na 1ª tentativa: `undefined symbol: _puts`, rc=1. [FORA DO ROTEIRO] 2ª tentativa com `-undefined dynamic_lookup`: t64.exe, t64a.exe e fat.exe gerados, rc=0. Executável i386: `missing or unsupported -arch i386`, rc=1 | P20_gera.txt, P20_ref.txt | sucesso (sem executável i386) | D2 |
| P21 | `monta.sh img_c3.dd 16 fat.o:100 t32.o:1000 t64.o:2000 fat.exe:3000 t64.exe:4000`; `foremost-ng -v -t macho -i img_c3.dd -o $O/C3` | 00000100, 00001000, 00002000, 00003000 e 00004000 (.macho) | rc=0; "2 FILES EXTRACTED": só 00000100.macho e 00003000.macho (os dois fat) | P21.log, P21_audit.txt, P21_img_c3.manifesto.tsv | falha (nenhum thin extraído) | D2 |
| P21b | [FORA DO ROTEIRO] `foremost-ng -v -a -t macho -i img_c3.dd -o $O/C3_diag_a`, para saber se os cabeçalhos thin são localizados | — | rc=0; "(Header dump)" de 10 MB nos blocos 1000, 2000 e 4000 e nas fatias dentro dos fat (108, 132, 3008, 3064); como arquivos de fato, só os dois fat | P21b_diag.log | sucesso (diagnóstico) | D2 |
| P22 | `file`, `llvm-objdump --macho --private-headers`, `llvm-lipo-18 -info`, `cmp` | reconhecido pelas ferramentas e prefixo idêntico | 00000100.macho e 00003000.macho: "Mach-O universal binary with 2 architectures", objdump rc=0, lipo "x86_64 arm64", arquivos IDÊNTICOS aos originais. Thin: "NAO EXTRAIDO" | P22.txt | sucesso para fat; falha para thin | D2 |
| P23 | `gcc -O0 -o e64 h.c; gcc -m32 -O0 -o e32 h.c; cp /usr/bin/ls ls64` | ELF32 e ELF64 de referência | gerados; os dois executáveis imprimem "ola foremost-ng" | P23_ref.txt | sucesso | D2 |
| P24 | `monta.sh img_c4.dd 16 e64:100 e32:1000 ls64:2000`; `foremost-ng -v -t elf -i img_c4.dd -o $O/C4` | 00000100, 00001000 e 00002000 (.elf) | rc=0; os 3 arquivos .elf, com 12.304 / 12.296 / 139.896 B (originais: 15.960 / 14.936 / 142.312 B) | P24.log, P24_audit.txt | sucesso | D2 |
| P25 | `file`; `readelf -h -l`; `readelf -S`; `cmp`; execução dos arquivos extraídos | readelf -h -l sem erro e classe correta | `readelf -h -l` rc=0, com ELF64/ELF32 e Machine corretos, mas imprime `readelf: Error: Reading 1984 bytes extends past end of file for section headers` (1160 no ELF32). O `file` diz "missing section headers". O prefixo é idêntico ao original. Os arquivos extraídos executam: e64 e e32 imprimem "ola foremost-ng", e ls64 lista /etc/hostname; rc=0 | P25.txt | inconclusivo (rc=0 e cabeçalhos lidos, mas há mensagem de erro sobre a tabela de seções) | D2 |
| P26 | `monta.sh img_misto.dd 64 e64:100 zlib1.dll:1000 e1.evtx:2048`; `foremost-ng -t evtx,elf,exe -i img_misto.dd -o $O/F_t` | só evtx, elf e exe/dll (artigo §4.1) | rc=0; subpastas elf (00000100.elf) e evtx (00002048.evtx, 66.060.288 B); nada em exe/dll | P26.log, P26_audit.txt | falha (zlib1.dll não extraída) | D2/D3 |
| P26b | [FORA DO ROTEIRO] `foremost-ng -a -t exe -i img_misto.dd -o $O/P26b_diag`; `file windows_dlls/*` | — | só "(Header dump)" de 2 MB (blocos 1000, 1101, 1123, 1124, 1124_1, 1178). As 16 DLLs de windows_dlls são "PE32+ … x86-64" | P26b_diag.txt | sucesso (diagnóstico) | D2 |
| P27 | [FORA DO ROTEIRO, substitui as DLLs do roteiro porque PE32+ não é extraído] download do EICAR; consulta prévia ao VT por hash de candidatos; config do revisor `c5.conf` (`com y 68 X5O!P%@AP`); `monta.sh img_c5.dd 8 zcat:100 e64:1000 eicar.com:2000` | imagem com arquivos conhecidos pelo VT | VT: EICAR malicious=65/undetected=2; zcat undetected=61; zgrep 60; gunzip 61; zlib1.dll 72. Imagem gerada | P27_*.txt/.tsv/.conf | sucesso | D2/D3 |
| P28 | `env -u VT_API_KEY foremost-ng -x -t script,elf -c c5.conf -i img_c5.dd -o $O/C5_sem` | aviso e extração sem consulta (artigo, p.7) | rc=0; 3 vezes "Error: VT_API_KEY environment variable is not set." (uma por arquivo); 3 arquivos extraídos; coluna VT "Clean (0)" nos 3 | P28.log, P28_audit.txt | sucesso | D3 |
| P29 | `VT_API_KEY=chave-invalida-teste foremost-ng -x -t script,elf -c c5.conf -i img_c5.dd -o $O/C5_inv` | aviso e extração (artigo, p.7) | rc=0; nenhuma mensagem de aviso ou de erro; 3 arquivos extraídos; coluna VT "Clean (0)" nos 3 | P29.log, P29_audit.txt | falha (sem aviso) | D3 |
| P30 | `foremost-ng -x -t script,elf -c c5.conf -i img_c5.dd -o $O/C5_ok` (chave válida); `sha256sum`; `vt_consulta.py <hashes>` | hash calculado, VT consultado e contagens registradas | rc=0. Audit: 00000100.script "Clean (61)"; 00001000.elf "Clean (0)"; 00002000.com "Malicious (65)". Hashes extraídos: script f0b4d86b… (= zcat), com 275a021b… (= EICAR), elf a1e39793… (≠ e64). Referência VT 16:01-16:02 UTC: zcat 0/61; elf HTTP 404 NotFound; EICAR 65/2; e64 original HTTP 404. O audit não traz hashes e não foi gerado recovery.log | P30.log, P30_audit.txt, P30_hashes.txt, P30_ref.tsv, P31.txt | sucesso | D3 |
| P31 | busca por evidence2.dd em $HOME e no sistema de arquivos do contêiner | 2.845.109.643 B | arquivo inexistente; o coordenador informou que não está disponível | P31.txt | bloqueado | — |
| P32 | `./foremost-ng -v -x evidence2.dd` | tabela da Fig. 2 | — | — | não executado (depende de P31) | — |
| P33 | comparação com a Fig. 2 | 12 nomes e offsets | — | — | não executado | — |
| P34 | `sha256sum` de todas as evidências; checagem de vazamento da chave | pacote íntegro e sem a chave | SHA256SUMS_evidencias.txt gerado; 0 arquivos contêm a chave | SHA256SUMS_evidencias.txt | sucesso | D2 |

## 3. Fatos observados por reivindicação

### C1: EVTX
- Com `-t evtx`, o arquivo extraído fica em `evtx/<bloco>.evtx`, com nome = offset/512 (P15).
- Em todos os casos o arquivo começa com "ElfFile", e os bytes iniciais são idênticos aos do original (P16).
- Os três arquivos extraídos foram lidos pela biblioteca python-evtx 0.8.1 com o mesmo número de chunks e de registros do original (1.601 e 2.261) e 0 erros de renderização (P16).
- EVTX isolado e seguido de zeros (img_A): o arquivo extraído tem 66.060.288 B, do offset até o fim da imagem de 64 MiB; o original tem 1.118.208 B.
- Dois EVTX consecutivos (img_B): o primeiro sai idêntico ao original (1.118.208 B, mesmo SHA-256); o segundo vai até o fim da imagem (64.942.080 B, contra 2.166.784 B do original).
- No offset 0x18 dos originais estão os valores 0x34D8 (13.528) em e1 e 0x08B2 (2.226) em e2. São iguais ao "header_next_record_number" reportado pelo python-evtx, enquanto o "chunk_count" do cabeçalho é 9 e 26 (P13, P16).
- O script `evtx_dump` instalado pelo pip falhou por erro de empacotamento (`ModuleNotFoundError: scripts`). A validação usou a API da mesma biblioteca (P13).

### C2: scripts
- Os scripts bash (64 B), python (60 B) e PowerShell com shebang `#!/usr/bin/env pwsh` (48 B) foram extraídos byte a byte idênticos, como `script/<bloco>.script`, com o shebang na primeira linha (P18, P19).
- O controle de 17 B (`#!/bin/sh\necho a\n`) não foi extraído (P18).
- O controle de 46 B formado só por shebang e linhas de comentário iniciadas por `#` foi extraído (00000400.script) (P18, P19).
- O sufixo de saída é `.script`; não foi gerado nenhum `.sh` (P18).
- Em P30, o script de sistema `/usr/bin/zcat` (1.984 B) também saiu idêntico (mesmo SHA-256 f0b4d86b…).

### C3: Mach-O
- Universais (fat) de objetos (21.208 B) e de executáveis x86_64+arm64 (82.752 B): extraídos idênticos ao original e reconhecidos por `file`, `llvm-objdump` e `llvm-lipo` (P21, P22).
- Thin de 32 bits (objeto i386, 4.768 B), thin de 64 bits (objeto x86_64, 4.880 B) e executável thin de 64 bits (x86_64, 20.768 B): nenhum foi extraído (P21).
- Com a opção `-a`, a ferramenta registra "(Header dump)" nos offsets desses arquivos thin e nas fatias internas dos fat. Ou seja, os cabeçalhos são localizados, mas não são gravados como arquivos extraídos (P21b).
- Não foi possível gerar um executável Mach-O i386 com o ld64.lld-18 ("missing or unsupported -arch i386") (P20).
- As amostras foram geradas localmente com clang/lld 18; não se usaram binários produzidos no macOS.

### C4: ELF
- ELF64 (PIE do gcc, 15.960 B), ELF32 (gcc -m32, 14.936 B) e /usr/bin/ls do Ubuntu 24.04 (142.312 B) foram extraídos como `elf/<bloco>.elf` (P24).
- Os tamanhos extraídos (12.304 / 12.296 / 139.896 B) são menores que os originais, e os bytes são idênticos ao prefixo do original (P25).
- `readelf -h -l` retorna rc=0 e mostra a classe (ELF64/ELF32), a máquina e os cabeçalhos de programa. Também imprime "Error: Reading … bytes extends past end of file for section headers". O `file` reporta "missing section headers at …" (P25).
- Os três arquivos extraídos executam no contêiner: os dois de teste imprimem "ola foremost-ng" e o `ls` lista um arquivo; rc=0 (P25).
- No exemplo do artigo com `-t evtx,elf,exe` (P26), o ELF e o EVTX foram extraídos; a DLL PE32+ (zlib1.dll) não. Com `-a`, só aparecem "(Header dump)" (P26b).

### C5: VirusTotal
- Sem VT_API_KEY: a extração termina (rc=0); é impressa uma linha "Error: VT_API_KEY environment variable is not set." por arquivo, e o audit grava "Clean (0)" na coluna VT (P28).
- Com uma chave inválida: a extração termina (rc=0); não aparece nenhuma mensagem, e o audit grava "Clean (0)" (P29).
- Com a chave válida (P30):
  - EICAR (extraído por uma entrada de configuração do revisor): "Malicious (65)". Consulta direta ao VT pelo mesmo SHA-256: malicious=65, undetected=2.
  - zcat (extraído como script): "Clean (61)". VT: malicious=0, undetected=61.
  - ELF extraído (hash a1e39793…, diferente do e64 original): "Clean (0)". VT: HTTP 404 NotFound.
- Os SHA-256 dos arquivos extraídos (P30_hashes.txt) são iguais aos dos originais no script e no EICAR, e diferentes no ELF.
- O audit.txt não traz hash nenhum, e nenhum recovery.log foi gerado (P31.txt, primeira parte).

### C6: Figura 2
- evidence2.dd não está no artefato nem no contêiner; segundo o coordenador, não foi encontrado publicamente e os autores não responderam (P31).
- A execução da Fig. 2 e a comparação de nomes e offsets não foram realizadas (P32 e P33).
- Fato relacionado: nesta versão, uma DLL PE32+ não foi extraída (P26, P26b). A Fig. 2 lista 6 arquivos .exe.

## 4. Observações gerais
- O procedimento de instalação do artigo (make na raiz) termina com "no makefile found". O do README (make em src/) compila sem erro, só com 2 avisos (P4, P5).
- A página de manual instalada lista os formatos legados e exemplos de uso, mas não menciona os formatos novos evtx, elf, macho e script (P11).
- No teste com a imagem DFTT nº 11 (formatos legados), 10 dos 15 arquivos do gabarito foram recuperados com MD5 idêntico (P12).
- Tempo total de execução no contêiner: cerca de 16 minutos, das 15:46 às 16:02 UTC.
