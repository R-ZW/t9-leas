# Roteiro de Execução e Verificação Experimental — Foremost-NG (SBSeg 2025)

**Artefato:** Foremost-NG: An Open-Source Toolkit for Advanced File Carving and Analysis  
**Versão:** `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d`  
**Objetivo:** Roteiro formal para verificação experimental dos selos Funcional (F) e Reprodutível (R) na Etapa E.  
**Ambiente Alvo:** Contêiner Docker com Ubuntu 24.04 LTS limpo, acesso à internet, usuário não-root com sudo, pacotes pré-instalados `sudo`, `unzip`, `man` (sem compilador inicial). Variável `VT_API_KEY` injetada.

---

## 1. Requisitos de Ambiente (Hardware e Software)

### Hardware Mínimo Recomendado
- **Arquitetura / Processador:** x86_64 com suporte a 64 bits, mínimo 2 núcleos vCPU.
- **Memória RAM:** Mínimo de 2 GB (recomendado 4 GB para permitir carregamento de buffers em memória e execução de múltiplos módulos).
- **Armazenamento:** Mínimo de 10 GB de espaço livre em disco para acomodar dependências de compilação, pacotes baixados, eventuais imagens forenses (como a imagem de 2 GB `evidence2.dd` de C6) e os diretórios com os arquivos extraídos.

### Software e Dependências
- **Sistema Operacional:** Ubuntu 24.04 LTS (Linux x86_64).
- **Permissões:** Usuário comum com acesso sudo sem senha (`sudo`).
- **Ferramentas e Bibliotecas:**
  - Compilador e build: `gcc`, `make` (conforme `artefato.txt:Dockerfile:5` e `README.md:33`).
  - Controle de versão e utilitários: `git`, `file`, `bsdextrautils` (para `hexdump` e inspeção de integridade).
  - Bibliotecas de desenvolvimento C: `libssl-dev` (OpenSSL EVP, para hash SHA-256) e `libcurl4-openssl-dev` (libcurl, para consultas HTTP REST à API v3 do VirusTotal), conforme `artefato.txt:Dockerfile:5` e `src/Makefile:46`.
- **Conectividade de Rede:** Acesso externo irrestrito aos repositórios do Ubuntu (`archive.ubuntu.com`), ao GitHub (`github.com`) e ao endpoint de API do VirusTotal (`www.virustotal.com`).
- **Segurança e Chaves:** A chave `VT_API_KEY` deve estar configurada no ambiente. Sob nenhuma hipótese seu conteúdo deve ser impresso em tela, exposto em arquivos de log ou salvo sem máscara.

---

## 2. Teste Mínimo de Funcionalidade (Selo F)

O teste mínimo para comprovação do Selo Funcional compreende:
1. Instalação das dependências oficiais (`gcc`, `make`, `git`, `libssl-dev`, `libcurl4-openssl-dev`);
2. Compilação do binário através do `src/Makefile` dos autores;
3. Instalação no sistema via `make install`;
4. Checagem dos comandos básicos de ajuda (`foremost-ng -h`), versão (`foremost-ng -V`) e página de manual (`man foremost-ng`);
5. Execução de carving sobre uma imagem de entrada sintética com verificação da criação dos subdiretórios de extração e do arquivo `audit.txt`.

---

## 3. Blocos por Reivindicação de Reprodutibilidade (Selo R)

Para a atribuição do Selo R, avaliam-se as reivindicações C1 a C6 fixadas em `reivindicacoes.md`:
- **C1 (Windows Event Logs - EVTX):** Recuperação de registros EVTX pela assinatura `ElfFile\0\0`, delimitando os blocos de 64 KiB (65536 bytes) especificados pelo campo `chunk_count` em `offset 0x18`.
- **C2 (Script Files):** Recuperação de scripts Bash, Python e PowerShell iniciados por shebang `#!`, texto legível com mínimo de 32 bytes e verificação de corpo além de comentários.
- **C3 (Mach-O):** Recuperação de binários Mach-O FAT (universal, `0xCAFEBABE`) e Thin (32-bit `0xCEFAEDFE` / 64-bit `0xCFFAEDFE`) calculando os limites via cabeçalhos e load commands (`LC_SEGMENT` / `LC_SEGMENT_64`).
- **C4 (ELF Executables):** Recuperação de executáveis ELF de 32 e 64 bits (`0x7F454C46`), delimitados pela união dos segmentos de carga (`PT_LOAD`).
- **C5 (VirusTotal API Enrichment):** Ativação da flag `-x`, cálculo do hash SHA-256 de cada arquivo recuperado, requisição HTTP GET com o header `x-apikey` e anotação do veredito (`Clean` ou `Malicious`) na coluna `VT` do arquivo `audit.txt`.
- **C6 (Experimento da Figura 2):** Execução do comando `./foremost-ng -v -x evidence2.dd` sobre a imagem de 2 GB, visando reproduzir a extração dos 12 arquivos (ELF, script, EXE, ZIP) nos offsets reportados na Figura 2 da página 8 do artigo.

---

## 4. Detalhamento Passo a Passo do Roteiro

