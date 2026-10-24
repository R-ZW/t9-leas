# Resumo da Execução Factual (Etapa E — Foremost-NG)

A execução do roteiro foi concluída no contêiner Docker `t9-gemini-c3` (Ubuntu 24.04 LTS, usuário `revisor`). As evidências e o relatório factual foram salvos em `D:\t9-trabalho\gemini-c3\execucao` (`/home/revisor/evidencias`).

### 1. Ambiente e Compilação (P01–P06)
- **Diagnóstico (P01):** Confirmado estado inicial sem compilador.
- **Dependências (P02, D1):** Instalados `gcc` (13.3.0), `make` (4.3), `libssl-dev`, `libcurl4-openssl-dev`, `file`, `binutils` (`readelf`) e `python3` (64.9 MB).
- **Extração e Compilação (P03–P05, D0):** `artefato.zip` descompactado no commit `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d`. Compilação via `make` em `src/` gerou o executável `foremost-ng` (87.200 bytes, saída 0). `sudo make install` instalou o binário em `/usr/local/bin`, a configuração em `/usr/local/etc/foremost.conf` e o manual em `/usr/share/man/man8/`.
- **Interface e Manual (P06, D0):** Opções `-V`, `-h` e `man foremost-ng` responderam com código de saída 0.

### 2. Teste Mínimo Funcional (P07)
- **Execução (D2):** Processamento de imagem sintética `min_test.img` pelo comando `foremost-ng -i min_test.img -o out_min`. O utilitário extraiu 1 arquivo (`00000004.script`, 41 B) no offset 2121 e gerou o relatório `audit.txt`.

### 3. Avaliação Factual das Reivindicações (P08–P14)
- **C1 (EVTX, P08, D2):** Extração de bloco EVTX estruturado com assinatura `ElfFile\0\0` e chunk de 64 KiB. Resultou em `00000008.evtx` com 65.536 bytes exatos e registro em `audit.txt` (`evtx=1`).
- **C2 (Scripts, P09, D2):** Extração de script bash válido (80 bytes) e descarte de script com menos de 32 bytes e de script contendo apenas comentários `#` (`script=1`).
- **C3 (Mach-O, P10, D2):** Extração de binário Mach-O FAT universal (`0xCAFEBABBE`) de 1.024 bytes delimitado pelos cabeçalhos de arquitetura (`macho=1`).
- **C4 (ELF, P11, D2):** Extração de binário ELF 64-bit (`/bin/echo` embutido) com 32.788 bytes (fim dos segmentos `PT_LOAD`). Cabeçalho ELF64 validado com sucesso por `readelf -h`.
- **C5 (VirusTotal, P12, D0):**
  - Com chave `VT_API_KEY` (presente no contêiner, mascarada nos relatórios): consulta realizada via HTTP e anotação `Clean (0)` na coluna VT do `audit.txt`.
  - Sem chave (`env -u VT_API_KEY`): emissão de aviso no `stderr` (`Error: VT_API_KEY environment variable is not set.`) e continuidade normal do carving com código 0.
- **C6 (Figura 2 / `evidence2.dd`, P13, D0):** **Falha**. O arquivo `evidence2.dd` não existe no repositório nem no contêiner. O comando `./foremost-ng -v -x evidence2.dd` falhou imediatamente com código 1 (`[!] File not found or is a directory: evidence2.dd`).
- **C7 (Arquitetura, P14, D2):** Inspeção de `src/extract.c` confirmou implementação por cadeia monolítica estática de `if ... else if` em `extract_file` (linhas 2630–2692).

### 4. Entregáveis
- **Manifesto de Evidências (P15):** 15 arquivos de evidência salvos em `D:\t9-trabalho\gemini-c3\execucao` (`p01` a `p15`) com hashes SHA-256 registrados em `p15_resumo_evidencias.txt`.
- **Registro Factual:** Gravado em `D:\t9-trabalho\gemini-c3\execucao\registro-factual.md`.