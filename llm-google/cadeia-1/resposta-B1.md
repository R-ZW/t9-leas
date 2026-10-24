# Roteiro de Avaliação Prática — Foremost-NG (Etapa E)

Este roteiro estabelece o plano sistemático de testes a ser executado no ambiente de contêiner Docker (Ubuntu 24.04 limpo, com acesso à internet, usuário comum com sudo, contendo previamente apenas `sudo`, `unzip`, `man`, e a variável `VT_API_KEY` configurada).

---

## 1. Requisitos do Ambiente

### 1.1. Hardware
- **Arquitetura de CPU:** x86_64 / amd64 (necessário para compatibilidade com o parser de executáveis ELF de 64 bits e binários nativos).
- **Memória RAM:** Mínimo de 2 GB (recomendado 4 GB para acomodar alocações de chunks e buffers de carving).
- **Armazenamento:** Mínimo de 5 GB de espaço livre em disco para acomodar pacotes do sistema operacional, compilação do artefato e criação de imagens de teste.

### 1.2. Software e Dependências
- **Sistema Operacional Base:** Ubuntu 24.04 LTS limpo.
- **Ferramentas pré-existentes:** `sudo`, `unzip`, `man`.
- **Conectividade:** Acesso à internet habilitado (para instalação de pacotes via APT e consulta HTTPS à API do VirusTotal).
- **Variáveis de Ambiente:** `VT_API_KEY` previamente exportada no contêiner (com valor mantido estritamente mascarado como `<VT_API_KEY>`).

---

## 2. Preparação do Ambiente e Compilação

### Passo P1: Inspeção do Ambiente e Checagem da Chave VirusTotal
- **Selo / Reivindicação:** Preparação geral / F e C5.
- **Classificação:** [NÃO DOCUMENTADO] (Necessário para registrar as características do ambiente limpo e assegurar a existência da chave mascarada sem vazar seu conteúdo).
- **Diretório:** `/home/ubuntu` (ou `$HOME`)
- **Comando exato:**
  ```bash
  uname -a && cat /etc/os-release && [ -n "$VT_API_KEY" ] && echo "VT_API_KEY configurada (<VT_API_KEY>)" || echo "VT_API_KEY ausente"
  ```
- **Resultado esperado segundo autores:** N/A (passo de diagnóstico).
- **Evidência a salvar:** `env_info.txt`
- **Critério de sucesso:** Ubuntu 24.04 LTS (x86_64) confirmado e presença da variável `VT_API_KEY` verificada.
- **Critério de falha:** Variável `VT_API_KEY` inexistente ou OS incompatível.
- **Critério de interrupção:** Não interrompe imediatamente, mas afeta C5.

---

### Passo P2: Instalação de Dependências de Compilação
- **Selo / Reivindicação:** Selo F (Instalação e Dependências).
- **Classificação:** [NÃO DOCUMENTADO] (O `README.md` não lista pacotes para distribuições Linux, mencionando apenas BSD e macOS. A lista de pacotes é extraída do `Dockerfile:4-5` do repositório: `gcc`, `make`, `git`, `libssl-dev`, `libcurl4-openssl-dev`).
- **Diretório:** `/home/ubuntu`
- **Comando exato:**
  ```bash
  sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev
  ```
- **Resultado esperado segundo autores:** `Dockerfile:3-6` instala com sucesso o compilador C e bibliotecas de desenvolvimento OpenSSL e cURL.
- **Evidência a salvar:** `apt_install.log`
- **Critério de sucesso:** Código de retorno 0 e binários `gcc` e `make` operacionais.
- **Critério de falha:** Falha de rede ou pacotes indisponíveis no repositório APT.
- **Critério de interrupção:** **Interrupção total**. Sem compilador e bibliotecas C, o artefato não pode ser construído.

---