### P1: Instalação das dependências de compilação
- **Tipo:** [DOCUMENTADO - artefato.txt:Dockerfile:3-6 / artigo.pdf:p.6, §4]
- **Selo / Reivindicação:** Selo F / Pré-requisito geral
- **Diretório (Cwd):** `/`
- **Comando exato:**
  ```bash
  sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev file bsdextrautils
  ```
- **Resultado esperado segundo os autores:** Instalação bem-sucedida das ferramentas de build (`gcc`, `make`), controle de versão e bibliotecas OpenSSL e libcurl sem erros.
- **Evidência a salvar:** `/tmp/evidencias/01_apt_install.log`
- **Critério de sucesso:** Código de retorno 0; comandos `gcc --version` e `make --version` disponíveis no PATH.
- **Critério de falha:** Falha de resolução de pacotes apt ou erro de rede.
- **Critério de interrupção:** Se o compilador GCC ou Make não puderem ser instalados, abortar imediatamente a avaliação.

---

### P2: Obtenção do código-fonte do artefato
- **Tipo:** [DOCUMENTADO - artigo.pdf:p.6, §4 / artefato.txt:Dockerfile:8]
- **Selo / Reivindicação:** Selo F / Pré-requisito geral
- **Diretório (Cwd):** `/home/ubuntu`
- **Comando exato:**
  ```bash
  if [ -d "/opt/foremost-ng/src" ]; then sudo cp -r /opt/foremost-ng /home/ubuntu/foremost-ng && sudo chown -R $(id -u):$(id -g) /home/ubuntu/foremost-ng; elif [ -f "/pacote/artefato.zip" ]; then unzip -q /pacote/artefato.zip -d /home/ubuntu/foremost-ng; else git clone https://github.com/cristianzsh/foremost-ng.git /home/ubuntu/foremost-ng; fi && cd /home/ubuntu/foremost-ng && git log -1 --format="Commit: %H (%cd)" > /tmp/evidencias/02_git_commit.log 2>&1 || ls -la /home/ubuntu/foremost-ng > /tmp/evidencias/02_git_commit.log
  ```
- **Resultado esperado segundo os autores:** Repositório do Foremost-NG clonado ou copiado, com o código-fonte C disponível no diretório `src/`.
- **Evidência a salvar:** `/tmp/evidencias/02_git_commit.log`
- **Critério de sucesso:** Existência do diretório `/home/ubuntu/foremost-ng/src` contendo `Makefile`, `main.c`, `extract.c`, `engine.c`, `dir.c`, `state.c`, `vt_query.c`.
- **Critério de falha:** Diretório ausente ou vazio.
- **Critério de interrupção:** Se o código-fonte não estiver acessível, abortar o roteiro.

---

### P3: Compilação do Foremost-NG
- **Tipo:** [DOCUMENTADO - artefato.txt:README.md:31-35 / artigo.pdf:p.6, §4 / artefato.txt:Dockerfile:10]
- **Selo / Reivindicação:** Selo F
- **Diretório (Cwd):** `/home/ubuntu/foremost-ng/src`
- **Comando exato:**
  ```bash
  make clean && make 2>&1 | tee /tmp/evidencias/03_make_build.log
  ```
- **Resultado esperado segundo os autores:** Compilação de todos os módulos objeto C (`main.o`, `extract.o`, `vt_query.o`, etc.) e ligação com flags `-lssl -lcrypto -lcurl`, produzindo o binário `foremost-ng`.
- **Evidência a salvar:** `/tmp/evidencias/03_make_build.log` e listagem `ls -lh foremost-ng`.
- **Critério de sucesso:** Código de retorno 0; binário executável `foremost-ng` criado.
- **Critério de falha:** Erro de sintaxe, tipos ou símbolos não resolvidos pelo linker (`exit code != 0`).
- **Critério de interrupção:** Se a compilação falhar, o artefato é não-executável; abortar os testes subsequentes.

---

### P4: Instalação do binário no sistema
- **Tipo:** [DOCUMENTADO - artefato.txt:README.md:34 / artigo.pdf:p.6, §4 / artefato.txt:Dockerfile:10]
- **Selo / Reivindicação:** Selo F
- **Diretório (Cwd):** `/home/ubuntu/foremost-ng/src`
- **Comando exato:**
  ```bash
  sudo make install 2>&1 | tee /tmp/evidencias/04_make_install.log && which foremost-ng >> /tmp/evidencias/04_make_install.log
  ```
- **Resultado esperado segundo os autores:** Binário instalado em `/usr/local/bin/foremost-ng`, man page em `/usr/share/man/man8/foremost-ng.8.gz` e configuração em `/usr/local/etc/foremost.conf`.
- **Evidência a salvar:** `/tmp/evidencias/04_make_install.log`
- **Critério de sucesso:** `which foremost-ng` retorna `/usr/local/bin/foremost-ng`.
- **Critério de falha:** Erro de permissão ou falha ao copiar arquivos para o sistema.
- **Critério de interrupção:** Se o binário não for instalado no sistema nem for executável diretamente, interromper.

---

### P5: Verificação dos comandos informativos e documentação
- **Tipo:** [DOCUMENTADO - artefato.txt:README.md:76-80 / artigo.pdf:p.6-7]
- **Selo / Reivindicação:** Selo F
- **Diretório (Cwd):** `/tmp`
- **Comando exato:**
  ```bash
  foremost-ng -V > /tmp/evidencias/05_version.txt 2>&1 && foremost-ng -h > /tmp/evidencias/05_help.txt 2>&1 && man -P cat foremost-ng | head -n 40 > /tmp/evidencias/05_man.txt 2>&1
  ```
