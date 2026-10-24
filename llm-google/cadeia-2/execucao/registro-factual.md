# Registro Factual de Execução Experimental — Foremost-NG (SBSeg 2025)

**Artefato:** Foremost-NG: An Open-Source Toolkit for Advanced File Carving and Analysis  
**Versão avaliada:** `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` (a partir de `/home/revisor/artefato.zip`)  
**Data da execução:** 24 de outubro de 2026  
**Ambiente de execução:** Contêiner Docker `t9-gemini-c2`  

---

## 1. Ambiente (Versões Observadas)

- **Sistema Operacional:** Ubuntu 24.04.2 LTS (Noble Numbat), Linux x86_64, kernel `6.18.54.1-microsoft-standard-WSL2`.
- **Compilador C:** `gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0`
- **GNU Make:** `GNU Make 4.3`
- **Git:** `git version 2.43.0`
- **Python:** `Python 3.12.3`
- **Bibliotecas de Desenvolvimento:**
  - `libssl-dev`: versão `3.0.13-0ubuntu3.5` (OpenSSL 3.0.13)
  - `libcurl4-openssl-dev`: versão `8.5.0-2ubuntu10.6` (libcurl 8.5.0)
- **Binário Foremost-NG:**
  - Versão reportada: `1.5.7` (compilada com `-DVERSION="\"1.5.7\""`)
  - Formato: `ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked`
  - BuildID: `a548ea1fd409bfb47f80c90fac8ed580e06ab13a`
- **Variável de Ambiente VirusTotal:**
  - `VT_API_KEY`: Configurada no contêiner e confirmada não-vazia (mascarada: `<VT_API_KEY>`).

---

## 2. Tabela de Execução dos Passos

**Legenda de Desvio:**
- **D0:** Procedimento dos autores, sem alteração.
- **D1:** Ajuste de ambiente (instalação de dependências do sistema).
- **D2:** Passo ou entrada proposta pelo revisor (síntese de dados de teste).
- **D3:** Teste externo com dados de terceiros.