### Passo P3: Obtenção e Descompactação do Artefato
- **Selo / Reivindicação:** Selo F (Instalação).
- **Classificação:** Documentado no `README.md:27-28` (`tar xzvf foremost-ng-<version>.tar.gz` ou cópia do artefato de trabalho).
- **Diretório:** `/home/ubuntu`
- **Comando exato:**
  ```bash
  cd /home/ubuntu && if [ -f /opt/foremost-ng/src/Makefile ]; then cp -r /opt/foremost-ng ./foremost-ng; elif [ -f /pacote/artefato.zip ]; then unzip -q /pacote/artefato.zip -d ./foremost-ng; fi && cd foremost-ng
  ```
- **Resultado esperado segundo autores:** Diretório do projeto estruturado contendo a pasta `src/` com todos os fontes e Makefile.
- **Evidência a salvar:** `tree_artifact.txt` (saída de `ls -laR`)
- **Critério de sucesso:** Diretório `foremost-ng/src` presente contendo `main.c`, `Makefile`, etc.
- **Critério de falha:** Arquivos fonte não encontrados.
- **Critério de interrupção:** **Interrupção total**.

---

### Passo P4: Compilação do Artefato
- **Selo / Reivindicação:** Selo F (Compilação e Executabilidade).
- **Classificação:** Documentado no `README.md:33` e `artigo.pdf:6` (`make`).
- **Diretório:** `/home/ubuntu/foremost-ng/src`
- **Comando exato:**
  ```bash
  make clean && make
  ```
- **Resultado esperado segundo autores:** Compilação dos arquivos `.c` sem erros e geração do executável `foremost-ng`.
- **Evidência a salvar:** `build.log`
- **Critério de sucesso:** Binário `foremost-ng` gerado com status de saída 0 e executável.
- **Critério de falha:** Erros de compilação ou linkagem (ausência de símbolos de OpenSSL/libcurl).
- **Critério de interrupção:** **Interrupção total**. Se o binário não compila, nenhuma funcionalidade pode ser testada.

---

### Passo P5: Instalação do Binário no Sistema
- **Selo / Reivindicação:** Selo F (Instalação).
- **Classificação:** Documentado no `README.md:34` e `artigo.pdf:6` (`sudo make install`).
- **Diretório:** `/home/ubuntu/foremost-ng/src`
- **Comando exato:**
  ```bash
  sudo make install && which foremost-ng
  ```
- **Resultado esperado segundo autores:** `foremost-ng` instalado em `/usr/local/bin/foremost-ng` e manual instalado em `/usr/share/man/man8`.
- **Evidência a salvar:** `install.log`
- **Critério de sucesso:** Executável encontrado no `$PATH` do sistema (`/usr/local/bin/foremost-ng`).
- **Critério de falha:** Falha na cópia dos binários ou permissão negada.
- **Critério de interrupção:** Não interrompe; o teste pode prosseguir usando `./foremost-ng`.

---

## 3. Teste Mínimo de Funcionalidade (Selo F)

### Passo P6: Verificação de Ajuda e Versão da CLI
- **Selo / Reivindicação:** Selo F (Exemplo mínimo / Execução).
- **Classificação:** Documentado no `artigo.pdf:7` e `src/main.c:92-112`.
- **Diretório:** `/home/ubuntu/foremost-ng/src`
- **Comando exato:**
  ```bash
  foremost-ng -V && foremost-ng -h
  ```
- **Resultado esperado segundo autores:** Exibição da versão (1.5.7), dados de autoria/copyright e menu detalhado de opções da CLI.
- **Evidência a salvar:** `cli_help_version.txt`
- **Critério de sucesso:** Saída sem crashes, retorno 0, exibindo "foremost-ng version 1.5.7" e resumo de flags (`-t`, `-x`, `-o`, etc.).
- **Critério de falha:** Falha de segmentação, erro de biblioteca dinâmica ou opção não reconhecida.
- **Critério de interrupção:** Interrupção dos testes funcionais caso ocorra core dump imediato.

---