- **Resultado esperado segundo os autores:** Exibição da versão `1.5.7`, mensagem de ajuda contendo as opções suportadas (`-v, -V, -h, -x, -t, -i, -o`) e renderização da man page instalada.
- **Evidência a salvar:** `/tmp/evidencias/05_version.txt`, `/tmp/evidencias/05_help.txt`, `/tmp/evidencias/05_man.txt`.
- **Critério de sucesso:** Execução limpa (código 0) exibindo a identificação do Foremost-NG e autores.
- **Critério de falha:** Segfault, crash ou erro de comando não encontrado.
- **Critério de interrupção:** Falha com crash crítico na execução das opções básicas.

---

### P6: Geração de arquivo de imagem de teste funcional mínimo
- **Tipo:** [NÃO DOCUMENTADO]  
  *Justificativa:* Os autores não forneceram no repositório imagens de teste prontas nem scripts auxiliares para exercitar a ferramenta em um caso mínimo. A síntese controlada de uma imagem de teste contendo cabeçalhos conhecidos é necessária para atestar a capacidade operacional do binário de realizar o carving e gerar as saídas esperadas sem dados externos.
- **Selo / Reivindicação:** Selo F
- **Diretório (Cwd):** `/tmp/teste_f`
- **Comando exato:**
  ```bash
  mkdir -p /tmp/teste_f && cd /tmp/teste_f && python3 -c '
  with open("test_f.img", "wb") as f:
      f.write(b"\x00" * 1024)
      # Script bash embutido
      script_data = b"#!/bin/bash\n# Minimal functional test\necho \"Foremost-NG is functional\"\nexit 0\n"
      f.write(script_data)
      f.write(b"\x00" * 2048)
      # Arquivo PNG minimo embutido
      png_header = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\x00IEND\xaeB`\x82"
      f.write(png_header)
      f.write(b"\x00" * 1024)
  ' && ls -lh test_f.img > /tmp/evidencias/06_prep_test_f.log 2>&1
  ```
- **Resultado esperado:** Arquivo de imagem `test_f.img` criado com artefatos injetados em posições conhecidas.
- **Evidência a salvar:** `/tmp/evidencias/06_prep_test_f.log`
- **Critério de sucesso:** Arquivo `test_f.img` criado com tamanho coerente (> 4 KiB).
- **Critério de falha:** Erro no interpretador python ou falha de escrita.
- **Critério de interrupção:** Se não for possível criar o arquivo de entrada, interromper o teste de carving.

---

### P7: Execução do carving mínimo e validação de saída
- **Tipo:** [DOCUMENTADO - artigo.pdf:p.7, §4.1 / artefato.txt:README.md:82-85]
- **Selo / Reivindicação:** Selo F
- **Diretório (Cwd):** `/tmp/teste_f`
- **Comando exato:**
  ```bash
  foremost-ng -i test_f.img -o /tmp/teste_f/output_f 2>&1 | tee /tmp/evidencias/07_exec_f.log && ls -laR /tmp/teste_f/output_f >> /tmp/evidencias/07_exec_f.log && cp /tmp/teste_f/output_f/audit.txt /tmp/evidencias/07_audit_f.txt
  ```
- **Resultado esperado segundo os autores:** Processamento completo da imagem, criação do diretório `/tmp/teste_f/output_f`, geração do arquivo `audit.txt` detalhando a sessão e extração dos arquivos reconhecidos em subpastas correspondentes.
- **Evidência a salvar:** `/tmp/evidencias/07_exec_f.log` e `/tmp/evidencias/07_audit_f.txt`.
- **Critério de sucesso:** Retorno 0; arquivo `audit.txt` gerado com cabeçalho de auditoria e listagem de processamento.
- **Critério de falha:** Falha de segmentação, diretório de saída não criado ou arquivo `audit.txt` ausente.
- **Critério de interrupção:** Não se aplica (conclui o teste de F).

---

### P8: Preparação de massa de teste para Windows Event Logs (EVTX)
- **Tipo:** [NÃO DOCUMENTADO]  
  *Justificativa:* Nenhum arquivo `.evtx` ou imagem correspondente foi incluído no repositório. Para testar o parser nativo de EVTX introduzido pelos autores (`extract_evtx`), é indispensável criar uma imagem de teste contendo o cabeçalho oficial de arquivo EVTX (`ElfFile\0\0`), o número de chunks de 64 KiB em offset 0x18 e padding apropriado.
- **Selo / Reivindicação:** Selo R (Reivindicação C1)
- **Diretório (Cwd):** `/tmp/teste_c1`
- **Comando exato:**
  ```bash
  mkdir -p /tmp/teste_c1 && cd /tmp/teste_c1 && python3 -c '
  import struct
  # Header EVTX: 8 bytes magic "ElfFile\0\0", 16 bytes dados, 4 bytes chunk_count = 1 em 0x18
  header = b"ElfFile\x00\x00" + (b"\x00" * 16) + struct.pack("<I", 1) + (b"\x00" * 4068)
  # Chunk de 64 KiB (65536 bytes)
  chunk = b"ElfChnk\x00" + (b"\xaa" * (65536 - 8))
  evtx_full = header + chunk
  with open("c1_evtx.img", "wb") as f:
      f.write(b"\x90" * 512) # offset de alinhamento
      f.write(evtx_full)
      f.write(b"\x90" * 512)
  ' && ls -lh c1_evtx.img > /tmp/evidencias/08_prep_c1.log 2>&1
  ```
- **Resultado esperado:** Imagem `c1_evtx.img` criada com a estrutura binária EVTX sintetizada conforme especificação técnica.
- **Evidência a salvar:** `/tmp/evidencias/08_prep_c1.log`
- **Critério de sucesso:** Arquivo gerado com integridade da assinatura `ElfFile\0\0`.
- **Critério de falha:** Erro na geração do arquivo.
- **Critério de interrupção:** Pular teste de C1 caso ocorra falha de geração.

---

### P9: Execução de carving de EVTX (C1)
- **Tipo:** [DOCUMENTADO - artigo.pdf:p.6, §3; p.7, §4.1]
- **Selo / Reivindicação:** Selo R (Reivindicação C1)
- **Diretório (Cwd):** `/tmp/teste_c1`
- **Comando exato:**
  ```bash
  foremost-ng -t evtx -i c1_evtx.img -o /tmp/teste_c1/output_c1 2>&1 | tee /tmp/evidencias/09_exec_c1.log && ls -la /tmp/teste_c1/output_c1/evtx >> /tmp/evidencias/09_exec_c1.log && cp /tmp/teste_c1/output_c1/audit.txt /tmp/evidencias/09_audit_c1.txt
  ```
- **Resultado esperado segundo os autores:** O módulo EVTX reconhece a assinatura `ElfFile\0\0`, extrai o log de eventos para a subpasta `output_c1/evtx/00000001.evtx` e registra a extração no `audit.txt`.
- **Evidência a salvar:** `/tmp/evidencias/09_exec_c1.log` e `/tmp/evidencias/09_audit_c1.txt`.
- **Critério de sucesso:** Arquivo `.evtx` recuperado na subpasta correspondente e registrado no arquivo de auditoria.
- **Critério de falha:** Nenhum arquivo recuperado, falha de segmentação no parser ou pasta `evtx/` não criada.
- **Critério de interrupção:** Não se aplica.

---

### P10: Preparação de massa de teste para scripts (C2)
- **Tipo:** [NÃO DOCUMENTADO]  
  *Justificativa:* Inexistência de arquivos de script de teste no pacote. É necessário sintetizar uma imagem contendo scripts com shebang (`#!`), corpo textual imprimível e tamanho > 32 bytes, bem como um falso-positivo contendo apenas comentários, para validar o filtro de relevância do parser.
