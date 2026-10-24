# GPT (Codex) — resultado das três cadeias da T9

Coleta em 24/10/2026, com três agentes `gpt-6-sol` (`xhigh`), um por cadeia. Cada agente recebeu inicialmente só a etapa A e continuou na mesma conversa por B1, E e B2. As quatro fontes foram copiadas por cadeia com hashes idênticos aos do pacote original. A etapa E usou contêineres Ubuntu 24.04 separados, construídos de `ambiente/Dockerfile`, com o ZIP do artefato no hash do manifesto e a chave VT somente no ambiente dos contêineres.

As primeiras sessões E foram interrompidas pelo limite de uso do Codex. Os três chats e contêineres foram retomados com o estado anterior, e os agentes continuaram do último passo concluído. As medições incluem **as duas sessões E**, inclusive o tempo e os tokens consumidos antes da interrupção. Cada `registro-factual.md` foi congelado por SHA-256 antes do respectivo B2.

## Decisões

| Cadeia | F em A | R em A | F em B2 | R em B2 | Confiança F A→B2 | Confiança R A→B2 |
|---|---|---|---|---|---:|---:|
| 1 | Não atribuir | Não atribuir | Não atribuir | Não atribuir | 15→25 | 3→1 |
| 2 | Não atribuir | Não atribuir | Não atribuir | Não atribuir | 15→25 | 3→1 |
| 3 | Não atribuir | Não atribuir | Não atribuir | Não atribuir | 20→30 | 5→1 |

As confianças estimam a chance de o comitê oficial ter atribuído cada selo; não são a decisão histórica do comitê. As decisões completas estão em `llm-openai/cadeia-N/resposta-A.md` e `resposta-B2.md`.

Na etapa B2, os três agentes observaram compilação, instalação e uma extração mínima, mas mantiveram F = **Não atribuir** porque o README continua sem versões suficientes de dependências/ambiente e sem exemplo mínimo completo. Mantiveram R = **Não atribuir** porque faltam procedimentos e entradas dos autores para C1–C6, sobretudo `evidence2.dd` para confrontar os arquivos e offsets da Figura 2. Os ensaios com entradas propostas pelo revisor (D2) e dados de terceiros (D3) foram tratados como complementares.

## Fatos observados na execução

| Reivindicação | Observações das cadeias |
|---|---|
| C1, EVTX | EVTX públicos foram extraídos e puderam ser lidos. As cadeias 1 e 3 registraram bytes adicionais; a cadeia 2 recuperou uma amostra original byte a byte, mas também anexou uma cauda de 64 KiB no controle de delimitação. |
| C2, scripts | Scripts positivos foram extraídos. As três cadeias também observaram extração de um caso contendo só shebang e comentários, contrariando a restrição do artigo. |
| C3, Mach-O | Amostras `fat` foram recuperadas; amostras `thin` válidas não foram extraídas nas três cadeias. |
| C4, ELF | Arquivos 32/64 bits foram recuperados, mas os controles encontraram arquivos menores que as origens e erros de leitura dos cabeçalhos de seção. |
| C5, VirusTotal | Hashes ELF não conhecidos pela API retornaram HTTP 404 na conferência direta, enquanto o registro do artefato mostrou `Clean (0)`; o caso sem chave também registrou `Clean (0)`. As cadeias 1 e 3 confirmaram, com ZIP EICAR público, resultado `Malicious (61)` igual à consulta direta por hash. Não houve envio de arquivo ao VirusTotal. |
| C6, Figura 2 | `evidence2.dd` não estava disponível. A execução literal da figura e a comparação de seus arquivos e offsets não ocorreram. |

A classificação por reivindicação não foi uniforme em B2: C1 recebeu `nao_reproduzivel` apenas na cadeia 2; C4 recebeu `depende_execucao` apenas na cadeia 2. Todas classificaram C2, C3 e C6 como `nao_reproduzivel` e C5 como `depende_execucao`. Essa variação não alterou R.