### Passo P7: Criação de Imagem Forense Mínima Sintética para Teste Funcional
- **Selo / Reivindicação:** Selo F (Exemplo mínimo executável).
- **Classificação:** [NÃO DOCUMENTADO] (Necessário porque os autores não disponibilizaram nenhuma imagem de teste no artefato, impossibilitando executar um exemplo mínimo ponta a ponta sem criar uma entrada sintética).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  mkdir -p /home/ubuntu/testes && cd /home/ubuntu/testes && python3 -c '
  import os
  # Gera imagem sintética de 10 MB com padding
  with open("test_minimo.img", "wb") as f:
      f.write(b"\x00" * 1024 * 1024)
      # Embed PNG
      png_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
      f.write(png_data)
      f.write(b"\x00" * 1024 * 512)
  '
  ```
- **Resultado esperado segundo autores:** N/A (geração de dado sintético).
- **Evidência a salvar:** `test_minimo_created.txt` (`ls -lh test_minimo.img`)
- **Critério de sucesso:** Arquivo `test_minimo.img` criado contendo assinatura PNG válida cercada de zeros.
- **Critério de falha:** Falha na escrita do arquivo.
- **Critério de interrupção:** Interrompe P8.

---

### Passo P8: Execução do Exemplo Mínimo e Verificação de Saídas
- **Selo / Reivindicação:** Selo F (Execução e Observação de Funcionalidades).
- **Classificação:** Documentado no `README.md:83-85` e `artigo.pdf:7` (`foremost-ng -i disk.img -o /temp/output/carved`).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  rm -rf output_f && foremost-ng -i test_minimo.img -o output_f && ls -laR output_f && cat output_f/audit.txt
  ```
- **Resultado esperado segundo autores:** Criação do diretório `output_f/`, subdiretório `output_f/png/`, extração do arquivo `.png` e geração do relatório `audit.txt`.
- **Evidência a salvar:** `audit_f.txt` e listagem de `output_f/`
- **Critério de sucesso:** Diretório `output_f` gerado, arquivo recuperado legível e `audit.txt` detalhando a extração.
- **Critério de falha:** Crash, diretório não criado ou arquivo não recuperado.
- **Critério de interrupção:** Interrompe concessão do Selo F.

---

## 4. Reivindicações Específicas do Artigo (Selo R)

---

### Bloco C1: Recuperação de Logs de Eventos do Windows (EVTX)

#### Passo P9: Geração de Amostra Sintética de EVTX
- **Selo / Reivindicação:** Selo R (C1).
- **Classificação:** [NÃO DOCUMENTADO] (Necessário pois o artefato não inclui amostras de log EVTX).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  python3 -c '
  # Cria arquivo com assinatura ElfFile\0\0, chunk_count = 1 (offset 0x18), e 64 KiB de tamanho total
  hdr = bytearray(b"\x00" * 65536)
  hdr[0:8] = b"ElfFile\x00\x00"
  hdr[0x18:0x1C] = (1).to_bytes(4, byteorder="little")
  with open("evtx_sample.raw", "wb") as f:
      f.write(b"\xAA" * 4096)
      f.write(hdr)
      f.write(b"\xBB" * 4096)
  '
  ```
- **Resultado esperado segundo autores:** N/A (preparação de artefato sintético com header `ElfFile\0\0` e chunk de 64 KiB).
- **Evidência a salvar:** `evtx_sample_spec.txt`
- **Critério de sucesso:** Criação do arquivo `evtx_sample.raw` com assinatura `ElfFile\0\0` e chunk size correspondente a 65536 bytes.
- **Critério de falha:** Falha de escrita.
- **Critério de interrupção:** Pula P10.

#### Passo P10: Carving e Validação de EVTX
- **Selo / Reivindicação:** Selo R (C1).
- **Classificação:** Documentado no `artigo.pdf:6-7` (seção 3 e exemplo `-t evtx,elf,exe`).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  rm -rf output_evtx && foremost-ng -t evtx -i evtx_sample.raw -o output_evtx && ls -la output_evtx/evtx/ && cat output_evtx/audit.txt
  ```
- **Resultado esperado segundo autores:** O parser reconhece a assinatura `ElfFile`, delimita o chunk de 64 KiB e extrai o log para `output_evtx/evtx/` registrando no `audit.txt`.
- **Evidência a salvar:** `audit_c1_evtx.txt` e saída do comando `file output_evtx/evtx/*`.
- **Critério de sucesso:** Arquivo `.evtx` recuperado com exatamente 65536 bytes (1 chunk) e listado no `audit.txt`.
- **Critério de falha:** Nenhum arquivo recuperado, tamanho incompatível ou erro no carving.
- **Critério de interrupção:** Não interrompe os demais testes.