- **Selo / Reivindicação:** Selo R (Reivindicação C2)
- **Diretório (Cwd):** `/tmp/teste_c2`
- **Comando exato:**
  ```bash
  mkdir -p /tmp/teste_c2 && cd /tmp/teste_c2 && python3 -c '
  with open("c2_script.img", "wb") as f:
      f.write(b"\x00" * 512)
      # Script Bash valido (> 32 bytes com codigo)
      f.write(b"#!/bin/bash\n# Script Forense SBSeg 2025\necho \"Carving Bash Script\"\nexit 0\n")
      f.write(b"\x00" * 1024)
      # Script Python valido
      f.write(b"#!/usr/bin/env python3\n# Python Carving Test\nprint(\"Carved Python Script Successfully\")\n")
      f.write(b"\x00" * 512)
      # Script falso positivo (apenas shebang e comentarios, deve ser descartado pelo parser)
      f.write(b"#!/bin/sh\n# Apenas comentarios\n# Sem codigo nenhum\n")
      f.write(b"\x00" * 512)
  ' && ls -lh c2_script.img > /tmp/evidencias/10_prep_c2.log 2>&1
  ```
- **Resultado esperado:** Imagem `c2_script.img` contendo os scripts de teste.
- **Evidência a salvar:** `/tmp/evidencias/10_prep_c2.log`
- **Critério de sucesso:** Arquivo gerado com sucesso.
- **Critério de falha:** Erro na criação da imagem.
- **Critério de interrupção:** Pular teste de C2 se falhar.

---

### P11: Execução de carving de scripts (C2)
- **Tipo:** [DOCUMENTADO - artigo.pdf:p.6, §3; p.7, §4.1]
- **Selo / Reivindicação:** Selo R (Reivindicação C2)
- **Diretório (Cwd):** `/tmp/teste_c2`
- **Comando exato:**
  ```bash
  foremost-ng -t script -i c2_script.img -o /tmp/teste_c2/output_c2 2>&1 | tee /tmp/evidencias/11_exec_c2.log && head -n 20 /tmp/teste_c2/output_c2/script/* >> /tmp/evidencias/11_exec_c2.log 2>&1 && cp /tmp/teste_c2/output_c2/audit.txt /tmp/evidencias/11_audit_c2.txt
  ```
