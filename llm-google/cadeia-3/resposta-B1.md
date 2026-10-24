# Roteiro de Execução e Avaliação Factual — Foremost-NG (SBSeg 2025)

Este roteiro estabelece o procedimento operacional que será executado na Etapa E dentro do contêiner Docker (`Ubuntu 24.04` limpo, usuário não-root com permissões de `sudo`, contendo inicialmente apenas `sudo`, `unzip` e `man`), visando comprovar factualmente os selos **Funcional (F)** e **Reprodutível (R)** de acordo com os critérios oficiais do SBSeg 2025.

---

## 1. Requisitos do Ambiente

### 1.1. Hardware
- **Arquitetura de CPU:** x86_64 (mínimo de 2 núcleos recomendados).
- **Memória RAM:** Mínimo de 2 GB (4 GB recomendados para bufferização de I/O em carving).
- **Armazenamento:** Mínimo de 5 GB de espaço livre em disco para acomodar dependências de compilação, código-fonte, amostras e diretórios de extração.

### 1.2. Software e Configuração Inicial
- **Sistema Operacional:** Ubuntu 24.04 LTS (base limpa).
- **Utilitários pré-instalados:** `sudo`, `unzip`, `man`.
- **Acesso à Rede:** Conexão à internet ativa para atualização de pacotes via `apt` e comunicação com a API do VirusTotal.
- **Variáveis de Ambiente:** A variável `VT_API_KEY` deve estar presente no ambiente para os testes da opção `-x`. A chave nunca será exposta em logs ou saídas (sempre mascarada como `<VT_API_KEY>`).

### 1.3. Dependências de Software a Instalar
- **Compilador e build tools:** `gcc`, `make`, `git`.
- **Bibliotecas de desenvolvimento (headers e bibliotecas dinâmicas):** `libssl-dev` (OpenSSL EVP), `libcurl4-openssl-dev` (libcurl).
- **Ferramentas de análise/validação:** `binutils` (`readelf`), `file`, `python3` (para estruturação das amostras de teste sintéticas).

---

## 2. Roteiro Passo a Passo

---

### Fase 1: Diagnóstico Inicial e Instalação de Dependências

#### **Passo P01** — Diagnóstico do estado inicial do contêiner
- **Selo / Reivindicação:** Requisito de ambiente / Selo F.
- **Origem documental:** [NÃO DOCUMENTADO] — Necessário para registrar com precisão o estado limpo do ambiente antes de qualquer alteração, comprovando ausência de compilador pré-instalado.
- **Diretório:** `/home/usuario` (ou `$HOME`).
- **Comando exato:**
  ```bash
  uname -a && id && gcc --version || true && make --version || true
  ```
- **Resultado esperado segundo os autores:** Sistema operacional identificado como Linux/Ubuntu; comandos `gcc` e `make` não encontrados.
- **Evidência a salvar:** `p01_ambiente_inicial.txt`
- **Critério de sucesso:** Informações de kernel, usuário e confirmação de ausência de compilador registradas.
- **Critério de falha:** Falha de execução de comandos básicos de shell.
- **Critério de interrupção:** Nenhum.

#### **Passo P02** — Instalação das dependências de compilação
- **Selo / Reivindicação:** Selo F (Instalação e Dependências).
- **Origem documental:** [DOCUMENTADO NO DOCKERFILE:3-6 / NÃO DOCUMENTADO NO README] — O `README.md` não informa dependências para Linux; o `Dockerfile` documenta a lista de pacotes apt necessários.
- **Diretório:** `/home/usuario`
- **Comando exato:**
  ```bash
  sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev file binutils python3
  ```
- **Resultado esperado segundo os autores:** Instalação bem-sucedida da toolchain GCC, bibliotecas OpenSSL e cURL, e utilitários auxiliares.
- **Evidência a salvar:** `p02_apt_install.log`
- **Critério de sucesso:** Retorno 0 do `apt-get` e disponibilidade de `gcc`, `make`, `libssl` e `libcurl`.
- **Critério de falha:** Erro de rede ou indisponibilidade de pacotes nos espelhos do Ubuntu.
- **Critério de interrupção:** Sim; sem compilador e bibliotecas C, o artefato não pode ser construído.

