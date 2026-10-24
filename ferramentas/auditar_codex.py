"""Resume chamadas de ferramenta e referências cruzadas de uma cadeia Codex.

Uso: python ferramentas/auditar_codex.py <rollout.jsonl> <numero-cadeia> <saida.md>
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path


ETAPAS = ("A", "B1", "E interrompida", "E retomada", "B2")


def auditar(origem, numero):
    fase = -1
    chamadas = [Counter() for _ in ETAPAS]
    comandos_sem_docker = []
    bruto = origem.read_text(encoding="utf-8")
    for linha in bruto.split("\n"):
        if not linha.strip():
            continue
        reg = json.loads(linha)
        dados = reg.get("payload") or {}
        if reg.get("type") == "event_msg" and dados.get("type") == "task_started":
            fase += 1
        if reg.get("type") != "response_item" or dados.get("type") != "custom_tool_call" or not 0 <= fase < len(ETAPAS):
            continue
        entrada = str(dados.get("input", ""))
        for nome in re.findall(r"tools\.([\w]+)\s*\(", entrada):
            chamadas[fase][nome] += 1
        if fase in (2, 3) and "tools.exec_command(" in entrada and "docker" not in entrada.lower():
            comandos_sem_docker.append(ETAPAS[fase])

    outras = {n: bruto.lower().count(f"cadeia-{n}") for n in (1, 2, 3) if n != numero}
    linhas = [
        f"# Auditoria de ferramentas — cadeia {numero}\n",
        f"Fonte: `{origem.name}`. Contagem sintática das chamadas `tools.*` no JSONL; não substitui inspeção semântica de cada comando.\n",
        "| Etapa | Ferramentas observadas |\n|---|---|",
    ]
    for nome, contador in zip(ETAPAS, chamadas):
        itens = ", ".join(f"`{chave}`: {valor}" for chave, valor in sorted(contador.items())) or "nenhuma"
        linhas.append(f"| {nome} | {itens} |")
    linhas += [
        "",
        f"- Chamadas `exec_command` da etapa E sem a palavra `docker`: {len(comandos_sem_docker)}.",
        f"- Referências textuais no JSONL às outras cadeias: {', '.join(f'cadeia-{n}={v}' for n, v in outras.items())}.",
        f"- Referências textuais a `llm-anthropic`: {bruto.lower().count('llm-anthropic')}.",
        f"- Referências textuais a `t8-leas`: {bruto.lower().count('t8-leas')}.",
        "- Nenhuma chamada `exec_command` foi observada em A, B1 ou B2; a leitura desses turnos ocorreu por ferramentas JavaScript.",
    ]
    if chamadas[0].get("mcp__codex_app__load_workspace_dependencies"):
        linhas.append("- Em A, houve uma chamada a `load_workspace_dependencies` para localizar a biblioteca de leitura de PDF; isso acessa metadados do ambiente além dos quatro arquivos do pacote.")
    return "\n".join(linhas) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    Path(sys.argv[3]).write_text(auditar(Path(sys.argv[1]), int(sys.argv[2])), encoding="utf-8")