| Passo | Comando Exato | Resultado Esperado | Resultado Observado (Trecho / Exit Code) | Arquivo de Evidência | Status | Desvio |
|---|---|---|---|---|---|---|
| **P1** | `sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev file bsdextrautils python3` | Instalação de compilador, make e libs de desenvolvimento | Pacotes instalados sem erro (`Setting up gcc... libssl-dev... libcurl4-openssl-dev...`). Exit Code: 0 | `01_apt_install.log` | sucesso | D1 |
| **P2** | `cd /home/revisor && unzip -q artefato.zip` | Descompactação do código-fonte do artefato | Diretório `foremost-ng-bb812a22` extraído com `src/`, `README.md`, `Makefile`, etc. Exit Code: 0 | `02_repo_check.log` | sucesso | D0 |
| **P3** | `cd /home/revisor/foremost-ng/src && make clean && make` | Compilação dos arquivos C e ligação do binário `foremost-ng` | Compilação de 10 objetos C e linkagem com `-lssl -lcrypto -lcurl`. Binário `foremost-ng` (86 KB) gerado. Exit Code: 0 | `03_make_build.log` | sucesso | D0 |
| **P4** | `sudo make install && which foremost-ng` | Instalação em `/usr/local/bin` e man page | Binário instalado em `/usr/local/bin/foremost-ng`, man page em `/usr/share/man/man8`, config em `/usr/local/etc`. Exit Code: 0 | `04_make_install.log` | sucesso | D0 |
| **P5** | `foremost-ng -V && foremost-ng -h && man -P cat foremost-ng` | Exibição de versão, opções de ajuda e man page | Versão 1.5.7 exibida, menu de opções renderizado, man page lida com sucesso. Exit Code: 0 | `05_version.txt`, `05_help.txt`, `05_man.txt` | sucesso | D0 |
| **P6** | `python3 /home/revisor/evidencias/p6_prep_f.py` | Geração de imagem sintética `test_f.img` | Imagem `/tmp/teste_f/test_f.img` criada com 4243 bytes contendo script bash e PNG. Exit Code: 0 | `06_prep_test_f.log` | sucesso | D2 |
| **P7** | `foremost-ng -i test_f.img -o output_f` | Execução de carving mínimo e geração de audit | `1 FILES EXTRACTED` (script=1 em `output_f/script/00000002.script`, 78 B, offset 1024). `audit.txt` gerado. Exit Code: 0 | `07_exec_f.log`, `07_audit_f.txt` | sucesso | D0 |
| **P8** | `python3 /home/revisor/evidencias/p8_prep_c1.py` | Geração de imagem com cabeçalho EVTX (`ElfFile\0\0`) | Arquivo `c1_evtx.img` criado com 66561 bytes (chunk de 64 KiB). Exit Code: 0 | `08_prep_c1.log` | sucesso | D2 |
| **P9** | `foremost-ng -t evtx -i c1_evtx.img -o output_c1` | Extração de log EVTX de 64 KiB delimitado | `1 FILES EXTRACTED` (`evtx/00000001.evtx`, 64 KB, offset 512). `file` confirma: MS Windows 10-11 Event Log. Exit Code: 0 | `09_exec_c1.log`, `09_audit_c1.txt` | sucesso | D0 |
| **P10** | `python3 /home/revisor/evidencias/p10_prep_c2.py` | Geração de imagem contendo scripts bash, python, pwsh | Arquivo `c2_script.img` criado com 4424 bytes. Exit Code: 0 | `10_prep_c2.log` | sucesso | D2 |
| **P11** | `foremost-ng -t script -i c2_script.img -o output_c2` | Extração de scripts válidos preservando shebang | `4 FILES EXTRACTED` em `output_c2/script/`. Scripts bash, python e pwsh íntegros com shebang. Exit Code: 0 | `11_exec_c2.log`, `11_audit_c2.txt` | sucesso | D0 |
| **P12** | `python3 /home/revisor/evidencias/p12_prep_c3.py` | Geração de imagem contendo Mach-O FAT e Thin 64-bit | Arquivo `c3_macho.img` criado com 14336 bytes. Exit Code: 0 | `12_prep_c3.log` | sucesso | D2 |
| **P13** | `foremost-ng -t macho -i c3_macho.img -o output_c3` | Extração de binário Mach-O | `1 FILES EXTRACTED` (`macho/00000011.macho`, 8 KB, offset 5632). `file` confirma: Mach-O universal binary. Exit Code: 0 | `13_exec_c3.log`, `13_audit_c3.txt` | sucesso | D0 |
| **P14** | `python3 /home/revisor/evidencias/p14_prep_c4.py` | Geração de imagem contendo executável ELF64 (`/bin/true`) | Arquivo `c4_elf.img` criado com 28984 bytes. Exit Code: 0 | `14_prep_c4.log` | sucesso | D2 |
| **P15** | `foremost-ng -t elf -i c4_elf.img -o output_c4` | Extração de binário ELF delimitado por segmentos PT_LOAD | `1 FILES EXTRACTED` (`elf/00000002.elf`, 24 KB, offset 1024). `readelf -h` confirma ELF64 DYN AMD x86-64 válido. Exit Code: 0 | `15_exec_c4.log`, `15_audit_c4.txt` | sucesso | D0 |
| **P16** | `bash /home/revisor/evidencias/p16_check_vt.sh` | Confirmação segura de que `VT_API_KEY` está configurada | `VT_API_KEY esta definida e nao-vazia (mascarada: <VT_API_KEY>)`. Exit Code: 0 | `16_vt_key_status.txt` | sucesso | D0 |
| **P17** | `foremost-ng -v -x -t elf -i c4_elf.img -o output_c5` | Consulta à API VT pelo hash do ELF e coluna VT anotada | Hash SHA-256 consultado via libcurl; coluna `VT` preenchida com `Clean (0)`. Sem chave: aviso emitido. Exit Code: 0 | `17_exec_c5.log`, `17_audit_c5.txt` | sucesso | D0 |
| **P18** | `find / -name "evidence2.dd"` | Busca da imagem de 2 GB da Figura 2 no contêiner | `Arquivo evidence2.dd NAO ENCONTRADO no sistema de arquivos`. Exit Code: 0 | `18_find_evidence2.log` | falha | D0 |
| **P19** | `foremost-ng -v -x evidence2.dd` | Reprodução da extração e tabela da Figura 2 | `[!] File not found or is a directory: evidence2.dd` / `[!] No valid input files to process.`. Exit Code: 1 | `19_exec_c6_fig2.log` | bloqueado | D0 |

---

## 3. Fatos Observados por Reivindicação

### C1: Recuperação de logs de eventos do Windows (EVTX)
- **Fato observado:** O Foremost-NG foi executado com `-t evtx` sobre a imagem sintetizada `c1_evtx.img` contendo assinatura de cabeçalho `ElfFile\0\0` e campo `chunk_count = 1` no offset `0x18`.
- O parser `extract_evtx` identificou a assinatura no offset 512 da imagem, calculou `full_size = 1 * 65536 = 65536 bytes`, e extraiu o arquivo `output_c1/evtx/00000001.evtx`.
- O tamanho do arquivo extraído foi de exatamente 65.536 bytes (64 KiB), coincidente com o tamanho de um chunk EVTX.
- A inspeção do utilitário `file` sobre o artefato extraído retornou: `MS Windows 10-11 Event Log, version 0.0, 0 chunks (no. 0 in use), empty`.
- O evento de extração foi registrado no arquivo de log `audit.txt` associado ao ID 0 e offset 512.

### C2: Recuperação de scripts (Bash, Python, PowerShell)
- **Fato observado:** O Foremost-NG foi executado com `-t script` sobre `c2_script.img` contendo scripts com shebang (`#!`) em diferentes linguagens e tamanhos superiores a 32 bytes.
- O parser `extract_script` extraiu com sucesso os scripts para a pasta `output_c2/script/`:
  - `00000001.script` (100 bytes): script Bash iniciado por `#!/bin/bash`, preservando comentários e comandos de execução.
  - `00000003.script` (100 bytes): script Python iniciado por `#!/usr/bin/env python3`.
  - `00000005.script` (84 bytes): script PowerShell iniciado por `#!/usr/bin/env pwsh`.
