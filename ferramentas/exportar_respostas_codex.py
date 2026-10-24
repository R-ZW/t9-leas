"""Salva as respostas finais dos quatro turnos de uma cadeia Codex.

Uso: python ferramentas/exportar_respostas_codex.py <rollout.jsonl> <pasta-cadeia>

Exporta somente `last_agent_message` dos eventos de conclusão. O valor de
VT_API_KEY, caso esteja no ambiente do processo, é substituído por marcador.
"""

import json
import os
import sys
from pathlib import Path


ETAPAS = ("A", "B1", "E", "B2")


def exportar(origem, destino):
    respostas = []
    for linha in origem.open(encoding="utf-8"):
        registro = json.loads(linha)
        if registro.get("type") == "event_msg" and registro.get("payload", {}).get("type") == "task_complete":
            resposta = registro["payload"].get("last_agent_message") or ""
            if resposta.strip():
                respostas.append(resposta)
    chave = os.environ.get("VT_API_KEY")
    destino.mkdir(parents=True, exist_ok=True)
    for etapa, resposta in zip(ETAPAS, respostas):
        if chave:
            resposta = resposta.replace(chave, "<VT_API_KEY>")
        (destino / f"resposta-{etapa}.md").write_text(resposta.rstrip() + "\n", encoding="utf-8")
    return len(respostas)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(f"{exportar(Path(sys.argv[1]), Path(sys.argv[2]))} respostas exportadas")
