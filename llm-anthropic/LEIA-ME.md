# Claude — cadeias da T9 (Foremost-NG)

Responsável: Eduardo Prates Tiadoro. Coleta em 24/10/2026, 15:31–16:07 UTC (12:31–13:07 em Brasília), com as três cadeias rodando em paralelo. Resumo das decisões, tokens e tempo: [`../analise/resumo-claude.md`](../analise/resumo-claude.md).

## Configuração efetiva

| Campo | Valor |
|---|---|
| Interface | Claude Code (app desktop, Windows 11), agente `general-purpose` lançado pela sessão orquestradora com a ferramenta Agent (A) e continuado com SendMessage (B1, E, B2), na mesma conversa |
| Modelo | `claude-opus-5-5` em todas as respostas das três cadeias (campo `modelos` de `medicoes.json`) |
| Nível de raciocínio | **High**, herdado da sessão orquestradora: todas as requisições à API das três cadeias levam `"output_config":{"effort":"high"}` (cadeia 1: 154; cadeia 2: 220; cadeia 3: 197). Na T8, o Claude rodou em `Médio` |
| Ambiente de execução | imagem `t9/foremost-ng-exec:1` (`sha256:31c85217c98a…`), um contêiner por cadeia (`t9-claude-c1` a `c3`) |
| Registro factual congelado antes do B2 | `cadeia-N/registro-factual.sha256` |

## Arquivos de cada cadeia

| Arquivo | Conteúdo |
|---|---|
| `transcricao.md` | os quatro prompts como o agente os recebeu, todas as chamadas de ferramenta (com horário) e a resposta final de cada etapa |
| `resposta-A.md`, `resposta-B1.md`, `resposta-E.md`, `resposta-B2.md` | a resposta final de cada etapa, sem alteração |
| `medicoes.json` | tokens, tempo, chamadas de ferramenta e comandos `docker exec` por etapa |
| `auditoria.md` | caminhos lidos ou citados em comandos fora da pasta da cadeia |
| `execucao/` | o que o agente gravou na pasta de evidências: `registro-factual.md`, logs, scripts e hashes. Arquivos binários extraídos (EICAR, imagens) ficaram só no contêiner |

As transcrições e respostas vêm da transcrição do Claude Code (`subagents/agent-<id>.jsonl`), pelo [`../ferramentas/medir_cadeia.py`](../ferramentas/medir_cadeia.py). A chave do VirusTotal não aparece em nenhum arquivo: a ferramenta troca o valor por `<VT_API_KEY>`, e `grep` deu 0 ocorrências nas três pastas de evidências.

## Desvios e observações

1. **Moldura das mensagens.** O Claude Code entrega ao agente os prompts B1, E e B2 precedidos de "The coordinator sent a message while you were working:". O texto do prompt vem inteiro e sem alteração, mas por isso os roteiros B1 falam em "coordenador" e pedem a ele aprovações. O agente também recebe um lembrete do próprio Claude Code para entregar a resposta final pela ferramenta `SubagentHandback`.
2. **Cadeia 1, etapa A:** um comando de shell só de leitura (`wc -l` e `head -150` em `artefato.txt`), dentro da pasta da cadeia, apesar da instrução de usar só leitura de arquivos. O próprio agente declarou o desvio na resposta.
3. **Cadeia 2, etapa E:** um comando rodou em segundo plano, e o agente leu a saída dele no arquivo temporário do Claude Code (`auditoria.md`). É a saída do próprio comando, não material de outra cadeia. O tempo da etapa E inclui a espera.
4. **Auditoria de acesso:** fora esse arquivo temporário, nenhuma chamada de ferramenta leu ou citou caminhos fora de `t9-trabalho\claude-cN`. As URLs dos downloads feitos dentro do contêiner aparecem em `transcricao.md`.
5. **Autorização de downloads** decidida antes da etapa E e igual nas três cadeias (adendo do [pré-registro](../preregistro.md)).
6. **O orquestrador conhece a T8.** A sessão que lançou os agentes tem o histórico da T8, mas cada agente recebeu só os prompts.
7. **Decisões e regra de R.** Na etapa B2, as cadeias usaram rótulos diferentes para C1, C2, C4 e C5, que só tinham evidência complementar (D2/D3): a cadeia 1 usou `nao_reproduzivel`, a 2 usou `depende_execucao` e a 3 usou `reproduzivel`. As três concordam em C3 e C6 (`nao_reproduzivel`) e em R = Não atribuir.
