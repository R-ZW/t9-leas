REAVALIAÇÃO DE F E R APÓS A EXECUÇÃO

Fontes: o registro D:\Lab-artefatos\t9-trabalho\claude-c3\execucao\registro-factual.md, as evidências da mesma pasta e o material da etapa A. Nada foi executado nesta etapa.

Resumo: F muda de Não atribuir para Atribuir (confiança 75). R continua Não atribuir (confiança 8). F muda porque a ferramenta compilou e funcionou pelo caminho dos autores e porque a man page tem os exemplos que faltavam; só a falta de versões continua aberta. R continua negado porque falta a imagem de C6 e porque os testes complementares contradizem C3 e partes de C2 e C5.

1. EFEITO DE CADA PASSO SOBRE A AVALIAÇÃO ANALÍTICA

| Passo | Resultado | Efeito |
|---|---|---|
| P2 (D0, via Dockerfile) | Os 5 pacotes do Dockerfile:5 bastaram para compilar. | Confirma que as dependências existem no artefato, só que no Dockerfile, que o README não cita (F2 continua parcial). Mostra que são suficientes. |
| P3 | O zip confere com o commit bb812a22. Difere do clone só nos fins de linha (CRLF no zip). | Não altera. |
| P4 (D0) | `make` na raiz responde "no makefile found". | Confirma: as instruções do artigo, p.6, estão erradas. |
| P5–P6 (D0) | Compila só com 2 avisos e instala binário, man page e configuração. | Confirma o que antes só era verificável por execução (F1). Mostra que o caminho do README funciona em Ubuntu 24.04. |
| P10 (D0) | Ajuda e versão 1.5.7 funcionam. | Confirma. |
| P11 (D0) | A man page tem seção EXAMPLES, por exemplo `foremost-ng -t gif,pdf -i image.dd` e `foremost-ng -x image.dd`. O README remete a ela (README.md:76-79). Ela não lista evtx, elf, macho nem script. | Contradiz em parte a falha que apontei em F7: há exemplo mínimo na documentação referenciada pelo README. Era evidência ausente na etapa A, porque o arquivo é binário. |
| P12 (comando D0; dados D3 de fonte citada pelos autores, artigo p.7) | 14 arquivos extraídos. 10 dos 15 do gabarito com MD5 idêntico, e os demais com tipo reconhecido. | Confirma F1 e F8: funcionalidade observada, com prova de execução. |
| P13–P16, C1 (D3) | O deslocamento 0x18 contém o próximo número de registro (13.528 e 2.226), não a contagem de chunks. Um EVTX isolado sai até o fim da imagem. Quando há um segundo EVTX logo depois, o corte acontece certo. Os 3 arquivos foram lidos com a contagem completa de registros. | Confirma o risco previsto (campo errado, extração excessiva). Resolve a dúvida sobre a legibilidade em favor do resultado esperado. |
| P17–P19, C2 (D2) | Positivos saem idênticos e o controle com menos de 32 bytes é rejeitado. O controle só com comentários foi extraído. | Contradiz o que eu disse na etapa A ("implementação compatível com o artigo"). O filtro "mais que só comentários" não funcionou no teste. |
| P20–P22, C3 (D2) | Os dois fat saem idênticos. Nenhum thin (i386, x86_64 objeto e x86_64 executável) foi extraído. Com `-a`, os cabeçalhos thin são localizados mas não gravados. | Contradiz a etapa A: eu previa só extração excessiva no thin de 64 bits e não percebi que ele simplesmente não é extraído. Pela leitura (inferência minha), a comparação com 0xCFFAEDFE/0xCEFAEDFE em extract.c:2363/2409 nunca casa em máquina little-endian. A metade "thin" de C3 falha. |
| P23–P25, C4 (D2) | ELF32 e ELF64 extraídos, idênticos ao prefixo do original e executáveis. A tabela de seções fica de fora: `readelf -h -l` retorna rc=0, mas acusa erro nos cabeçalhos de seção. | Confirma a previsão (sem tabela de seções; "symbol information" do artigo não se mantém). O resultado esperado, "estruturalmente legível", é atendido nos cabeçalhos ELF e de programa. |
| P26/P26b (D2) | No exemplo `-t evtx,elf,exe`, a DLL PE32+ não foi extraída. Com `-a`, só aparecem "Header dump". | Fato novo, fora de C1–C5. Indica que PE de 64 bits não é extraído nesta versão, o que reduz a possibilidade de comparar a Fig. 2 se os .exe dela forem PE32+. |
| P28 (D3) | Sem chave: uma linha de aviso por arquivo, extração concluída e audit com "Clean (0)". | Confirma a leitura (vt_query.c:140-142; rótulo enganoso). |
| P29 (D3) | Chave inválida: nenhum aviso e "Clean (0)". | Confirma a divergência prevista com o artigo, p.7. |
| P30 (D3) | Com chave válida, os rótulos batem com a consulta direta por hash (EICAR "Malicious (65)", zcat "Clean (61)", ELF desconhecido "Clean (0)"). O audit não traz hash e não há recovery.log. | Resolve em favor do artigo o risco de parsing que eu levantei (sscanf). Confirma a ausência de hash no log. |
| P31–P33 | evidence2.dd indisponível; P32 e P33 não executados. | Confirma que falta o dado de C6. |