---

### Fase 2: Obtenção do Código, Compilação e Instalação

#### **Passo P03** — Descompactação / Obtenção do repositório no commit exato
- **Selo / Reivindicação:** Selo F (Instalação).
- **Origem documental:** [DOCUMENTADO NO README:27-28 E ARTIGO: p. 6, §4] — Descompactação do arquivo do repositório ou clone/checkout no commit `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d`.
- **Diretório:** `/home/usuario`
- **Comando exato:**
  ```bash
  if [ -f /pacote/artefato.zip ]; then
      unzip -q /pacote/artefato.zip -d /home/usuario/
      mv /home/usuario/foremost-ng-* /home/usuario/foremost-ng || true
  else
      git clone https://github.com/cristianzsh/foremost-ng.git /home/usuario/foremost-ng
      cd /home/usuario/foremost-ng && git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d
  fi
  ls -la /home/usuario/foremost-ng
  ```
- **Resultado esperado segundo os autores:** Estrutura de diretórios contendo `src/`, `README.md`, `Dockerfile`, etc.
- **Evidência a salvar:** `p03_source_tree.txt`
- **Critério de sucesso:** Diretório `/home/usuario/foremost-ng/src` existente contendo `Makefile` e código C.
- **Critério de falha:** Código-fonte ausente ou diretório inacessível.
- **Critério de interrupção:** Sim.

#### **Passo P04** — Compilação do Foremost-NG
- **Selo / Reivindicação:** Selo F (Instalação).
- **Origem documental:** [DOCUMENTADO NO README:31-33 E DOCKERFILE:10 / DISCREPÂNCIA NO ARTIGO: p. 6] — No README e Dockerfile, a compilação ocorre dentro de `src/` via `make`. (No artigo §4 foi omitido o subdiretório `src`).
- **Diretório:** `/home/usuario/foremost-ng/src`
- **Comando exato:**
  ```bash
  make clean && make
  ```
- **Resultado esperado segundo os autores:** Compilação dos 10 módulos objeto (`main.o`, `state.o`, `helpers.o`, `config.o`, `cli.o`, `engine.o`, `dir.o`, `extract.o`, `api.o`, `vt_query.o`) e geração do binário executável `foremost-ng`.
- **Evidência a salvar:** `p04_build.log`
- **Critério de sucesso:** Executável `foremost-ng` gerado com status de saída 0 do `make`.
- **Critério de falha:** Erro de compilação ou falha de linkedição (ex.: símbolos ausentes de OpenSSL ou cURL).
- **Critério de interrupção:** Sim; a executabilidade é pré-requisito mandatório para F e R.

#### **Passo P05** — Instalação no sistema
- **Selo / Reivindicação:** Selo F (Instalação).
- **Origem documental:** [DOCUMENTADO NO README:34 E ARTIGO: p. 6, §4]
- **Diretório:** `/home/usuario/foremost-ng/src`
- **Comando exato:**
  ```bash
  sudo make install && which foremost-ng && ls -la /usr/local/bin/foremost-ng /usr/local/etc/foremost.conf /usr/share/man/man8/foremost-ng.8.gz
  ```
- **Resultado esperado segundo os autores:** Binário instalado em `/usr/local/bin/foremost-ng`, configuração copiada para `/usr/local/etc/foremost.conf` e manual instalado em `/usr/share/man/man8/`.
- **Evidência a salvar:** `p05_install.log`
- **Critério de sucesso:** Arquivos copiados nos diretórios de sistema e `which foremost-ng` retornando `/usr/local/bin/foremost-ng`.
- **Critério de falha:** Falha de permissão ou alvos ausentes no Makefile.
- **Critério de interrupção:** Parcial (pode-se rodar via caminho local `./foremost-ng`, mas a instalação global valida o README).

---

### Fase 3: Teste Mínimo de Funcionalidade (Selo F)

#### **Passo P06** — Validação de metadados, versão e documentação man
- **Selo / Reivindicação:** Selo F (Execução e Interface).
- **Origem documental:** [DOCUMENTADO NO README:79 E ARTIGO: p. 7]
- **Diretório:** `/home/usuario`
- **Comando exato:**
  ```bash
  foremost-ng -V && echo "---" && foremost-ng -h && echo "---" && man -P cat foremost-ng | head -n 30
  ```
