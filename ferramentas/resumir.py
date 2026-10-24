"""Junta decisões, tokens e tempo das cadeias de um provedor em analise/resumo.md.

Uso: python resumir.py <pasta llm-provedor> <arquivo de saída .md>
Lê, em cada cadeia-N/, medicoes.json e o último bloco JSON de resposta-A.md e resposta-B2.md.
"""
import json
import re
import sys
from pathlib import Path


def ultimo_json(texto):
    """Último objeto JSON com chaves F e R no texto."""
    melhor = None
    for m in re.finditer(r"\{", texto):
        prof = 0
        for i in range(m.start(), len(texto)):
            if texto[i] == "{":
                prof += 1
            elif texto[i] == "}":
                prof -= 1
                if prof == 0:
                    try:
                        obj = json.loads(texto[m.start():i + 1])
                    except json.JSONDecodeError:
                        break
                    if isinstance(obj, dict) and "F" in obj and "R" in obj:
                        melhor = obj
                    break
    return melhor


def fmt_min(s):
    return f"{s / 60:.1f}".replace(".", ",")


def main():
    base, saida = Path(sys.argv[1]), Path(sys.argv[2])
    cadeias = sorted(p for p in base.glob("cadeia-*") if p.is_dir())
    dec, med = [], []
    for c in cadeias:
        a = ultimo_json((c / "resposta-A.md").read_text(encoding="utf-8"))
        b = ultimo_json((c / "resposta-B2.md").read_text(encoding="utf-8"))
        m = json.loads((c / "medicoes.json").read_text(encoding="utf-8"))
        dec.append((c.name, a, b))
        med.append((c.name, m))

    l = ["# Resumo — " + base.name, "", "Gerado por `ferramentas/resumir.py` a partir de `resposta-A.md`, `resposta-B2.md` e `medicoes.json` de cada cadeia.", ""]
    l += ["## Decisões", "", "| Cadeia | F (A) | F (B2) | R (A) | R (B2) | C1–C6 no B2 |", "|---|---|---|---|---|---|"]
    for nome, a, b in dec:
        pr = b["R"].get("por_reivindicacao", {}) if b else {}
        abrev = {"reproduzivel": "rep", "nao_reproduzivel": "não rep", "depende_execucao": "dep. exec"}
        l.append(f"| {nome} | {a['F']['decisao']} ({a['F']['confianca']}) | {b['F']['decisao']} ({b['F']['confianca']}) | "
                 f"{a['R']['decisao']} ({a['R']['confianca']}) | {b['R']['decisao']} ({b['R']['confianca']}) | "
                 + ", ".join(f"{k}: {abrev.get(v, v)}" for k, v in pr.items()) + " |")
    l += ["", "Entre parênteses, a confiança (0–100) de que o comitê atribuiu o selo.", ""]

    l += ["## Tokens e tempo por etapa", "",
          "| Cadeia | Etapa | Tempo (min) | Saída | Entrada | Cache criado | Cache lido | Total | Respostas da API | `docker exec` |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for nome, m in med:
        for et, v in m["etapas"].items():
            t = v["tokens"]
            l.append(f"| {nome} | {et} | {fmt_min(v['duracao_s'])} | {t['saida']:,} | {t['entrada']:,} | {t['cache_criado']:,} | "
                     f"{t['cache_lido']:,} | {t['total']:,} | {v['respostas_api']} | {v['comandos_docker_exec']} |".replace(",", "."))
        t = m["total"]["tokens"]
        l.append(f"| **{nome}** | **total** | **{fmt_min(m['total']['duracao_s'])}** | **{t['saida']:,}** | {t['entrada']:,} | "
                 f"{t['cache_criado']:,} | {t['cache_lido']:,} | **{t['total']:,}** | | |".replace(",", "."))

    l += ["", "## Médias por etapa (3 cadeias)", "", "| Etapa | Tempo médio (min) | Saída média | Total médio |", "|---|---|---|---|"]
    for et in ("A", "B1", "E", "B2"):
        vs = [m["etapas"][et] for _, m in med if et in m["etapas"]]
        if vs:
            n = len(vs)
            l.append(f"| {et} | {fmt_min(sum(v['duracao_s'] for v in vs) / n)} | {round(sum(v['tokens']['saida'] for v in vs) / n):,} | "
                     f"{round(sum(v['tokens']['total'] for v in vs) / n):,} |".replace(",", "."))
    l += ["", "Tempo: do envio do prompt até a última resposta do agente na etapa. Tokens: soma das respostas da API do agente "
          "(entrada sem cache, saída, criação e leitura de cache). Não inclui a sessão orquestradora.", ""]
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("\n".join(l), encoding="utf-8")
    print("\n".join(l))


if __name__ == "__main__":
    main()