2. NOVAS DECISÕES (mesma regra da etapa A)

SELO F: Atribuir

Situação de cada critério de [instrucoes-oficiais.md:15]:

| Critério | Situação | Evidência |
|---|---|---|
| F1 Executável, com funcionalidades observáveis | Atendido. | P5, P6, P10, P12, por caminho D0 com dados da fonte indicada pelos autores |
| F2 Dependências | Atendido em parte. Estão no Dockerfile do artefato, não no README, e bastaram (P2). | P2 |
| F3 Versões | Não atendido. Não há versões; o Dockerfile usa ubuntu:latest. | — |
| F4 Ambiente | Atendido. | — |
| F5 Instalação | Atendido pelo README. O artigo está errado (P4). | P4–P6 |
| F6 Execução | Atendido (README e man page). | P10, P11 |
| F7 Exemplo mínimo | Atendido pela man page, que o README referencia. | P11 |
| F8 Prova de execução | Fornecida. | P12_run.log, P12_audit.txt, P12_comparacao.tsv |

Justificativa e mudança: na etapa A a decisão foi Não atribuir por F2, F3 e F7, sem poder verificar F1 e F8. A execução satisfez F1 e F8 por caminho dos autores sem nenhuma alteração. F7 caiu ao abrir a man page, que era evidência ausente. F2 mostrou-se suficiente pelo Dockerfile do próprio artefato. Fica só F3, a falta de versões. Considero essa lacuna parcial e não impeditiva: os pacotes documentados, na versão atual do Ubuntu LTS, compilaram sem ajuste. Uma leitura estrita de F3 levaria a Não atribuir, e registro isso de forma explícita.

Confiança de que o comitê atribuiu F: 75 (era 55).

SELO R: Não atribuir

1. C6 não tem o dado necessário (P31). Esse é o caso-exemplo de "Não atribuir" da regra.
2. A documentação não traz instruções de reprodução nem o processo dos autores (R1, R2 da etapa A), e a execução não muda isso.
3. Os testes complementares (D2/D3) não reproduzem os experimentos dos autores, que não fornecem nem dados nem procedimento para C1–C5. Ainda assim, contradizem parte das reivindicações:
   - C3: thin não é extraído;
   - C2: o filtro de comentários não funcionou;
   - C5: não há aviso com chave inválida.

Não uso Indeterminado: não falta evidência que mudaria a decisão, porque C6 sozinho já impede R.

Confiança de que o comitê atribuiu R: 8 (era 15). Baixou porque surgiu evidência concreta de não conformidade (C3) além da falta do dado.

Situação por reivindicação (evidência complementar, sem reprodução de experimento dos autores):

| Reivindicação | Classificação | Base |
|---|---|---|
| C1 | reproduzivel (complementar) | O resultado esperado, "legível por ferramenta de análise de eventos", foi observado. A delimitação usa um campo errado (extração excessiva quando não há EVTX seguinte). |
| C2 | reproduzivel (complementar), com divergência | Os scripts saem com interpretador e corpo, e o mínimo de 32 bytes funciona. O filtro "mais que só comentários" falhou no teste. |
| C3 | nao_reproduzivel | Thin não é extraído; só fat funciona. |
| C4 | reproduzivel (complementar), com divergência | ELF de 32 e 64 bits legíveis em cabeçalhos ELF e de programa e executáveis. A tabela de seções e os símbolos ficam de fora. |
| C5 | reproduzivel (complementar), com divergência | Consulta por hash e resultado registrado conferem com o VT. Sem chave, há aviso e extração. Com chave inválida, não há aviso, e o hash não é registrado. |
| C6 | nao_reproduzivel | evidence2.dd indisponível. |

{"F": {"decisao": "Atribuir", "confianca": 75, "mudou": true, "evidencias": ["execucao/P2_versoes.txt", "execucao/P4_make_raiz.log", "execucao/P5_make.log", "execucao/P6_install.log", "execucao/P10_uso.txt", "execucao/P11_man.txt", "execucao/P12_run.log", "execucao/P12_audit.txt", "execucao/P12_comparacao.tsv", "artefato.txt:README.md:31-34", "artefato.txt:README.md:76-84", "artefato.txt:Dockerfile:1-10", "instrucoes-oficiais.md:15"]},
 "R": {"decisao": "Não atribuir", "confianca": 8, "mudou": false, "evidencias": ["execucao/P31.txt", "reivindicacoes.md:12", "reivindicacoes.md:17", "artigo.pdf:p.8 Fig. 2", "execucao/P16_valida.txt", "execucao/P18.log", "execucao/P19.txt", "execucao/P21.log", "execucao/P21b_diag.log", "execucao/P22.txt", "execucao/P25.txt", "execucao/P26b_diag.txt", "execucao/P28.log", "execucao/P29.log", "execucao/P30_audit.txt", "execucao/P30_ref.tsv", "instrucoes-oficiais.md:19"],
       "por_reivindicacao": {"C1": "reproduzivel", "C2": "reproduzivel", "C3": "nao_reproduzivel", "C4": "reproduzivel", "C5": "reproduzivel", "C6": "nao_reproduzivel"}}}