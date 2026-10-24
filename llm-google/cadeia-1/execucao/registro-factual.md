# Registro Factual de Execução — Foremost-NG

Data de Execução: 24 de outubro de 2026  
Ambiente: Contêiner Docker `t9-gemini-c1` (Ubuntu 24.04.2 LTS x86_64)  
Usuário: `revisor` (com privilégios de `sudo` sem senha)  
Diretório de Evidências no Host: `D:\t9-trabalho\gemini-c1\execucao`  
Diretório de Evidências no Contêiner: `/home/revisor/evidencias`

---

## 1. Ambiente e Versões Observadas

- **Sistema Operacional:** Ubuntu 24.04.2 LTS (Noble Numbat), kernel Linux 6.18.54.1-microsoft-standard-WSL2 x86_64
- **Compilador C:** GCC 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04)
- **Make:** GNU Make 4.3
- **Bibliotecas C:** GNU C Library (glibc) 2.39, OpenSSL 3.0.13 (libssl-dev), libcurl 8.5.0 (libcurl4-openssl-dev)
- **Linguagens Auxiliares:** Python 3.12.3
- **Utilitários de Diagnóstico:** `file` 5.45, `readelf` (GNU binutils 2.42), `unzip` 6.0
- **Variáveis de Ambiente:** `VT_API_KEY` presente e ativa no ambiente do contêiner (valor mantido estritamente mascarado como `<VT_API_KEY>`)

---

## 2. Tabela de Execução dos Passos do Roteiro

