# GPT (Codex) — três cadeias da T9

Execução concluída em 24/10/2026. Cada cadeia usou um agente Codex independente,
sem histórico do orquestrador (`fork_turns: none`), e continua **na mesma conversa**
pelas etapas A, B1, E e B2. A etapa E foi interrompida por limite de uso e
retomada no mesmo chat e contêiner, sem repetir os passos concluídos. O modelo efetivo registrado nos três chats é
`gpt-6-sol`, com raciocínio `xhigh`.

## Pacote e ambiente

- As quatro fontes de A foram copiadas separadamente para `cadeia-N/pacote/`;
  seus SHA-256 coincidem com `pacote/MANIFESTO.sha256`.
- Os prompts usados são `prompts/prompt-A.txt`, `prompt-B1.txt`,
  `prompt-E.txt` e `prompt-B2.txt`, com os caminhos da cadeia substituídos.
  As mensagens A/B1 também identificaram a cadeia e pediram a entrega da
  resposta final no chat; após o limite de uso houve uma mensagem de
  retomada de E para continuar das evidências existentes.
- A imagem `t9/foremost-ng-exec:1` foi construída de `ambiente/Dockerfile`.
  Cada cadeia usa seu próprio contêiner `t9-openai-cN`, com o mesmo
  `artefato.zip` (SHA-256 `955c770e29893527f789e11afc28dcc6b83d7af4a64f14b416e39f554b388e0a`).
- A chave fornecida para `VT_API_KEY` entrou apenas no ambiente dos
  contêineres; não deve constar dos arquivos versionados. As evidências
  persistem em `cadeia-N/execucao/`. Os contêineres foram parados após B2,
  mantendo seus sistemas de arquivos para eventual inspeção.

## Arquivos por cadeia

| Arquivo | Conteúdo |
|---|---|
| `resposta-A.md`, `resposta-B1.md`, `resposta-E.md`, `resposta-B2.md` | Resposta final de cada etapa, extraída do evento `task_complete` do respectivo chat |
| `medicoes.json` | Início, fim, tempo ativo e tokens por etapa, extraídos dos eventos de uso do Codex |
| `registro-factual.sha256` | Hash do registro da etapa E, calculado antes de enviar B2 |
| `transcricao.md` | Prompts base reconstruídos dos arquivos congelados, chamadas de ferramenta e respostas finais |
| `auditoria.md` | Contagens de ferramentas e referências textuais a outras cadeias |
| `execucao/` | Registro factual e arquivos de evidência gravados pelo agente |

`ferramentas/medir_codex.py`, `ferramentas/exportar_respostas_codex.py`,
`ferramentas/exportar_transcricao_codex.py`, `ferramentas/auditar_codex.py`
e `ferramentas/medir_orquestrador.py`
processam as transcrições JSONL locais dos chats. As mensagens de
orquestração vêm cifradas no JSONL do agente; a transcrição mostra o texto
base reconstruído dos prompts versionados e deixa essa limitação explícita.
`input_tokens` inclui
`cached_input_tokens`; `total_tokens` é o total reportado pelo Codex, sem
somar o cache outra vez. A duração é o intervalo entre os eventos
`task_started` e `task_complete` de cada etapa.

As conclusões e medições consolidadas estão em `analise/resumo-openai.md`.
