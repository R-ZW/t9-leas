# Registro factual da execução: Foremost-NG (commit bb812a22)

Este documento registra apenas fatos observados na execução, sem juízo sobre os selos.

- **Data:** 2026-10-24, entre 15:47:05 e 16:00:12 UTC, conforme os timestamps de P1.log e P32.log.
- **Onde rodou:** tudo dentro do contêiner `t9-claude-c2`, chamado com `docker exec t9-claude-c2 bash -lc '...'`.
- **Onde estão as evidências:** em `/home/revisor/evidencias`, que corresponde a esta pasta. Os hashes de todos os arquivos de evidência estão em `SHA256SUMS.txt`.
- **Como os logs foram gerados:** pelo registrador `scripts/reg.sh`, que grava data, diretório, comando, saída e código de saída. Ele foi adaptado para gravar em `~/evidencias` em vez de `~/aval/evidencias`.

Classificação de desvio usada na tabela:
- **D0:** procedimento dos autores, sem alteração.
- **D1:** ajuste de ambiente.
- **D2:** passo ou entrada proposta pelo revisor.
- **D3:** teste externo, com dados de terceiros.

## 1. Ambiente observado

| Item | Valor observado | Evidência |
|---|---|---|
| Sistema | Ubuntu 24.04.2 LTS (noble) | P1.log |
| Kernel e arquitetura | 6.18.33.2-microsoft-standard-WSL2, x86_64 | P1.log |
| Ordem de bytes | Little Endian | P1.log |
| CPU e RAM | 16 vCPU, 7,6 GiB de RAM | P1.log |
| Usuário | revisor (uid 1001), com sudo sem senha (`sudo_ok`) | P1.log |
| gcc | 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04) | P2.log |
| GNU Make | 4.3 | P2.log |
| git | 2.43.0 | P2.log |
| OpenSSL | 3.0.13 | P2.log |
| libssl-dev | 3.0.13-0ubuntu3.5 | P2.log |
| libcurl4-openssl-dev | 8.5.0-2ubuntu10.6 | P2.log |
| curl | 8.5.0 | P9.log |
| Python | 3.12.3 | P9.log |
| file | 5.45 | P9.log |
| readelf (binutils) | 2.42 | P9.log |
| python-evtx | 0.8.1, num venv | P9.log |
| Artefato | `/home/revisor/artefato.zip`, 7.252.858 bytes, SHA-256 955c770e…8e0a, comentário do ZIP bb812a22cb06ef87b5a2d877dfb6f40eb12d460d | P3.log |
| VT_API_KEY | definida, com 64 caracteres. O valor não foi impresso. Ao final, uma busca pelo valor nas evidências e nas saídas não o encontrou. | P25.log |

## 2. Tabela de passos

