## Confronto com a avaliação analítica

Os resultados D2 e D3 abaixo são **evidência complementar**. Eles testam a versão fixada, mas não reproduzem o processo nem as entradas dos autores.

| Passo | Efeito sobre a avaliação analítica |
|---|---|
| P1–P4 | **Não altera.** Confirmam recursos, dependências e o commit examinado; não verificam reivindicações. [registro-factual.md:Ambiente observado; P1–P4] |
| P5–P6 | **Confirma** que a compilação, instalação e abertura do manual funcionaram nesse contêiner. Eram etapas documentadas; o resultado não supre as versões e o exemplo mínimo ausentes do README. [registro-factual.md:P5–P6; README.md:21–85] |
| P7 | **Não altera** a falha documental de F. O programa extraiu um script no teste mínimo, mas a entrada foi criada pelo revisor (D2). [registro-factual.md:P7; p7-saidas.txt:Audit] |
| P8 / C1 | **Não altera** a classificação analítica de dependência de reprodução dos autores. Com EVTX de terceiro (D3), o arquivo foi legível, porém saiu um byte maior que a origem. [registro-factual.md:C1; p8-c1-saidas.txt:cmp] |
| P9 / C2 | **Confirma** a divergência identificada no código: além de extrair scripts válidos, extraiu o caso composto só por shebang e comentário. [registro-factual.md:C2; p9-c2-comments-audit.txt:Audit; src/extract.c:2598–2604] |
| P10 / C3 | **Confirma** a divergência identificada no reconhecimento *thin*: o `fat` foi extraído exatamente, enquanto os dois *thin* válidos produziram zero arquivos. [registro-factual.md:C3; p10-c3-thin32-audit.txt:Audit; p10-c3-thin64-audit.txt:Audit] |
| P11 / C4 | **Não altera** a exigência de reprodução pelos autores, mas acrescenta evidência de saída incompleta: os dois ELF permitem ler cabeçalhos de programa; `readelf -S` relata seções fora do arquivo. O código de saída zero de `readelf` não elimina esse erro textual. [registro-factual.md:C4; p11-c4-validacao.txt:CASE=ELF32/ELF64] |
| P12 / C5 | **Confirma** que há consulta e registro VT em um caso conhecido: o ZIP EICAR de terceiro (D3) produziu `Malicious (61)`, igual à API. Também confirma o risco previsto: um hash inexistente (HTTP 404) e o caso sem chave foram rotulados `Clean (0)`. Não reproduz os resultados dos autores. [registro-factual.md:C5; p12-c5-eicar-audit.txt:Audit; p12-vt-eicar-stats.txt; p12-vt-check.txt; p12-c5-sem-chave.txt] |
| P13 / C6 | **Confirma** a lacuna decisiva: `evidence2.dd` não está disponível; a execução e a comparação com a Figura 2 não ocorreram. [registro-factual.md:C6; p13-c6-bloqueio.txt] |
| P14 / C7 | **Não altera.** Não houve experimento; C7 está fora da regra de R. [registro-factual.md:P14; reivindicacoes.md:Regra para o selo R] |

## Decisões revistas

**F — Não atribuir; decisão inalterada.** A compilação e a extração observadas resolvem parte da incerteza funcional, mas o critério obrigatório exige que o **README** informe versões das dependências e do ambiente e ao menos um exemplo mínimo [instrucoes-oficiais.md:Funcional (F)]. O README continua oferecendo plataformas, comandos de instalação e sintaxe genérica, sem esses elementos [README.md:21–85]. O teste D2 não altera o conteúdo do README. Minha estimativa de que o comitê oficial atribuiu F sobe de **20 para 30/100**, porque há agora prova de execução bem-sucedida em um ambiente, embora permaneça a falha documental. Não é caso de “Indeterminado”: há critério obrigatório não atendido na documentação.

**R — Não atribuir; decisão inalterada.** A regra exige C1 a C6 [reivindicacoes.md:Regra para o selo R]. Os testes complementares corroboram problemas em C2 e C3 e mostram limitações adicionais em C1, C4 e na interpretação do resultado VT. Sobretudo, falta a imagem **`evidence2.dd`**, indispensável para comparar arquivos e offsets da Figura 2; C6 não foi executada [artigo.pdf:p.8, Fig.2; registro-factual.md:C6]. Também continuam ausentes as instruções por reivindicação e o processo dos autores exigidos oficialmente [instrucoes-oficiais.md:Reprodutível (R); README.md:74–107]. Minha estimativa de atribuição oficial de R cai de **5 para 1/100**. Não é caso de “Indeterminado”: a ausência de C6 e da documentação obrigatória já fundamenta “Não atribuir”, independentemente das execuções complementares.

Para reavaliar R com o processo dos autores, faltariam a imagem `evidence2.dd` identificada por hash, as demais entradas usadas nas reivindicações, os procedimentos de preparação e validação e a comparação de resultados produzidos com os publicados. Possíveis esclarecimentos posteriores dos autores e a decisão oficial não constam dos materiais examinados.

```json
{"F":{"decisao":"Não atribuir","confianca":30,"mudou":false,"evidencias":["instrucoes-oficiais.md:Funcional (F)","README.md:21-85","registro-factual.md:P5-P7","p7-saidas.txt:Audit"]},"R":{"decisao":"Não atribuir","confianca":1,"mudou":false,"evidencias":["instrucoes-oficiais.md:Reprodutível (R)","reivindicacoes.md:Regra para o selo R","registro-factual.md:C1-C6","p9-c2-comments-audit.txt:Audit","p10-c3-thin32-audit.txt:Audit","p11-c4-validacao.txt:CASE=ELF32/ELF64","p13-c6-bloqueio.txt"],"por_reivindicacao":{"C1":"depende_execucao","C2":"nao_reproduzivel","C3":"nao_reproduzivel","C4":"nao_reproduzivel","C5":"depende_execucao","C6":"nao_reproduzivel"}}}
```