- **Resultado esperado segundo os autores:** Foremost-NG identifica os scripts por shebang (`#!`), extrai o corpo de código completo descartando entradas que contenham apenas comentários, gravando em `output_c2/script/`.
- **Evidência a salvar:** `/tmp/evidencias/11_exec_c2.log` e `/tmp/evidencias/11_audit_c2.txt`.
- **Critério de sucesso:** Scripts válidos extraídos com shebang preservado e corpo de código legível; registro correspondente no `audit.txt`.
- **Critério de falha:** Scripts válidos ignorados ou corrupção de conteúdo.
- **Critério de interrupção:** Não se aplica.

---

### P12: Preparação de massa de teste para Mach-O (C3)
- **Tipo:** [NÃO DOCUMENTADO]  
  *Justificativa:* O repositório não inclui binários Mach-O nem imagens de disco para sua recuperação. É necessário sintetizar uma estrutura compatível com os identificadores universais (`0xCAFEBABE`) ou Mach-O 64-bit LE (`0xCFFAEDFE`) e comando `LC_SEGMENT_64` (0x19) para testar a rotina `extract_macho`.
- **Selo / Reivindicação:** Selo R (Reivindicação C3)
- **Diretório (Cwd):** `/tmp/teste_c3`
- **Comando exato:**
  ```bash
  mkdir -p /tmp/teste_c3 && cd /tmp/teste_c3 && python3 -c '
  import struct
  # Mach-O 64-bit LE: magic 0xFEEDFACF (LE: 0xCF, 0xFA, 0xED, 0xFE)
  # mach_header_64 tem 32 bytes: magic(4), cputype(4), cpusubtype(4), filetype(4), ncmds(4), sizeofcmds(4), flags(4), reserved(4)
  magic = struct.pack("<I", 0xFEEDFACF)
  header = magic + struct.pack("<IIIIIII", 0x01000007, 3, 2, 1, 72, 0, 0)
  # Load command: LC_SEGMENT_64 = 0x19, cmdsize = 72, segname = "__TEXT\0...", vmaddr=0, vmsize=4096, fileoff=0, filesize=4096
  lc = struct.pack("<II16sQQQQII", 0x19, 72, b"__TEXT\x00", 0, 4096, 0, 4096, 7, 5)
  payload = b"\x90" * (4096 - len(header) - len(lc))
  macho_full = header + lc + payload
  with open("c3_macho.img", "wb") as f:
      f.write(b"\x00" * 512)
      f.write(macho_full)
      f.write(b"\x00" * 512)
  ' && ls -lh c3_macho.img > /tmp/evidencias/12_prep_c3.log 2>&1
  ```
- **Resultado esperado:** Imagem `c3_macho.img` contendo cabeçalho Mach-O de 64 bits sintetizado.
- **Evidência a salvar:** `/tmp/evidencias/12_prep_c3.log`
- **Critério de sucesso:** Imagem gerada com o cabeçalho Mach-O estruturado.
- **Critério de falha:** Erro na criação do arquivo.
- **Critério de interrupção:** Pular teste de C3 se falhar.

---

### P13: Execução de carving de Mach-O (C3)
- **Tipo:** [DOCUMENTADO - artigo.pdf:p.6, §3; p.7, §4.1]
- **Selo / Reivindicação:** Selo R (Reivindicação C3)
- **Diretório (Cwd):** `/tmp/teste_c3`
- **Comando exato:**
  ```bash
  foremost-ng -t macho -i c3_macho.img -o /tmp/teste_c3/output_c3 2>&1 | tee /tmp/evidencias/13_exec_c3.log && file /tmp/teste_c3/output_c3/macho/* >> /tmp/evidencias/13_exec_c3.log 2>&1 && cp /tmp/teste_c3/output_c3/audit.txt /tmp/evidencias/13_audit_c3.txt
  ```
- **Resultado esperado segundo os autores:** O Foremost-NG reconhece a assinatura Mach-O, calcula a extensão do executável via load commands e extrai o binário para `output_c3/macho/`.
- **Evidência a salvar:** `/tmp/evidencias/13_exec_c3.log` e `/tmp/evidencias/13_audit_c3.txt`.
- **Critério de sucesso:** Arquivo `.macho` extraído e reconhecido como binário Mach-O pelo utilitário `file`, registrado no log `audit.txt`.
- **Critério de falha:** Binário ignorado ou falha de segmentação no parser.
- **Critério de interrupção:** Não se aplica.

---

### P14: Preparação de massa de teste para executáveis ELF (C4)
- **Tipo:** [NÃO DOCUMENTADO]  
  *Justificativa:* Não foram providenciadas amostras ou imagens contendo binários ELF no repositório. Para testar o delimitador de executáveis ELF de 32/64 bits baseado na tabela de program headers (`PT_LOAD`), é necessário embutir um executável ELF real do sistema em uma imagem de teste.
- **Selo / Reivindicação:** Selo R (Reivindicação C4)
- **Diretório (Cwd):** `/tmp/teste_c4`
- **Comando exato:**
  ```bash
  mkdir -p /tmp/teste_c4 && cd /tmp/teste_c4 && python3 -c '
  with open("/bin/true", "rb") as f_in:
      elf_data = f_in.read()
  with open("c4_elf.img", "wb") as f_out:
      f_out.write(b"\x00" * 1024)
      f_out.write(elf_data)
      f_out.write(b"\x00" * 1024)
  ' && ls -lh c4_elf.img > /tmp/evidencias/14_prep_c4.log 2>&1
  ```
