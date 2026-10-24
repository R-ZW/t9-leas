# Parecer de Avaliação Analítica de Artefatos — SBSeg 2025 (Etapa A)

**Artefato:** Foremost-NG: An Open-Source Toolkit for Advanced File Carving and Analysis  
**Versão analisada (commit):** `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d`  
**Avaliador:** Revisor do Comitê de Avaliação de Artefatos do SBSeg 2025  

---

## A. Materiais examinados

Foram consultados e examinados exclusivamente os arquivos fornecidos no pacote de avaliação (`D:\t9-trabalho\gemini-c2\pacote`):
1. `instrucoes-oficiais.md`: Critérios oficiais de revisão do SBSeg 2025 para os selos Funcional (F) e Reprodutível (R).
2. `reivindicacoes.md`: Relação de reivindicações principais (C1 a C7) e regras para atribuição de R.
3. `artigo.pdf`: Texto integral do artigo submetido aos Anais Estendidos do SBSeg 2025 (8 páginas).
4. `artefato.txt`: Repositório completo do Foremost-NG em arquivo único consolidado no commit `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d`, contendo o índice e código-fonte integral de:
   - `.gitignore`
   - `Dockerfile`
   - `LICENSE`
   - `README.md`
   - `src/Makefile`
   - `src/ansi_colors.h`
   - `src/api.c`
   - `src/cli.c`
   - `src/config.c`
   - `src/dir.c`
   - `src/engine.c`
   - `src/extract.c`
   - `src/extract.h`
   - `src/foremost.conf`
   - `src/helpers.c`
   - `src/main.c`
   - `src/main.h`
   - `src/ole.h`
   - `src/state.c`
   - `src/vt_query.c`
   - `src/vt_query.h`
   - Referências de binários e bibliotecas dinâmicas em `windows_dlls/`.

Nenhum comando foi executado e não houve compilação nesta etapa analítica.

---

## B. Selo Funcional (F)

### 1. Critérios oficiais aplicáveis
Trecho das instruções oficiais (`instrucoes-oficiais.md:15`):
> "O artefato precisa ser executável e permitir a observação de funcionalidades. O README deve informar dependências, versões de dependências/linguagens/ambiente, ambiente de execução, instalação, execução e pelo menos um exemplo mínimo. O revisor deve **executar** o artefato e apresentar prova de execução e saídas no parecer. Ler código ou README, por si só, não constitui prova de funcionamento."

### 2. Análise por critério
- **Dependências e ambiente de execução:** *Atendido parcialmente na documentação*. O `README.md:37-69` e o `Dockerfile:3-6` informam ferramentas e bibliotecas necessárias (`gcc`, `make`, `git`, `libssl-dev`, `libcurl4-openssl-dev`, `curl`, `openssl@3`, MinGW) e ambientes operacionais suportados (Linux, BSD, macOS, Windows). Todavia, não há declaração das versões exatas mínimas de dependências ou da linguagem C (o Dockerfile fixa apenas `FROM ubuntu:latest`).
- **Instalação:** *Atendido na documentação*. O `README.md:21-71` descreve os passos de compilação via `make` e `sudo make install`, bem como alvos para BSD (`make unix`), macOS (`make mac`) e cross-compilation para Windows (`make cross`). O `Dockerfile:10` automatiza com `RUN make && make install`, e o `src/Makefile:1-171` implementa todos os alvos descritos.
- **Execução:** *Atendido na documentação*. O `README.md:74-87` e `89-108` documenta a sintaxe de invocação `foremost-ng [options] [image_or_device]`, a opção `-x` e a configuração da chave de API através da variável de ambiente `VT_API_KEY`.
- **Exemplo mínimo:** *Não atendido na documentação do repositório*. O `README.md:82-85` fornece apenas a sinopse genérica de uso (`foremost-ng [options] [image_or_device]`). Não há um comando de exemplo concreto com parâmetros definidos e arquivos de entrada reais ou demonstrativos no README, nem arquivos de teste distribuídos no repositório. O artigo (`artigo.pdf:p. 7, §4.1`) traz comandos ilustrativos (`foremost-ng -i disk.img -o /temp/output/carved`), mas estes não constam na documentação do artefato.
- **Executabilidade e observação de funcionalidades:** *Só verificável por execução*. Por definição explícita das instruções, a leitura estática de código e documentação não comprova execução sem falhas.