---

### Bloco C2: Recuperação de Scripts (Bash, Python, PowerShell)

#### Passo P11: Geração de Amostras de Scripts em Imagem de Teste
- **Selo / Reivindicação:** Selo R (C2).
- **Classificação:** [NÃO DOCUMENTADO] (Necessário pois o artefato não contém imagens com scripts embutidos).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  python3 -c '
  # Script 1: Bash com shebang, comentários e corpo real > 32 bytes
  s1 = b"#!/bin/bash\n# Script de teste forense\necho \"Executando rotina forense\"\nexit 0\n\x00\xFF"
  # Script 2: Python com shebang e corpo > 32 bytes
  s2 = b"#!/usr/bin/env python3\n# Test script\nimport sys\nprint(\"Hello forensic world\")\n\x00\xFE"
  with open("script_sample.raw", "wb") as f:
      f.write(b"\x90" * 2048)
      f.write(s1)
      f.write(b"\x90" * 2048)
      f.write(s2)
      f.write(b"\x90" * 2048)
  '
  ```
- **Resultado esperado segundo autores:** N/A (preparação de dados com shebang e sentinela não imprimível).
- **Evidência a salvar:** `script_sample_spec.txt`
- **Critério de sucesso:** Arquivo `script_sample.raw` criado com os scripts formatados.
- **Critério de falha:** Erro de escrita.
- **Critério de interrupção:** Pula P12.

#### Passo P12: Carving de Scripts
- **Selo / Reivindicação:** Selo R (C2).
- **Classificação:** Documentado no `artigo.pdf:6` (seção 3 "Script Files") e `reivindicacoes.md:8`.
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  rm -rf output_script && foremost-ng -t script -i script_sample.raw -o output_script && ls -la output_script/script/ && cat output_script/audit.txt && head -n 10 output_script/script/*
  ```
- **Resultado esperado segundo autores:** Extração dos scripts preservando a linha do interpretador (`#!`), delimitando o conteúdo textual até a sentinela não imprimível, com no mínimo 32 bytes e descartando arquivos com apenas comentários.
- **Evidência a salvar:** `audit_c2_script.txt` e conteúdo dos scripts recuperados.
- **Critério de sucesso:** Scripts extraídos no subdiretório `script/` com interpretador e corpo legíveis.
- **Critério de falha:** Scripts não detectados ou truncados.
- **Critério de interrupção:** Não interrompe os demais testes.

---

### Bloco C3: Recuperação de Binários Mach-O (macOS Binaries)

#### Passo P13: Geração de Estruturas Mach-O Sintéticas
- **Selo / Reivindicação:** Selo R (C3).
- **Classificação:** [NÃO DOCUMENTADO] (Necessário pois o artefato não inclui binários Mach-O nem imagens de disco Apple).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  python3 -c '
  import struct
  # Mach-O thin 64-bit LE (magic 0xCFFAEDFE)
  # Header: magic(4), cputype(4), cpusubtype(4), filetype(4), ncmds(4), sizeofcmds(4), flags(4), reserved(4) = 32 bytes
  # LC_SEGMENT_64 = 0x19, cmdsize = 72 bytes
  # fileoff = 0, filesize = 512
  magic = struct.pack("<I", 0xCFFAEDFE)
  hdr = magic + struct.pack("<IIIIIII", 0x01000007, 3, 2, 1, 72, 0, 0)
  lc_seg = struct.pack("<II16sQQQQII", 0x19, 72, b"__TEXT\x00"*2, 0, 512, 0, 512, 7, 7, 0, 0)
  payload = hdr + lc_seg + b"\x90" * (512 - len(hdr) - len(lc_seg))
  with open("macho_sample.raw", "wb") as f:
      f.write(b"\x00" * 1024)
      f.write(payload)
      f.write(b"\x00" * 1024)
  '
  ```
- **Resultado esperado segundo autores:** N/A (preparação de payload com header e comandos de carga válidos).
- **Evidência a salvar:** `macho_sample_spec.txt`
- **Critério de sucesso:** Arquivo `macho_sample.raw` gerado contendo cabeçalho Mach-O de 64 bits.
- **Critério de falha:** Erro na síntese dos bytes.
- **Critério de interrupção:** Pula P14.

#### Passo P14: Carving de Mach-O
- **Selo / Reivindicação:** Selo R (C3).
- **Classificação:** Documentado no `artigo.pdf:6` (seção 3 "Mach-O") e `reivindicacoes.md:9`.
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  rm -rf output_macho && foremost-ng -t macho -i macho_sample.raw -o output_macho && ls -la output_macho/macho/ && cat output_macho/audit.txt
  ```
