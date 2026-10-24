# Avaliação de Artefato SBSeg 2025 — Foremost-NG (Etapa Analítica)

## A. Materiais examinados
Foram examinados exclusivamente os arquivos disponibilizados na pasta do pacote (`D:\t9-trabalho\gemini-c1\pacote`):
1. `instrucoes-oficiais.md`: Resumo oficial dos critérios de avaliação do SBSeg 2025 para os selos Funcional (F) e Reprodutível (R).
2. `reivindicacoes.md`: Relação oficial das reivindicações principais (C1 a C7) do artigo Foremost-NG e regra para concessão do selo R.
3. `artefato.txt`: Código integral e índice de arquivos do artefato na versão/commit `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` (incluindo `README.md`, `Dockerfile`, `src/Makefile`, `src/main.c`, `src/engine.c`, `src/extract.c`, `src/extract.h`, `src/vt_query.c`, `src/vt_query.h`, etc.).
4. `artigo.pdf`: Texto integral do artigo *"Foremost-NG: An Open-Source Toolkit for Advanced File Carving and Analysis"* (Anais Estendidos do SBSeg 2025).

---

## B. Selo Funcional (F)

### 1. Critérios oficiais aplicáveis
Conforme `instrucoes-oficiais.md:15`:
> "O artefato precisa ser executável e permitir a observação de funcionalidades. O README deve informar dependências, versões de dependências/linguagens/ambiente, ambiente de execução, instalação, execução e pelo menos um exemplo mínimo. O revisor deve **executar** o artefato e apresentar prova de execução e saídas no parecer. Ler código ou README, por si só, não constitui prova de funcionamento."

### 2. Análise detalhada por critério

1. **Executabilidade e observação de funcionalidades:**
   - *Status:* Só verificável por execução.
   - *Evidência:* [`artefato.txt:src/main.c:197-304`] e [`artefato.txt:src/Makefile:65-76`]. A estrutura de código em C e as regras de compilação existem no artefato, mas a prova de executabilidade só pode ser obtida por execução real.
   - *Trecho:* `instrucoes-oficiais.md:15`: *"O revisor deve executar o artefato e apresentar prova de execução e saídas no parecer. Ler código ou README, por si só, não constitui prova de funcionamento."*

2. **Dependências:**
   - *Status:* Atendido na documentação (parcialmente).
   - *Evidência:* [`artefato.txt:README.md:39-42`], [`artefato.txt:README.md:52-55`], [`artefato.txt:README.md:64-68`], e [`artefato.txt:Dockerfile:4-5`].
   - *Trechos:*
     - `README.md:39-42`: *"Make sure curl is installed: pkg_add curl ... pkg install curl"*
     - `README.md:52-55`: *"Install OpenSSL: brew install openssl@3"*
     - `README.md:64-68`: *"Install MinGW in your Linux distribution and cross-compile: make cross. Required DLLs can be found in the windows_dlls directory"*
     - `Dockerfile:4-5`: *"apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev"* (embora o Dockerfile não seja citado explicitamente no README).

3. **Versões de dependências / linguagens / ambiente:**
   - *Status:* Não atendido.
   - *Evidência:* [`artefato.txt:README.md:21-71`]. O README omite as versões mínimas ou testadas do GCC, da linguagem C, do libcurl e da distribuição Linux alvo. A única menção a versão de dependência é `openssl@3` para macOS (`README.md:54`) e uma ressalva histórica em `README.md:70` (*"On systems with glibc < 2.2.0, you may see harmless warnings"*).

4. **Ambiente de execução:**
   - *Status:* Atendido na documentação.
   - *Evidência:* [`artefato.txt:README.md:3`], [`artefato.txt:README.md:31`], [`artefato.txt:README.md:37`], [`artefato.txt:README.md:50`], [`artefato.txt:README.md:62`].
   - *Trechos:*
     - `README.md:3`: *"`foremost-ng` is a Linux-based file recovery tool..."*
     - `README.md:31-62`: Seções específicas para *"Linux"*, *"BSD"*, *"macOS"* e *"Cross compiling for Windows"*.

5. **Instruções de instalação:**
   - *Status:* Atendido na documentação.
   - *Evidência:* [`artefato.txt:README.md:21-68`].
   - *Trecho:* `README.md:32-35`:
     ```bash
     make
     sudo make install
     ```

