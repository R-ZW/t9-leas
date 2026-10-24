REAVALIAÇÃO DE F E R APÓS A EXECUÇÃO: Foremost-NG (bb812a22)
Nesta etapa não executei nada. Usei o registro-factual.md, as evidências em D:\Lab-artefatos\t9-trabalho\claude-c2\execucao e o material da etapa A.

Os dois selos continuam **Não atribuir**. As razões mudaram em parte:
- **F:** compilar, instalar e executar funcionou, e o manual traz exemplos. A única exigência obrigatória que segue sem atendimento é a de versões no README.
- **R:** C6 não pôde ser executada porque evidence2.dd não existe em lugar nenhum. Além disso, o teste de C3 confirmou a falha prevista no Mach-O "thin".

Seguindo o item 3, tratei os passos D2 e D3 como evidência complementar.
- Um resultado positivo com entradas montadas por mim não conta como reprodução das reivindicações.
- Um resultado negativo sobre entrada válida conta como evidência contrária, e no caso de C3 o defeito também está no código dos autores.

======================================================================
1. EFEITO DE CADA PASSO SOBRE A AVALIAÇÃO ANALÍTICA
======================================================================
| Passo (desvio) | Fato observado | Efeito |
|---|---|---|
| P3 (D1) e P3b (D0/D2) | O ZIP e 13 arquivos conferem com o índice. O commit bb812a22 existe no repositório. | Não altera: o código executado é o que analisei. |
| P2 (D0) | As dependências do Dockerfile:3-6 bastaram: gcc 13.3.0, OpenSSL 3.0.13, libcurl 8.5.0. | Confirma que o README sozinho não lista as dependências para Linux e que elas estão no Dockerfile. Também confirma que não há versões fixadas: o que vale é o que o ubuntu 24.04 instalou. |
| P4 e P5 (D0) | `make` exit=0, só com 2 avisos `-Wunused-result`. `sudo make install` instalou binário, manual e configuração. | Elimina o risco que eu tinha levantado sobre compilar com GCC recente. Confirma que o procedimento de instalação do README funciona. |
| P6 (D0) | `-h`, `-V` (1.5.7) e `man foremost-ng` funcionaram. O manual tem uma seção EXAMPLES (por exemplo `foremost-ng -t gif,pdf -i image.dd` e `foremost-ng -x image.dd`). A seção BUILT-IN FORMATS não lista elf, macho, evtx nem script. | **Contradiz** em parte a minha avaliação. Na etapa A eu marquei o exemplo mínimo como não atendido porque o manual era binário e eu não pude lê-lo. O README remete ao manual (README.md:76-79), e o manual traz exemplos concretos, então o exemplo mínimo está atendido, embora fora do README. Também confirma uma lacuna de documentação: os formatos novos não aparecem no manual. |
| P8 (comando D0 da p. 7 §4.1, dados D3 do DFTT, que o próprio artigo indica na p. 7) | 14 arquivos extraídos, audit.txt gerado, 10 dos 15 arquivos publicados pelo DFTT com MD5 idêntico. Nenhum recovery.log. | Confirma que o artefato executa e que dá para observar a funcionalidade. Confirma também a divergência do artigo: o registro gerado é audit.txt, não recovery.log. |
| P11, P12 e P13b (D3/D2), C1 | Nos dois EVTX, o campo em 0x18 vale 13.528 e 2.226 (próximo identificador de registro). A contagem real de chunks está em 0x2A e vale 9 e 26. Os arquivos extraídos vão até o próximo "ElfFile" ou até o fim da imagem, maiores que os originais, com o início idêntico. A biblioteca python-evtx leu o mesmo número de chunks e de registros dos originais. | **Confirma** a observação de código: o deslocamento lido é o errado. **Contradiz** a consequência que eu temia: com estas entradas, o resultado foi legível. |
| P15 e P16 (D2), C2 | Os 3 scripts saíram com hash idêntico e o controle com menos de 32 bytes foi descartado. O controle que só tem comentários **foi extraído**. | **Contradiz** a minha avaliação, que dizia que o código correspondia bem à descrição. A regra "mais que só comentários" (artigo p. 6) não se sustentou nesse teste. O resultado esperado da tabela (script com shebang e corpo legível) foi observado. |
| P19, P20 e P20b (D3/D2), C3 | Thin x86_64 e arm64: 0 arquivos extraídos, embora `-a` mostre que a assinatura foi encontrada nos dois offsets. Fat: 1 arquivo idêntico ao original. | **Confirma** a previsão analítica: o parser rejeita o Mach-O thin em host little-endian, e o fat funciona. |
| P22 e P23 (D2), C4 | ELF de 32 e de 64 bits extraídos como prefixos idênticos, com classe correta no `readelf -h -l`. Os três ficaram sem a tabela de seções ("extends past end of file for section headers"), e os símbolos FUNC caíram de 12 para 0. | **Confirma** o risco que eu tinha levantado: o corte no último segmento carregável deixa de fora a tabela de seções e os símbolos. Isso contradiz a afirmação do artigo de que os símbolos são preservados. A parte estrutural mínima (cabeçalho e program headers) é legível. |
| P24 (D2), C5 sem chave | Carving feito, 3 mensagens "Error: VT_API_KEY … not set" e audit com "Clean (0)". | **Confirma** a divergência prevista: o artigo fala em aviso e consulta pulada, mas o audit registra um rótulo "Clean (0)". |
| P26 e P27 (D2/D3) | Os 3 ELF extraídos aparecem como "Clean (0)" no audit, e a API devolve 404 NotFoundError para os 3 hashes. | Não altera: o rótulo é coerente com hash desconhecido. Os hashes são desconhecidos em parte porque os ELF saem truncados (P23). |
| P28 e P28c (D3) | O eicar_com.zip foi extraído com hash idêntico. O audit registrou "Malicious (62)" e a API informa malicious=62 para o mesmo SHA-256. | **Contradiz** o risco que eu tinha levantado sobre o sscanf: com a API atual, a leitura funcionou. **Confirma** que a consulta é feita pelo hash do arquivo extraído e que o resultado vai para o audit. Confirma também que o audit não tem coluna de hash. |
| P29 (D2) e P30 (bloqueado), C6 | Não há evidence2.dd no ZIP nem em nenhum dos 51 commits. O coordenador informou que o arquivo não é público e que os autores não responderam. | **Confirma** que falta o dado da Fig. 2. |
| P31 (D2), C7 | O despachante é uma cadeia if/else em extract.c:2668-2690, com um ramo explícito para cada tipo novo. | **Confirma** a inspeção: adicionar um parser exige editar o despachante. |
| P13 (D2) | O utilitário `evtx_dump` do python-evtx 0.8.1 está quebrado. | Não altera: é problema da ferramenta de validação, não do artefato. |

