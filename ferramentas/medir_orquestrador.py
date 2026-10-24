"""Registra uso do chat orquestrador, inclusive turno corrente em andamento.

Uso: python ferramentas/medir_orquestrador.py <rollout.jsonl> <saida.json>
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from medir_codex import medir


def momento(valor):
    return datetime.fromisoformat(valor.replace("Z", "+00:00"))


def medir_orquestrador(origem):
    base = medir(origem)
    originais = list(base["etapas"].values())
    nomes = ("orquestracao-inicial", "retomada")
    etapas = {}
    ultimo_registro = None
    for linha in origem.open(encoding="utf-8"):
        reg = json.loads(linha)
        if reg.get("type") == "token_usage_record":
            ultimo_registro = reg["timestamp"]
    for indice, dados in enumerate(originais):
        nome = nomes[indice] if indice < len(nomes) else f"turno-{indice + 1}"
        if "fim_utc" not in dados and ultimo_registro:
            dados["observado_utc"] = ultimo_registro
            dados["duracao_s_ate_registro"] = round((momento(ultimo_registro) - momento(dados["inicio_utc"])).total_seconds(), 1)
            dados["parcial"] = True
        etapas[nome] = dados
    base["etapas"] = etapas
    base["tempo_ativo_s"] = round(sum(x.get("duracao_s", x.get("duracao_s_ate_registro", 0)) for x in etapas.values()), 1)
    base["observacao"] = "O turno de retomada é uma fotografia anterior à resposta final do orquestrador."
    return base


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    resultado = medir_orquestrador(Path(sys.argv[1]))
    Path(sys.argv[2]).write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