| Passo | Comando Exato | Resultado Esperado | Resultado Observado (Trecho curto e Código de Saída) | Arquivo de Evidência | Status | Desvio |
|---|---|---|---|---|---|---|
| **P1** | `bash /home/revisor/evidencias/step_p1.sh` | Confirmar SO Ubuntu 24.04 e presença de `VT_API_KEY` | `PRETTY_NAME="Ubuntu 24.04.2 LTS"` / `VT_API_KEY: presente (mascarada: <VT_API_KEY>)` (exit code: 0) | `env_info.txt`, `step_p1.sh` | Sucesso | D1 |
| **P2** | `bash /home/revisor/evidencias/step_p2.sh` | Instalar gcc, make, git, libssl-dev, libcurl4-openssl-dev | `Setting up gcc (4:13.2.0-7ubuntu1)` / `GNU Make 4.3` (exit code: 0) | `apt_install.log`, `step_p2.sh` | Sucesso | D1 |
| **P3** | `bash /home/revisor/evidencias/step_p3.sh` | Descompactar `artefato.zip` em `foremost-ng` | Diretório `foremost-ng-bb812a22/src` criado com arquivos fonte (exit code: 0) | `tree_artifact.txt`, `step_p3.sh` | Sucesso | D0 |
| **P4** | `bash /home/revisor/evidencias/step_p4.sh` | Compilação do binário via `make clean && make` | `gcc ... -o foremost-ng -lssl -lcrypto -lcurl` / `foremost-ng: ELF 64-bit LSB pie executable` (exit code: 0) | `build.log`, `step_p4.sh` | Sucesso | D0 |
| **P5** | `bash /home/revisor/evidencias/step_p5.sh` | Instalação no sistema via `sudo make install` | `install -m 755 foremost-ng /usr/local/bin` / `/usr/local/bin/foremost-ng` (exit code: 0) | `install.log`, `step_p5.sh` | Sucesso | D0 |
| **P6** | `bash /home/revisor/evidencias/step_p6.sh` | Verificar versão (`-V`) e menu de ajuda (`-h`) | `foremost-ng version 1.5.7 by Cristian Souza.` / menu de opções listado (exit code: 0) | `cli_help_version.txt`, `step_p6.sh` | Sucesso | D0 |
| **P7** | `bash /home/revisor/evidencias/step_p7.sh` | Gerar imagem sintética `test_minimo.img` com PNG | Arquivo de 1.6 MB criado com padding e PNG embutido (exit code: 0) | `test_minimo_created.txt`, `step_p7.sh` | Sucesso | D2 |
| **P8** | `bash /home/revisor/evidencias/step_p8.sh` | Carving básico com `foremost-ng -i test_minimo.img -o output_f` | `1 FILES EXTRACTED (png=1)` / `00002048.png: PNG image data, 1 x 1` (exit code: 0) | `audit_f.txt`, `step_p8.sh` | Sucesso | D0 (sob D2) |
| **P9** | `bash /home/revisor/evidencias/step_p9.sh` | Gerar amostra sintética de EVTX (`ElfFile\0\0`, 2 chunks de 64 KiB) | Arquivo `evtx_sample.raw` de 137 KB criado com padding (exit code: 0) | `evtx_sample_spec.txt`, `step_p9.sh` | Sucesso | D2 |
| **P10** | `bash /home/revisor/evidencias/step_p10.sh` | Carving de EVTX (`foremost-ng -t evtx -i evtx_sample.raw -o output_evtx`) | `1 FILES EXTRACTED (evtx=1)` / `00000008.evtx: MS Windows 10-11 Event Log, 128 KB` (exit code: 0) | `audit_c1_evtx.txt`, `step_p10.sh` | Sucesso | D0 (sob D2) |
| **P11** | `bash /home/revisor/evidencias/step_p11.sh` | Gerar amostras de scripts (Bash, POSIX, Python) em imagem | Arquivo `script_sample.raw` de 4.3 KB criado (exit code: 0) | `script_sample_spec.txt`, `step_p11.sh` | Sucesso | D2 |
| **P12** | `bash /home/revisor/evidencias/step_p12.sh` | Carving de scripts (`foremost-ng -t script -i script_sample.raw -o output_script`) | `3 FILES EXTRACTED (script=3)` / scripts Bash, POSIX e Python recuperados íntegros (exit code: 0) | `audit_c2_script.txt`, `step_p12.sh` | Sucesso | D0 (sob D2) |
| **P13** | `bash /home/revisor/evidencias/step_p13.sh` | Gerar amostras sintéticas de binários Mach-O (universal FAT e thin 64-bit) | Arquivo `macho_sample.raw` de 13 KB criado (exit code: 0) | `macho_sample_spec.txt`, `step_p13.sh` | Sucesso | D2 |
| **P14** | `bash /home/revisor/evidencias/step_p14.sh` | Carving de Mach-O (`foremost-ng -t macho -i macho_sample.raw -o output_macho`) | `1 FILES EXTRACTED (macho=1)` / `00000012.macho: Mach-O universal binary` (5120 B) (exit code: 0) | `audit_c3_macho.txt`, `step_p14.sh` | Sucesso | D0 (sob D2) |
| **P15** | `bash /home/revisor/evidencias/step_p15.sh` | Compilar binário ELF autêntico e embutir em `elf_sample.raw` | Binário compilado e inserido em `elf_sample.raw` (32 KB) (exit code: 0) | `elf_target_info.txt`, `step_p15.sh` | Sucesso | D2 |
| **P16** | `bash /home/revisor/evidencias/step_p16.sh` | Carving e execução de ELF (`foremost-ng -t elf -i elf_sample.raw -o output_elf`) | `1 FILES EXTRACTED (elf=1)` / `readelf -l` válido / execução direta retornou 42 (exit code: 0) | `audit_c4_elf.txt`, `step_p16.sh` | Sucesso | D0 (sob D2) |
| **P17** | `bash /home/revisor/evidencias/step_p17.sh` | Teste do enriquecimento VT sem chave (`VT_API_KEY=""`) | `Error: VT_API_KEY environment variable is not set.` / carving concluiu com `Clean (0)` (exit code: 0) | `vt_nokey_err.txt`, `step_p17.sh` | Sucesso | D0 (sob D2) |
| **P18** | `bash /home/revisor/evidencias/step_p18.sh` | Carving com `-x` e `VT_API_KEY` ativa | `foremost-ng -x -t elf ...` executou consulta sem erros / coluna VT preenchida (exit code: 0) | `audit_c5_vt.txt`, `step_p18.sh` | Sucesso | D0 (sob D2) |
| **P19** | `bash /home/revisor/evidencias/step_p19.sh` | Busca por `evidence2.dd` em todo o sistema de arquivos | `find` retornou vazio para `evidence2.dd` e `*.dd` (exit code: 0) | `evidence2_find.txt`, `step_p19.sh` | Sucesso (busca diagnóstica) | D2 |
| **P20** | `bash /home/revisor/evidencias/step_p20.sh` | Tentativa de executar comando da Figura 2 (`./foremost-ng -v -x evidence2.dd`) | `[!] File not found or is a directory: evidence2.dd` / `[!] No valid input files to process.` (exit code: 1) | `figura2_reproduction.txt`, `step_p20.sh` | Falha (dado ausente) | D0 |

