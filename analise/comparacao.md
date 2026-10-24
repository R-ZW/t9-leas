# Comparação das três LLMs — T9, Foremost-NG

Escrita em 24/10/2026, depois de publicadas as nove cadeias (3 por LLM). Fontes: `resposta-A.md`, `resposta-B2.md`, `medicoes.json`, `execucao/registro-factual.md` e `LEIA-ME.md` de cada provedor, além dos resumos [`resumo-claude.md`](resumo-claude.md), [`resumo-openai.md`](resumo-openai.md) e [`resumo-gemini.md`](resumo-gemini.md). Selos oficiais do Foremost-NG: **F e R atribuídos**, conforme registrado na T8 ([R-ZW/t8-leas](https://github.com/R-ZW/t8-leas), `runs/foremost-ng/referencia/`). Nenhuma LLM teve acesso a eles.

## 1. Configuração de cada LLM

| | Claude | GPT | Gemini |
|---|---|---|---|
| Responsável | Eduardo | Reinaldo | Miguel |
| Interface | Claude Code (agente por cadeia) | Codex (agente por cadeia) | Antigravity (subagente por cadeia) |
| Modelo registrado | `claude-opus-5-5` | `gpt-6-sol` | `Gemini 3.8 Flash` (`gemini-3.8-flash`) |
| Nível de raciocínio | High | xhigh | High |
| Coleta (UTC, 24/10) | 15:31–16:07 | a partir de 17:08, com pausa por limite de uso na etapa E | 16:44–17:13 |
| Pasta de trabalho da LLM | fora do repositório | **dentro** do repositório (`t9-leas\llm-openai\cadeia-N`) | fora do repositório |

## 2. Decisões

Confiança entre parênteses: chance, segundo a LLM, de o comitê ter atribuído o selo (0–100).

| LLM | Cadeia | F em A | F em B2 | R em A | R em B2 | C1–C6 em B2 |
|---|---|---|---|---|---|---|
| Claude | 1 | Não atribuir (60) | Não atribuir (70) | Não atribuir (20) | Não atribuir (15) | N N N N N N |
| Claude | 2 | Não atribuir (60) | Não atribuir (75) | Não atribuir (25) | Não atribuir (25) | D D N D D N |
| Claude | 3 | Não atribuir (55) | **Atribuir** (75) | Não atribuir (15) | Não atribuir (8) | R R N R R N |
| GPT | 1 | Não atribuir (15) | Não atribuir (25) | Não atribuir (3) | Não atribuir (1) | D N N N D N |
| GPT | 2 | Não atribuir (15) | Não atribuir (25) | Não atribuir (3) | Não atribuir (1) | N N N D D N |
| GPT | 3 | Não atribuir (20) | Não atribuir (30) | Não atribuir (5) | Não atribuir (1) | D N N N D N |
| Gemini | 1 | Indeterminado (80) | **Atribuir** (95) | Não atribuir (15) | Não atribuir (95)\* | R R R R R N |
| Gemini | 2 | Indeterminado (80) | **Atribuir** (100) | Não atribuir (20) | Não atribuir (10) | R R N R R N |
| Gemini | 3 | Indeterminado (85) | **Atribuir** (95) | Não atribuir (10) | Não atribuir (5) | R R R R R N |

R = reproduzível, N = não reproduzível, D = depende de execução. \* ver inconsistência 2.

### Métricas

| Medida | Claude | GPT | Gemini |
|---|---|---|---|
| Coincidência com o oficial em A (F+R, 6 decisões) | 0/6 | 0/6 | 0/6 |
| Coincidência com o oficial em B2 | 1/6 (F da cadeia 3) | 0/6 | 3/6 (F nas três) |
| Estabilidade em B2 (mesma decisão nas 3 cadeias) | F 2/3, R 3/3 | F 3/3, R 3/3 | F 3/3, R 3/3 |
| Transição de F de A para B2 | confirma, confirma, **contradiz** (N→A) | confirma ×3 | resolve incerteza ×3 (I→A) |
| Transição de R de A para B2 | confirma ×3 | confirma ×3 | confirma ×3 |

- **Total:** 0/18 decisões coincidem com o oficial em A e 4/18 em B2, todas no F.
- **R:** as nove cadeias negaram R nas duas etapas.
- **F em B2:** as LLMs discordam entre si. A moda é Não atribuir no Claude e no GPT e Atribuir no Gemini.
- **Primeira contradição A→B do estudo:** a cadeia 3 do Claude. Na T8, nenhuma transição contradisse a etapa A.

## 3. Causas das decisões

### Selo F: o mesmo fato, três leituras do critério

As nove execuções observaram o mesmo:
- o artefato compila em `src/` e instala com `sudo make install` usando as dependências do Dockerfile;
- `-h`, `-V` e `man` funcionam;
- uma extração mínima gera `audit.txt`.

A divergência está em como cada LLM aplica a frase "o README deve informar dependências, versões … e pelo menos um exemplo mínimo" ([`instrucoes-oficiais.md`](../pacote/instrucoes-oficiais.md)).

| Leitura | Quem | Efeito |
|---|---|---|
| **Critério documental obrigatório, aplicado ao pé da letra.** Faltam versões e um exemplo mínimo completo no README; a execução não muda isso | GPT 1–3; Claude 1 (também conta dependências só no Dockerfile e exemplos do manual sem dado) | Não atribuir, já em A |
| **Obrigatório, mas o manual citado pelo README supre o exemplo.** Sobra só a falta de versões, que ainda decide | Claude 2 | Não atribuir |
| **Falta de versões é lacuna parcial e não impeditiva**, porque os pacotes compilaram sem ajuste | Claude 3 (a própria resposta diz que a leitura estrita levaria a Não atribuir) | Atribuir |
| **F é funcional: o que importa é executar.** Em A, marcou versões e exemplo mínimo como "não atendido", mas decidiu Indeterminado porque "ler código não é prova". Em B2, decidiu Atribuir porque executou, sem voltar às lacunas do README | Gemini 1–3 | Indeterminado → Atribuir |

A confiança mostra a mesma divisão. O GPT acha improvável que o comitê tenha dado F (25–30). O Claude acha provável (70–75), embora negue o selo. O Gemini quase certo (95–100).

O oficial é Atribuir. Então a leitura mais estrita do critério (GPT e Claude 1–2) é a que mais se afasta do comitê. É a mesma causa de divergência da T8.

### Selo R: unânime, por motivos que se somam

1. **C6 sem dado:** `evidence2.dd` não existe em lugar nenhum. As nove cadeias citam isso, e a regra do prompt dá exatamente esse caso como exemplo de Não atribuir.
2. **Documentação de reprodução:** Claude e GPT apontam que o README não traz instruções por reivindicação nem o processo dos autores.
3. **Defeitos observados na execução** (só Claude e GPT os usam como argumento):

| Fato observado | Claude | GPT | Gemini |
|---|---|---|---|
| Mach-O thin não é extraído (comparação de bytes invertida) | 3/3 | 3/3 | cadeias 1 e 2; a cadeia 3 só testou fat |
| Script só com comentários é extraído | 3/3 | 3/3 | cadeias 1 e 2; a cadeia 3 usou um controle só com `#`, que não dispara o defeito |
| ELF sai sem a tabela de seções | 3/3 | 3/3 | observado, mas tratado como "conforme projetado" |
| Sem chave, o VirusTotal anota "Clean (0)" | 3/3 | 3/3 | registrado, sem comentário |
| Com chave válida, o rótulo bate com a API (EICAR malicioso) | 3/3 | cadeias 1 e 3 | só hash desconhecido (404 → "Clean (0)"); a cadeia 1 consultou o EICAR direto na API, fora do artefato |

O rótulo de C1–C5 varia porque os testes usaram entradas do revisor (D2/D3), e o prompt manda tratá-las como complementares:
- **Claude:** dividido. A cadeia 1 marcou não reproduzível, a 2 depende de execução e a 3 reproduzível.
- **GPT:** marcou C2 e C3 como não reproduzíveis.
- **Gemini:** marcou quase tudo reproduzível, até C3 nas cadeias 1 e 3.

Nenhuma dessas diferenças mudou R, porque C6 decide sozinho.

## 4. Custo

Totais comparáveis entre os três: tokens processados = entrada (inclusive cache) + saída. O GPT informa a entrada já com o cache, e Claude e Gemini informam as parcelas separadas, que aqui foram somadas. O tempo é o de atividade do agente. No GPT, ele não inclui a pausa por limite de uso.

| Média por cadeia | Claude | GPT | Gemini |
|---|---|---|---|
| Tempo | 28,6 min | 23,4 min | 24,5 min |
| Tokens de saída | 108.382 | 74.462 | 117.286 |
| Tokens processados | 14,3 mi | 13,1 mi | 14,4 mi |
| Parcela de cache nos processados | 94–97% | 97–98% | 95–97% |
| Etapa E: parte do tempo / dos tokens | 58% / 81% | 65% / 77% | 62% / 85% |

| Média por etapa (tempo · saída · processados) | Claude | GPT | Gemini |
|---|---|---|---|
| A | 4,6 min · 24,9 mil · 1,97 mi | 4,3 min · 14,4 mil · 2,26 mi | 5,9 min · 36,4 mil · 1,21 mi |
| B1 | 5,9 min · 35,4 mil · 0,23 mi | 2,4 min · 11,0 mil · 0,11 mi | 2,0 min · 27,1 mil · 0,30 mi |
| E | 16,6 min · 38,7 mil · 11,6 mi | 15,3 min · 42,9 mil · 10,1 mi | 15,3 min · 42,0 mil · 12,2 mi |
| B2 | 1,6 min · 9,5 mil · 0,51 mi | 1,3 min · 6,3 mil · 0,66 mi | 1,3 min · 11,8 mil · 0,70 mi |

O GPT foi o mais econômico em saída (cerca de 30% menos que os outros), principalmente em A e B1, que tiveram respostas mais curtas. Os três gastaram parecido na execução. Nenhum valor inclui as sessões orquestradoras. O GPT mediu a dele à parte, em [`llm-openai/medicoes-orquestrador.json`](../llm-openai/medicoes-orquestrador.json).

## 5. Inconsistências encontradas

Nenhum arquivo dos colegas foi alterado; os itens abaixo ficam registrados para correção ou declaração no relatório.

1. **Modelo e nível do Gemini confirmados.** Miguel confirmou em `llm-google/LEIA-ME.md` e `medicoes.json` o uso de `Gemini 3.8 Flash` (`gemini-3.8-flash`) com nível de raciocínio `High` (`thinking` ativo em todas as respostas de todas as etapas).
2. **Confiança de R na cadeia 1 do Gemini.** Em B2, a cadeia 1 decide Não atribuir com confiança 95. Pela definição do prompt, isso seria "95% de chance de o comitê ter atribuído R". O próprio texto da resposta mostra que ela usou o número como confiança na própria decisão. Em A, o valor era 15, e as cadeias 2 e 3 deram 10 e 5. Esse valor não deve entrar em médias de confiança.
3. **C3 da cadeia 1 do Gemini contradiz o próprio registro.** A cadeia 1 registra que o thin não foi extraído, mas marca C3 como reproduzível (pelo sucesso no Mach-O FAT universal `0xCAFEBABE`). O LEIA-ME do Gemini foi corrigido: apenas a cadeia 2 rotulou C3 formalmente como `nao_reproduzivel`.
4. **Testes diferentes na cadeia 3 do Gemini.** Ela não testou Mach-O thin. O controle de comentários usou só `#`, sem letras. O ELF foi checado só com `readelf -h`. Por isso ela não viu três defeitos que as outras oito cadeias viram. O LEIA-ME generaliza ("todas comprovaram … integridade estrutural").
5. **Regra de F no Gemini.** Em A, as três cadeias do Gemini classificaram versões e exemplo mínimo como "não atendido" no README. Mesmo assim decidiram Indeterminado, e a regra do prompt manda Não atribuir quando um critério obrigatório falha na documentação. Em B2, dizem que o artefato "atende plenamente", sem voltar a essas lacunas.
6. **Isolamento do GPT.** As pastas de trabalho dos agentes do GPT ficaram dentro do repositório (`…\t9-leas\llm-openai\cadeia-N`). A cópia local partiu do commit `723be8f`, que já tinha os resultados do Claude em `llm-anthropic/`. A auditoria do Reinaldo não encontrou referências a `llm-anthropic`, `t8-leas` nem às outras cadeias. Ainda assim, o isolamento é mais fraco que o do Claude e o do Gemini, que trabalharam fora do repositório. Deve constar como desvio.
7. **Prompts do GPT com texto a mais.** As mensagens A e B1 também identificaram a cadeia e pediram a entrega da resposta no chat. A etapa E foi interrompida pelo limite de uso e retomada com uma mensagem extra. Além disso, as mensagens do orquestrador vêm cifradas no log do Codex, então a transcrição do GPT reconstrói os prompts a partir dos arquivos congelados e não é literal. Tudo isso está declarado no LEIA-ME do GPT.
8. **Moldura nos prompts do Claude.** O Claude Code entregou B1, E e B2 com o prefixo "The coordinator sent a message while you were working:", e por isso os roteiros B1 do Claude falam em coordenador. Isso está declarado em `llm-anthropic/LEIA-ME.md`.
9. **Níveis de raciocínio diferentes:** Claude High, GPT xhigh e Gemini High. Como na T8, a comparação é de "produto + modelo + nível".
10. **Formatos de medição diferentes.** O GPT soma o cache dentro da entrada. O Gemini não informa cache criado. O tempo do GPT exclui a pausa. A seção 4 normaliza os totais, mas os campos de `medicoes.json` não têm o mesmo significado entre provedores.
11. **Imagem Docker reconstruída por provedor.** O ID do Gemini é `sha256:97726f4c…` e o do Claude é `sha256:31c85217…`. O GPT não registrou o ID. Todas vêm do mesmo Dockerfile, com o apt fixado no mesmo dia, então a diferença de ID deve vir só da data de construção. O conteúdo não foi comparado.

## 6. Conclusões

- **R:** quando cada LLM executa o próprio roteiro, a decisão é unânime e firme (9/9 Não atribuir). Ela se apoia na falta da `evidence2.dd` e, no Claude e no GPT, em defeitos reais observados (Mach-O thin, filtro de comentários). O comitê deu R. A divergência vem do insumo indisponível e dos defeitos, que um comitê pode não ter testado.
- **F:** depende da leitura do critério documental, não da execução. Todas as execuções funcionaram, e mesmo assim as decisões vão de Não atribuir (GPT) a Atribuir (Gemini). Essa é a principal fonte de divergência entre provedores, a mesma da T8.
- **Rigor dos testes:** quem testou mais casos negativos (Claude e GPT) achou mais defeitos e foi mais estrito no R. A cadeia 3 do Gemini, com testes mais brandos, não viu três defeitos.
- **Custo:** semelhante entre provedores, entre 13 e 14 milhões de tokens processados e de 23 a 29 minutos por cadeia. A etapa E concentra cerca de 80% dos tokens.