- Constatou-se uma particularidade na implementação da linha 2601 de `src/extract.c`: a checagem que busca caracteres de código além de comentários (`if (!isspace(*p)) { if (*p != '#') { found_real = 1; break; } }`) varre caractere por caractere de todo o corpo; assim, qualquer linha de comentário que contenha texto com letras normais faz `found_real = 1`, resultando também na extração do arquivo `00000007.script` (44 bytes).
- Todos os scripts extraídos mantiveram a integridade textual e a diretiva do interpretador.

### C3: Recuperação de binários Mach-O (fat e thin)
- **Fato observado:** O Foremost-NG foi executado com `-t macho` sobre a imagem `c3_macho.img` contendo estruturas Mach-O Universal/FAT (`0xCAFEBABE`) e Mach-O Thin 64-bit LE (`0xCFFAEDFE`).
- O parser `extract_macho` reconheceu o cabeçalho universal FAT, processou a estrutura `fat_arch` e calculou a extensão em 8.192 bytes, gravando o arquivo `output_c3/macho/00000011.macho`.
- O utilitário `file` inspecionou o arquivo e confirmou: `Mach-O universal binary with 1 architecture: [x86_64: - Mach-O 64-bit x86_64 executable]`.
- Para o binário Thin 64-bit LE, observou-se que o código em `src/extract.c:2408` compara a variável inteira `magic_le` (lida via `read_le32`) contra a constante literal `0xCFFAEDFE` (e `0xCEFAEDFE` para 32-bit). Como a leitura em little-endian dos bytes `0xCF 0xFA 0xED 0xFE` produz o número inteiro `0xFEEDFACF`, a condição não é satisfeita, impedindo a extração isolada do binário thin na imagem de teste.

### C4: Recuperação de executáveis ELF de 32 e 64 bits
- **Fato observado:** O Foremost-NG foi executado com `-t elf` sobre `c4_elf.img` contendo o binário ELF de 64 bits de `/bin/true` cercado por blocos de preenchimento nulo.
- O parser `extract_elf` validou o número mágico `0x7F 'E' 'L' 'F'`, identificou a classe `ELFCLASS64` e a codificação `ELFDATA2LSB`.
- O parser leu a tabela de cabeçalhos de programa a partir do offset `0x20` e iterou sobre as 13 entradas, somando os extents dos segmentos marcados com `PT_LOAD` (`p_offset_64 + p_filesz_64`), obtendo a extensão máxima de 24.520 bytes.
- O arquivo `output_c4/elf/00000002.elf` foi extraído com 24.520 bytes e registrado no `audit.txt`.
- O utilitário `readelf -h` leu o arquivo e validou: ELF64, 2's complement little endian, AMD x86-64, Type DYN, 13 program headers. A omissão das seções posteriores aos segmentos de carga (section headers) gerou o aviso esperado de leitura parcial de section headers no `readelf`, confirmando o comportamento documentado pelos autores na Seção 3 do artigo de extrair a união dos segmentos de carga `PT_LOAD`.

### C5: Enriquecimento pelo VirusTotal
- **Fato observado:** O Foremost-NG foi executado com a flag `-x` e a variável de ambiente `VT_API_KEY` configurada no contêiner.
- Durante a extração do executável ELF em `output_c5`, a rotina `sha_checksum` calculou o hash SHA-256 do arquivo recuperado (`d0cd2bec3dc342c1c1fd5e8a0e880a4d14e878e7a6e3fe8f858034cc600ae753`).
- A função `vt_check_hash` disparou uma requisição HTTP GET via libcurl para o endpoint `https://www.virustotal.com/api/v3/files/<hash>` enviando o cabeçalho `x-apikey: <VT_API_KEY>`.
- O log `output_c5/audit.txt` registrou o arquivo extraído com a coluna `VT` preenchida com o veredito: `Clean (0)`.
- Em teste adicional sem a variável de ambiente (`env -u VT_API_KEY`), o programa emitiu para o stderr o aviso: `Error: VT_API_KEY environment variable is not set.`, prosseguiu com a extração e manteve o valor padrão `Clean (0)` no log de auditoria, confirmando o tratamento de ausência de chave descrito na página 7 do artigo.

### C6: Exemplo de execução da Figura 2 (`./foremost-ng -v -x evidence2.dd`)
- **Fato observado:** Realizou-se busca recursiva em todo o sistema de arquivos do contêiner (`find / -name "evidence2.dd"`), confirmando que o arquivo `evidence2.dd` não se encontra presente.
- A invocação direta do comando documentado pelos autores (`foremost-ng -v -x evidence2.dd`) no diretório do artefato retornou imediatamente os erros:
  `[!] File not found or is a directory: evidence2.dd`
  `[!] No valid input files to process.`
  com código de saída 1.
- A extração dos 12 arquivos (ELF, script, EXE, ZIP) nos offsets decimais exatos (2228224 a 914965615) e o confronto da tabela da Figura 2 não puderam ser realizados devido à indisponibilidade da imagem forense de 2 GB.
