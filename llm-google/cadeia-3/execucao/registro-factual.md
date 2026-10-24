# Registro Factual de Execução — Foremost-NG (SBSeg 2025)

## 1. Ambiente de Execução Observado

A execução do roteiro de avaliação foi realizada no contêiner Docker `t9-gemini-c3`, com os seguintes parâmetros e versões observadas:
- **Sistema Operacional:** Linux Ubuntu 24.04 LTS (Noble Numbat)
- **Kernel:** `6.18.54.1-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Tue Oct 6 19:13:07 UTC 2026 x86_64`
- **Usuário:** `uid=1001(revisor) gid=1001(revisor) groups=1001(revisor)` (com privilégio de `sudo` sem senha)
- **Compilador C:** `gcc (Ubuntu 13.3.0-6ubuntu2~24.04) 13.3.0`
- **Build System:** `GNU Make 4.3`
- **Bibliotecas de Desenvolvimento:**
  - `libssl-dev`: OpenSSL 3.0.13 (headers e bibliotecas em `/usr/include/openssl`, `/usr/lib/x86_64-linux-gnu`)
  - `libcurl4-openssl-dev`: libcurl 8.5.0
- **Interpretador Python:** `Python 3.12.3`
- **Utilitários auxiliares:** `file-5.45`, `GNU readelf 2.42`
- **Variável de Ambiente VirusTotal:** A variável `VT_API_KEY` está presente no ambiente do contêiner (`VT_API_KEY present: True`). Seu valor é estritamente mantido mascarado como `<VT_API_KEY>` em todos os logs e relatórios.

---

## 2. Tabela de Execução dos Passos

| ID | Selo / Reiv. | Desvio | Comando Exato | Resultado Esperado | Resultado Observado (Saída e Código) | Evidência | Status |
|---|---|---|---|---|---|---|---|
| **P01** | Ambiente / Selo F | D1 | `uname -a && id && (gcc --version 2>&1 \|\| true) && (make --version 2>&1 \|\| true)` | SO identificado; sem compiladores instalados | Linux x86_64, user revisor; `gcc: command not found`; `make: command not found` (código 0) | `p01_ambiente_inicial.txt` | Sucesso |
| **P02** | Selo F (Deps) | D1 | `sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev file binutils python3` | Instalação bem-sucedida das ferramentas de build | 64.9 MB baixados; pacotes instalados com sucesso (código 0) | `p02_apt_install.log` | Sucesso |
| **P03** | Selo F (Instalação) | D0 | `cd /home/revisor && unzip -q -o artefato.zip && ln -sfn foremost-ng-bb812a22 foremost-ng && ls -la /home/revisor/foremost-ng` | Descompactação do commit `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` | Diretório descompactado contendo `src/`, `README.md`, `Dockerfile` (código 0) | `p03_source_tree.txt` | Sucesso |
| **P04** | Selo F (Compilação)| D0 | `cd /home/revisor/foremost-ng/src && make clean && make` | Compilação e linkedição do executável `foremost-ng` | 10 módulos compilados com `-O2`; binário `foremost-ng` (87.200 bytes) gerado (código 0) | `p04_build.log` | Sucesso |
| **P05** | Selo F (Instalação) | D0 | `sudo make install && which foremost-ng && ls -la /usr/local/bin/foremost-ng /usr/local/etc/foremost.conf /usr/share/man/man8/foremost-ng.8.gz` | Instalação em `/usr/local/bin`, `/usr/local/etc` e man | Binário copiado para `/usr/local/bin/foremost-ng`; config e man page instaladas (código 0) | `p05_install.log` | Sucesso |
| **P06** | Selo F (Interface) | D0 | `foremost-ng -V && echo "---" && foremost-ng -h && echo "---" && man -P cat foremost-ng \| head -n 30` | Exibição de versão, opções CLI e manual | Versão `1.5.7 by Cristian Souza`, help completo e página de manual renderizados (código 0) | `p06_cli_help.txt` | Sucesso |
| **P07** | Selo F (Teste Mínimo) | D2 | `cd /home/revisor/work && foremost-ng -i min_test.img -o out_min` | Carving de arquivo e geração de `audit.txt` | `1 FILES EXTRACTED` (`00000004.script`, 41 B, offset 2121); `out_min/audit.txt` gerado (código 0) | `p07_min_test_audit.txt` | Sucesso |
| **P08** | Selo R / C1 (EVTX) | D2 | `foremost-ng -t evtx -i c1_evtx.img -o out_c1` | Reconhecimento de magic `ElfFile` e chunk de 64 KiB | `1 FILES EXTRACTED`: `00000008.evtx` extraído com 65.536 bytes (64 KB) no offset 4096 (código 0) | `p08_c1_evtx_audit.txt` | Sucesso |
| **P09** | Selo R / C2 (Script) | D2 | `foremost-ng -t script -i c2_script.img -o out_c2` | Extração de script válido (>32 B com código) e rejeição de comentários/curtos | `1 FILES EXTRACTED`: `00000002.script` (80 B, offset 1024) recuperado; script curto (18 B) e script só com `#` rejeitados (código 0) | `p09_c2_script_audit.txt` | Sucesso |
| **P10** | Selo R / C3 (Mach-O) | D2 | `foremost-ng -t macho -i c3_macho.img -o out_c3` | Reconhecimento de cabeçalho universal FAT e extração delimitada | `1 FILES EXTRACTED`: `00000002.macho` extraído com 1.024 bytes (1 KB) no offset 1024 (código 0) | `p10_c3_macho_audit.txt` | Sucesso |
| **P11** | Selo R / C4 (ELF) | D2 | `foremost-ng -t elf -i c4_elf.img -o out_c4` | Extração de binário ELF 64-bit pela extensão `PT_LOAD` | `1 FILES EXTRACTED`: `00000008.elf` de 32.788 bytes esculpido no offset 4096; cabeçalho ELF64 validado por `readelf` (código 0) | `p11_c4_elf_audit.txt` | Sucesso |
| **P12** | Selo R / C5 (VT) | D0 | `foremost-ng -x -t elf -i c4_elf.img -o out_c5_vt` e sem chave com `env -u VT_API_KEY` | Consulta à API via hash com chave; aviso no stderr sem abortar quando ausente | Com chave: coluna `VT` preenchida com `Clean (0)`. Sem chave: aviso `Error: VT_API_KEY environment variable is not set.` no stderr; extração mantida (código 0) | `p12_c5_vt_audit.txt`, `p12_c5_nokey.err` | Sucesso |
| **P13** | Selo R / C6 (Fig. 2) | D0 | `cd /home/revisor/foremost-ng/src && ./foremost-ng -v -x evidence2.dd` | Processamento de `evidence2.dd` e replicação dos 12 arquivos e offsets | `[!] File not found or is a directory: evidence2.dd` e `[!] No valid input files to process.` (código 1). Arquivo ausente | `p13_c6_figura2_output.txt` | **Falha** |
| **P14** | Reiv. C7 (Arquitetura)| D2 | `sed -n "2628,2695p" /home/revisor/foremost-ng/src/extract.c` | Verificação do despachante modular desacoplado | Cadeia estática de condicionais `if ... else if` codificada rigidamente (código 0) | `p14_c7_arquitetura_dispatch.txt` | Sucesso (inspeção) |
| **P15** | Auditoria Geral | D2 | `cd /home/revisor/evidencias && sha256sum p* > p15_resumo_evidencias.txt` | Coleta e catalogação de todos os hashes das evidências | 15 arquivos de evidência catalogados com SHA-256 (código 0) | `p15_resumo_evidencias.txt` | Sucesso |

