"""Exporta prompts, chamadas de ferramenta e respostas finais de um chat Codex.

Uso: python ferramentas/exportar_transcricao_codex.py <agente.jsonl> <saida.md> <raiz-repo> <numero-cadeia>

Resultados de ferramentas não são copiados: os arquivos de evidência da cadeia
guardam as saídas relevantes. O script não exporta mensagens de sistema,
desenvolvedor ou raciocínio interno.
"""

import json
import os
import sys
from pathlib import Path


ETAPAS = ("A", "B1", "E interrompida", "E retomada", "B2")


def texto_mensagem(item):
    return "\n".join(
        parte.get("text", "")
        for parte in item.get("content", [])
        if parte.get("type") in ("input_text", "output_text")
    )


def prompts_base(raiz, numero):
    cadeia = raiz / "llm-openai" / f"cadeia-{numero}"
    pacote = str(cadeia / "pacote")
    execucao = str(cadeia / "execucao")
    conteiner = f"t9-openai-c{numero}"
    def ler(nome):
        return (raiz / "prompts" / f"prompt-{nome}.txt").read_text(encoding="utf-8").strip()
    return [
        ler("A").replace("{PACOTE}", pacote),
        ler("B1"),
        ler("E").replace("{CONTEINER}", conteiner).replace("{EXEC_HOST}", execucao).replace("{PACOTE}", pacote),
        "Retomada da etapa E após interrupção por limite de uso; conferir evidências e continuar do último passo concluído.",
        ler("B2").replace("{EXEC_HOST}", execucao),
    ]


def exportar(origem, prompts):
    pendente = ""
    secoes = []
    atual = None
    for linha in origem.open(encoding="utf-8"):
        reg = json.loads(linha)
        dados = reg.get("payload") or {}
        tipo = reg.get("type")
        if tipo == "response_item" and dados.get("type") == "agent_message" and dados.get("author") == "/root":
            texto = texto_mensagem(dados)
            mensagem = texto.split("Payload:\n", 1)[-1].strip()
            if atual is not None and not atual["prompt"]:
                atual["prompt"] = mensagem
            else:
                pendente = mensagem
        elif tipo == "event_msg" and dados.get("type") == "task_started":
            nome = ETAPAS[len(secoes)] if len(secoes) < len(ETAPAS) else f"turno {len(secoes) + 1}"
            atual = {"nome": nome, "inicio": reg["timestamp"], "prompt": pendente, "chamadas": []}
            secoes.append(atual)
            pendente = ""
        elif tipo == "response_item" and atual is not None:
            if dados.get("type") == "custom_tool_call":
                atual["chamadas"].append((reg["timestamp"], dados.get("name", ""), str(dados.get("input", ""))))
            elif dados.get("type") == "function_call":
                nome = f"{dados.get('namespace', '')}.{dados.get('name', '')}".strip(".")
                atual["chamadas"].append((reg["timestamp"], nome, str(dados.get("arguments", ""))))
        if tipo == "event_msg" and dados.get("type") == "task_complete" and atual is not None:
            atual["fim"] = reg["timestamp"]
            atual["resposta"] = dados.get("last_agent_message") or ""
            atual = None

    partes = [f"# Transcrição da cadeia Codex\n\nFonte: `{origem.name}`. As chamadas de ferramenta e respostas finais vêm do JSONL. Os prompts base abaixo foram reconstruídos dos arquivos congelados com os caminhos da cadeia; o JSONL cifra as mensagens de orquestração, então esta não é uma transcrição byte a byte dessas mensagens. Os resultados de ferramentas estão nos arquivos de evidência.\n"]
    for indice, secao in enumerate(secoes):
        if indice < len(prompts):
            secao["prompt"] = prompts[indice]
        partes.append(f"\n## Etapa {secao['nome']}\n\n**Prompt base** ({secao['inicio']}):\n\n~~~text\n{secao['prompt']}\n~~~\n")
        partes.append("\n### Chamadas de ferramenta\n")
        if not secao["chamadas"]:
            partes.append("\nNenhuma.\n")
        for instante, nome, argumento in secao["chamadas"]:
            partes.append(f"\n**{instante} — {nome}**\n\n~~~text\n{argumento}\n~~~\n")
        resposta = secao.get("resposta", "")
        partes.append("\n### Resposta final\n\n" + (resposta.strip() or "Turno interrompido sem resposta final.") + "\n")
    conteudo = "".join(partes)
    chave = os.environ.get("VT_API_KEY")
    return conteudo.replace(chave, "<VT_API_KEY>") if chave else conteudo


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    prompts = prompts_base(Path(sys.argv[3]), int(sys.argv[4]))
    Path(sys.argv[2]).write_text(exportar(Path(sys.argv[1]), prompts), encoding="utf-8")
