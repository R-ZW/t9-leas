# t9-leas

Tarefa 9 de LEAS 2026/2 (Unipampa): avaliação dos selos F e R do **Foremost-NG** (SBSeg 2025) por três LLMs, cada uma executando o próprio roteiro, com registro de tokens e tempo. Continua a T8 ([R-ZW/t8-leas](https://github.com/R-ZW/t8-leas)) com o protocolo enxugado pelo professor:

- apenas o Foremost-NG;
- chave da API do VirusTotal fornecida pelo professor (fora do Git);
- execução feita pelas três LLMs, sem interação humana;
- gasto de tokens e tempo de execução registrados.

| LLM | Responsável | Situação |
|---|---|---|
| Claude | Eduardo Prates Tiadoro | 3 cadeias concluídas em 24/10/2026 — [`llm-anthropic/`](llm-anthropic/LEIA-ME.md) |
| GPT | Reinaldo Zimmer Wendt | 3 cadeias concluídas em 24/10/2026 — [`llm-openai/`](llm-openai/LEIA-ME.md) |
| Gemini | Miguel Ângelo Bastos Muniz | 3 cadeias concluídas em 24/10/2026 — [`llm-google/`](llm-google/LEIA-ME.md) |

## Estrutura

| Caminho | Conteúdo |
|---|---|
| [`preregistro.md`](preregistro.md) | o que muda em relação à T8, etapas, ambiente e medição (parte do Claude), com o adendo antes da etapa E |
| [`CONGELAMENTO.sha256`](CONGELAMENTO.sha256) | hashes do pré-registro, dos prompts, do Dockerfile e do manifesto do pacote |
| [`pacote/`](pacote/) | material entregue às LLMs, igual ao da T8 (`MANIFESTO.sha256`) |
| [`prompts/`](prompts/) | prompts A, B1, E (execução) e B2 |
| [`ambiente/Dockerfile`](ambiente/Dockerfile) | contêiner de execução: Ubuntu 24.04 limpo, sem as dependências do artefato |
| [`ferramentas/`](ferramentas/) | `medir_cadeia.py` (transcrição, tokens, tempo e auditoria) e `resumir.py` (tabela de decisões e medições) |
| `llm-<provedor>/cadeia-N/` | transcrição, respostas, medições e evidências de cada cadeia |
| [`analise/`](analise/) | resumos por provedor e [comparação das três LLMs](analise/comparacao.md) |

## Comparação das três LLMs

Em [`analise/comparacao.md`](analise/comparacao.md): decisões das 9 cadeias, causas, custo normalizado e 11 inconsistências registradas.

- **R:** Não atribuir em 9/9 cadeias, nas duas etapas. Motivos: falta `evidence2.dd` (C6); Claude e GPT também se apoiam em defeitos observados (Mach-O thin, filtro de comentários).
- **F em B2:** Gemini 3/3 Atribuir, Claude 1/3 e GPT 0/3. Todas as execuções funcionaram; a divergência é a leitura da exigência de versões e exemplo mínimo no README.
- **Coincidência com o oficial (F e R atribuídos):** 0/18 decisões em A e 4/18 em B2.
- **Custo médio por cadeia:** 23–29 min e 13–14 milhões de tokens processados; a execução concentra cerca de 80% dos tokens.

## Resultado do Claude (3 cadeias)

Detalhes em [`analise/resumo-claude.md`](analise/resumo-claude.md).

- **Etapa A** (só documentação): F e R = Não atribuir nas três cadeias.
- **Etapa B2** (depois da própria execução): R = Não atribuir nas três; F = Não atribuir nas cadeias 1 e 2 (README sem versões) e Atribuir na cadeia 3.
- **O que as três execuções observaram:**
  - o artefato compila e instala pelo README; o `make` na raiz, como manda o artigo, falha;
  - Mach-O thin não é extraído;
  - script só com comentários é extraído;
  - ELF sai sem a tabela de seções;
  - EVTX sai legível, mas o tamanho vem do campo errado;
  - sem chave, a coluna do VirusTotal registra "Clean (0)" (com chave inválida também, nas cadeias 1 e 3, que testaram); com a chave válida, o rótulo bate com a consulta direta à API;
  - `evidence2.dd` (Fig. 2, C6) continua indisponível.
- **Custo médio por cadeia:** cerca de 29 min e 108 mil tokens de saída (14 milhões no total, quase todos leitura de cache). A execução (E) leva mais da metade do tempo e cerca de 80% dos tokens.


## Resultado do GPT (3 cadeias)

Detalhes, medições por sessão e diferenças entre cadeias em [`analise/resumo-openai.md`](analise/resumo-openai.md).

- **Etapa A e B2:** F e R = Não atribuir nas três cadeias.
- O artefato compilou e executou um teste mínimo nos três contêineres. Os controles complementares observaram extração de scripts compostos só por comentários, ausência de extração Mach-O `thin` e limitações na delimitação de EVTX e ELF.
- A imagem `evidence2.dd` da Figura 2 permaneceu indisponível; C6 não foi reproduzida.
- As três etapas E foram interrompidas pelo limite de uso do Codex e retomadas nos mesmos chats e contêineres. Os tokens e tempos das duas sessões E de cada cadeia foram preservados nas medições.

## Resultado do Gemini (3 cadeias)

Detalhes em [`analise/resumo-gemini.md`](analise/resumo-gemini.md).

- **Etapa A** (só documentação): F = Indeterminado (confiança 80–85) e R = Não atribuir (confiança 10–20) nas três cadeias.
- **Etapa B2** (depois da própria execução): F = Atribuir nas três cadeias (confiança 95–100, `mudou: true`); R = Não atribuir nas três cadeias (confiança 5–95).
- **O que as três execuções observaram:**
  - o artefato compila via `make` em `src/` e instala via `sudo make install` no sistema;
  - o teste mínimo de carving extrai arquivos válidos e gera `audit.txt`;
  - EVTX (C1), Scripts (C2) e ELF (C4) foram recuperados com sucesso em testes complementares (D2);
  - Mach-O universal FAT (C3) é extraído nas três cadeias; Mach-O thin de 64 bits falha por bug de endianness em `src/extract.c:2408` (C3 marcado como `não rep` na cadeia 2 e como `rep` nas cadeias 1 e 3, com ressalva textual na 1);
  - a integração com o VirusTotal (C5) funciona via HTTP REST populando a coluna `VT` quando `VT_API_KEY` está presente, emitindo aviso sem abortar quando ausente;
  - `evidence2.dd` (Fig. 2, C6) continua indisponível no artefato e no ambiente, inviabilizando a reprodução da tabela e offsets publicados;
  - a cadeia 1 inverteu a polaridade da confiança de R no B2 (registrou 95 de certeza no próprio Não atribuir, em vez de confiança na atribuição pelo comitê).
- **Custo médio por cadeia:** cerca de 24,5 min e 117 mil tokens de saída (14,4 milhões no total, quase todos leitura de cache). A execução (E) leva a maior parte do tempo (~15 min) e dos tokens.
