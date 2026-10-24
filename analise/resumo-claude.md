# Resumo — llm-anthropic

Gerado por `ferramentas/resumir.py` a partir de `resposta-A.md`, `resposta-B2.md` e `medicoes.json` de cada cadeia.

## Decisões

| Cadeia | F (A) | F (B2) | R (A) | R (B2) | C1–C6 no B2 |
|---|---|---|---|---|---|
| cadeia-1 | Não atribuir (60) | Não atribuir (70) | Não atribuir (20) | Não atribuir (15) | C1: não rep, C2: não rep, C3: não rep, C4: não rep, C5: não rep, C6: não rep |
| cadeia-2 | Não atribuir (60) | Não atribuir (75) | Não atribuir (25) | Não atribuir (25) | C1: dep. exec, C2: dep. exec, C3: não rep, C4: dep. exec, C5: dep. exec, C6: não rep |
| cadeia-3 | Não atribuir (55) | Atribuir (75) | Não atribuir (15) | Não atribuir (8) | C1: rep, C2: rep, C3: não rep, C4: rep, C5: rep, C6: não rep |

Entre parênteses, a confiança (0–100) de que o comitê atribuiu o selo.

## Tokens e tempo por etapa

| Cadeia | Etapa | Tempo (min) | Saída | Entrada | Cache criado | Cache lido | Total | Respostas da API | `docker exec` |
|---|---|---|---|---|---|---|---|---|---|
| cadeia-1 | A | 5.2 | 26.310 | 42 | 209.941 | 2.447.451 | 2.683.744 | 21 | 0 |
| cadeia-1 | B1 | 7.1 | 41.562 | 4 | 13.261 | 209.941 | 264.768 | 1 | 0 |
| cadeia-1 | E | 15.5 | 35.477 | 52 | 326.185 | 6.905.558 | 7.267.272 | 25 | 19 |
| cadeia-1 | B2 | 1.6 | 8.583 | 6 | 3.689 | 654.229 | 666.507 | 2 | 0 |
| **cadeia-1** | **total** | **29.4** | **111.932** | 104 | 553.076 | 10.217.179 | **10.882.291** | | |
| cadeia-2 | A | 4.3 | 25.045 | 30 | 146.689 | 1.477.996 | 1.649.760 | 15 | 0 |
| cadeia-2 | B1 | 5.0 | 31.261 | 4 | 18.602 | 146.689 | 196.556 | 1 | 0 |
| cadeia-2 | E | 16.0 | 36.419 | 118 | 262.572 | 12.425.882 | 12.724.991 | 56 | 48 |
| cadeia-2 | B2 | 1.7 | 10.652 | 6 | 3.116 | 527.160 | 540.934 | 2 | 0 |
| **cadeia-2** | **total** | **27.0** | **103.377** | 158 | 430.979 | 14.577.727 | **15.112.241** | | |
| cadeia-3 | A | 4.2 | 23.303 | 26 | 195.723 | 1.348.886 | 1.567.938 | 13 | 0 |
| cadeia-3 | B1 | 5.4 | 33.324 | 4 | 13.484 | 195.723 | 242.535 | 1 | 0 |
| cadeia-3 | E | 18.3 | 44.068 | 108 | 322.845 | 14.415.881 | 14.782.902 | 53 | 51 |
| cadeia-3 | B2 | 1.5 | 9.144 | 4 | 1.969 | 322.845 | 333.962 | 1 | 0 |
| **cadeia-3** | **total** | **29.5** | **109.839** | 142 | 534.021 | 16.283.335 | **16.927.337** | | |

## Médias por etapa (3 cadeias)

| Etapa | Tempo médio (min) | Saída média | Total médio |
|---|---|---|---|
| A | 4.6 | 24.886 | 1.967.147 |
| B1 | 5.9 | 35.382 | 234.620 |
| E | 16.6 | 38.655 | 11.591.722 |
| B2 | 1.6 | 9.460 | 513.801 |

Tempo: do envio do prompt até a última resposta do agente na etapa. Tokens: soma das respostas da API do agente (entrada sem cache, saída, criação e leitura de cache). Não inclui a sessão orquestradora.