- **Resultado esperado segundo autores:** Extração do binário Mach-O delimitado conforme tamanho indicado no segmento de carga.
- **Evidência a salvar:** `audit_c3_macho.txt` e saída de `file output_macho/macho/*`.
- **Critério de sucesso:** Arquivo `.macho` extraído para `output_macho/macho/` com tamanho de 512 bytes e registrado em `audit.txt`.
- **Critério de falha:** Falha na identificação do magic ou no cálculo do tamanho.
- **Critério de interrupção:** Não interrompe os demais testes.

---

### Bloco C4: Recuperação de Executáveis ELF (32 e 64 bits)

#### Passo P15: Compilação de Binário ELF e Inclusão em Imagem
- **Selo / Reivindicação:** Selo R (C4).
- **Classificação:** [NÃO DOCUMENTADO] (Necessário para gerar um binário ELF autêntico e íntegro para teste, na ausência de dataset fornecido pelos autores).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  echo 'int main(){return 42;}' | gcc -x c - -O2 -o elf_target && python3 -c '
  with open("elf_target", "rb") as f:
      elf_data = f.read()
  with open("elf_sample.raw", "wb") as f:
      f.write(b"\xCC" * 8192)
      f.write(elf_data)
      f.write(b"\xCC" * 8192)
  '
  ```
- **Resultado esperado segundo autores:** N/A (preparação de imagem de teste com executável ELF autêntico).
- **Evidência a salvar:** `elf_target_info.txt` (`readelf -h elf_target`)
- **Critério de sucesso:** Binário compilado e inserido com offset dentro de `elf_sample.raw`.
- **Critério de falha:** Falha de compilação do `elf_target`.
- **Critério de interrupção:** Pula P16.

#### Passo P16: Carving de Executável ELF
- **Selo / Reivindicação:** Selo R (C4).
- **Classificação:** Documentado no `artigo.pdf:6-7` (seção 3 "ELF" e exemplo `-x -t elf`).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  rm -rf output_elf && foremost-ng -t elf -i elf_sample.raw -o output_elf && ls -la output_elf/elf/ && cat output_elf/audit.txt && readelf -h output_elf/elf/*
  ```
- **Resultado esperado segundo autores:** Arquivo ELF de 64 bits extraído com base nos cabeçalhos de programa `PT_LOAD`, preservando layout e legibilidade estrutural por analisador ELF (`readelf`).
- **Evidência a salvar:** `audit_c4_elf.txt` e saída do `readelf -h`.
- **Critério de sucesso:** Arquivo `.elf` extraído e legível por `readelf` com cabeçalhos consistentes.
- **Critério de falha:** Arquivo corrompido, truncated ou rejeitado pelo `readelf`.
- **Critério de interrupção:** Não interrompe os demais testes.

---

### Bloco C5: Enriquecimento pelo VirusTotal