======================================================================
2. NOVAS DECISÕES
======================================================================
**Selo F: NÃO ATRIBUIR (sem mudança de decisão; mudam os motivos)**

Situação de cada critério de instrucoes-oficiais.md:15:
- **F1 dependências:** parcial. O README não as lista para Linux. O Dockerfile:5 lista, e elas bastaram (P2).
- **F2 versões:** **não atendido**. A execução não muda isso: as versões observadas foram as do Ubuntu 24.04 (P2), mas nenhum documento dos autores fixa versões. O Dockerfile usa `ubuntu:latest` e clona o HEAD do repositório.
- **F3 ambiente:** parcial, sem mudança.
- **F4 instalação:** atendido e executado sem alteração (P4 e P5, D0).
- **F5 execução:** atendido, porque o README remete ao manual e o manual mostrou as opções (P6, D0).
- **F6 exemplo mínimo:** **agora atendido**, pela seção EXAMPLES do manual que o README indica (P6-manpage.txt). Nenhum exemplo traz dados de entrada.
- **F7 executável com funcionalidades observáveis:** atendido. P8 usou o comando da p. 7 §4.1 sobre a imagem do DFTT, que o artigo indica.
- **F8 prova de execução:** existe (P4.log, P5.log, P6.log, P8.log, P8-audit.txt).

Regra aplicada: F2 continua sendo uma exigência obrigatória ("O README deve informar … versões") sem atendimento, então a regra leva a Não atribuir. O motivo de reprovação ficou restrito a essa lacuna de documentação, que é leve. Tudo o que depende de execução teve sucesso com o procedimento dos próprios autores (D0).

