# Auditoria de ferramentas — cadeia 2

Fonte: `rollout-2026-10-24T14-08-45-01a16ee2-e1db-7851-b737-6ef70a9095e1.jsonl`. Contagem sintática das chamadas `tools.*` no JSONL; não substitui inspeção semântica de cada comando.

| Etapa | Ferramentas observadas |
|---|---|
| A | `mcp__node_repl__js`: 25 |
| B1 | nenhuma |
| E interrompida | `exec_command`: 31, `write_stdin`: 2 |
| E retomada | `exec_command`: 53 |
| B2 | `mcp__node_repl__js`: 3 |

- Chamadas `exec_command` da etapa E sem a palavra `docker`: 0.
- Referências textuais no JSONL às outras cadeias: cadeia-1=0, cadeia-3=0.
- Referências textuais a `llm-anthropic`: 0.
- Referências textuais a `t8-leas`: 0.
- Nenhuma chamada `exec_command` foi observada em A, B1 ou B2; a leitura desses turnos ocorreu por ferramentas JavaScript.