- **Resultado esperado:** Imagem `c4_elf.img` contendo o binário ELF real do sistema circundado por padding.
- **Evidência a salvar:** `/tmp/evidencias/14_prep_c4.log`
- **Critério de sucesso:** Arquivo gerado contendo o executável ELF intacto.
- **Critério de falha:** Falha de leitura de `/bin/true` ou na escrita da imagem.
- **Critério de interrupção:** Pular teste de C4 se falhar.

---

### P15: Execução de carving de ELF e validação de integridade (C4)
- **Tipo:** [DOCUMENTADO - artigo.pdf:p.6, §3; p.7, §4.1]
- **Selo / Reivindicação:** Selo R (Reivindicação C4)
- **Diretório (Cwd):** `/tmp/teste_c4`
- **Comando exato:**
  ```bash
  foremost-ng -t elf -i c4_elf.img -o /tmp/teste_c4/output_c4 2>&1 | tee /tmp/evidencias/15_exec_c4.log && readelf -h /tmp/teste_c4/output_c4/elf/00000002.elf >> /tmp/evidencias/15_exec_c4.log 2>&1 || readelf -h /tmp/teste_c4/output_c4/elf/* >> /tmp/evidencias/15_exec_c4.log 2>&1 && cp /tmp/teste_c4/output_c4/audit.txt /tmp/evidencias/15_audit_c4.txt
  ```
- **Resultado esperado segundo os autores:** Foremost-NG localiza a assinatura `\x7FELF`, calcula o final dos segmentos `PT_LOAD`, extrai o executável preservando cabeçalhos e símbolos, registrando a extração no `audit.txt`.
- **Evidência a salvar:** `/tmp/evidencias/15_exec_c4.log` e `/tmp/evidencias/15_audit_c4.txt`.
- **Critério de sucesso:** Executável extraído em `output_c4/elf/` com cabeçalho íntegro reconhecido com sucesso pelo `readelf -h`.
- **Critério de falha:** ELF truncado, corrompido ou não reconhecido por ferramentas do sistema.
- **Critério de interrupção:** Não se aplica.

---

### P16: Verificação de segurança da variável VT_API_KEY (C5)
- **Tipo:** [DOCUMENTADO - artefato.txt:README.md:91-108 / artigo.pdf:p.3, §2]
- **Selo / Reivindicação:** Selo R (Reivindicação C5)
- **Diretório (Cwd):** `/tmp/teste_c5`
- **Comando exato:**
  ```bash
  mkdir -p /tmp/teste_c5 && cd /tmp/teste_c5 && if [ -n "$VT_API_KEY" ]; then echo "VT_API_KEY esta definida e nao-vazia (mascarada)"; else echo "AVISO: VT_API_KEY nao configurada no ambiente"; fi > /tmp/evidencias/16_vt_key_status.txt
  ```
- **Resultado esperado segundo os autores:** Confirmação da presença da chave de API no ambiente para viabilizar as consultas externas à plataforma VirusTotal.
- **Regra obrigatória de segurança:** Jamais imprimir, exibir ou salvar em logs o valor da chave `VT_API_KEY`.
- **Evidência a salvar:** `/tmp/evidencias/16_vt_key_status.txt`
- **Critério de sucesso:** Registro do status "VT_API_KEY esta definida e nao-vazia (mascarada)".
- **Critério de falha:** Variável vazia ou não declarada.
- **Critério de interrupção:** Se a variável não estiver presente, as consultas à API falharão (emitindo aviso documentado pelo autor).

---

### P17: Execução de carving com enriquecimento pelo VirusTotal (C5)
- **Tipo:** [DOCUMENTADO - artigo.pdf:p.7, §4.1; p.8, Fig. 2 / artefato.txt:README.md:89-108]
- **Selo / Reivindicação:** Selo R (Reivindicação C5)
- **Diretório (Cwd):** `/tmp/teste_c5`
- **Comando exato:**
  ```bash
  foremost-ng -v -x -t elf -i /tmp/teste_c4/c4_elf.img -o /tmp/teste_c5/output_c5 2>&1 | tee /tmp/evidencias/17_exec_c5.log && cat /tmp/teste_c5/output_c5/audit.txt >> /tmp/evidencias/17_exec_c5.log && cp /tmp/teste_c5/output_c5/audit.txt /tmp/evidencias/17_audit_c5.txt
  ```
- **Resultado esperado segundo os autores:** O Foremost-NG calcula o hash criptográfico do arquivo extraído, conecta-se via libcurl ao endpoint `https://www.virustotal.com/api/v3/files/<hash>`, obtém o veredito e anota o `audit.txt` na coluna `VT` com o status (`Clean` ou `Malicious`) e as contagens de detecção.
- **Evidência a salvar:** `/tmp/evidencias/17_exec_c5.log` e `/tmp/evidencias/17_audit_c5.txt`.
- **Critério de sucesso:** Coluna `VT` preenchida no relatório `audit.txt` associada ao artefato extraído.
- **Critério de falha:** Crash por libcurl/SSL, falha na manipulação de memória de resposta ou ausência da coluna VT.
- **Critério de interrupção:** Não se aplica.