- **Resultado esperado segundo os autores:** Exibição da versão (`1.5.7`), texto de copyright, menu de opções com todas as flags documentadas (incluindo `-x`, `-t`, `-i`, `-o`) e manual do sistema renderizado.
- **Evidência a salvar:** `p06_cli_help.txt`
- **Critério de sucesso:** Retorno de código 0 em `-V` e `-h`, e exibição coerente dos parâmetros.
- **Critério de falha:** *Segmentation fault*, comando travado ou opção ausente.
- **Critério de interrupção:** Não.

#### **Passo P07** — Teste mínimo funcional de carving
- **Selo / Reivindicação:** Selo F (Exemplo mínimo / Prova de funcionamento).
- **Origem documental:** [NÃO DOCUMENTADO NO README / EXEMPLO CONCEITUAL NO ARTIGO: p. 7, §4.1] — O README não inclui exemplo executável com arquivo real. Criamos uma imagem sintética contendo um JPEG válido para validação mínima do motor.
- **Diretório:** `/home/usuario/work`
- **Comando exato:**
  ```bash
  mkdir -p /home/usuario/work && cd /home/usuario/work
  python3 -c '
  import sys
  # Cria um arquivo raw contendo padding e um JPEG minimalista integro
  jpeg = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb\x00C\x00" + b"\x01"*64 + b"\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9"
  raw_data = b"\x00" * 1024 + jpeg + b"\x00" * 2048
  with open("min_test.img", "wb") as f:
      f.write(raw_data)
  '
  foremost-ng -i min_test.img -o out_min
  ls -la out_min && cat out_min/audit.txt
  ```
- **Resultado esperado segundo os autores:** Criação da pasta de saída `out_min`, geração do arquivo `audit.txt` e extração do arquivo para `out_min/jpg/00000002.jpg`.
- **Evidência a salvar:** `p07_min_test_audit.txt` e listagem de `out_min/`.
- **Critério de sucesso:** Diretório `out_min` criado, `audit.txt` gerado registrando o offset (1024) e arquivo JPEG recuperado.
- **Critério de falha:** O programa trava, não gera `audit.txt` ou falha ao esculpir o JPEG.
- **Critério de interrupção:** Sim; se o teste mínimo básico de carving falhar, o artefato não é funcional.

---

### Fase 4: Avaliação das Reivindicações Principais (Selo R)

#### **Passo P08** — Reivindicação C1: Carving de Windows Event Logs (EVTX)
- **Selo / Reivindicação:** Selo R / C1.
- **Origem documental:** [DOCUMENTADO NO ARTIGO: p. 6, §3 E §4.1 / AMOSTRA NÃO DOCUMENTADA] — Sintaxe `-t evtx` documentada. Amostra estruturada com magic `ElfFile\0\0` e chunk de 64 KiB gerada sinteticamente para teste do parser `extract_evtx`.
- **Diretório:** `/home/usuario/work`
- **Comando exato:**
  ```bash
  python3 -c '
  # Estrutura EVTX: 8 bytes ElfFile\0\0, offset 0x18: chunk_count (ex: 1)
  evtx_hdr = bytearray(b"\x00" * 4096)
  evtx_hdr[0:8] = b"ElfFile\x00\x00"
  evtx_hdr[0x18:0x1C] = (1).to_bytes(4, byteorder="little")
  evtx_body = b"\x00" * (65536 - 4096)
  evtx_file = evtx_hdr + evtx_body
  raw_data = b"\xaa" * 2048 + evtx_file + b"\xbb" * 2048
  with open("c1_evtx.img", "wb") as f:
      f.write(raw_data)
  '
  foremost-ng -t evtx -i c1_evtx.img -o out_c1
  cat out_c1/audit.txt && ls -la out_c1/evtx/
  ```