| Passo | Comando exato (resumo fiel; o comando completo está na linha `# cmd:` do log) | Resultado esperado | Resultado observado (trecho, exit) | Evidência | Status | Desvio |
|---|---|---|---|---|---|---|
| P1 | `mkdir -p ~/aval/{bin,amostras,imagens,saidas}`; `reg.sh P1 bash -c "uname -a; cat /etc/os-release; nproc; free -h; df -h ~; lscpu \| grep -i 'byte order'; id; sudo -n true && echo sudo_ok; which gcc make git curl file python3 unzip man"` | Ubuntu 24.04, little-endian | Ubuntu 24.04.2, "Little Endian", sudo_ok. `which` só achou unzip e man. exit=1, vindo do `which` para as ferramentas ausentes | P1.log | sucesso | D2 |
| P2 | `sudo apt-get update && sudo apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev` (comandos do Dockerfile:3-6) | pacotes instalados | gcc 13.3.0, make 4.3, git 2.43.0, OpenSSL 3.0.13; exit=0 | P2.log | sucesso | D0 |
| P3 | `sha256sum ~/artefato.zip; unzip -q ~/artefato.zip -d ~/aval; mv foremost-ng-bb812a22 foremost-ng; sha256sum README.md Dockerfile src/...` | hash do ZIP e dos arquivos iguais aos do índice do artefato.txt | ZIP 955c770e…; os 13 arquivos conferidos coincidem com o índice (README ff3414f0…, extract.c 4f81160c…, helpers.c fffa904b…, man page c77ca018…); exit=0 | P3.log | sucesso | D1 |
| P3b | `git clone https://github.com/cristianzsh/foremost-ng.git; git cat-file -t bb812a22…; git diff --stat bb812a22… HEAD` | o commit existe no repositório | HEAD atual 09ad68b3…. O commit bb812a22 existe ("Add Foremost-NG Dockerfile"). Diferença para o HEAD: CITATION.cff (+36) e README.md (+19). exit=0. O código avaliado é o do ZIP. | P3b.log | sucesso | D0 (clone) + D2 (conferência) |
| P4 | `cd ~/aval/foremost-ng/src && make` | binário foremost-ng gerado | exit=0, binário de 87.200 bytes. Dois avisos `-Wunused-result` (realpath em state.c:95 e :121) | P4.log | sucesso | D0 |
| P5 | `sudo make install` | binário, manual e configuração instalados | /usr/local/bin/foremost-ng, /usr/share/man/man8/foremost-ng.8.gz e /usr/local/etc/foremost.conf criados; exit=0 | P5.log | sucesso | D0 |
| P6 | `foremost-ng -h; foremost-ng -V; MANPAGER=cat man foremost-ng` | ajuda com -x, versão 1.5.7, manual | ajuda lista "-x Enable VirusTotal scan (needs API key)"; `-V` → "1.5.7"; manual exibido, com seção EXAMPLES (por exemplo "foremost-ng -x image.dd"). A seção BUILT-IN FORMATS do manual não lista elf, macho, evtx nem script. exit=0 | P6.log, P6-manpage.txt | sucesso | D0 |
| P7 | `curl -sSL -o dftt11.zip "http://prdownloads.sourceforge.net/dftt/11-carve-fat.zip?download"; unzip dftt11.zip; md5sum 11-carve-fat.dd` | imagem DFTT #11 com MD5 0069813c… (publicado na página do DFTT) | ZIP de 11.596.213 bytes, SHA-256 0c5e850a…1b67. Imagem 11-carve-fat.dd de 64.979.456 bytes, MD5 0069813c892a462f88dc6d376624f7d9 (igual ao publicado), SHA-256 83585232…8d26. exit=0. O pacote `curl` foi instalado aqui, antes de P9. | P7.log, P7-dftt-test11.html | sucesso | D3 |
| P8 | `foremost-ng -i ~/aval/amostras/11-carve-fat/11-carve-fat.dd -o ~/aval/saidas/P8` | diretório de saída, subdiretórios por formato, NNNNNNNN.ext, registro com offsets | exit=0; "14 FILES EXTRACTED" (jpg=3, gif=1, wmv=2, mov=1, rif=1, ole=3, zip=1, pdf=2); audit.txt com tamanho e offset. 10 dos 15 arquivos listados pelo DFTT foram extraídos com MD5 idêntico. Nenhum recovery.log foi gerado. O pacote `file` foi instalado aqui, antes de P9. | P8.log, P8-audit.txt, P8-arquivos.txt, P8-validacao.txt | sucesso | D3 |
| P9 | `sudo apt-get install -y file python3 python3-venv curl gcc-multilib; python3 -m venv ~/aval/venv; pip install python-evtx` | ferramentas de validação instaladas | python-evtx 0.8.1; exit=0 | P9.log | sucesso | D1 |
| P10 | `sha256sum ~/aval/bin/reg.sh mkimg.sh mkfat.py` (scripts do roteiro) | scripts registrados | hashes a172414e…, 39d28cf5…, 3ba8c3ba…; exit=0 | P10.log, scripts/ | sucesso | D2 |
| P11 | `curl -sSL -o a.evtx …/python-evtx/master/tests/data/system.evtx; curl -sSL -o b.evtx …/security.evtx` | arquivos com magic "ElfFile" | a.evtx 1.118.208 B, SHA-256 ccb83cfe…449e; b.evtx 2.166.784 B, SHA-256 5f29a03c…4d8d; ambos começam com "ElfFile\0"; exit=0 | P11.log | sucesso | D3 |
| P12 | `mkimg.sh c1.dd a.evtx b.evtx; foremost-ng -t evtx -i c1.dd -o saidas/P12` | 2 .evtx nos blocos 2048 e 4480 | 00002048.evtx (1.245.184 B) e 00004480.evtx (3.342.336 B); exit=0 | P12.log, P12-audit.txt, P12-manifest.csv | sucesso | D3 |
| P13 | `cmp -n …; evtx_dump <arquivo>` | mesmo número de eventos no original e no extraído | os prefixos são idênticos aos originais. O `evtx_dump` do python-evtx 0.8.1 falhou para todos os arquivos, inclusive os originais: "ModuleNotFoundError: No module named 'scripts'". exit=0 do laço | P13.log | falha (do validador, não do artefato) | D2 |
| P13b [FORA DO ROTEIRO] | `venv/bin/python conta_evtx.py a.evtx 00002048.evtx b.evtx 00004480.evtx` (usa a biblioteca Evtx.Evtx). Justificativa: o ponto de entrada do pacote está quebrado, e a biblioteca é a mesma ferramenta. | mesmo número de registros | a.evtx 9 chunks, 1601 registros, 1601 com XML; 00002048.evtx igual. b.evtx 26 chunks, 2261 registros, 2261 com XML; 00004480.evtx igual. erro=-; exit=0 | P13b.log, scripts/conta_evtx.py | sucesso | D2 |
| P14 | criação de s1.sh, s2.py, s3.ps1, neg_curto.sh e neg_coment.sh com `printf` | tamanhos conforme o roteiro | 100, 94, 94, 18 e 78 bytes; exit=0 | P14.log | sucesso | D2 |
| P15 | `mkimg.sh c2.dd s1.sh s2.py s3.ps1 neg_curto.sh neg_coment.sh; foremost-ng -t script -i c2.dd -o saidas/P15` | 3 scripts extraídos e nenhum controle | 4 arquivos extraídos: blocos 2048, 2304, 2560 e 3072. O bloco 3072 é neg_coment.sh. neg_curto.sh não foi extraído. exit=0 | P15.log, P15-audit.txt, P15-manifest.csv | falha (critério do roteiro: o controle negativo de só comentários foi extraído) | D2 |
| P16 | `head -1 *; sha256sum *` em saidas/P15/script | hashes iguais aos originais, primeira linha com shebang | os SHA-256 dos 3 scripts são idênticos aos originais (ea56ffad…, efd87339…, 128bf90a…) e a primeira linha é o shebang. O 4.º arquivo tem o hash de neg_coment.sh (ac91dc9c…). exit=0 | P16.log | sucesso (para os 3 scripts) | D2 |
| P17 | `curl -sSL -o m64_x86 https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-macos-amd64` (idem para jq-macos-arm64) | Mach-O 64-bit, bytes cf fa ed fe | m64_x86 851.328 B, SHA-256 4155822b…7443, "Mach-O 64-bit x86_64 executable". m64_arm 807.984 B, SHA-256 0bbe619e…2e8a, "Mach-O 64-bit arm64 executable". Ambos começam com cf fa ed fe; exit=0 | P17.log | sucesso | D3 |
| P18 | `python3 mkfat.py fat.bin m64_x86 m64_arm` | universal com 2 arquiteturas | `file`: "Mach-O universal binary with 2 architectures"; 1.676.336 B; SHA-256 12a05b7d…f41a; exit=0 | P18.log | sucesso | D2 |
| P19 | `foremost-ng -t macho -i c3_thin.dd -o saidas/P19_thin`; `foremost-ng -t macho -i c3_fat.dd -o saidas/P19_fat` | 2 thin e 1 fat extraídos | P19_thin: "0 FILES EXTRACTED". P19_fat: "1 FILES EXTRACTED" (00002048.macho). exit=0 nas duas | P19.log, P19_thin-audit.txt, P19_fat-audit.txt, P19-manifests.csv | falha (parte thin) | D3 |
| P20 | `file`, `sha256sum` e `cmp` dos extraídos | os 3 reconhecidos como Mach-O, com hash igual | fat extraído idêntico ao original (SHA-256 12a05b7d…, "fat_identico"; `file`: universal com 2 arquiteturas). Nenhum arquivo thin extraído (P19_thin só tem audit.txt). exit=0 | P20.log | falha (parte thin) | D2 |
| P20b [FORA DO ROTEIRO] | `foremost-ng -a -t macho -i c3_thin.dd -o saidas/P20b`. Justificativa: distinguir assinatura não encontrada de parser que rejeitou o arquivo; `-a` grava os cabeçalhos encontrados sem verificação. | – | "(Header dump)" nos offsets 1048576 e 1966080. `file`: Mach-O 64-bit x86_64 e arm64. exit=0 | P20b.log, P20b-audit.txt | sucesso (diagnóstico) | D2 |
| P21 | `gcc -m32 -o e32 h.c; gcc -o e64 h.c; cp /usr/bin/ls e64_ls` | ELF 32-bit e ELF 64-bit | e32 "ELF 32-bit LSB pie executable, Intel 80386" (14.904 B); e64 "ELF 64-bit … x86-64" (15.776 B); e64_ls 142.312 B; exit=0 | P21.log | sucesso | D2 |
| P22 | `mkimg.sh c4.dd e32 e64 e64_ls; foremost-ng -t evtx,elf,exe -i c4.dd -o saidas/P22` | 3 .elf nos blocos 2048, 2304 e 2560 | 00002048.elf (12 KB), 00002304.elf (12 KB), 00002560.elf (136 KB); "3 FILES EXTRACTED"; exit=0 | P22.log, P22-audit.txt, P22-manifest.csv | sucesso | D2 |
| P23 | `cmp -n`, `file`, `readelf -h -l -S`, `readelf -s` | cabeçalhos legíveis, classe correta, prefixo idêntico | prefixos idênticos. Classes ELF32/ELF64 corretas. `readelf -h` e `-l` exit=0 e listam os program headers. `readelf` também emite "Error: Reading N bytes extends past end of file for section headers". `file`: "missing section headers". Símbolos FUNC em `readelf -s`: 12 no e64 original, 0 no extraído | P23.log | sucesso (critério -h/-l), com erros de seção registrados | D2 |
| P24 | `env -u VT_API_KEY foremost-ng -x -t elf -i c4.dd -o saidas/P24` | carving feito, aviso, consulta pulada | 3 linhas "Error: VT_API_KEY environment variable is not set."; 3 ELF extraídos; coluna VT do audit "Clean (0)" nas 3 linhas; exit=0 | P24.log, P24-audit.txt | sucesso (carving e aviso); rótulo registrado como "Clean (0)" | D2 |
| P25 | `[ -n "${VT_API_KEY:-}" ] && echo definida …` | chave presente | "VT_API_KEY definida (comprimento 64)"; exit=0 | P25.log | sucesso | D1 |
| P26 | `foremost-ng -x -t elf -i c4.dd -o saidas/P26` | coluna VT preenchida | 3 ELF extraídos; VT "Clean (0)" nas 3 linhas; nenhuma mensagem de erro de curl; exit=0 | P26.log, P26-audit.txt, P26-sha256.txt | sucesso | D2 |
| P27 | `curl -s -H "x-apikey: $VT_API_KEY" https://www.virustotal.com/api/v3/files/<sha256>` para cada .elf de P26, com intervalos de 16 s | rótulo do audit igual ao resultado da API | 404 NotFoundError para os 3 SHA-256 (a55edda8…, 784e6de3…, 22b6b28b…). Audit: "Clean (0)". exit=0 | P27.log, P27_*.json | sucesso (rótulo coerente com hash desconhecido) | D3 |
| P28 | `curl -sSL -o eicar_com.zip https://secure.eicar.org/eicar_com.zip; mkimg.sh c5.dd eicar_com.zip; foremost-ng -x -t zip -i c5.dd -o saidas/P28` | "Malicious (n)" com n > 0, hash igual ao original | eicar_com.zip 184 B, SHA-256 2546dcff…edad. Extraído 00002048.zip com o mesmo SHA-256. Audit: "Malicious (62)". exit=0 | P28.log, P28-audit.txt, P28-manifest.csv | sucesso | D3 |
| P28c | conferência pela API do SHA-256 2546dcff… (comando igual ao de P27) | n igual ao do JSON | http=200; last_analysis_stats: malicious 62, suspicious 0, undetected 5, harmless 0, failure 1, type-unsupported 7; exit=0 | P28c.log, P28_2546dcff….json | sucesso | D3 |
| P29 | `unzip -l ~/artefato.zip \| grep -i -E "evidence\|\.dd$\|\.img$\|\.raw$"`; `git log --all --name-only \| grep -i -E "evidence\|\.dd$"`; `git ls-files \| grep …` | encontrar evidence2.dd | "nenhum_dd_no_artefato_zip"; nenhum arquivo com evidence ou .dd em nenhum dos 51 commits; "nenhum_dd_no_repositorio_HEAD"; exit=0. Informação do coordenador: não está disponível publicamente e os autores não responderam. | P29.log | falha (dado não encontrado) | D2 |
| P30 | `./foremost-ng -v -x evidence2.dd` (em src/) | 12 nomes e offsets da Fig. 2 | não executado: falta a entrada | – | bloqueado | – |
| P31 | `grep -n "init_builtin(state" state.c \| wc -l; grep -n "needle->type ==" extract.c \| tail -12; grep -n "extract_file(" engine.c` | organização como na Fig. 1 | 21 chamadas `init_builtin(state…)`. Cadeia `else if (needle->type == …)` em extract.c:2668-2690, com ramos para ELF, MACHO, EVTX e SCRIPT. engine.c chama `extract_file(` nas linhas 334 e 357. exit=0 | P31.log | sucesso (inspeção executada) | D2 |
| P32 | `tar czf ~/evidencias/saidas_20261024.tgz …`; depois `find ~/aval/saidas -type f -exec sha256sum` | pacote de evidências com hash | tgz criado (13.557.650 B, SHA-256 588bfe57…). Depois foi **removido** da pasta de evidências: era grande e continha o eicar_com.zip extraído, que iria para o host Windows. No lugar, P32-saidas-sha256.txt lista os 43 arquivos de saída com hash. As saídas continuam em `~/aval/saidas` no contêiner. Busca pelo valor da chave nas evidências e nas saídas: "chave_nao_encontrada_nas_evidencias". | P32.log, P32-saidas-sha256.txt, SHA256SUMS.txt | sucesso (com ajuste) | D2 |