#### Passo P17: Teste de Comportamento sem VT_API_KEY
- **Selo / Reivindicação:** Selo R (C5).
- **Classificação:** Documentado no `artigo.pdf:7` (*"If the API key is missing or invalid, Foremost-NG will still perform carving but will emit a warning and skip all VT lookups"*).
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  rm -rf output_vt_nokey && VT_API_KEY="" foremost-ng -x -t elf -i elf_sample.raw -o output_vt_nokey 2> vt_nokey_err.txt && cat vt_nokey_err.txt && cat output_vt_nokey/audit.txt
  ```
- **Resultado esperado segundo autores:** Emissão de mensagem de aviso de chave ausente/inválida, realização normal do carving do ELF e rotulação como `Clean (0)` ou valor padrão sem bloquear.
- **Evidência a salvar:** `vt_nokey_err.txt` e `audit_vt_nokey.txt`.
- **Critério de sucesso:** Alerta de ausência de chave capturado em stderr e arquivo recuperado normalmente.
- **Critério de falha:** Abort do programa (crash) ou interrupção prematura sem carving.
- **Critério de interrupção:** Não interrompe.

#### Passo P18: Consulta à API do VirusTotal com Chave Válida
- **Selo / Reivindicação:** Selo R (C5).
- **Classificação:** Documentado no `artigo.pdf:3`, `artigo.pdf:7` e `README.md:91-108`.
- **Diretório:** `/home/ubuntu/testes`
- **Comando exato:**
  ```bash
  rm -rf output_vt_key && foremost-ng -x -t elf -i elf_sample.raw -o output_vt_key 2> vt_run_err.txt && cat output_vt_key/audit.txt
  ```
- **Resultado esperado segundo autores:** O `foremost-ng` calcula o SHA-256 do arquivo extraído, consulta `https://www.virustotal.com/api/v3/files/<hash>` via libcurl com o header `x-apikey`, extrai `last_analysis_stats` e popula a coluna `VT` no `audit.txt` com veredito (ex.: `Clean (0)` ou `Malicious (N)`).
- **Evidência a salvar:** `audit_c5_vt.txt` (higienizado, garantindo que não contenha o valor em claro da chave).
- **Critério de sucesso:** Coluna `VT` preenchida com o veredito da consulta no `audit.txt` sem falha de rede/curl.
- **Critério de falha:** Erro de curl persistente ou falha de segmentação ao parsear o JSON de resposta.
- **Critério de interrupção:** Não interrompe os demais passos.

---

### Bloco C6: Exemplo de Execução da Figura 2 (`evidence2.dd`)

#### Passo P19: Busca e Verificação de Existência de `evidence2.dd`
- **Selo / Reivindicação:** Selo R (C6).
- **Classificação:** [NÃO DOCUMENTADO] (Verificação factual no ambiente para averiguar se a imagem `evidence2.dd` citada no artigo e na Figura 2 está presente em algum caminho do artefato).
- **Diretório:** `/home/ubuntu`
- **Comando exato:**
  ```bash
  find / -name "evidence2.dd" 2>/dev/null || echo "evidence2.dd NAO ENCONTRADO NO AMBIENTE"
  ```
- **Resultado esperado segundo autores:** Segundo o artigo (`artigo.pdf:7-8`), a execução foi realizada sobre `evidence2.dd`.
- **Evidência a salvar:** `evidence2_find.txt`
- **Critério de sucesso:** Arquivo `evidence2.dd` localizado com tamanho de 2 GB (2045109643 bytes).
- **Critério de falha:** Arquivo inexistente no repositório/contêiner.
- **Critério de interrupção:** Se o arquivo não existir, P20 falhará necessariamente.

#### Passo P20: Tentativa de Reprodução da Figura 2
- **Selo / Reivindicação:** Selo R (C6).
- **Classificação:** Documentado no `artigo.pdf:8, Fig. 2` e `reivindicacoes.md:12` (`./foremost-ng -v -x evidence2.dd`).
- **Diretório:** `/home/ubuntu/foremost-ng/src`
- **Comando exato:**
  ```bash
  if [ -f evidence2.dd ]; then ./foremost-ng -v -x evidence2.dd; else ./foremost-ng -v -x evidence2.dd 2>&1 || echo "FALHA: evidence2.dd nao encontrado para reproduzir a Fig. 2"; fi
  ```