### 3. Evidências documentais citadas
- [artefato.txt:README.md:21-35]: *"## Installation ... cd foremost-ng-<version>/src ... make ... sudo make install"*
- [artefato.txt:README.md:74-85]: *"## Usage ... Basic syntax: foremost-ng [options] [image_or_device]"*
- [artefato.txt:README.md:91-101]: *"foremost-ng supports automatic file reputation checks using the VirusTotal API via the -x command-line option ... export VT_API_KEY=yourkey"*
- [artefato.txt:Dockerfile:1-12]: *"FROM ubuntu:latest ... RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev ... WORKDIR /opt/foremost-ng/src RUN make && make install"*
- [artefato.txt:src/Makefile:1-10]: *"RAW_CC = gcc ... NAME = foremost-ng ... GOAL = $(NAME)"*

### 4. Decisão: Indeterminado
**Regra aplicada:** *Indeterminado: nenhum critério obrigatório falha na documentação, mas a decisão depende de execução.*  
A base de código em C está completa, acompanhada de Makefile abrangente e Dockerfile funcional. Não há vício insanável no código que impeça previamente a tentativa de compilação e execução, porém o selo F exige prova fática de execução que só pode ser obtida na Etapa E.

### 5. Confiança
**80 / 100** de que o comitê oficial atribuiu o selo F.  
A implementação C é modular e padrão, as dependências são convencionais em distribuições Linux (`gcc`, `libcurl`, `openssl`), e o repositório traz instruções de build coerentes, conferindo alta probabilidade de sucesso prático.

### 6. O que precisaria ser observado na execução para mudar a decisão
- Compilação bem-sucedida do binário `foremost-ng` a partir do código-fonte via `make` sem erros;
- Execução regular dos parâmetros informativos (`foremost-ng -h` e `foremost-ng -V`);
- Execução de um comando básico de extração gerando a estrutura de diretórios prevista (`carved/`) e o arquivo de log `audit.txt`.

---

## C. Selo Reprodutível (R) (por reivindicação)

### 1. Critérios oficiais aplicáveis
Trecho das instruções oficiais (`instrucoes-oficiais.md:19`):
> "O revisor deve conseguir reproduzir as **principais reivindicações do artigo**. A documentação do artefato deve trazer instruções de execução dessas reivindicações e descrever o processo usado pelos autores para chegar aos resultados publicados. O revisor deve executar os experimentos e confrontar os resultados com os do artigo, incluindo figuras/tabelas pertinentes, resumindo a comparação no parecer."

Conforme `reivindicacoes.md:15-22`, as reivindicações avaliadas são C1 a C6, sendo o selo R concedido somente se C1 a C6 forem integralmente reproduzidas.

### 2. Avaliação detalhada por reivindicação

#### C1: Recuperação de logs de eventos do Windows (EVTX)
- **Onde está no artigo:** p. 1 (resumo); p. 2 (introdução); p. 6, §3, item "Windows Event Logs (EVTX)"; p. 7, §4.1.
- **Evidências no artefato:**
  - [artefato.txt:src/state.c:693-694]: `init_builtin(s, EVTX, "evtx", "ElfFile\0\0", NULL, 8, 0, max_file_size, TRUE);`
  - [artefato.txt:src/extract.c:2458-2490]: `extract_evtx ... if (memcmp(buf, "ElfFile\0\0", 8) != 0) ... chunk_count = htoi(&buf[0x18], FOREMOST_LITTLE_ENDIAN); ... full_size = (uint64_t)chunk_count * 65536ULL;`
- **Documentação para reprodução:** O `README.md:74-85` contém apenas sintaxe geral; não há arquivos `.evtx` ou imagens de disco no repositório.
- **Situação:** **depende_execucao**. O algoritmo reconhece a assinatura `ElfFile\0\0` e delimita blocos de 64 KiB, mas a extração de arquivo íntegro e legível só pode ser atestada executando o binário com amostras compatíveis.

#### C2: Recuperação de scripts (Bash, Python, PowerShell)
- **Onde está no artigo:** p. 1 (resumo); p. 2 (introdução); p. 6, §3, item "Script Files".
- **Evidências no artefato:**
  - [artefato.txt:src/state.c:696-697]: `init_builtin(s, SCRIPT, "script", "#!", NULL, 2, 0, 2 * MEGABYTE, TRUE);`
  - [artefato.txt:src/extract.c:2519-2613]: `extract_script ... const uint64_t MIN_SCRIPT_SIZE = 32; ... while (p < end) { if (!isspace(*p)) { if (*p != '#') { found_real = 1; break; } } ... if (!found_real) return ...`
