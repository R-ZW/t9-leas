# Resumo — llm-google

Gerado por `ferramentas/resumir.py` a partir de `resposta-A.md`, `resposta-B2.md` e `medicoes.json` de cada cadeia.

## Decisões

| Cadeia | F (A) | F (B2) | R (A) | R (B2) | C1–C6 no B2 |
|---|---|---|---|---|---|
| cadeia-1 | Indeterminado (80) | Atribuir (95) | Não atribuir (15) | Não atribuir (95) | C1: rep, C2: rep, C3: rep, C4: rep, C5: rep, C6: não rep |
| cadeia-2 | Indeterminado (80) | Atribuir (100) | Não atribuir (20) | Não atribuir (10) | C1: rep, C2: rep, C3: não rep, C4: rep, C5: rep, C6: não rep |
| cadeia-3 | Indeterminado (85) | Atribuir (95) | Não atribuir (10) | Não atribuir (5) | C1: rep, C2: rep, C3: rep, C4: rep, C5: rep, C6: não rep |

Entre parênteses, a confiança (0–100) de que o comitê atribuiu o selo.

## Tokens e tempo por etapa

| Cadeia | Etapa | Tempo (min) | Saída | Entrada | Cache criado | Cache lido | Total | Respostas da API | `docker exec` |
|---|---|---|---|---|---|---|---|---|---|
| cadeia-1 | A | 5.3 | 36.126 | 154.019 | 0 | 807.686 | 997.831 | 18 | 0 |
| cadeia-1 | B1 | 1.6 | 23.102 | 18.280 | 0 | 255.261 | 296.643 | 2 | 0 |
| cadeia-1 | E | 15.8 | 38.673 | 198.665 | 0 | 13.083.203 | 13.320.541 | 74 | 48 |
| cadeia-1 | B2 | 1.5 | 13.134 | 17.682 | 0 | 648.224 | 679.040 | 3 | 0 |
| **cadeia-1** | **total** | **24.2** | **111.035** | 388.646 | 0 | 14.794.374 | **15.294.055** | | |
| cadeia-2 | A | 7.0 | 37.628 | 161.671 | 0 | 1.485.537 | 1.684.836 | 29 | 0 |
| cadeia-2 | B1 | 2.5 | 33.808 | 26.278 | 0 | 270.896 | 330.982 | 2 | 0 |
| cadeia-2 | E | 16.1 | 45.126 | 351.885 | 0 | 13.323.409 | 13.720.420 | 68 | 52 |
| cadeia-2 | B2 | 1.1 | 9.567 | 12.040 | 0 | 728.013 | 749.620 | 3 | 0 |
| **cadeia-2** | **total** | **26.6** | **126.129** | 551.874 | 0 | 15.807.855 | **16.485.858** | | |
| cadeia-3 | A | 5.5 | 35.401 | 134.032 | 0 | 781.844 | 951.277 | 19 | 0 |
| cadeia-3 | B1 | 1.9 | 24.286 | 20.133 | 0 | 217.374 | 261.793 | 2 | 0 |
| cadeia-3 | E | 13.9 | 42.216 | 289.202 | 0 | 9.173.261 | 9.504.679 | 55 | 47 |
| cadeia-3 | B2 | 1.3 | 12.792 | 17.672 | 0 | 643.144 | 673.608 | 3 | 0 |
| **cadeia-3** | **total** | **22.6** | **114.695** | 461.039 | 0 | 10.815.623 | **11.391.357** | | |

## Médias por etapa (3 cadeias)

| Etapa | Tempo médio (min) | Saída média | Total médio |
|---|---|---|---|
| A | 5.9 | 36.385 | 1.211.315 |
| B1 | 2.0 | 27.065 | 296.473 |
| E | 15.3 | 42.005 | 12.181.880 |
| B2 | 1.3 | 11.831 | 700.756 |

Tempo: do envio do prompt até a última resposta do agente na etapa. Tokens: soma das respostas da API do agente (entrada sem cache, saída, criação e leitura de cache). Não inclui a sessão orquestradora.
