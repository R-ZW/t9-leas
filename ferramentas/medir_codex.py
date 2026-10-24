"""Extrai tempo e tokens por turno de uma transcrição JSONL do Codex.

Uso: python ferramentas/medir_codex.py <rollout.jsonl> [saida.json]

Lê somente metadados de eventos e de uso; não copia prompts, respostas ou
parâmetros de ferramentas, que podem conter segredos.
"""

import json
import sys
from datetime import datetime
from pathlib import Path


ETAPAS = ("A", "B1", "E-interrompida", "E-retomada", "B2")
CAMPOS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)


def momento(valor):
    return datetime.fromisoformat(valor.replace("Z", "+00:00"))


def medir(caminho):
    sessoes = {}
    ordem = []
    identificador = None
    for linha in caminho.open(encoding="utf-8"):
        registro = json.loads(linha)
        tipo = registro.get("type")
        dados = registro.get("payload") or {}
        if tipo == "session_meta":
            identificador = dados.get("id")
        elif tipo == "event_msg":
            evento = dados.get("type")
            turno = dados.get("turn_id")
            if evento == "task_started" and turno:
                sessoes[turno] = {"inicio_utc": registro["timestamp"]}
                ordem.append(turno)
            elif evento == "task_complete" and turno in sessoes:
                sessoes[turno]["fim_utc"] = registro["timestamp"]
                sessoes[turno]["duracao_s"] = round(
                    (momento(registro["timestamp"]) - momento(sessoes[turno]["inicio_utc"])).total_seconds(), 1
                )
        elif tipo == "token_usage_record":
            turno = dados.get("turn_id")
            if turno in sessoes:
                sessoes[turno]["tokens"] = {
                    campo: dados.get("turn_token_usage", {}).get(campo, 0)
                    for campo in CAMPOS
                }

    etapas = {}
    for indice, turno in enumerate(ordem):
        nome = ETAPAS[indice] if indice < len(ETAPAS) else f"turno-{indice + 1}"
        etapas[nome] = {"turn_id": turno, **sessoes[turno]}
    total = {campo: sum(etapa.get("tokens", {}).get(campo, 0) for etapa in etapas.values()) for campo in CAMPOS}
    return {"chat_id": identificador, "etapas": etapas, "total_tokens": total,
            "tempo_ativo_s": round(sum(etapa.get("duracao_s", 0) for etapa in etapas.values()), 1)}


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    resultado = medir(Path(sys.argv[1]))
    conteudo = json.dumps(resultado, ensure_ascii=False, indent=2) + "\n"
    if len(sys.argv) == 3:
        Path(sys.argv[2]).write_text(conteudo, encoding="utf-8")
    else:
        print(conteudo)