## 3. Fatos observados por reivindicação

### C1 – EVTX
- **Entradas:** duas amostras públicas do python-evtx: system.evtx (salvo como a.evtx, 1.118.208 B) e security.evtx (salvo como b.evtx, 2.166.784 B). Ficaram nos offsets 1.048.576 e 2.293.760 da imagem c1.dd, de 5.636.096 B (P11, P12).
- **Campos do cabeçalho** (P11.log, `od`):
  - a.evtx: bytes 0x18-0x1B = d8 34 00 00 (13.528); 0x2A-0x2B = 09 00 (9).
  - b.evtx: 0x18 = b2 08 (2.226); 0x2A = 1a 00 (26).
- **Resultado do carving com `-t evtx`:** 2 arquivos.
  - 00002048.evtx tem 1.245.184 B. É exatamente a distância até o cabeçalho "ElfFile" seguinte.
  - 00004480.evtx tem 3.342.336 B, até o fim da imagem.
  - Os dois são maiores que os originais, e os bytes iniciais de cada um são idênticos ao original (`cmp -n`).
- **Leitura com a biblioteca python-evtx 0.8.1** (P13b):
  - Os extraídos têm os mesmos números de chunks (9 e 26) e de registros (1601 e 2261) dos originais.
  - Todos os registros geraram XML com `<Event `, sem exceção.
  - O utilitário de linha de comando `evtx_dump` do pacote não rodou em nenhum arquivo, nem nos originais (P13).

