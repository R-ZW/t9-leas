"""Mede tokens e tempo de uma cadeia da T9 a partir da transcrição do Claude Code.

Uso: python medir_cadeia.py <agent-*.jsonl> <pasta-de-saida> [--chave-env ARQUIVO]

Lê a transcrição do agente (subagents/agent-<id>.jsonl), divide em etapas pelos
prompts enviados pela sessão orquestradora (A, B1, E, B2, nessa ordem) e grava:
  - medicoes.json  tokens, tempo, chamadas de ferramenta e comandos por etapa;
  - transcricao.md prompts, respostas finais e todas as chamadas de ferramenta,
                   na ordem, com o valor da chave VirusTotal trocado por <VT_API_KEY>;
  - auditoria.md   caminhos lidos ou citados fora das pastas permitidas.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ETAPAS = ["A", "B1", "E", "B2"]
# Início fixo de cada prompt (prompts/prompt-*.txt). Outras mensagens de usuário, como
# avisos de tarefa em segundo plano do Claude Code, não abrem etapa nova.
INICIOS = ("Atue como revisor", "Com base no mesmo material", "Agora execute você mesmo", "Leia o registro factual")


def carregar(caminho):
    with open(caminho, encoding="utf-8") as f:
        return [json.loads(linha) for linha in f if linha.strip()]


def eh_prompt(reg):
    """Mensagem de usuário com texto (prompt da etapa), não resultado de ferramenta."""
    if reg.get("type") != "user":
        return False
    conteudo = (reg.get("message") or {}).get("content")
    if isinstance(conteudo, list) and any(isinstance(c, dict) and c.get("type") == "tool_result" for c in conteudo):
        return False
    return sem_moldura(texto(conteudo or "")).startswith(INICIOS)


# O Claude Code entrega ao agente as mensagens enviadas com SendMessage (B1, E, B2) com esta moldura.
MOLDURA = "The coordinator sent a message while you were working:"


def sem_moldura(t):
    t = t.lstrip()
    return t[len(MOLDURA):].lstrip() if t.startswith(MOLDURA) else t


def texto(conteudo):
    if isinstance(conteudo, str):
        return conteudo
    return "\n".join(c.get("text", "") for c in conteudo if isinstance(c, dict) and c.get("type") == "text")


def ts(reg):
    return datetime.fromisoformat(reg["timestamp"].replace("Z", "+00:00"))


def dividir(registros):
    """Lista de (prompt, [registros da etapa]). Prompts repetidos em sequência viram um só."""
    etapas = []
    for reg in registros:
        if eh_prompt(reg):
            t = texto(reg["message"]["content"]).strip()  # com a moldura, como o agente recebeu
            if etapas and not any(r.get("type") == "assistant" for r in etapas[-1][1]) and t == etapas[-1][0]["texto"]:
                continue
            etapas.append(({"texto": t, "ts": ts(reg)}, []))
        elif etapas:
            etapas[-1][1].append(reg)
    return etapas


def medir(prompt, regs):
    # Uma resposta da API chega em vários registros com o mesmo id; vale o último.
    por_id = {}
    for r in regs:
        if r.get("type") == "assistant":
            m = r["message"]
            por_id[m.get("id") or id(r)] = r
    soma = {"entrada": 0, "saida": 0, "cache_criado": 0, "cache_lido": 0}
    for r in por_id.values():
        u = r["message"].get("usage") or {}
        soma["entrada"] += u.get("input_tokens", 0)
        soma["saida"] += u.get("output_tokens", 0)
        soma["cache_criado"] += u.get("cache_creation_input_tokens", 0)
        soma["cache_lido"] += u.get("cache_read_input_tokens", 0)
    soma["total"] = sum(soma.values())
    ferramentas, docker_exec = {}, 0
    for r in regs:
        if r.get("type") != "assistant":
            continue
        for c in r["message"].get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                ferramentas[c["name"]] = ferramentas.get(c["name"], 0) + 1
                cmd = (c.get("input") or {}).get("command", "")
                docker_exec += len(re.findall(r"\bdocker\s+exec\b", cmd))
    # Contagem por chamada: o mesmo tool_use aparece uma vez por registro.
    ultimos = [r for r in regs if r.get("type") == "assistant"]
    fim = max((ts(r) for r in ultimos), default=prompt["ts"])
    modelos = sorted({r["message"].get("model") for r in por_id.values() if r["message"].get("model")})
    return {
        "inicio_utc": prompt["ts"].isoformat(),
        "fim_utc": fim.isoformat(),
        "duracao_s": round((fim - prompt["ts"]).total_seconds(), 1),
        "respostas_api": len(por_id),
        "tokens": soma,
        "chamadas_ferramenta": ferramentas,
        "comandos_docker_exec": docker_exec,
        "modelos": modelos,
    }


def ocultar(s, chave):
    return s.replace(chave, "<VT_API_KEY>") if chave else s


def caminhos_citados(regs):
    for r in regs:
        if r.get("type") != "assistant":
            continue
        for c in r["message"].get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                inp = c.get("input") or {}
                for campo in ("file_path", "path", "notebook_path"):
                    if inp.get(campo):
                        yield c["name"], inp[campo]
                if inp.get("command"):
                    for p in re.findall(r"(?<![A-Za-z])[A-Za-z]:[\\/][^\s'\"|;&]+|(?<![\w:/])/(?:c|d)/[^\s'\"|;&]+", inp["command"]):
                        yield c["name"], p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcricao")
    ap.add_argument("saida")
    ap.add_argument("--chave-env", help="arquivo .env com VT_API_KEY, para ocultar o valor")
    ap.add_argument("--permitido", action="append", default=[], help="prefixo de caminho permitido (repetível)")
    a = ap.parse_args()

    chave = None
    if a.chave_env:
        for linha in Path(a.chave_env).read_text(encoding="utf-8").splitlines():
            if linha.startswith("VT_API_KEY="):
                chave = linha.split("=", 1)[1].strip()

    regs = carregar(a.transcricao)
    etapas = dividir(regs)
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)

    medicoes = {"transcricao": Path(a.transcricao).name, "etapas": {}}
    md = ["# Transcrição da cadeia", "", f"Fonte: `{Path(a.transcricao).name}` (Claude Code). "
          "Prompts e respostas finais sem alteração; a chave VirusTotal aparece como `<VT_API_KEY>`.", ""]
    for i, (prompt, rs) in enumerate(etapas):
        nome = ETAPAS[i] if i < len(ETAPAS) else f"extra-{i - len(ETAPAS) + 1}"
        medicoes["etapas"][nome] = medir(prompt, rs)
        md += [f"## Etapa {nome}", "", f"**Prompt** ({prompt['ts'].isoformat()}):", "", "```text",
               ocultar(prompt["texto"], chave), "```", ""]
        md += ["### Chamadas de ferramenta", ""]
        vistos = set()
        for r in rs:
            if r.get("type") != "assistant":
                continue
            for c in r["message"].get("content") or []:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c["id"] not in vistos:
                    vistos.add(c["id"])
                    md.append(f"- `{r['timestamp']}` **{c['name']}** `{ocultar(json.dumps(c.get('input'), ensure_ascii=False), chave)[:600]}`")
        # A resposta final do agente é a mensagem do SubagentHandback; sem ela, o último texto.
        entregas = [c["input"]["message"] for r in rs if r.get("type") == "assistant"
                    for c in r["message"].get("content") or []
                    if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "SubagentHandback"
                    and (c.get("input") or {}).get("message")]
        finais = [r for r in rs if r.get("type") == "assistant" and texto(r["message"].get("content") or []).strip()]
        if entregas:
            resposta = entregas[-1]
        else:
            resposta = texto(finais[-1]["message"]["content"]) if finais else "(sem resposta de texto)"
        md += ["", "### Resposta final", "", ocultar(resposta, chave), ""]
        (saida / f"resposta-{nome}.md").write_text(ocultar(resposta, chave), encoding="utf-8")

    tot = {k: sum(e["tokens"][k] for e in medicoes["etapas"].values()) for k in ("entrada", "saida", "cache_criado", "cache_lido", "total")}
    medicoes["total"] = {"tokens": tot, "duracao_s": round(sum(e["duracao_s"] for e in medicoes["etapas"].values()), 1)}
    (saida / "medicoes.json").write_text(json.dumps(medicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    (saida / "transcricao.md").write_text("\n".join(md), encoding="utf-8")

    fora = sorted({(n, p) for _, rs in etapas for n, p in caminhos_citados(rs)
                   if not any(p.replace("/", "\\").lower().startswith(x.replace("/", "\\").lower()) for x in a.permitido)})
    aud = ["# Auditoria de acesso", "", "Caminhos citados em chamadas de ferramenta fora dos prefixos permitidos:", ""]
    aud += [f"- {n}: `{p}`" for n, p in fora] or ["- nenhum"]
    (saida / "auditoria.md").write_text("\n".join(aud) + "\n", encoding="utf-8")
    json.dump(medicoes["total"], sys.stdout, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