---

## 3. Fatos Observados por Reivindicação

### Reivindicação C1: Recuperação de logs de eventos do Windows (EVTX)
- **Comportamento observado:** O parser de EVTX (`extract_evtx`) inspecionou o fluxo de dados em busca da assinatura de 8 bytes `ElfFile\0\0`. Ao localizá-la no offset 4096 do arquivo de teste, leu o campo `chunk_count` no offset 0x18 (valor = 2) e calculou a extensão de $2 \times 65536 = 131072$ bytes.
- **Arquivo extraído:** Foi gerado o arquivo `output_evtx/evtx/00000008.evtx` com exatamente 131072 bytes (128 KB).
- **Validação de integridade:** A ferramenta de identificação `file` classificou o arquivo extraído como `MS Windows 10-11 Event Log, version 0.0, 0 chunks (no. 0 in use), next record no. 2`. O relatório `audit.txt` registrou corretamente a extração com offset 4096 e tamanho de 128 KB.

### Reivindicação C2: Recuperação de scripts (Bash, Python, PowerShell)
- **Comportamento observado:** O parser de scripts (`extract_script`) identificou arquivos iniciando com a assinatura de shebang `#!`. Realizou a varredura progressiva do conteúdo textual até encontrar a sentinela não imprimível (`\x00`).
- **Arquivos extraídos:**
  - `00000002.script`: 83 bytes (Bourne-Again shell script, ASCII text executable, offset 1024), contendo a linha `#!/bin/bash` e o corpo do script intacto.
  - `00000004.script`: 49 bytes (POSIX shell script, offset 2132), contendo `#!/bin/sh` e comentários.
  - `00000006.script`: 90 bytes (Python script, ASCII text executable, offset 3206), contendo `#!/usr/bin/env python3` e o código Python legível.
- **Validação de integridade:** Os arquivos recuperados mantiveram tanto a linha do interpretador quanto o conteúdo do corpo totalmente preservados e executáveis.

### Reivindicação C3: Recuperação de binários Mach-O (macOS/iOS Binaries)
- **Comportamento observado:** O parser (`extract_macho`) identificou a assinatura universal FAT `0xCAFEBABE` no offset 6144, interpretou a tabela de arquiteturas e determinou a extensão total com base nos offsets de carga ($arch\_fileoff + arch\_size = 4096 + 1024 = 5120$ bytes).
- **Arquivo extraído:** Foi extraído `output_macho/macho/00000012.macho` com exatamente 5120 bytes. O comando `file` o classificou como `Mach-O universal binary with 1 architecture: [i386:\012- ELF]`.
- **Divergência factual no código de Mach-O thin:** Observou-se no código-fonte que, para binários Mach-O thin de 64 bits, a assinatura registrada na inicialização da tabela em `src/state.c:7000` é a sequência de bytes `\xCF\xFA\xED\xFE` (byte 0 = `0xCF`, byte 1 = `0xFA`, byte 2 = `0xED`, byte 3 = `0xFE`), enquanto a verificação interna na rotina `extract_macho` em `src/extract.c:2409` compara o valor lido via `read_le32(buf)` contra a constante `0xCFFAEDFE` (que em bytes little-endian em disco corresponderia a `0xFE, 0xED, 0xFA, 0xCF`). Dessa forma, binários thin com a ordem canônica em disco foram ignorados pelo dispatch, enquanto o formato universal FAT (`0xCAFEBABE`) funcionou perfeitamente.

