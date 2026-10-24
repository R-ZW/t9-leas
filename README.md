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
| Gemini | Miguel Ângelo Bastos Muniz | a fazer |

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
| [`analise/`](analise/) | resumos por provedor |

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