- **Resultado esperado segundo autores:** Tabela idêntica à da Figura 2: 12 arquivos (3 ELFs, 1 script, 6 EXEs, 2 ZIPs) com os offsets exatos (ex.: 2228224, 2467840, 2615296, 2811904, 204740608, etc.) e as contagens do VirusTotal.
- **Evidência a salvar:** `figura2_reproduction.txt`
- **Critério de sucesso:** Tabela e offsets da Figura 2 reproduzidos e confrontados com os dados publicados.
- **Critério de falha:** Imagem `evidence2.dd` ausente ou arquivos/offsets divergentes da publicação.
- **Critério de interrupção:** Fim dos testes de reprodução.

---

## 5. Estimativa de Tempo

- **P1 a P3 (Preparação e dependências):** ~1 a 2 minutos (dependente da velocidade do download via apt).
- **P4 e P5 (Compilação e instalação):** ~30 segundos.
- **P6 a P8 (Teste mínimo funcional - Selo F):** ~30 segundos.
- **P9 a P16 (Testes de parsers C1 a C4):** ~1 minuto.
- **P17 e P18 (Testes VirusTotal - C5):** ~1 a 2 minutos (dependente do tempo de resposta da API externa).
- **P19 e P20 (Verificação da Figura 2 - C6):** ~30 segundos.
- **Tempo Total Estimado:** **~5 a 7 minutos**.

---

## 6. Tabela Síntese dos Passos