- **Resultado esperado segundo os autores:** Reconhecimento do magic `ElfFile`, delimitação correta do chunk de 64 KiB e extração do arquivo em `out_c1/evtx/`.
- **Evidência a salvar:** `p08_c1_evtx_audit.txt` e saída do comando `ls -la out_c1/evtx/`.
- **Critério de sucesso:** Arquivo `.evtx` recuperado com tamanho correspondente a 65.536 bytes registrado em `audit.txt`.
- **Critério de falha:** O parser ignora a assinatura ou o arquivo não é esculpido.
- **Critério de interrupção:** Não.

#### **Passo P09** — Reivindicação C2: Carving de scripts (Bash, Python)
- **Selo / Reivindicação:** Selo R / C2.
- **Origem documental:** [DOCUMENTADO NO ARTIGO: p. 6, §3 / AMOSTRA NÃO DOCUMENTADA] — Testa extração de scripts com shebang (`#!`), tamanho >= 32 bytes e conteúdo textual além de comentários, e teste negativo com script só de comentários.
- **Diretório:** `/home/usuario/work`
- **Comando exato:**
  ```bash
  python3 -c '
  valid_script = b"#!/bin/bash\n# Script de teste SBSeg\necho \"Foremost-NG Script Carving Test\"\nexit 0\n"
  only_comment = b"#!/bin/bash\n# Apenas comentario\n# Sem conteudo real\n"
  raw_data = b"\x00"*1024 + valid_script + b"\x00"*512 + only_comment + b"\x00"*1024
  with open("c2_script.img", "wb") as f:
      f.write(raw_data)
  '
  foremost-ng -t script -i c2_script.img -o out_c2
  cat out_c2/audit.txt && head -n 20 out_c2/script/* || true
  ```
- **Resultado esperado segundo os autores:** Extração apenas do script válido (com corpo executável) e rejeição do script que contém somente comentários.
- **Evidência a salvar:** `p09_c2_script_audit.txt` e conteúdo do arquivo em `out_c2/script/`.
- **Critério de sucesso:** O script válido é recuperado na íntegra em `out_c2/script/` e listado no `audit.txt`; o script somente com comentários é descartado.
- **Critério de falha:** Nenhum script recuperado ou extração de ruído binário não imprimível.
- **Critério de interrupção:** Não.

#### **Passo P10** — Reivindicação C3: Carving de binários Mach-O (fat e thin)
- **Selo / Reivindicação:** Selo R / C3.
- **Origem documental:** [DOCUMENTADO NO ARTIGO: p. 6, §3 / AMOSTRA NÃO DOCUMENTADA] — Verificação da lógica de `extract_macho` com cabeçalho Universal/FAT (`0xCAFEBABBE`) e thin Mach-O (`0xCFFAEDFE`).
- **Diretório:** `/home/usuario/work`
- **Comando exato:**
  ```bash
  python3 -c '
  # Sintetiza estrutura Mach-O 64-bit minima valida (header + load command LC_SEGMENT_64)
  macho_hdr = bytearray(b"\x00" * 72)
  macho_hdr[0:4] = b"\xfe\xed\xfa\xcf" # magic MH_MAGIC_64 little endian (0xcffaedfe)
  macho_hdr[16:20] = (1).to_bytes(4, "little") # ncmds = 1
  macho_hdr[20:24] = (40).to_bytes(4, "little") # sizeofcmds = 40 (72 - 32)
  # Load command LC_SEGMENT_64 (cmd = 0x19, cmdsize = 40) no offset 32
  macho_hdr[32:36] = (0x19).to_bytes(4, "little")
  macho_hdr[36:40] = (40).to_bytes(4, "little")
  macho_hdr[64:72] = (1024).to_bytes(8, "little") # fileoff = 0, filesize = 1024
  macho_full = bytes(macho_hdr) + b"\x90" * (1024 - 72)
  raw_data = b"\x00" * 512 + macho_full + b"\x00" * 512
  with open("c3_macho.img", "wb") as f:
      f.write(raw_data)
  '
  foremost-ng -t macho -i c3_macho.img -o out_c3
  cat out_c3/audit.txt && ls -la out_c3/macho/ || true
  ```