### Reivindicação C4: Recuperação de executáveis ELF (32 e 64 bits)
- **Comportamento observado:** O parser de ELF (`extract_elf`) identificou o magic `\x7fELF`, verificou `ei_class = 2` (ELF64) e `ei_data = 1` (little-endian), e percorreu os 13 cabeçalhos de programa (`program header table`). Calculou a extensão máxima cobrindo todos os segmentos carregáveis `PT_LOAD` ($max\_seg\_end = 12304$ bytes).
- **Arquivo extraído:** Foi gerado `output_elf/elf/00000016.elf` com 12304 bytes a partir do offset 8192.
- **Validação e execução:**
  - O utilitário `readelf -l` analisou a tabela de segmentos carregáveis sem erros, confirmando `Type LOAD` nos endereços virtuais correspondentes.
  - Conforme projetado no parser do Foremost-NG, a tabela de seções (`section header table`), localizada após o último segmento `PT_LOAD`, não é incorporada ao carving.
  - O binário extraído foi tornado executável (`chmod +x`) e rodado nativamente no contêiner, executando com sucesso e retornando o código de saída exato `42`.

### Reivindicação C5: Enriquecimento pelo VirusTotal
- **Comportamento sem chave:** Quando a variável `VT_API_KEY` estava desprovida de valor, o executável emitiu na saída de erro a mensagem `Error: VT_API_KEY environment variable is not set.`. O carving dos artefatos prosseguiu sem interrupções e o log `audit.txt` registrou o status `Clean (0)` para o arquivo recuperado.
- **Comportamento com chave ativa:** Com a variável `VT_API_KEY` devidamente configurada, o `foremost-ng` calculou o hash SHA-256 do arquivo extraído (`c7b5a21d935c8c92b30f5106a058de1e45ffdca365eb72b74de86b5b9e3a96fe`) e efetuou a requisição HTTP GET via libcurl para o endpoint `https://www.virustotal.com/api/v3/files/<hash>`. Como o binário gerado sinteticamente era inédito na base do VirusTotal, a API retornou código 404 (Not Found), tratado pela rotina como ausência de detecções e rotulado como `Clean (0)` no `audit.txt`, sem erros ou travamentos.
- **Verificação independente da API:** A funcionalidade da API do VirusTotal e a validade da chave configurada foram atestadas por meio de consulta avulsa por hash do arquivo de teste EICAR (`275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f`) e do binário público BusyBox (`6e123e7f3202a8c1e9b1f94d8941580a25135382b99e8d3e34fb858bba311348`), obtendo resposta `HTTP 200` com os objetos `last_analysis_stats` contendo detecções reais (`{"malicious": 66, ...}` e `{"malicious": 1, ...}`).

### Reivindicação C6: Exemplo de execução da Figura 2 (`./foremost-ng -v -x evidence2.dd`)
- **Comportamento observado:** A varredura de busca (`find / -name "evidence2.dd"`) confirmou que o arquivo de imagem forense `evidence2.dd` (citado na Figura 2 e na Seção 4.2 do artigo como tendo 2 GB / 2045109643 bytes) não existe no contêiner, não acompanha o artefato `artefato.zip` e não possui dados ou scripts de recomposição no repositório.
- **Tentativa de execução:** O comando indicado pelos autores no artigo (`./foremost-ng -v -x evidence2.dd`) foi executado no diretório `foremost-ng-bb812a22/src`. O programa falhou imediatamente com a saída:
  ```text
  [!] File not found or is a directory: evidence2.dd
  [!] No valid input files to process.
  ```
  encerrando com código de erro 1.
- **Resultado comparativo:** Não foi possível observar a tabela de extração, os 12 arquivos recuperados (ELF, script, EXE, ZIP), nem os offsets de disco descritos na Figura 2 (pág. 8 do artigo).