---

### P18: Busca e conferência do dataset da Figura 2 (`evidence2.dd`) (C6)
- **Tipo:** [DOCUMENTADO no artigo / NÃO DOCUMENTADO: localização e fornecimento no repositório]  
  *Justificativa:* A Figura 2 do artigo descreve uma execução empírica sobre uma imagem de 2 GB denominada `evidence2.dd`. Como o arquivo não integra o repositório público (`artefato.txt`), é mandatório checar se ele se encontra presente no sistema de arquivos do contêiner para viabilizar a reprodução.
- **Selo / Reivindicação:** Selo R (Reivindicação C6)
- **Diretório (Cwd):** `/`
- **Comando exato:**
  ```bash
  find / -name "evidence2.dd" 2>/dev/null > /tmp/evidencias/18_find_evidence2.log && if [ -s /tmp/evidencias/18_find_evidence2.log ]; then ls -lh $(cat /tmp/evidencias/18_find_evidence2.log) >> /tmp/evidencias/18_find_evidence2.log; else echo "Arquivo evidence2.dd NAO ENCONTRADO no sistema de arquivos" >> /tmp/evidencias/18_find_evidence2.log; fi
  ```
- **Resultado esperado segundo os autores:** Localização do arquivo forense `evidence2.dd` de 2 GB (2045109643 bytes).
- **Evidência a salvar:** `/tmp/evidencias/18_find_evidence2.log`
- **Critério de sucesso:** Arquivo `evidence2.dd` localizado com tamanho condizente.
- **Critério de falha:** Arquivo não localizado (fato impeditivo para execução direta de C6).
- **Critério de interrupção:** Se o arquivo não existir e não houver meio de baixá-lo ou gerá-lo, o passo P19 não pode ser executado diretamente, registrando-se a ausência fática do dataset.

---

### P19: Execução do experimento da Figura 2 (C6)
- **Tipo:** [DOCUMENTADO - artigo.pdf:p.7, §4.2; p.8, Fig. 2]
- **Selo / Reivindicação:** Selo R (Reivindicação C6)
- **Diretório (Cwd):** Diretório de localização do arquivo `evidence2.dd` (se existente) ou `/home/ubuntu`
- **Comando exato:**
  ```bash
  EV_PATH=$(cat /tmp/evidencias/18_find_evidence2.log | head -n 1)
  if [ -f "$EV_PATH" ]; then
      cd $(dirname "$EV_PATH") && foremost-ng -v -x $(basename "$EV_PATH") 2>&1 | tee /tmp/evidencias/19_exec_c6_fig2.log
      cp output/audit.txt /tmp/evidencias/19_audit_fig2.txt 2>/dev/null || true
  else
      echo "EXECUCAO IMPOSSIBILITADA: Arquivo evidence2.dd nao encontrado no ambiente de teste." > /tmp/evidencias/19_exec_c6_fig2.log
  fi
  ```
- **Resultado esperado segundo os autores:** Execução com saída idêntica à da Figura 2, reportando 12 arquivos recuperados (IDs 0 a 11: ELF, script, EXE, ZIP) nos offsets exatos de 2228224 a 914965615 e preenchimento da coluna VT.
- **Evidência a salvar:** `/tmp/evidencias/19_exec_c6_fig2.log` e `/tmp/evidencias/19_audit_fig2.txt`.
- **Critério de sucesso:** Extração dos 12 arquivos especificados nos offsets documentados na Figura 2.
- **Critério de falha:** Divergência nos offsets/arquivos ou impossibilidade de execução por falta do arquivo `evidence2.dd`.
- **Critério de interrupção:** Não se aplica.

---

## 5. Estimativa de Tempo

| Fase | Descrição | Tempo Estimado |
|---|---|---|
| **Fase 1 (P1 a P4)** | Atualização do apt, download de pacotes, compilação via `make` e instalação do binário | ~2 a 4 minutos |
| **Fase 2 (P5 a P7)** | Verificação de comandos informativos e teste funcional mínimo de carving (Selo F) | ~1 a 2 minutos |
| **Fase 3 (P8 a P17)** | Preparação das massas de dados e testes das reivindicações C1 a C5 (incluindo consultas de rede VT) | ~3 a 5 minutos |
| **Fase 4 (P18 a P19)** | Busca e eventual processamento da imagem de 2 GB de C6 | ~1 minuto (se ausente) a ~4 minutos (se presente) |
| **Tempo Total Estimado** | Execução integral do roteiro experimental no contêiner | **~7 a 15 minutos** |

---

## 6. Tabela Consolidada de Passos