- **Resultado esperado segundo os autores:** Detecção do cabeçalho Mach-O, leitura dos comandos de carga e extração do binário delimitado.
- **Evidência a salvar:** `p10_c3_macho_audit.txt` e listagem de `out_c3/macho/`.
- **Critério de sucesso:** Binário esculpido na pasta `out_c3/macho/` com tamanho registrado de 1024 bytes.
- **Critério de falha:** O módulo `extract_macho` não reconhece a assinatura ou ignora o arquivo.
- **Critério de interrupção:** Não.

#### **Passo P11** — Reivindicação C4: Carving de executáveis ELF (32 e 64 bits)
- **Selo / Reivindicação:** Selo R / C4.
- **Origem documental:** [DOCUMENTADO NO ARTIGO: p. 6, §3 E p. 7, §4.1 / AMOSTRA NÃO DOCUMENTADA] — Teste do parser `extract_elf` utilizando um binário ELF 64-bit real do ambiente (`/bin/echo` ou pequeno binário compilado).
- **Diretório:** `/home/usuario/work`
- **Comando exato:**
  ```bash
  python3 -c '
  with open("/bin/echo", "rb") as f:
      elf_data = f.read()
  raw_data = b"\x00" * 4096 + elf_data + b"\x00" * 4096
  with open("c4_elf.img", "wb") as f:
      f.write(raw_data)
  '
  foremost-ng -t elf -i c4_elf.img -o out_c4
  cat out_c4/audit.txt && ls -la out_c4/elf/ && readelf -h out_c4/elf/*.elf
  ```
- **Resultado esperado segundo os autores:** Detecção do magic `\x7fELF`, determinação dos limites através dos cabeçalhos de segmento `PT_LOAD` e recuperação de arquivo ELF estruturalmente legível por ferramentas padrão (como `readelf`).
- **Evidência a salvar:** `p11_c4_elf_audit.txt` e saída do `readelf -h`.
- **Critério de sucesso:** Arquivo `.elf` extraído em `out_c4/elf/` e validado com sucesso pelo `readelf`.
- **Critério de falha:** Falha ao extrair ou arquivo resultante truncado/ilegível.
- **Critério de interrupção:** Não.

#### **Passo P12** — Reivindicação C5: Enriquecimento via VirusTotal
- **Selo / Reivindicação:** Selo R / C5.
- **Origem documental:** [DOCUMENTADO NO README:89-108 E ARTIGO: p. 3, §2; p. 7, §4.1] — Teste da opção `-x` com variável `VT_API_KEY` (configurada no ambiente de execução, mascarada nos relatórios) e teste do comportamento sem a chave.
- **Diretório:** `/home/usuario/work`
- **Comando exato:**
  ```bash
  # Teste 1: Execução com VT_API_KEY ativa (herdada do contêiner)
  foremost-ng -x -t elf -i c4_elf.img -o out_c5_vt
  cat out_c5_vt/audit.txt
  
  # Teste 2: Execução com chave ausente para validar o aviso documentado
  env -u VT_API_KEY foremost-ng -x -t elf -i c4_elf.img -o out_c5_nokey 2> out_c5_nokey.err || true
  cat out_c5_nokey.err && cat out_c5_nokey/audit.txt
  ```
- **Resultado esperado segundo os autores:**
  - Com chave: O hash SHA-256 do ELF é consultado na API do VirusTotal, preenchendo a coluna `VT` no `audit.txt` com o veredito (`Clean (X)` ou `Malicious (X)`).
  - Sem chave: Emissão do aviso de chave ausente no `stderr`, execução do carving sem interrupção e anotação como `Clean (0)` ou `N/A`.
- **Evidência a salvar:** `p12_c5_vt_audit.txt` e `out_c5_nokey.err`.
- **Critério de sucesso:** Consulta realizada e registrada na coluna VT quando a chave está presente; emissão de aviso no `stderr` sem abortar o carving quando ausente.
- **Critério de falha:** Quebra da execução por erro fatal de libcurl/OpenSSL ou ausência da coluna VT.
- **Critério de interrupção:** Não.