### C2 – Scripts
- **Entradas:** s1.sh (bash, 100 B), s2.py (python, 94 B) e s3.ps1 (pwsh, 94 B), todos com shebang. Controles: neg_curto.sh (18 B) e neg_coment.sh (78 B, só linhas de comentário depois do shebang).
- **Carving com `-t script`** (P15, P16):
  - Os 3 scripts foram extraídos com SHA-256 idêntico ao original. A primeira linha de cada um é o shebang, e a extensão é `.script`.
  - neg_curto.sh não foi extraído.
  - neg_coment.sh foi extraído (00003072.script, hash idêntico).

### C3 – Mach-O fat e thin
- **Entradas:**
  - jq 1.7.1 jq-macos-amd64 e jq-macos-arm64: Mach-O 64-bit thin, começando com cf fa ed fe.
  - fat.bin: universal binary montado pelo revisor com as duas fatias, reconhecido pelo `file` como universal com 2 arquiteturas (P17, P18).
- **c3_thin.dd com `-t macho`:** "0 FILES EXTRACTED" (P19).
- **Mesmo com `-a`** (gravar todos os cabeçalhos): o audit mostra "(Header dump)" nos dois offsets, e os arquivos despejados são reconhecidos como Mach-O x86_64 e arm64 (P20b).
- **c3_fat.dd com `-t macho`:** 1 arquivo, 00002048.macho, de 1.676.336 B, com SHA-256 idêntico ao fat.bin e reconhecido como universal com 2 arquiteturas. Não foram extraídos arquivos nos offsets das fatias internas (P19, P20).
- Não foi testado Mach-O de 32 bits.