| ID | Selo / Reivindicação | Classificação | Diretório | Comando Exato | Evidência | Critério de Sucesso | Critério de Interrupção |
|---|---|---|---|---|---|---|---|
| **P1** | Geral / F / C5 | [NÃO DOCUMENTADO] | `/home/ubuntu` | `uname -a && cat /etc/os-release && [ -n "$VT_API_KEY" ] && echo "VT_API_KEY configurada (<VT_API_KEY>)"` | `env_info.txt` | Ubuntu 24.04 verificado e chave presente | Não interrompe |
| **P2** | Selo F | [NÃO DOCUMENTADO] | `/home/ubuntu` | `sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev` | `apt_install.log` | Dependências instaladas com código 0 | Interrupção total se falhar |
| **P3** | Selo F | Documentado (README/Dockerfile) | `/home/ubuntu` | `cd /home/ubuntu && if [ -f /opt/foremost-ng/src/Makefile ]; then cp -r /opt/foremost-ng ./foremost-ng; elif [ -f /pacote/artefato.zip ]; then unzip -q /pacote/artefato.zip -d ./foremost-ng; fi && cd foremost-ng` | `tree_artifact.txt` | Fontes disponíveis em `foremost-ng/` | Interrupção total se falhar |
| **P4** | Selo F | Documentado (README:33) | `/home/ubuntu/foremost-ng/src` | `make clean && make` | `build.log` | Binário `foremost-ng` compilado sem erros | Interrupção total se falhar |
| **P5** | Selo F | Documentado (README:34) | `/home/ubuntu/foremost-ng/src` | `sudo make install && which foremost-ng` | `install.log` | Binário instalado em `/usr/local/bin` | Não interrompe |
| **P6** | Selo F | Documentado (artigo p.7) | `/home/ubuntu/foremost-ng/src` | `foremost-ng -V && foremost-ng -h` | `cli_help_version.txt` | Versão e menu de ajuda exibidos sem crash | Interrompe testes de CLI |
| **P7** | Selo F | [NÃO DOCUMENTADO] | `/home/ubuntu/testes` | `mkdir -p /home/ubuntu/testes && cd /home/ubuntu/testes && python3 -c '<cria test_minimo.img com PNG>'` | `test_minimo_created.txt` | Imagem sintética criada | Interrompe P8 |
| **P8** | Selo F | Documentado (artigo p.7) | `/home/ubuntu/testes` | `rm -rf output_f && foremost-ng -i test_minimo.img -o output_f && ls -laR output_f && cat output_f/audit.txt` | `audit_f.txt` | Carving concluído, diretório e `audit.txt` gerados | Interrompe concessão de F |
| **P9** | Selo R (C1) | [NÃO DOCUMENTADO] | `/home/ubuntu/testes` | `python3 -c '<cria evtx_sample.raw com ElfFile\0\0 e chunk 64 KiB>'` | `evtx_sample_spec.txt` | Imagem com EVTX sintético criada | Pula P10 |
| **P10** | Selo R (C1) | Documentado (artigo p.6-7) | `/home/ubuntu/testes` | `rm -rf output_evtx && foremost-ng -t evtx -i evtx_sample.raw -o output_evtx && ls -la output_evtx/evtx/ && cat output_evtx/audit.txt` | `audit_c1_evtx.txt` | Arquivo `.evtx` de 64 KiB recuperado | Não interrompe |
| **P11** | Selo R (C2) | [NÃO DOCUMENTADO] | `/home/ubuntu/testes` | `python3 -c '<cria script_sample.raw com Bash e Python>'` | `script_sample_spec.txt` | Imagem com scripts sintéticos criada | Pula P12 |
| **P12** | Selo R (C2) | Documentado (artigo p.6) | `/home/ubuntu/testes` | `rm -rf output_script && foremost-ng -t script -i script_sample.raw -o output_script && ls -la output_script/script/ && cat output_script/audit.txt` | `audit_c2_script.txt` | Scripts extraídos com corpo legível | Não interrompe |
| **P13** | Selo R (C3) | [NÃO DOCUMENTADO] | `/home/ubuntu/testes` | `python3 -c '<cria macho_sample.raw com header Mach-O 64-bit>'` | `macho_sample_spec.txt` | Imagem com Mach-O sintético criada | Pula P14 |
| **P14** | Selo R (C3) | Documentado (artigo p.6) | `/home/ubuntu/testes` | `rm -rf output_macho && foremost-ng -t macho -i macho_sample.raw -o output_macho && ls -la output_macho/macho/ && cat output_macho/audit.txt` | `audit_c3_macho.txt` | Binário Mach-O extraído com 512 bytes | Não interrompe |
| **P15** | Selo R (C4) | [NÃO DOCUMENTADO] | `/home/ubuntu/testes` | `echo 'int main(){return 42;}' \| gcc -x c - -O2 -o elf_target && python3 -c '<cria elf_sample.raw>'` | `elf_target_info.txt` | Imagem contendo binário ELF autêntico criada | Pula P16 |
| **P16** | Selo R (C4) | Documentado (artigo p.6-7) | `/home/ubuntu/testes` | `rm -rf output_elf && foremost-ng -t elf -i elf_sample.raw -o output_elf && ls -la output_elf/elf/ && cat output_elf/audit.txt && readelf -h output_elf/elf/*` | `audit_c4_elf.txt` | Executável ELF recuperado e legível por `readelf` | Não interrompe |
| **P17** | Selo R (C5) | Documentado (artigo p.7) | `/home/ubuntu/testes` | `rm -rf output_vt_nokey && VT_API_KEY="" foremost-ng -x -t elf -i elf_sample.raw -o output_vt_nokey 2> vt_nokey_err.txt && cat vt_nokey_err.txt` | `vt_nokey_err.txt` | Aviso de chave ausente emitido sem abortar | Não interrompe |
| **P18** | Selo R (C5) | Documentado (artigo p.3, 7) | `/home/ubuntu/testes` | `rm -rf output_vt_key && foremost-ng -x -t elf -i elf_sample.raw -o output_vt_key 2> vt_run_err.txt && cat output_vt_key/audit.txt` | `audit_c5_vt.txt` | Coluna VT preenchida com veredito da API | Não interrompe |
| **P19** | Selo R (C6) | [NÃO DOCUMENTADO] | `/home/ubuntu` | `find / -name "evidence2.dd" 2>/dev/null \|\| echo "evidence2.dd NAO ENCONTRADO NO AMBIENTE"` | `evidence2_find.txt` | Averiguação factual da presença de `evidence2.dd` | Não interrompe |
| **P20** | Selo R (C6) | Documentado (artigo p.8, Fig. 2) | `/home/ubuntu/foremost-ng/src` | `if [ -f evidence2.dd ]; then ./foremost-ng -v -x evidence2.dd; else ./foremost-ng -v -x evidence2.dd 2>&1 \|\| echo "FALHA: evidence2.dd ausente"; fi` | `figura2_reproduction.txt` | Tabela e offsets da Figura 2 reproduzidos | Fim dos testes |