## Tempo e tokens por sessão de cada chat

`Entrada` já **inclui** `cache lido`; `total = entrada + saída`. O cache é mostrado como parte da entrada, não somado novamente. O tempo é a duração ativa de cada turno entre `task_started` e `task_complete`, sem contar a pausa pelo limite de uso. Valores exatos e carimbos UTC estão nos `medicoes.json` de cada cadeia.

| Chat | Sessão | Tempo (min:s) | Entrada | Cache lido | Saída | Total |
|---:|---|---:|---:|---:|---:|---:|
| 1 | A | 4:44 | 2,640,440 | 2,569,856 | 14,396 | 2,654,836 |
| 1 | B1 | 2:22 | 90,102 | 85,760 | 10,524 | 100,626 |
| 1 | E interrompida | 6:38 | 2,954,778 | 2,920,960 | 13,203 | 2,967,981 |
| 1 | E retomada | 7:03 | 5,200,471 | 5,038,592 | 28,134 | 5,228,605 |
| 1 | B2 | 1:22 | 666,505 | 650,240 | 6,356 | 672,861 |
| **1 total** | | **22:09** | **11,552,296** | **11,265,408** | **72,613** | **11,624,909** |
| 2 | A | 4:03 | 1,819,067 | 1,752,192 | 14,545 | 1,833,612 |
| 2 | B1 | 2:27 | 95,426 | 89,600 | 11,279 | 106,705 |
| 2 | E interrompida | 7:07 | 4,157,923 | 4,118,144 | 13,772 | 4,171,695 |
| 2 | E retomada | 9:26 | 8,336,483 | 8,173,568 | 34,908 | 8,371,391 |
| 2 | B2 | 1:32 | 770,391 | 756,864 | 7,363 | 777,754 |
| **2 total** | | **24:36** | **15,179,290** | **14,890,368** | **81,867** | **15,261,157** |
| 3 | A | 4:12 | 2,277,876 | 2,204,672 | 14,201 | 2,292,077 |
| 3 | B1 | 2:27 | 100,767 | 95,360 | 11,108 | 111,875 |
| 3 | E interrompida | 6:37 | 3,251,253 | 3,219,968 | 10,312 | 3,261,565 |
| 3 | E retomada | 9:02 | 6,131,158 | 5,987,840 | 28,242 | 6,159,400 |
| 3 | B2 | 1:08 | 517,960 | 507,776 | 5,044 | 523,004 |
| **3 total** | | **23:27** | **12,279,014** | **12,015,616** | **68,907** | **12,347,921** |

Os três chats somaram **39.233.987 tokens reportados**, sendo **223.387 de saída**, e **70:11** de tempo ativo somado. Como rodaram em paralelo, esse tempo agregado não é tempo de relógio decorrido. O chat orquestrador tem duas sessões registradas em `llm-openai/medicoes-orquestrador.json`: a sessão inicial fechada e a retomada medida até a última fotografia de uso anterior à resposta final.

## Integridade e auditoria

- Os SHA-256 em `llm-openai/cadeia-N/registro-factual.sha256` correspondem aos registros factuais após B2.
- A busca pelo valor literal da chave VT em `llm-openai/` encontrou **zero ocorrências**.
- `transcricao.md` preserva chamadas de ferramenta e respostas finais; os prompts base são reconstruídos dos arquivos congelados porque as mensagens de orquestração aparecem cifradas no JSONL local do agente. `auditoria.md` resume as ferramentas por etapa e as referências cruzadas observadas.
- Na etapa A da cadeia 1, uma chamada a `load_workspace_dependencies` consultou metadados do ambiente para localizar a biblioteca de PDF. As auditorias não encontraram referências textuais às outras cadeias nem a `llm-anthropic`.
- Os JSONL locais dos chats forneceram as contagens exatas de tokens. Os arquivos `medicoes.json` guardam os identificadores dos chats e turnos, início, fim e consumo de cada sessão.