### C4 – ELF de 32 e 64 bits
- **Entradas:** e32 (ELF32 i386, 14.904 B), e64 (ELF64 x86-64, 15.776 B) e cópia de /usr/bin/ls (ELF64, 142.312 B) (P21).
- **Carving com `-t evtx,elf,exe`:** 3 arquivos .elf nos blocos esperados (2048, 2304 e 2560) (P22).
- **Tamanhos extraídos contra originais:**

  | Original | Original (B) | Extraído (B) |
  |---|---|---|
  | e32 | 14.904 | 12.296 |
  | e64 | 15.776 | 12.304 |
  | ls | 142.312 | 139.896 |

  Cada extraído é um prefixo idêntico do original (P23).
- **readelf e file** (P23):
  - `readelf -h` informa a classe correta (ELF32 ou ELF64) e `readelf -l` lista os program headers, os dois com exit=0.
  - O `readelf` emite "Error: Reading N bytes extends past end of file for section headers" (N = 1160, 1856 e 1984).
  - O `file` informa "missing section headers at …".
  - `readelf -s` encontra 12 símbolos FUNC no e64 original e 0 no extraído.

### C5 – VirusTotal
- **Sem VT_API_KEY** (`env -u`): o carving foi feito (3 ELF). Na saída apareceu 3 vezes "Error: VT_API_KEY environment variable is not set.". O audit registrou "Clean (0)" na coluna VT dos 3 arquivos (P24).
- **Com VT_API_KEY, `-x -t elf`:** a coluna VT do audit registrou "Clean (0)" para os 3 ELF (P26). A consulta independente pela API, com o SHA-256 de cada ELF extraído, retornou HTTP 404 NotFoundError para os 3 (P27).
- **Com VT_API_KEY, `-x -t zip` sobre a imagem com eicar_com.zip:**
  - O ZIP extraído tem SHA-256 2546dcff…edad, idêntico ao original.
  - O audit registrou "Malicious (62)".
  - A API, para o mesmo SHA-256, retornou malicious 62, undetected 5, suspicious 0, harmless 0 (P28, P28c).