- **Documentação para reprodução:** Parcial no README (apenas sintaxe geral); sem massa de dados de teste.
- **Situação:** **depende_execucao**. A implementação contempla a validação de cabeçalho `#!`, corpo com texto imprimível além de comentários e tamanho mínimo de 32 bytes; sua eficácia prática depende de teste de execução.

#### C3: Recuperação de binários Mach-O (fat e thin)
- **Onde está no artigo:** p. 1 (resumo); p. 2 (introdução); p. 6, §3, item "Mach-O (macOS/iOS Binaries)".
- **Evidências no artefato:**
  - [artefato.txt:src/state.c:677-687]: Registro em `set_search_def` do cabeçalho universal `\xCA\xFE\xBA\xBE`, do 32-bit `\xCE\xFA\xED\xFE` e do 64-bit `\xCF\xFA\xED\xFE`.
  - [artefato.txt:src/extract.c:2327-2444]: `extract_macho ... uint32_t nfat_arch = read_be32(&buf[4]); ... if (cmd == 0x19 /* LC_SEGMENT_64 */) ...`
- **Documentação para reprodução:** Parcial no README; nenhuma amostra Mach-O inclusa.
- **Situação:** **depende_execucao**. O código calcula extents via cabeçalho universal e comandos de carga (`LC_SEGMENT` / `LC_SEGMENT_64`), exigindo verificação experimental.

#### C4: Recuperação de executáveis ELF de 32 e 64 bits
- **Onde está no artigo:** p. 1 (resumo); p. 2 (introdução); p. 6, §3, item "ELF"; p. 7, §4.1.
- **Evidências no artefato:**
  - [artefato.txt:src/state.c:452-453]: `init_builtin(s, ELF, "elf", "\x7F\x45\x4C\x46", NULL, 4, 0, max_file_size, TRUE);`
  - [artefato.txt:src/extract.c:2159-2286]: `extract_elf ... ei_class == 1 ... e_phoff_32 ... p_type_32 == 1 /* PT_LOAD */ ... ei_class == 2 ... e_phoff_64 ... p_type_64 == 1`
- **Documentação para reprodução:** Parcial no README; sem amostras binárias no repositório.
- **Situação:** **depende_execucao**. O algoritmo extrai executáveis baseando-se na união dos segmentos `PT_LOAD`; a integridade dos arquivos recuperados requer execução contra imagens com ELF.

#### C5: Enriquecimento pelo VirusTotal
- **Onde está no artigo:** p. 1 (resumo); pp. 2–3, §2; p. 7, §4, §4.1; p. 8, Fig. 2 (coluna VT).
- **Evidências no artefato:**
  - [artefato.txt:src/vt_query.c:136-186]: `VTResult vt_check_hash(const char *hash) ... curl_easy_setopt(curl, CURLOPT_URL, url) ... sscanf(stats, "\"last_analysis_stats\": {\"malicious\": %d, \"suspicious\": %*d, \"undetected\": %d", ...`
  - [artefato.txt:src/dir.c:274-283]: `if (get_mode(s, mode_virustotal)) { sha_checksum(fn, "sha256", sha256); vt = vt_check_hash(sha256); snprintf(nd->vt_label, sizeof(nd->vt_label), vt.is_malicious ? "Malicious (%d)" : "Clean (%d)", ...); }`
  - [artefato.txt:README.md:91-108]: Seção detalhando a opção `-x` e a variável `VT_API_KEY`.
- **Documentação para reprodução:** Instruído no README; requer ambiente com chave e conectividade de rede.
- **Situação:** **depende_execucao**. A rotina calcula o hash SHA-256 e consome a API v3 da plataforma, preenchendo as colunas do `audit.txt`. Sua constatação depende de teste com conexão ativa e chave válida.

#### C6: Exemplo de execução da Figura 2 (`./foremost-ng -v -x evidence2.dd`)
- **Onde está no artigo:** p. 7, §4.2; p. 8, Fig. 2. A Figura 2 reporta uma execução exata sobre a imagem forense `evidence2.dd` de 2 GB (2045109643 bytes), com extração de 12 arquivos (ELF, script, EXE, ZIP) em offsets decimais estritos (2228224 a 914965615) e verdicts do VT.
- **Evidências no artefato:**
  - [artefato.txt:ÍNDICE:9-49]: O arquivo `evidence2.dd` **NÃO CONSTA** no repositório do artefato.
  - [artefato.txt:README.md:74-87]: Não há nenhuma menção ao arquivo `evidence2.dd`, nem procedimentos ou scripts para obter/sintetizar a imagem forense correspondente.
  - [artigo.pdf:p. 7, §4]: É feita apenas uma menção genérica de que amostras de teste podem ser obtidas em `https://dftt.sourceforge.net`, sem referência à composição específica de `evidence2.dd`.
  - [reivindicacoes.md:12]: A linha C6 registra expressamente *"O README indica como reproduzir? não"*.