---

## 3. Fatos Observados por Reivindicação (C1 a C6)

### Reivindicação C1: Recuperação de logs de eventos do Windows (EVTX)
- **Fato observado:** O parser `extract_evtx` (`src/extract.c:2460`) processou uma imagem sintética contendo o cabeçalho `ElfFile\0\0` com contagem de chunks igual a 1 (no offset `0x18`).
- **Resultado factual:** O utilitário delimitou o bloco em 65.536 bytes (64 KiB), gravou o arquivo `out_c1/evtx/00000008.evtx` com tamanho exato de 65.536 bytes, e registrou no `audit.txt` o offset `4096` e o total de 1 arquivo EVTX extraído.

### Reivindicação C2: Recuperação de scripts (Bash, Python, PowerShell)
- **Fato observado:** O módulo `extract_script` (`src/extract.c:2519`) impõe tamanho mínimo `MIN_SCRIPT_SIZE = 32` bytes e varre caracteres imprimíveis a partir de `#!`.
- **Resultado factual:** Em imagem de teste com três scripts:
  1. Script válido de 80 bytes (código bash executável após shebang): extraído em `out_c2/script/00000002.script` (tamanho 80 bytes, offset 1024).
  2. Script curto de 18 bytes: descartado por ter tamanho inferior a 32 bytes.
  3. Script de 48 bytes composto exclusivamente por caracteres `#` e quebras de linha: descartado pelo parser por ausência de caracteres fora de comentários.
  O arquivo `audit.txt` confirmou a extração de exatamente 1 arquivo (`script=1`).

### Reivindicação C3: Recuperação de binários Mach-O (fat e thin)
- **Fato observado:** O parser `extract_macho` (`src/extract.c:2314`) reconhece o magic `0xCAFEBABBE` (FAT/universal) e calcula a extensão total a partir dos campos `arch_fileoff` e `arch_size`.
- **Resultado factual:** Uma estrutura Mach-O FAT de 1.024 bytes (cabeçalho de 28 bytes apontando offset 28 e tamanho 996 bytes) embutida na imagem `c3_macho.img` foi localizada no offset 1024 e esculpida na íntegra para `out_c3/macho/00000002.macho` com exatamente 1.024 bytes. O relatório `audit.txt` computou `macho=1`.

