# Pré-registro — T9 (LEAS 2026/2), parte do Claude

Escrito em 24/10/2026, antes de qualquer Prompt A da T9. Responsável: Eduardo Prates Tiadoro, que roda a parte do Claude. Reinaldo (GPT) e Miguel (Gemini) rodam as suas partes separadamente.

## O que muda em relação à T8

A T9 repete o protocolo da T8 com as mudanças pedidas pelo professor:

1. **Apenas o Foremost-NG** (SBSeg 2025), na mesma versão proxy `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` e com o mesmo pacote (hashes em [`pacote/MANIFESTO.sha256`](pacote/MANIFESTO.sha256), iguais aos da T8).
2. **A execução é feita pela própria LLM, sem interação humana.** Não há execução de referência única nem roteiro consolidado: cada cadeia executa o próprio roteiro B1 e decide o B2 com o próprio registro.
3. **A chave da API do VirusTotal é fornecida pelo professor**, o que permite testar C5 com chave. Ela fica fora do Git (`C:\Users\eduar\t9-leas-chaves\vt.env`) e entra no contêiner como variável `VT_API_KEY`. Qualquer ocorrência do valor nos registros é trocada por `<VT_API_KEY>` antes do commit.
4. **Gasto de tokens e tempo** de cada etapa é registrado.

O resto segue a T8: três cadeias independentes, selos F e R, decisões Atribuir / Não atribuir / Indeterminado, confiança de 0 a 100, regra de R = C1 a C6 reproduzidas ([`pacote/reivindicacoes.md`](pacote/reivindicacoes.md)), classes de desvio D0–D3, verificação cega das evidências e métricas.

## Interface e modelo

| Campo | Valor |
|---|---|
| Interface | Claude Code (app desktop, Windows), um agente novo (`general-purpose`) por cadeia, lançado pela sessão orquestradora com a ferramenta Agent e continuado com SendMessage na mesma conversa |
| Modelo | `claude-opus-5-5` (o mesmo da T8), nível de raciocínio herdado da sessão |
| Contexto inicial do agente | só o prompt da etapa: o agente não recebe o histórico da sessão orquestradora; não há `CLAUDE.md` nem memória de projeto |
| Ferramentas | as do agente (leitura, escrita, terminal). A restrição de leitura às pastas da cadeia e a proibição de executar em A, B1 e B2 são feitas por instrução no prompt e **auditadas** depois na transcrição |

## Etapas de cada cadeia (mesma conversa)

| Etapa | Prompt | O que o agente pode fazer |
|---|---|---|
| A | [`prompts/prompt-A.txt`](prompts/prompt-A.txt) | ler os 4 arquivos de `pacote/` da cadeia |
| B1 | [`prompts/prompt-B1.txt`](prompts/prompt-B1.txt) | idem; escreve o roteiro sem executar |
| E | [`prompts/prompt-E.txt`](prompts/prompt-E.txt) | executa o próprio roteiro no contêiner da cadeia e escreve `registro-factual.md` |
| B2 | [`prompts/prompt-B2.txt`](prompts/prompt-B2.txt) | lê o próprio registro e decide de novo |

Os campos `{PACOTE}`, `{EXEC_HOST}` e `{CONTEINER}` são trocados pelos caminhos da cadeia; nada mais muda entre as cadeias.

**Diferenças deliberadas em relação aos prompts da T8**, iguais nas três cadeias:
- "anexados" virou "nesta pasta", e o A proíbe executar comandos (antes, a interface de chat já impedia);
- o B1 diz que o próprio revisor executará e descreve o ambiente (Ubuntu 24.04 limpo, com sudo, unzip e man, sem compilador);
- a etapa E é nova;
- o B2 não fala mais em roteiro consolidado de três revisores nem em `{CONDICAO}`, porque a LLM conhece o próprio ambiente.

## Ambiente de execução

- Pasta de trabalho de cada cadeia, fora do repositório: `D:\Lab-artefatos\t9-trabalho\claude-cN\` (`pacote/` com os 4 arquivos, `execucao/` montada no contêiner como `/home/revisor/evidencias`).
- Imagem `t9/foremost-ng-exec:1`, de [`ambiente/Dockerfile`](ambiente/Dockerfile): Ubuntu 24.04 (`noble-20250619`), apt fixado em 08/07/2025, só `sudo`, `unzip` e `man`. Sem dependências do Foremost-NG.
- Um contêiner novo por cadeia (`t9-claude-cN`), criado pelo orquestrador antes da etapa E, com `artefato.zip` copiado para `/home/revisor/artefato.zip` e `VT_API_KEY` no ambiente.
- C6 continua sem `evidence2.dd` (não publicada; o pedido aos autores, enviado em 19/10/2026, não teve resposta até 24/10/2026).

## Medição

- **Tokens:** somados das mensagens do agente na transcrição do Claude Code (`subagents/agent-*.jsonl`), por etapa: entrada, saída, cache criado e cache lido.
- **Tempo:** do envio do prompt até a última mensagem do agente em cada etapa (carimbos da transcrição), e tempo total da cadeia.
- Também se registram o número de chamadas de ferramenta e de comandos `docker exec` por etapa.

## Adendo antes da etapa E (24/10/2026)

Os três roteiros B1 pediram aprovação de um "coordenador" para downloads de amostras públicas e previram um operador humano para exportar a chave e conferir o VirusTotal. Como a execução não tem interação humana, o aluno decidiu (24/10/2026), antes de qualquer E, autorizar de uma vez, igual nas três cadeias: pacotes apt/pip, clone do repositório dos autores e downloads de dados públicos de teste, **só dentro do contêiner**, com URL, tamanho e SHA-256 registrados. As conferências atribuídas a um humano ficam com a própria LLM; no VirusTotal, só consultas por hash, sem envio de arquivos. O prompt E ganhou o bloco "AUTORIZAÇÕES", que também informa que `evidence2.dd` não está disponível. Os hashes congelados foram refeitos depois desta mudança.

## Ameaças já conhecidas

- O executor e o avaliador são o mesmo modelo: o registro factual é escrito pela própria LLM que decide o B2, e pode ser enviesado. A verificação cega confere as evidências citadas contra os arquivos de evidência.
- O agente roda no computador do aluno, que também tem o repositório da T8 com os selos oficiais e as respostas da T8. O isolamento é por instrução. A auditoria da transcrição lista todo arquivo lido fora das pastas da cadeia.
- O agente é lançado por uma sessão que conhece a T8, mas não recebe nada dela além do prompt.