6. **Instruções de execução:**
   - *Status:* Atendido na documentação.
   - *Evidência:* [`artefato.txt:README.md:74-86`].
   - *Trecho:* `README.md:82-85`:
     ```bash
     Basic syntax:
     foremost-ng [options] [image_or_device]
     ```
     e remissão ao manual em `README.md:78-80` (`man foremost-ng`).

7. **Pelo menos um exemplo mínimo:**
   - *Status:* Não atendido (insuficiente).
   - *Evidência:* [`artefato.txt:README.md:82-85`]. O README traz apenas um modelo abstrato de sintaxe com metavariáveis (`foremost-ng [options] [image_or_device]`), sem fornecer um exemplo prático executável ponta a ponta com dados reais ou mockados.

### 3. Decisão para o Selo F
- **Decisão:** **Indeterminado**
- **Regra aplicada:** *"Indeterminado: nenhum critério obrigatório falha na documentação, mas a decisão depende de execução."* O código-fonte em C está completo no repositório, com Makefile funcional e Dockerfile de suporte, não havendo impedimento documental intrínseco que desqualifique a compilação, mas a concessão de F exige estritamente prova de execução das funcionalidades.

### 4. Confiança da decisão oficial
- **Confiança:** 80% de que o comitê oficial atribuiu o selo F.
- *Justificativa:* Trata-se de uma ferramenta de linha de comando com código-fonte C autocontido, dependências comuns (`libssl`, `libcurl`, `gcc`, `make`), man page e opções CLI padronizadas. Em ambiente real de avaliação, o comitê oficial consegue compilar e rodar a ferramenta em imagens de teste.

### 5. O que precisaria ser observado na execução para mudar a decisão
- Compilação limpa do binário `foremost-ng` via `make` em ambiente Linux/Ubuntu.
- Execução bem-sucedida das opções básicas de linha de comando (`./foremost-ng -h`, `./foremost-ng -V`).
- Carving real sobre uma imagem de entrada, com criação do diretório de saída estruturado e geração do log `audit.txt`.

---

## C. Selo Reprodutível (R) — por reivindicação

### 1. Critérios oficiais aplicáveis
Conforme `instrucoes-oficiais.md:19`:
> "O revisor deve conseguir reproduzir as **principais reivindicações do artigo**. A documentação do artefato deve trazer instruções de execução dessas reivindicações e descrever o processo usado pelos autores para chegar aos resultados publicados. O revisor deve executar os experimentos e confrontar os resultados com os do artigo, incluindo figuras/tabelas pertinentes, resumindo a comparação no parecer."

Conforme a regra específica em `reivindicacoes.md:17`:
> "O README não marca reivindicações a reproduzir. Por isso, valem as reivindicações principais desta lista: **C1 a C6**. **R é atribuído se C1 a C6 forem reproduzidas.** C7 é uma contribuição arquitetural, sem experimento associado no artigo; ela pode ser inspecionada, mas não entra na regra de R."

### 2. Avaliação individual das reivindicações

#### C1: Recuperação de logs de eventos do Windows (EVTX)
- **Critério / Reivindicação:** O parser reconhece a assinatura `ElfFile`, delimita chunks de 64 KiB e extrai o log legível.
- **Local no artigo:** p. 1 (resumo); p. 2; p. 6, §3, item "Windows Event Logs (EVTX)"; p. 7, §4.1 (`-t evtx,elf,exe`).
- **Resultado esperado:** Arquivo `.evtx` extraído, legível por ferramenta de análise de eventos.
- **Atendimento documental:** Parcial (`reivindicacoes.md:7`). O README não traz instruções específicas para reproduzir C1 nem inclui arquivos de teste `.evtx`.
- **Evidência no código:** [`artefato.txt:src/extract.c:2460-2517`] (implementação da função `extract_evtx`) e [`artefato.txt:src/state.c:689-695`] (`init_builtin(s, EVTX, "evtx", "ElfFile\0\0", ...)`).
- **Trecho:** `src/extract.c:2474`:
  ```c
  if (memcmp(buf, "ElfFile\0\0", 8) != 0) { return foundat + needle->header_len; }
  ```
- **Status:** Só verificável por execução.
- **Classificação C1:** `depende_execucao`.