| ID | Selo / Reiv. | Tipo | Diretório | Comando Exato | Resultado Esperado | Evidência | Sucesso | Falha | Interrupção? |
|---|---|---|---|---|---|---|---|---|---|
| **P1** | F / Pré-req. | [DOC] | `/` | `sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev file bsdextrautils` | Instalação de compilador e libs | `01_apt_install.log` | GCC e Make disponíveis | Erro apt/rede | Sim (se sem gcc/make) |
| **P2** | F / Pré-req. | [DOC] | `/home/ubuntu` | `if [ -d "/opt/foremost-ng/src" ]; then sudo cp -r /opt/foremost-ng /home/ubuntu/foremost-ng; ... fi` | Código-fonte acessível | `02_git_commit.log` | Pasta `src/` com `.c` e Makefile | Código ausente | Sim (se sem fonte) |
| **P3** | F | [DOC] | `.../src` | `make clean && make` | Binário compilado | `03_make_build.log` | Executável `foremost-ng` | Erro compilação | Sim (se compilação falhar) |
| **P4** | F | [DOC] | `.../src` | `sudo make install && which foremost-ng` | Instalação no sistema | `04_make_install.log` | Binário em `/usr/local/bin` | Erro instalação | Sim (se sem binário) |
| **P5** | F | [DOC] | `/tmp` | `foremost-ng -V && foremost-ng -h && man -P cat foremost-ng` | Versão, ajuda e man page | `05_version.txt`, `05_help.txt` | Retorno 0 e texto informativo | Segfault / crash | Sim (se crash básico) |
| **P6** | F | [NÃO DOC] | `/tmp/teste_f` | Script Python gerando `test_f.img` com artefatos | Imagem sintética criada | `06_prep_test_f.log` | Imagem criada (> 4 KiB) | Erro de escrita | Sim (se sem imagem) |
| **P7** | F | [DOC] | `/tmp/teste_f` | `foremost-ng -i test_f.img -o /tmp/teste_f/output_f` | Carving executado e audit gerado | `07_exec_f.log`, `07_audit_f.txt` | Pasta `output_f/` e `audit.txt` | Crash / sem audit | Não |
| **P8** | R (C1) | [NÃO DOC] | `/tmp/teste_c1` | Script Python gerando `c1_evtx.img` com `ElfFile\0\0` | Imagem com EVTX sintetizado | `08_prep_c1.log` | Arquivo criado com cabeçalho EVTX | Erro na criação | Não |
| **P9** | R (C1) | [DOC] | `/tmp/teste_c1` | `foremost-ng -t evtx -i c1_evtx.img -o /tmp/teste_c1/output_c1` | Extração de `.evtx` de 64 KiB | `09_exec_c1.log`, `09_audit_c1.txt` | `.evtx` recuperado e audit registrado | Falha no carving | Não |
| **P10** | R (C2) | [NÃO DOC] | `/tmp/teste_c2` | Script Python gerando `c2_script.img` com scripts | Imagem com scripts bash/python | `10_prep_c2.log` | Imagem criada com scripts | Erro na criação | Não |
| **P11** | R (C2) | [DOC] | `/tmp/teste_c2` | `foremost-ng -t script -i c2_script.img -o /tmp/teste_c2/output_c2` | Extração de scripts válidos | `11_exec_c2.log`, `11_audit_c2.txt` | Scripts extraídos com shebang | Script ignorado/truncado | Não |
| **P12** | R (C3) | [NÃO DOC] | `/tmp/teste_c3` | Script Python gerando `c3_macho.img` com Mach-O | Imagem com Mach-O 64-bit LE | `12_prep_c3.log` | Imagem criada com header Mach-O | Erro na criação | Não |
| **P13** | R (C3) | [DOC] | `/tmp/teste_c3` | `foremost-ng -t macho -i c3_macho.img -o /tmp/teste_c3/output_c3` | Extração de binário Mach-O | `13_exec_c3.log`, `13_audit_c3.txt` | `.macho` extraído e reconhecido | Falha no carving | Não |
| **P14** | R (C4) | [NÃO DOC] | `/tmp/teste_c4` | Script Python gerando `c4_elf.img` a partir de `/bin/true` | Imagem contendo executável ELF | `14_prep_c4.log` | Imagem criada com ELF real | Erro na criação | Não |
| **P15** | R (C4) | [DOC] | `/tmp/teste_c4` | `foremost-ng -t elf -i c4_elf.img -o /tmp/teste_c4/output_c4` | Extração de ELF legível | `15_exec_c4.log`, `15_audit_c4.txt` | ELF íntegro no `readelf -h` | ELF corrompido/truncado | Não |
| **P16** | R (C5) | [DOC] | `/tmp/teste_c5` | Checagem segura e mascarada de `VT_API_KEY` | Confirmação da chave no env | `16_vt_key_status.txt` | Chave confirmada mascarada | Chave não definida | Não |
| **P17** | R (C5) | [DOC] | `/tmp/teste_c5` | `foremost-ng -v -x -t elf -i ... -o /tmp/teste_c5/output_c5` | Consulta VT e coluna VT no log | `17_exec_c5.log`, `17_audit_c5.txt` | Coluna VT preenchida no audit | Crash libcurl / sem VT | Não |
| **P18** | R (C6) | [DOC/NÃO DOC] | `/` | `find / -name "evidence2.dd"` | Busca da imagem da Figura 2 | `18_find_evidence2.log` | `evidence2.dd` encontrado | Arquivo ausente | Não |
| **P19** | R (C6) | [DOC] | `dir(evidence2.dd)` | `foremost-ng -v -x evidence2.dd` | Tabela exata da Figura 2 (12 arqs) | `19_exec_c6_fig2.log`, `19_audit_fig2.txt` | 12 arquivos e offsets idênticos | Offsets divergem ou sem dado | Não |