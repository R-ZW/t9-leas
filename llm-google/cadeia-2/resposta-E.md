# Resumo da Execução Experimental (Etapa E) — Foremost-NG

A execução experimental do roteiro foi concluída no contêiner `t9-gemini-c2` (Ubuntu 24.04.2 LTS, x86_64). O relatório completo e factual foi gerado e salvo em `D:\t9-trabalho\gemini-c2\execucao\registro-factual.md`, acompanhado de todos os logs e arquivos de evidência na mesma pasta (`/home/revisor/evidencias`).

### Síntese do que foi executado:

1. **Instalação e Compilação (P1 a P4):**
   - Dependências (`gcc`, `make`, `git`, `libssl-dev`, `libcurl4-openssl-dev`, `file`, `python3`) foram instaladas com sucesso via `apt-get` (P1).
   - O código-fonte do commit `bb812a22` foi descompactado de `/home/revisor/artefato.zip` (P2).
   - O binário `foremost-ng` foi compilado limpo via `make` com suporte a OpenSSL e libcurl (P3) e instalado em `/usr/local/bin/foremost-ng` (P4).

2. **Teste Mínimo Funcional (P5 a P7):**
   - Comandos informativos (`-V`, `-h`) e a man page funcionaram sem erros (P5).
   - A imagem de teste `test_f.img` foi processada com sucesso (`foremost-ng -i test_f.img -o output_f`), gerando `output_f/audit.txt` e extraindo os artefatos com sucesso (P6 e P7).

3. **Verificação das Reivindicações (C1 a C6):**
   - **C1 (EVTX):** Processou imagem com cabeçalho `ElfFile\0\0` e chunk de 64 KiB, extraindo com sucesso `00000001.evtx` (64 KiB), validado pelo comando `file` como `MS Windows 10-11 Event Log` (P8 e P9).
   - **C2 (Scripts):** Carving com `-t script` recuperou scripts Bash, Python e PowerShell na pasta `output_c2/script/`, mantendo shebang e corpo de código intactos (P10 e P11).
   - **C3 (Mach-O):** Carving com `-t macho` recuperou com sucesso o binário Mach-O universal FAT (`0xCAFEBABE`, 8 KiB), validado por `file`. Constatou-se uma discrepância no código-fonte em `src/extract.c:2408` que compara a variável lida por `read_le32` contra a constante literal `0xCFFAEDFE` (e `0xCEFAEDFE` para 32-bit), o que impede a extração de binários thin (P12 e P13).
   - **C4 (ELF):** Carving com `-t elf` recuperou com sucesso o executável ELF64 (`/bin/true`), delimitado estritamente pelos segmentos `PT_LOAD` (24.520 bytes), validado por `readelf -h` como ELF64 AMD x86-64 (P14 e P15).
   - **C5 (VirusTotal):** Com `-x` e a variável `VT_API_KEY`, o Foremost-NG calculou o hash SHA-256, consultou a API v3 do VirusTotal via libcurl e anotou a coluna `VT` com `Clean (0)`. Quando executado sem a variável, emitiu o aviso `Error: VT_API_KEY environment variable is not set.` e realizou o carving normalmente (P16 e P17).
   - **C6 (Figura 2 / evidence2.dd):** A busca em todo o sistema de arquivos confirmou que o arquivo `evidence2.dd` (2 GB) **não existe** no ambiente de teste (P18). A execução direta de `foremost-ng -v -x evidence2.dd` resultou em erro de arquivo inexistente (`exit code 1`), restando a reprodução da Figura 2 e seus 12 arquivos/offsets bloqueada por ausência do dado mandatório (P19).

Todos os logs de execução, saídas brutas e o arquivo `registro-factual.md` estão disponíveis em `D:\t9-trabalho\gemini-c2\execucao\`.