#### C2: Recuperação de scripts (Bash, Python, PowerShell)
- **Critério / Reivindicação:** Reconhecimento por shebang (`#!`) e conteúdo textual (mínimo de 32 bytes e mais que apenas comentários).
- **Local no artigo:** p. 1 (resumo); p. 2; p. 6, §3, item "Script Files".
- **Resultado esperado:** Script extraído com a linha do interpretador e o corpo legível.
- **Atendimento documental:** Parcial (`reivindicacoes.md:8`). O README não detalha a extração de scripts nem disponibiliza amostras.
- **Evidência no código:** [`artefato.txt:src/extract.c:2519-2622`] (função `extract_script`).
- **Trecho:** `src/extract.c:2521`:
  ```c
  const uint64_t MIN_SCRIPT_SIZE = 32; // don’t carve anything smaller than 32 bytes
  ```
- **Status:** Só verificável por execução.
- **Classificação C2:** `depende_execucao`.

#### C3: Recuperação de binários Mach-O (fat e thin)
- **Critério / Reivindicação:** Recuperação de binários Mach-O `fat` e `thin`, usando o cabeçalho universal (`0xCAFEBABE`) ou comandos de carga (`0xCEFAEDFE` / `0xCFFAEDFE`) para determinar o tamanho.
- **Local no artigo:** p. 1 (resumo); p. 2; p. 6, §3, item "Mach-O (macOS/iOS Binaries)".
- **Resultado esperado:** Binário Mach-O extraído e reconhecível por ferramenta apropriada.
- **Atendimento documental:** Parcial (`reivindicacoes.md:9`).
- **Evidência no código:** [`artefato.txt:src/extract.c:2314-2455`] (função `extract_macho`).
- **Trecho:** `src/extract.c:2327`:
  ```c
  if (buf[0] == 0xCA && buf[1] == 0xFE && buf[2] == 0xBA && buf[3] == 0xBE)
  ```
- **Status:** Só verificável por execução.
- **Classificação C3:** `depende_execucao`.

#### C4: Recuperação de executáveis ELF (32 e 64 bits)
- **Critério / Reivindicação:** Recuperação de executáveis ELF de 32 e 64 bits, delimitados pelos cabeçalhos de programa (`PT_LOAD`).
- **Local no artigo:** p. 1 (resumo); p. 2; p. 6, §3, item "ELF"; p. 7, §4.1 (`-t evtx,elf,exe` e `-x -t elf`).
- **Resultado esperado:** Arquivo `.elf` extraído e estruturalmente legível por analisador ELF.
- **Atendimento documental:** Parcial (`reivindicacoes.md:10`).
- **Evidência no código:** [`artefato.txt:src/extract.c:2147-2309`] (função `extract_elf`).
- **Trecho:** `src/extract.c:2213`:
  ```c
  if (p_type_32 == 1 /* PT_LOAD */) { ... }
  ```
- **Status:** Só verificável por execução.
- **Classificação C4:** `depende_execucao`.

#### C5: Enriquecimento pelo VirusTotal
- **Critério / Reivindicação:** Com `-x` e `VT_API_KEY`, consulta a API pelo hash de cada arquivo recuperado e registra o resultado de detecção no log; sem a chave, emite aviso e prossegue o carving sem consulta.
- **Local no artigo:** p. 1 (resumo); pp. 2–3, §2; p. 7, §4 e §4.1; p. 8, Fig. 2 (coluna VT).
- **Resultado esperado:** Consulta associada ao hash do arquivo extraído, com veredito de detecção registrado; sem chave, aviso e carving sem consulta.
- **Atendimento documental:** Parcial (`reivindicacoes.md:11`). O README explica como definir `VT_API_KEY` (`README.md:99-108`), mas não há dados de teste com hashes previamente conhecidos.
- **Evidência no código:** [`artefato.txt:src/vt_query.c:136-198`] (`vt_check_hash`), [`artefato.txt:src/dir.c:275-283`] e [`artefato.txt:src/main.c:131`].
- **Trecho:** `src/dir.c:275-283`:
  ```c
  if (get_mode(s, mode_virustotal)) {
      char sha256[65];
      VTResult vt = {0};
      sha_checksum(fn, "sha256", sha256);
      vt = vt_check_hash(sha256);
  ```
- **Status:** Só verificável por execução (depende de chave válida e acesso à rede).
- **Classificação C5:** `depende_execucao`.