- O audit.txt não tem coluna de hash. Nenhum arquivo `recovery.log` foi gerado em nenhuma execução. O registro gerado se chama `audit.txt`.

### C6 – Execução da Figura 2
- evidence2.dd não está em artefato.zip nem em nenhum commit do repositório clonado (P29).
- O coordenador informou que o arquivo não foi encontrado publicamente e que os autores não responderam.
- O comando da Fig. 2 (`./foremost-ng -v -x evidence2.dd`) não foi executado (P30: bloqueado).
- Não houve comparação de nomes ou offsets com a Fig. 2.

### C7 – Arquitetura (inspeção, fora da regra de R)
- state.c contém 21 chamadas `init_builtin(state, …)`.
- extract.c tem uma cadeia `else if (needle->type == …)` (linhas 2668-2690), com ramos explícitos para ELF, MACHO, EVTX e SCRIPT.
- engine.c chama `extract_file(` nas linhas 334 e 357 (P31).

## 4. Desvios e ocorrências registradas
- Os pacotes `curl` e `file` (previstos em P9) foram instalados antes, durante P7 e P8, para baixar e validar os arquivos.
- O código avaliado veio do artefato.zip fornecido (P3). O clone (P3b) serviu só para confirmar que o commit existe.
- P13: o utilitário `evtx_dump` do python-evtx 0.8.1 está quebrado no ambiente. Ele foi substituído pelo script `scripts/conta_evtx.py` (P13b, [FORA DO ROTEIRO]).
- P20b ([FORA DO ROTEIRO]) foi um diagnóstico com `-a`.
- P32: o tgz das saídas foi removido da pasta de evidências, e foram mantidos os hashes por arquivo.
- Nenhuma alteração foi feita no código do artefato. Nenhum arquivo foi enviado ao VirusTotal: foram feitas só consultas por hash, pelo artefato e pelos passos P27 e P28c.
