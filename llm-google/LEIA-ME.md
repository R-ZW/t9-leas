# Gemini — cadeias da T9 (Foremost-NG)

Responsável: Miguel Ângelo Bastos Muniz. Coleta em 24/10/2026, 16:44–17:13 UTC (13:44–14:13 em Brasília), com as três cadeias rodando em paralelo no Antigravity desktop. Resumo das decisões, tokens e tempo: [`../analise/resumo-gemini.md`](../analise/resumo-gemini.md).

## Configuração efetiva

| Campo | Valor |
|---|---|
| Interface | Antigravity (app desktop, Windows 11), subagente isolado `revisor-gemini-t9` lançado pela sessão orquestradora via `invoke_subagent` (A) e continuado com `send_message` (B1, E, B2), na mesma conversa |
| Modelo | `Gemini 3.8 Flash` (`gemini-3.8-flash`) em todas as respostas das três cadeias (campo `modelos` de `medicoes.json`) |
| Nível de raciocínio | `High` (`thinking` ativo em todas as respostas de todas as etapas) |
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
4. **Decisões sobre o Selo R.** Todas as três cadeias concordaram em `Não atribuir` tanto na etapa A quanto na etapa B2. O motivo determinante nas três execuções foi a indisponibilidade fática da imagem de 2 GB `evidence2.dd`, inviabilizando a reprodução da Figura 2 (C6).
5. **Classificação de C3 (Mach-O) no B2:** Apenas a **Cadeia 2** marcou C3 como `nao_reproduzivel`, pois constatou no código e no teste que o Mach-O thin de 64 bits falha devido a um bug de endianness (`src/extract.c:2408`). A **Cadeia 1**, apesar de documentar no texto que o Mach-O thin não foi extraído e notar a mesma divergência de endianness, marcou C3 como `reproduzivel` no bloco JSON considerando o sucesso na extração do Mach-O FAT universal (`0xCAFEBABE`). A **Cadeia 3** também marcou C3 como `reproduzivel` pela extração do FAT universal.
6. **Polaridade da confiança de R na Cadeia 1 (B2):** O prompt solicitava expressamente a confiança (0 a 100) de que o comitê oficial atribuiu o selo. Na Cadeia 1, o modelo reportou confiança `95` para a decisão `Não atribuir`, justificando no texto que sua convicção foi "elevada de 85% para 95% na certeza de que falta o dado", invertendo a polaridade e reportando confiança na sua própria decisão negativa. As Cadeias 2 e 3 responderam na polaridade esperada pelo comitê (`10` e `5`, respectivamente).
7. **Observações sobre os demais parsers:**
   - Em C1 (EVTX), as três cadeias observaram extração bem-sucedida baseada na assinatura `ElfFile\0\0` e chunks de 64 KiB.
   - Em C2 (scripts), observaram a extração com shebang `#!`, respeitando o tamanho mínimo de 32 bytes.
   - Em C4 (ELF), todas comprovaram a extração delimitada pelos cabeçalhos `PT_LOAD` com integridade estrutural validada por `readelf`.
   - Em C5 (VirusTotal), a consulta via HTTP REST com a variável `VT_API_KEY` funcionou nas três execuções preenchendo a coluna VT com `Clean (0)` ou diagnósticos de detecção, enquanto sem a chave o utilitário emitiu o aviso documentado e continuou o carving sem travamentos.