**Confiança de que o comitê atribuiu F: 75** (antes, 60).
Subiu porque a execução eliminou o risco de compilação e mostrou o artefato funcionando com o procedimento dos autores. Um comitê que não trate a falta de versões como impeditiva teria atribuído F.

**Selo R: NÃO ATRIBUIR (sem mudança)**

Regra fixada [reivindicacoes.md:17]: R exige reproduzir de C1 a C6.
- **C6:** não reproduzível. O dado de entrada não existe (P29) e a execução da Fig. 2 ficou bloqueada (P30). É exatamente o caso que a regra cita como motivo para Não atribuir.
- **C3:** não reproduzível. A parte thin falhou com binários Mach-O reais e válidos (P19, P20b), e a falha corresponde ao defeito no código dos autores (src/extract.c:2360-2409 junto com src/helpers.c:353).
- **R1 e R2** (instruções por reivindicação e descrição do processo que gerou os resultados) continuam sem atendimento. A execução não muda isso.
- **C1, C2, C4 e C5:** o comportamento esperado na tabela de reivindicacoes.md foi observado, mas só com entradas montadas por mim (D2) ou de terceiros (D3). Pelo item 3, isso é evidência complementar e não reprodução. Os autores não fornecem dados nem procedimento específico para essas reivindicações, então não há como reproduzi-las "como os autores fizeram". No JSON, uso "depende_execucao" para elas no sentido de que **falta reprodução com material dos autores, que não existe**. Não é falta de execução. Há ressalvas:
  - C2: o controle só de comentários foi extraído.
  - C4: ficam faltando a tabela de seções e os símbolos.
  - C5: sem chave, o audit registra "Clean (0)"; o hash não é registrado; não existe recovery.log.

Não uso Indeterminado. A evidência que falta (evidence2.dd e o processo da Fig. 2) não muda a decisão: a ausência dela já é, pela regra, motivo para Não atribuir.

**Confiança de que o comitê atribuiu R: 25** (sem mudança).
- Para baixo: a falha em C3 agora está confirmada.
- Para cima: C1, C2, C4 e C5 se comportaram como descrito em testes complementares, e o VirusTotal funcionou de ponta a ponta.
- Um comitê leniente, que não exigisse a Fig. 2 nem testasse Mach-O thin, poderia ter atribuído R.

======================================================================
3. BLOCO JSON
======================================================================
{"F": {"decisao": "Não atribuir", "confianca": 75, "evidencias": ["instrucoes-oficiais.md:15", "artefato.txt:README.md:31-35", "artefato.txt:README.md:76-84", "artefato.txt:Dockerfile:1", "artefato.txt:Dockerfile:5", "execucao/P2.log", "execucao/P4.log", "execucao/P5.log", "execucao/P6.log", "execucao/P6-manpage.txt:EXAMPLES", "execucao/P8.log", "execucao/P8-audit.txt", "execucao/P8-validacao.txt", "execucao/registro-factual.md:tabela P2-P8"], "mudou": false},
 "R": {"decisao": "Não atribuir", "confianca": 25, "evidencias": ["instrucoes-oficiais.md:19", "reivindicacoes.md:12", "reivindicacoes.md:17", "reivindicacoes.md:21", "artigo.pdf:p.8 Fig. 2", "execucao/P29.log", "execucao/P19_thin-audit.txt", "execucao/P20b-audit.txt", "execucao/P20.log", "artefato.txt:src/extract.c:2360-2409", "artefato.txt:src/helpers.c:353-354", "execucao/P13b.log", "execucao/P15-audit.txt", "execucao/P16.log", "execucao/P23.log", "execucao/P24-audit.txt", "execucao/P28-audit.txt", "execucao/P28c.log", "execucao/registro-factual.md:seção 3"],
       "por_reivindicacao": {"C1": "depende_execucao", "C2": "depende_execucao", "C3": "nao_reproduzivel", "C4": "depende_execucao", "C5": "depende_execucao", "C6": "nao_reproduzivel"}, "mudou": false}}

Nota sobre o JSON: em C1, C2, C4 e C5, "depende_execucao" significa que houve comportamento consistente com a reivindicação em teste complementar D2/D3, mas não houve reprodução com material dos autores, que não existe. Não significa que a execução não foi feita.