### Reivindicação C4: Recuperação de executáveis ELF de 32 e 64 bits
- **Fato observado:** O parser `extract_elf` (`src/extract.c:2147`) reconhece o magic `\x7fELF`, valida formato little-endian (`ei_data == 1`), e determina o tamanho do arquivo como a extensão máxima dos segmentos `PT_LOAD`.
- **Resultado factual:** Ao processar um binário ELF 64-bit do sistema (`/bin/echo`) embutido no offset 4096, o Foremost-NG esculpiu o arquivo `out_c4/elf/00000008.elf` com tamanho de 32.788 bytes (equivalente ao fim dos segmentos de carga). A ferramenta `readelf -h` inspecionou o arquivo esculpido e validou com sucesso seu cabeçalho ELF64 (`Magic: 7f 45 4c 46 02 01 01 00...`, `Class: ELF64`, `Data: 2's complement, little endian`, `Type: DYN`, `Machine: AMD x86-64`).

### Reivindicação C5: Enriquecimento via VirusTotal
- **Fato observado:** Com a opção `-x`, a função `write_to_disk` calcula o hash SHA-256 do arquivo recuperado e chama `vt_check_hash` (`src/vt_query.c:136`).
- **Resultado factual:**
  1. Com a variável de ambiente `VT_API_KEY` ativa, a execução consultou a API v3 e gravou no `audit.txt` a anotação `Clean (0)` na coluna `VT` para o arquivo ELF esculpido.
  2. Quando a variável `VT_API_KEY` foi removida do ambiente (`env -u VT_API_KEY`), o utilitário emitiu no `stderr` a mensagem `Error: VT_API_KEY environment variable is not set.` e prosseguiu com a extração normalmente, registrando `Clean (0)` na coluna `VT` e finalizando com código de saída 0.

### Reivindicação C6: Exemplo de execução da Figura 2 (`./foremost-ng -v -x evidence2.dd`)
- **Fato observado:** O comando exato `./foremost-ng -v -x evidence2.dd` documentado na Seção 4.2 e ilustrado na Figura 2 do artigo foi executado no diretório `foremost-ng/src`.
- **Resultado factual:** O arquivo `evidence2.dd` não existe no repositório nem no contêiner (`find / -name "evidence2.dd"` retornou vazio). O comando falhou imediatamente com código de saída 1, exibindo as mensagens:
  ```
  [!] File not found or is a directory: evidence2.dd
  [!] No valid input files to process.
  ```
  Não foi possível reproduzir a tabela com os 12 arquivos (3 ELF, 1 script, 6 EXE, 2 ZIP) e seus respectivos offsets reportados na Figura 2.

---

## 4. Manifestos de Hashes das Evidências Salvas

Arquivo gerado em `/home/revisor/evidencias/p15_resumo_evidencias.txt`:
```
908a683ce650ac2809e19a47803237df513ac03135484a5f3a7dfb2606cbc744  p01_ambiente_inicial.txt
68cde2c1b1ae408fede97e1cec3654f19eb8db7436895d761760172e3c9c3320  p02_apt_install.log
def37b7a1f38f75a8c8935f2efdc6f8a94cf00263976a3e5d03a1f75f034eb7c  p03_source_tree.txt
fd50c711a1ede00e8b3cccaa75f39b318e325d9798e5ce7f28810d952755bc57  p04_build.log
42383bb6e0f1766b6b7c3717380046e07cbfe83097f582160c32fed3b8c919d6  p05_install.log
61a45fde2c6ca2d06a1274023ad33675e1154465fb34ce9fdac2267c07296442  p06_cli_help.txt
bebfb4bb01bd10d0e8a874407134470a41e6a5258c7b6e30f205508687d8e701  p07_min_test_audit.txt
0c6f5e705319d92cc13e12ffbe6780538c12be011a097a5c6830d8bb1b50ab01  p08_c1_evtx_audit.txt
bd5fc47be27ccdc669512b1aad89f214c4020ede985721279efc7e69fb58153a  p09_c2_script_audit.txt
c75b28faf9b5fc4981a57ea06f53818d551ce84cc443665f2a31184bd1ab1ba3  p10_c3_macho_audit.txt
2ac3ec4e40206d131583c2750c213bc57280e54aaced534b6a68b92c6c9f4183  p11_c4_elf_audit.txt
f8cbb744bcf49d6f740da951f047f97c835a7a381dcd6021e98227a1e7874769  p12_c5_nokey.err
5ff90c4bc6e2520317ffb0dea65f46b4247996bd0a99f127f04e9f04b7103c17  p12_c5_vt_audit.txt
d6d9835ade1f38ad4c1f3ace731a957c39749c2f72c0b2400d6047ca09b36247  p13_c6_figura2_output.txt
d3231d8bd44d5f40d14042c2d5365edfd0114e0aa0458fcc213d60f37d5a507f  p14_c7_arquitetura_dispatch.txt
```
