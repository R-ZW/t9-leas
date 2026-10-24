# Gemini — cadeias da T9 (Foremost-NG)

Responsável: Miguel Ângelo Bastos Muniz. Coleta em 24/10/2026, 16:44–17:13 UTC (13:44–14:13 em Brasília), com as três cadeias rodando em paralelo no Antigravity desktop. Resumo das decisões, tokens e tempo: [`../analise/resumo-gemini.md`](../analise/resumo-gemini.md).

## Configuração efetiva

| Campo | Valor |
|---|---|
| Interface | Antigravity (app desktop, Windows 11), subagente isolado `revisor-gemini-t9` lançado pela sessão orquestradora via `invoke_subagent` (A) e continuado com `send_message` (B1, E, B2), na mesma conversa |
| Modelo | Gemini no Antigravity (com reasoning/thinking ativo) em todas as respostas das três cadeias |
| Ambiente de execução | imagem `t9/foremost-ng-exec:1` (`sha256:97726f4c1e83…`), um contêiner por cadeia (`t9-gemini-c1` a `c3`) |
| Registro factual congelado antes do B2 | `cadeia-N/registro-factual.sha256` |

## Arquivos de cada cadeia

| Arquivo | Conteúdo |
|---|---|
| `transcricao.md` | os quatro prompts como o subagente os recebeu, todas as chamadas de ferramenta (com horário) e a resposta final de cada etapa |
| `resposta-A.md`, `resposta-B1.md`, `resposta-E.md`, `resposta-B2.md` | a resposta final de cada etapa, sem alteração |
| `medicoes.json` | tokens (entrada, saída, cache lido e total), tempo, chamadas de ferramenta e comandos `docker exec` por etapa |
| `auditoria.md` | caminhos lidos ou citados em chamadas de ferramenta fora da pasta da cadeia |
| `execucao/` | o que o agente gravou na pasta de evidências: `registro-factual.md`, logs, scripts de teste e relatórios `audit.txt`. Imagens e binários compilados ficaram no contêiner |

As transcrições e respostas vêm dos registros oficiais do Antigravity (`transcript_full.jsonl`), processados pelo [`../ferramentas/medir_cadeia_gemini.py`](../ferramentas/medir_cadeia_gemini.py). A chave do VirusTotal não aparece em nenhum arquivo: a ferramenta troca o valor por `<VT_API_KEY>`, e a busca deu 0 ocorrências em todas as pastas de evidências.

## Desvios e observações

1. **Isolamento de contexto.** Cada subagente operou em conversa independente sem histórico da sessão orquestradora nem arquivos fora de sua respectiva pasta de trabalho (`D:\t9-trabalho\gemini-cN\`).
2. **Auditoria de acesso.** Nenhuma chamada de ferramenta acessou caminhos fora dos limites permitidos.
3. **Decisões sobre o Selo F.** Na etapa A, todas as três cadeias julgaram F como `Indeterminado` (confiança 80–85) devido ao critério oficial de que leitura documental não constitui prova de execução. Na etapa B2, após a compilação, instalação e observação empírica de carving com logs estruturados, as três cadeias convergiram em `Atribuir` (confiança 95–100).
4. **Decisões sobre o Selo R.** Todas as três cadeias concordaram em `Não atribuir` tanto na etapa A (confiança 10–20) quanto na etapa B2 (confiança 5–95). O motivo determinante nas três execuções foi a indisponibilidade fática da imagem de 2 GB `evidence2.dd`, inviabilizando a reprodução da Figura 2 (C6).
5. **Observações sobre parsers específicos:**
   - Em C1 (EVTX), as três cadeias observaram extração bem-sucedida baseada na assinatura `ElfFile\0\0` e chunks de 64 KiB.
   - Em C2 (scripts), observaram a extração com shebang `#!`, respeitando o tamanho mínimo de 32 bytes.
   - Em C3 (Mach-O), todas extraíram binários universais FAT (`0xCAFEBABE`), mas a Cadeia 2 e a Cadeia 1 identificaram no código-fonte uma falha de endianness na comparação do cabeçalho de binários Thin 64-bit (`src/extract.c:2408`), rotulando C3 como `nao_reproduzivel`.
   - Em C4 (ELF), todas comprovaram a extração delimitada pelos cabeçalhos `PT_LOAD` com integridade estrutural validada por `readelf`.
   - Em C5 (VirusTotal), a consulta via HTTP REST com a variável `VT_API_KEY` funcionou nas três execuções preenchendo a coluna VT com `Clean (0)` ou diagnósticos de detecção, enquanto sem a chave o utilitário emitiu o aviso documentado e continuou o carving sem travamentos.
