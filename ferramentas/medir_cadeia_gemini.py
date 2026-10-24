"""Mede tokens e tempo de uma cadeia da T9 a partir da transcrição do Antigravity (Gemini).

Uso: python medir_cadeia_gemini.py <conversation-id-ou-pasta> <pasta-de-saida> [--chave-env ARQUIVO] [--permitido PREFIXO]

Lê a transcrição do subagente do Antigravity (transcript_full.jsonl ou transcript.jsonl),
divide em etapas pelos prompts enviados (A, B1, E, B2, nessa ordem) e grava:
  - medicoes.json   tokens, tempo, chamadas de ferramenta e comandos por etapa;
  - transcricao.md  prompts, respostas finais e todas as chamadas de ferramenta,
                    com o valor da chave VirusTotal trocado por <VT_API_KEY>;
  - auditoria.md    caminhos lidos ou citados fora das pastas permitidas;
  - resposta-A.md, resposta-B1.md, resposta-E.md, resposta-B2.md.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ETAPAS = ["A", "B1", "E", "B2"]
INICIOS = (
    "Atue como revisor",
    "Com base no mesmo material",
    "Agora execute você mesmo",
    "Leia o registro factual"
)

BRAIN_BASE = Path(r"C:\Users\Usuario\.gemini\antigravity\brain")


def carregar_transcricao(origem: str):
    p = Path(origem)
    if not p.is_file():
        # Pode ser conversation-id
        c1 = BRAIN_BASE / origem / ".system_generated" / "logs" / "transcript_full.jsonl"
        c2 = BRAIN_BASE / origem / ".system_generated" / "logs" / "transcript.jsonl"
        if c1.exists():
            p = c1
        elif c2.exists():
            p = c2
        else:
            raise FileNotFoundError(f"Transcrição não encontrada em {origem}")
    
    with open(p, encoding="utf-8") as f:
        return [json.loads(linha) for linha in f if linha.strip()], p


def extrair_texto_prompt(content: str) -> str:
    """Extrai texto do prompt removendo eventuais tags de sistema ou molduras."""
    if not content:
        return ""
    # Se houver tag <SYSTEM_MESSAGE>, pega o conteúdo interno
    m = re.search(r"<SYSTEM_MESSAGE>(.*?)</SYSTEM_MESSAGE>", content, re.DOTALL)
    t = m.group(1).strip() if m else content.strip()
    # Se começar com [Message] ... content=...
    m_msg = re.search(r"content=(.*)$", t, re.DOTALL)
    if m_msg:
        t = m_msg.group(1).strip()
    return t


def eh_prompt_etapa(step):
    stype = step.get("type", "")
    if stype not in ("USER_INPUT", "SYSTEM_MESSAGE"):
        return False, ""
    raw = step.get("content", "") or ""
    t = extrair_texto_prompt(raw)
    for inicio in INICIOS:
        if inicio in t:
            # Encontra onde começa o prompt
            idx = t.find(inicio)
            return True, t[idx:]
    return False, ""


def ts(iso_str):
    if not iso_str:
        return datetime.now()
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))


def extrair_argumentos(tc):
    args = tc.get("args") or tc.get("arguments") or {}
    if isinstance(args, str):
        try:
            return json.loads(args)
        except Exception:
            return {"raw": args}
    return args


def dividir_em_etapas(steps):
    etapas = []
    for step in steps:
        is_p, p_text = eh_prompt_etapa(step)
        if is_p:
            p_time = ts(step.get("created_at"))
            etapas.append(({"texto": p_text, "ts": p_time}, []))
        elif etapas:
            etapas[-1][1].append(step)
    return etapas


def medir_etapa(prompt_info, steps):
    inicio = prompt_info["ts"]
    fim = inicio
    
    in_tok = 0
    out_tok = 0
    cache_read = 0
    respostas_api = 0
    ferramentas = {}
    docker_exec_count = 0
    modelos = set()
    
    for step in steps:
        stype = step.get("type")
        created = step.get("created_at")
        if created:
            cur_ts = ts(created)
            if cur_ts > fim:
                fim = cur_ts
                
        if stype == "PLANNER_RESPONSE":
            respostas_api += 1
            in_tok += step.get("input_tokens", 0)
            out_tok += step.get("output_tokens", 0)
            cache_read += step.get("cache_read_tokens", 0)
            
            for tc in step.get("tool_calls", []):
                tname = tc.get("name") or tc.get("tool_name") or "tool"
                ferramentas[tname] = ferramentas.get(tname, 0) + 1
                args = extrair_argumentos(tc)
                cmd = args.get("CommandLine") or args.get("command") or ""
                if cmd:
                    docker_exec_count += len(re.findall(r"\bdocker\s+exec\b", cmd))
    
    duracao_s = round((fim - inicio).total_seconds(), 1)
    tot_tok = in_tok + out_tok + cache_read
    
    tokens = {
        "entrada": in_tok,
        "saida": out_tok,
        "cache_criado": 0,
        "cache_lido": cache_read,
        "total": tot_tok
    }
    
    return {
        "inicio_utc": inicio.isoformat(),
        "fim_utc": fim.isoformat(),
        "duracao_s": duracao_s,
        "respostas_api": respostas_api,
        "tokens": tokens,
        "chamadas_ferramenta": ferramentas,
        "comandos_docker_exec": docker_exec_count,
        "modelos": ["Gemini 3.8 Flash (High)"]
    }


def extrair_resposta_final(steps):
    """Obtém a resposta final de texto ou mensagem entregue via send_message."""
    # Procura send_message
    for step in reversed(steps):
        if step.get("type") == "PLANNER_RESPONSE":
            for tc in step.get("tool_calls", []):
                tname = tc.get("name") or tc.get("tool_name")
                if tname == "send_message":
                    args = extrair_argumentos(tc)
                    msg = args.get("Message", "")
                    if msg.strip():
                        return msg.strip()
    
    # Se não houver send_message, pega o último content do PLANNER_RESPONSE
    for step in reversed(steps):
        if step.get("type") == "PLANNER_RESPONSE":
            c = step.get("content", "")
            if c and c.strip():
                return c.strip()
    return "(sem resposta de texto)"


def caminhos_citados(steps):
    for step in steps:
        if step.get("type") == "PLANNER_RESPONSE":
            for tc in step.get("tool_calls", []):
                tname = tc.get("name") or tc.get("tool_name") or "tool"
                args = extrair_argumentos(tc)
                for campo in ("Path", "file_path", "path", "AbsolutePath"):
                    if args.get(campo):
                        yield tname, str(args[campo])
                cmd = args.get("CommandLine") or args.get("command") or ""
                if cmd:
                    for p in re.findall(r"(?<![A-Za-z])[A-Za-z]:[\\/][^\s'\"|;&]+|(?<![\w:/])/(?:c|d)/[^\s'\"|;&]+", cmd):
                        yield tname, p


def ocultar(texto: str, chave: str) -> str:
    if not chave:
        return texto
    return texto.replace(chave, "<VT_API_KEY>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("origem", help="Caminho do transcript.jsonl ou ID da conversa no brain")
    ap.add_argument("saida", help="Pasta de saída da cadeia")
    ap.add_argument("--chave-env", help="Arquivo .env com VT_API_KEY")
    ap.add_argument("--permitido", action="append", default=[], help="Prefixos de caminho permitidos")
    a = ap.parse_args()

    chave = ""
    if a.chave_env and Path(a.chave_env).exists():
        for linha in Path(a.chave_env).read_text(encoding="utf-8").splitlines():
            if linha.startswith("VT_API_KEY="):
                chave = linha.split("=", 1)[1].strip()

    steps, file_path = carregar_transcricao(a.origem)
    etapas = dividir_em_etapas(steps)
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)

    medicoes = {"transcricao": file_path.name, "etapas": {}}
    md = [
        "# Transcrição da cadeia",
        "",
        f"Fonte: `{file_path.name}` (Antigravity Gemini). "
        "Prompts e respostas finais sem alteração; a chave VirusTotal aparece como `<VT_API_KEY>`.",
        ""
    ]

    for i, (prompt_info, st_steps) in enumerate(etapas):
        nome = ETAPAS[i] if i < len(ETAPAS) else f"extra-{i - len(ETAPAS) + 1}"
        medicoes["etapas"][nome] = medir_etapa(prompt_info, st_steps)
        
        md += [
            f"## Etapa {nome}",
            "",
            f"**Prompt** ({prompt_info['ts'].isoformat()}):",
            "",
            "```text",
            ocultar(prompt_info["texto"], chave),
            "```",
            ""
        ]
        
        md += ["### Chamadas de ferramenta", ""]
        vistos = set()
        for s in st_steps:
            if s.get("type") == "PLANNER_RESPONSE":
                for tc in s.get("tool_calls", []):
                    tc_id = tc.get("id") or str(tc)
                    if tc_id not in vistos:
                        vistos.add(tc_id)
                        tname = tc.get("name") or tc.get("tool_name")
                        args = extrair_argumentos(tc)
                        ts_str = s.get("created_at", "")
                        md.append(f"- `{ts_str}` **{tname}** `{ocultar(json.dumps(args, ensure_ascii=False), chave)[:600]}`")
        
        resp_final = extrair_resposta_final(st_steps)
        md += ["", "### Resposta final", "", ocultar(resp_final, chave), ""]
        (saida / f"resposta-{nome}.md").write_text(ocultar(resp_final, chave), encoding="utf-8")

    tot_tok = {
        k: sum(e["tokens"][k] for e in medicoes["etapas"].values())
        for k in ("entrada", "saida", "cache_criado", "cache_lido", "total")
    }
    medicoes["total"] = {
        "tokens": tot_tok,
        "duracao_s": round(sum(e["duracao_s"] for e in medicoes["etapas"].values()), 1)
    }

    (saida / "medicoes.json").write_text(json.dumps(medicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    (saida / "transcricao.md").write_text("\n".join(md), encoding="utf-8")

    fora = sorted({
        (n, p) for _, rs in etapas for n, p in caminhos_citados(rs)
        if not any(p.replace("/", "\\").lower().startswith(x.replace("/", "\\").lower()) for x in a.permitido)
    })
    aud = ["# Auditoria de acesso", "", "Caminhos citados em chamadas de ferramenta fora dos prefixos permitidos:", ""]
    aud += [f"- {n}: `{p}`" for n, p in fora] or ["- nenhum"]
    (saida / "auditoria.md").write_text("\n".join(aud) + "\n", encoding="utf-8")

    print(json.dumps(medicoes["total"], ensure_ascii=False))


if __name__ == "__main__":
    main()