#### **Passo P13** — Reivindicação C6: Tentativa de reprodução da Figura 2 (`evidence2.dd`)
- **Selo / Reivindicação:** Selo R / C6.
- **Origem documental:** [DOCUMENTADO NO ARTIGO: p. 7, §4.2 E p. 8, Fig. 2 / ARQUIVO AUSENTE] — Comando exato da Figura 2: `./foremost-ng -v -x evidence2.dd`.
- **Diretório:** `/home/usuario/foremost-ng/src`
- **Comando exato:**
  ```bash
  cd /home/usuario/foremost-ng/src
  if [ -f evidence2.dd ]; then
      ./foremost-ng -v -x evidence2.dd
      cat output/audit.txt
  else
      echo "[REGISTRO FACTUAL] Arquivo evidence2.dd nao encontrado no diretorio de trabalho nem no artefato."
      ./foremost-ng -v -x evidence2.dd || true
  fi
  ```
- **Resultado esperado segundo os autores:** Na documentação do artigo, o comando processa `evidence2.dd` e gera a tabela da Figura 2 com 12 arquivos (ELF, script, EXE, ZIP) nos offsets reportados.
- **Evidência a salvar:** `p13_c6_figura2_output.txt`
- **Critério de sucesso (reprodução):** O arquivo `evidence2.dd` existe, é processado e gera os 12 arquivos nos offsets idênticos aos da Figura 2.
- **Critério de falha / factual observado:** O arquivo `evidence2.dd` não existe, o utilitário emite mensagem de erro (`File not found or is a directory: evidence2.dd`) e a reprodução falha por falta de dados.
- **Critério de interrupção:** Não.

#### **Passo P14** — Reivindicação C7: Inspeção da arquitetura de parsers
- **Selo / Reivindicação:** Reivindicação C7 (Arquitetura).
- **Origem documental:** [NÃO DOCUMENTADO EXPERIMENTALMENTE / CONFRONTO COM ARTIGO: p. 2-3, §2 E FIG. 1] — Inspeção textual de `src/extract.c` para confrontar o alegado despachante dinâmico com a implementação real.
- **Diretório:** `/home/usuario/foremost-ng/src`
- **Comando exato:**
  ```bash
  grep -n -C 5 "extract_file" extract.c | head -n 40
  ```
- **Resultado esperado segundo os autores:** Despachante modular com registro desacoplado.
- **Evidência a salvar:** `p14_c7_arquitetura_dispatch.txt`
- **Critério de sucesso:** Registro factual exato da estrutura de código de `extract_file` (revelando se é modular dinâmico ou condicional estático).
- **Critério de falha:** Arquivo inacessível.
- **Critério de interrupção:** Não.

---

### Fase 5: Consolidação das Evidências e Registro Factual

#### **Passo P15** — Consolidação e coleta dos artefatos de evidência
- **Selo / Reivindicação:** Fechamento e Auditoria Geral (F e R).
- **Origem documental:** [NÃO DOCUMENTADO] — Passo operacional do revisor para consolidar todos os logs na pasta de evidências montada no host (`{EXEC_HOST}`).
- **Diretório:** `/home/usuario/work`
- **Comando exato:**
  ```bash
  mkdir -p /exec_host/evidencias
  cp -v /home/usuario/work/p*.txt /home/usuario/work/p*.log /home/usuario/foremost-ng/src/p*.txt /exec_host/evidencias/ 2>/dev/null || true
  ls -lh /exec_host/evidencias/
  ```
- **Resultado esperado segundo os autores:** N/A (procedimento de auditoria).
- **Evidência a salvar:** `p15_resumo_evidencias.txt`
- **Critério de sucesso:** Todos os arquivos de log e dumps das evidências P01 a P14 salvos com sucesso na pasta de saída.
- **Critério de falha:** Falha de escrita no volume montado.
- **Critério de interrupção:** Não.

---

## 3. Estimativa de Tempo

| Etapa | Duração Estimada | Justificativa |
|---|---|---|
| **Fase 1: Diagnóstico e Dependências (P01–P02)** | 1 min 30 s | Atualização do `apt` e instalação dos pacotes dev no Ubuntu |
| **Fase 2: Obtenção e Compilação (P03–P05)** | 45 s | Descompactação e compilação em C com GCC/Make |
| **Fase 3: Teste Mínimo Selo F (P06–P07)** | 1 min | Execução de help, man e carving de imagem mínima JPEG |
| **Fase 4: Reivindicações Selo R (P08–P14)** | 4 min | Geração de amostras sintéticas, execuções de carving C1–C4, chamadas de rede C5, checagem C6 e inspeção C7 |
| **Fase 5: Consolidação (P15)** | 30 s | Cópia e estruturação dos arquivos de evidência |
| **Tempo Total Estimado** | **~8 minutos** | Processamento rápido devido ao código em C nativo |