- **Situação:** **nao_reproduzivel**. O dataset de 2 GB é o elemento empírico mandatório para confrontar os resultados publicados da Figura 2 e está formalmente ausente do artefato e de sua documentação.

### 3. Decisão: Não atribuir
**Regra aplicada:** *Não atribuir: há evidência de que um critério obrigatório não é atendido (por exemplo, falta o dado necessário para uma reivindicação principal).*  
A instrução do SBSeg 2025 (`instrucoes-oficiais.md:19`) exige que a documentação traga instruções de execução e descreva o processo usado para chegar aos resultados publicados, permitindo confrontar tabelas e figuras. Como o arquivo `evidence2.dd` não foi fornecido e inexiste roteiro para reproduzir a Figura 2, a reivindicação obrigatória C6 falha no exame documental, impossibilitando a concessão do selo R com o pacote atual.

### 4. Confiança
**20 / 100** de que o comitê oficial atribuiu o selo R.  
Sem os dados de teste correspondentes à imagem forense de 2 GB ou um script reprodutor no repositório oficial, um comitê de avaliação padrão reprova a reprodutibilidade dos experimentos numéricos/figuras específicas.

### 5. O que precisaria ser observado na execução para mudar a decisão
- Existência ou injeção prévia do arquivo `evidence2.dd` no contêiner de execução;
- Execução do comando `./foremost-ng -v -x evidence2.dd` resultando na exata listagem de 12 arquivos recuperados nos offsets apontados pela Figura 2;
- Validação satisfatória da extração e integridade estrutural para C1 a C5.

---

## D. Lacunas e riscos

1. **Ausência de dados de teste (Datasets ausentes):** O repositório não acompanha a imagem de 2 GB `evidence2.dd`, inviabilizando a checagem direta do experimento da Figura 2 sem dados externos. Amostras para testes de EVTX e Mach-O também estão ausentes no pacote.
2. **Deficiência documental no README:** O `README.md` não cita o suporte aos novos formatos implementados (EVTX, Mach-O, scripts), carece de exemplos práticos de linha de comando com arquivos fictícios e omite versões exatas das dependências.
3. **Fragilidade no parser de resposta da API do VirusTotal:** Em `src/vt_query.c:180`, a extração dos contadores da API v3 do VirusTotal é realizada via `sscanf` sobre o buffer de texto (`"last_analysis_stats": {"malicious": %d, "suspicious": %*d, "undetected": %d`), sem uso de uma biblioteca robusta de parsing JSON. Quaisquer alterações na ordenação das chaves pela API da VirusTotal quebrarão silenciosamente a leitura dos contadores.
4. **Dependência de fatores externos voláteis:** A funcionalidade de enriquecimento por inteligência de ameaças requer conectividade com a internet, validade da chave `VT_API_KEY` e está sujeita a variações temporais nas contagens de motores antivírus.

---

```json
{
  "F": {
    "decisao": "Indeterminado",
    "confianca": 80,
    "evidencias": [
      "artefato.txt:README.md:21-71",
      "artefato.txt:README.md:74-85",
      "artefato.txt:README.md:89-108",
      "artefato.txt:Dockerfile:1-12",
      "artefato.txt:src/Makefile:1-10"
    ]
  },
  "R": {
    "decisao": "Não atribuir",
    "confianca": 20,
    "evidencias": [
      "artefato.txt:ÍNDICE:9-49",
      "artefato.txt:README.md:74-87",
      "artigo.pdf:p. 7, §4.2",
      "artigo.pdf:p. 8, Fig. 2",
      "reivindicacoes.md:11-17"
    ],
    "por_reivindicacao": {
      "C1": "depende_execucao",
      "C2": "depende_execucao",
      "C3": "depende_execucao",
      "C4": "depende_execucao",
      "C5": "depende_execucao",
      "C6": "nao_reproduzivel"
    }
  }
}
```