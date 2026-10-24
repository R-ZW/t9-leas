# Auditoria de ferramentas — cadeia 1

Fonte: `rollout-2026-10-24T14-08-37-01a16ee2-c24b-7910-9e58-7e801516197f.jsonl`. Contagem sintática das chamadas `tools.*` no JSONL; não substitui inspeção semântica de cada comando.

| Etapa | Ferramentas observadas |
|---|---|
| A | `mcp__codex_app__load_workspace_dependencies`: 1, `mcp__node_repl__js`: 36, `mcp__node_repl__js_add_node_module_dir`: 1 |
| B1 | nenhuma |
| E interrompida | `exec_command`: 22, `write_stdin`: 3 |
| E retomada | `apply_patch`: 4, `exec_command`: 32 |
| B2 | `mcp__node_repl__js`: 3 |

- Chamadas `exec_command` da etapa E sem a palavra `docker`: 0.
- Referências textuais no JSONL às outras cadeias: cadeia-2=0, cadeia-3=0.
- Referências textuais a `llm-anthropic`: 0.
- Referências textuais a `t8-leas`: 0.
- Nenhuma chamada `exec_command` foi observada em A, B1 ou B2; a leitura desses turnos ocorreu por ferramentas JavaScript.
- Em A, houve uma chamada a `load_workspace_dependencies` para localizar a biblioteca de leitura de PDF; isso acessa metadados do ambiente além dos quatro arquivos do pacote.