---

## 4. Tabela-Resumo dos Passos

| ID | Selo / Reivindicação | Origem Documental | Diretório | Comando Principal | Evidência a Salvar | Interrupção? |
|---|---|---|---|---|---|---|
| **P01** | Ambiente / Selo F | [NÃO DOCUMENTADO] | `$HOME` | `uname -a && gcc --version || true` | `p01_ambiente_inicial.txt` | Não |
| **P02** | Selo F (Dependências) | [DOC DOCKERFILE / NÃO DOC README] | `$HOME` | `apt-get install gcc make libssl-dev libcurl4-openssl-dev...` | `p02_apt_install.log` | **Sim** |
| **P03** | Selo F (Instalação) | [DOC README / DOC ARTIGO] | `$HOME` | `unzip /pacote/artefato.zip` | `p03_source_tree.txt` | **Sim** |
| **P04** | Selo F (Compilação) | [DOC README:33 / DOC DOCKERFILE:10] | `foremost-ng/src` | `make clean && make` | `p04_build.log` | **Sim** |
| **P05** | Selo F (Instalação) | [DOC README:34 / DOC ARTIGO: p. 6] | `foremost-ng/src` | `sudo make install && which foremost-ng` | `p05_install.log` | Não |
| **P06** | Selo F (Interface/CLI) | [DOC README:79 / DOC ARTIGO: p. 7] | `$HOME` | `foremost-ng -V && foremost-ng -h && man foremost-ng` | `p06_cli_help.txt` | Não |
| **P07** | Selo F (Teste Mínimo) | [NÃO DOC README / ARTIGO CONCEITUAL] | `work/` | `foremost-ng -i min_test.img -o out_min` | `p07_min_test_audit.txt` | **Sim** |
| **P08** | Selo R / C1 (EVTX) | [DOC ARTIGO: p. 6 / AMOSTRA NÃO DOC] | `work/` | `foremost-ng -t evtx -i c1_evtx.img -o out_c1` | `p08_c1_evtx_audit.txt` | Não |
| **P09** | Selo R / C2 (Scripts) | [DOC ARTIGO: p. 6 / AMOSTRA NÃO DOC] | `work/` | `foremost-ng -t script -i c2_script.img -o out_c2` | `p09_c2_script_audit.txt` | Não |
| **P10** | Selo R / C3 (Mach-O) | [DOC ARTIGO: p. 6 / AMOSTRA NÃO DOC] | `work/` | `foremost-ng -t macho -i c3_macho.img -o out_c3` | `p10_c3_macho_audit.txt` | Não |
| **P11** | Selo R / C4 (ELF) | [DOC ARTIGO: p. 6 / AMOSTRA NÃO DOC] | `work/` | `foremost-ng -t elf -i c4_elf.img -o out_c4` | `p11_c4_elf_audit.txt` | Não |
| **P12** | Selo R / C5 (VirusTotal) | [DOC README:89 / DOC ARTIGO: p. 3, 7] | `work/` | `foremost-ng -x -t elf -i c4_elf.img -o out_c5_vt` | `p12_c5_vt_audit.txt` | Não |
| **P13** | Selo R / C6 (Figura 2) | [DOC ARTIGO: p. 7-8 / DADOS NÃO DOC] | `foremost-ng/src` | `./foremost-ng -v -x evidence2.dd` | `p13_c6_figura2_output.txt` | Não |
| **P14** | Reivindicação C7 | [NÃO DOC EXPERIMENTAL / ARTIGO: p. 2] | `foremost-ng/src` | `grep -n -C 5 "extract_file" extract.c` | `p14_c7_arquitetura_dispatch.txt` | Não |
| **P15** | Auditoria Geral | [NÃO DOCUMENTADO] | `work/` | `cp p*.txt p*.log /exec_host/evidencias/` | `p15_resumo_evidencias.txt` | Não |