#### C6: Exemplo de execução da Figura 2 (`./foremost-ng -v -x evidence2.dd`)
- **Critério / Reivindicação:** Execução exata `./foremost-ng -v -x evidence2.dd` reproduzindo a tabela da Fig. 2, com arquivos ELF, script, EXE e ZIP nos offsets especificados (ex.: 2228224, 2467840, 2811904, 204740608, etc.) e a coluna VT.
- **Local no artigo:** p. 7, §4.2; p. 8, Fig. 2.
- **Resultado esperado:** Tabela idêntica à da Fig. 2 com os arquivos recuperados e seus respectivos offsets.
- **Atendimento documental:** **Não atendido**.
- **Evidência:** O arquivo de imagem forense `evidence2.dd` (de 2 GB / 2045109643 bytes, conforme indicado na Fig. 2) não está presente no pacote do artefato ([`artefato.txt:ÍNDICE:9-50`]). O `README.md` não descreve como obter `evidence2.dd` nem apresenta receita para gerá-lo (`reivindicacoes.md:12`).
- **Trecho:** `reivindicacoes.md:12`:
  > *"O README indica como reproduzir? não"*
- **Status:** Não atendido (falta o dado obrigatório da reivindicação).
- **Classificação C6:** `nao_reproduzivel`.

#### Observação sobre C7 (Arquitetura de parsers extensível)
- Conforme `reivindicacoes.md:17`, C7 é uma contribuição arquitetural sem experimento associado e não integra o cômputo da regra do selo R. A modularidade pode ser inspecionada em [`artefato.txt:src/extract.c:2628-2695`].

### 3. Decisão para o Selo R
- **Decisão:** **Não atribuir**
- **Regra aplicada:** *"Não atribuir: há evidência de que um critério obrigatório não é atendido (por exemplo, falta o dado necessário para uma reivindicação principal)."* A regra de `reivindicacoes.md:17` estipula taxativamente que *"R é atribuído se C1 a C6 forem reproduzidas"*. Como `evidence2.dd` inexiste no artefato e o README não oferece meios para reconstituí-lo, a reivindicação principal C6 é irreproduzível.

### 4. Confiança da decisão oficial
- **Confiança:** 15% de que o comitê oficial atribuiu o selo R.
- *Justificativa:* É altamente improvável que um comitê de avaliação de artefatos conceda o selo Reprodutível quando a imagem forense correspondente ao único experimento ilustrado no artigo (`evidence2.dd` na Figura 2) foi omitida e não há roteiro de reprodução das tabelas publicadas no README.

### 5. O que precisaria ser observado na execução para mudar a decisão
- Para mudar a decisão de R para Atribuir, seria necessário dispor da imagem exata `evidence2.dd` (ou instrução completa de regeneração), executar `./foremost-ng -v -x evidence2.dd` e obter exatamente a lista de artefatos, tipos e offsets exibidos na Figura 2 da página 8 do artigo, além de demonstrar com sucesso o carving funcional para C1, C2, C3, C4 e C5.

---

## D. Lacunas e riscos

1. **Ausência de dados experimentais (`evidence2.dd`):** O artefato não inclui a imagem de disco usada no experimento da Seção 4.2 e Figura 2, impossibilitando a checagem dos offsets e arquivos publicados.
2. **Documentação sem roteiro de reprodução:** O `README.md` funciona apenas como manual genérico do software, sem menção a como reproduzir os achados do artigo ou testar especificamente os novos parsers adicionados.
3. **Ausência de suíte de testes automatizada:** Não há scripts de teste unitário ou de regressão (`make test`, `ctest` ou scripts em shell) para validação rápida dos formatos suportados.
4. **Dependência de serviço externo (VirusTotal API):** A funcionalidade `-x` depende de conectividade externa, de uma chave de API válida e está sujeita a mudanças de contagem de detecção e limitações de cota ao longo do tempo.
5. **Risco de parsers heurísticos:** O parsing de scripts e EVTX utiliza verificações simplificadas de sentinela e delimitadores de cabeçalho que podem ser suscetíveis a falsos positivos em cenários de alta fragmentação de dados.

---

```json
{"F": {"decisao": "Indeterminado", "confianca": 80, "evidencias": ["artefato.txt:README.md:21-68", "artefato.txt:src/Makefile:65-76", "artefato.txt:Dockerfile:1-12", "artefato.txt:src/main.c:197-220", "instrucoes-oficiais.md:15"]},
 "R": {"decisao": "Não atribuir", "confianca": 15, "evidencias": ["artefato.txt:README.md:1-119", "artefato.txt:ÍNDICE:9-50", "artigo.pdf:p.8,Fig.2", "reivindicacoes.md:12", "reivindicacoes.md:17", "instrucoes-oficiais.md:19"],
       "por_reivindicacao": {"C1": "depende_execucao", "C2": "depende_execucao", "C3": "depende_execucao", "C4": "depende_execucao", "C5": "depende_execucao", "C6": "nao_reproduzivel"}}}
```