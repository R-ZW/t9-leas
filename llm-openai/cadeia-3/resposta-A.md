## A. Materiais examinados

Abri somente `artigo.pdf`, `artefato.txt`, `instrucoes-oficiais.md` e `reivindicacoes.md`, todos no pacote indicado. Li o índice e os trechos pertinentes do código contidos em `artefato.txt`, além da Figura 2 do PDF. **Não compilei nem executei o artefato.** Os números de confiança abaixo estimam a chance de atribuição pelo comitê; o pacote não contém a decisão oficial nem eventuais esclarecimentos dos autores [instrucoes-oficiais.md:Contexto de revisão], “a decisão final considera também os esclarecimentos dos autores”.

## B. Selo F

**Critérios oficiais e situação documental**

| Critério | Trecho oficial | Avaliação e evidência |
|---|---|---|
| Executabilidade e observação das funções | [instrucoes-oficiais.md:Funcional (F)], “precisa ser executável e permitir a observação de funcionalidades” | **Só verificável por execução.** Há alvo de compilação em [src/Makefile:100–101], “`$(GOAL): $(OBJ)`”, mas isso não prova que compile ou funcione. |
| Dependências, versões e ambiente no README | [instrucoes-oficiais.md:Funcional (F)], “O README deve informar dependências, versões de dependências/linguagens/ambiente, ambiente de execução” | **Não atendido integralmente.** O README identifica plataformas e alguns requisitos — [README.md:37–54], “Make sure `curl` is installed” e “Install OpenSSL” — sem fixar versões do compilador, curl, OpenSSL ou ambiente. O ambiente alternativo também é variável: [Dockerfile:1], “`FROM ubuntu:latest`”. |
| Instalação | [instrucoes-oficiais.md:Funcional (F)], “O README deve informar … instalação” | **Atendido na documentação.** [README.md:31–35], “`make`” e “`sudo make install`”; há variantes para outras plataformas [README.md:37–68]. |
| Execução e exemplo mínimo | [instrucoes-oficiais.md:Funcional (F)], “execução e pelo menos um exemplo mínimo” | **Não atendido integralmente.** O README oferece apenas a forma geral [README.md:82–85], “`foremost-ng [options] [image_or_device]`”; não dá um comando mínimo com entrada concreta e saída esperada. Remete ao manual [README.md:76–80], “`man foremost-ng`”, cujo conteúdo comprimido não está transcrito em `artefato.txt` [artefato.txt:ÍNDICE], “`src/foremost-ng.8.gz … binário (omitido)`”. |
| Prova de funcionamento no parecer | [instrucoes-oficiais.md:Funcional (F)], “O revisor deve **executar** o artefato e apresentar prova de execução e saídas” | **Só verificável por execução.** Não há observação de compilação, execução ou saída nesta avaliação. |

**Decisão F: Não atribuir.** Faltam informações obrigatórias no README, sobretudo versões do ambiente e um exemplo mínimo concreto. A leitura do código não substitui a execução exigida [instrucoes-oficiais.md:Funcional (F)], “Ler código ou README, por si só, não constitui prova de funcionamento”.

**Confiança de que o comitê oficial atribuiu F: 20/100.** A ausência de parecer de execução e de possíveis respostas dos autores limita essa estimativa.

**Para mudar a decisão:** seria necessário um README com dependências e versões, ambiente reproduzível e exemplo mínimo com entrada e saída esperada; depois, observar compilação, execução do exemplo, arquivos extraídos e registro das saídas.

## C. Selo R — por reivindicação

**Critérios oficiais aplicáveis.** O revisor deve conseguir reproduzir “as **principais reivindicações do artigo**”; a documentação deve trazer “instruções de execução dessas reivindicações” e “descrever o processo usado pelos autores”; é necessário “executar os experimentos e confrontar os resultados com os do artigo, incluindo figuras/tabelas pertinentes” [instrucoes-oficiais.md:Reprodutível (R)]. A regra específica exige **C1 a C6**; C7 não integra R [reivindicacoes.md:Regra para o selo R], “R é atribuído se C1 a C6 forem reproduzidas”.

Para **C1 a C5**, as instruções específicas e o processo empregado pelos autores **não estão atendidos na documentação**: o README fornece instalação, sintaxe genérica e configuração da chave VT [README.md:21–107], sem identificar entradas de teste, preparação ou verificações para cada formato. A comparação dos resultados **só é verificável por execução**. Há código pertinente, mas sua presença não demonstra o resultado.

### C1 — EVTX: depende de execução

O artigo reivindica a assinatura e os chunks [artigo.pdf:p.6, §3, “Windows Event Logs (EVTX)”], “ElfFile” e “64 KiB chunks”. O registro do formato aparece em [src/state.c:381–382], “`EVTX, "evtx", "ElfFile\0\0"`”; a extração calcula o tamanho em [src/extract.c:2485–2490], “`chunk_count * 65536ULL`”, e grava em [src/extract.c:2513–2514], “`write_to_disk`”. **Não há resultado observado**, amostra EVTX identificada ou instrução específica de validação. Para mudar o estado, observar a extração de uma entrada EVTX conhecida, delimitação correta e abertura do arquivo resultante em analisador de eventos, com entrada e processo documentados.

### C2 — scripts: não reproduzível na íntegra com esta versão

O artigo exige script com shebang, ao menos 32 bytes e conteúdo além de comentários [artigo.pdf:p.6, §3, “Script Files”]. O código impõe 32 bytes [src/extract.c:2521], “`MIN_SCRIPT_SIZE = 32`”, mas sua verificação do corpo percorre **caractere por caractere** e aceita o primeiro que não seja `#` [src/extract.c:2598–2604], “`if (*p != '#') … found_real = 1`”. Assim, numa linha composta apenas por comentário `# texto`, a letra após `#` satisfaz a condição. Essa é uma divergência estática da restrição “mais que só comentários”, além da falta de roteiro de reprodução. Para mudar a conclusão, seria necessária correção ou evidência que explicasse outro caminho efetivo; a execução deveria mostrar scripts Bash, Python e PowerShell legíveis **e** rejeição de uma entrada suficientemente longa composta apenas por comentários.

### C3 — Mach-O fat e thin: não reproduzível na íntegra com esta versão

O artigo reivindica ambos os tipos [artigo.pdf:p.6, §3, “Mach-O”], “whether fat or thin”. Há caminho FAT [src/extract.c:2325–2355]. No caminho *thin*, porém, o código lê quatro bytes como inteiro *little endian* [src/extract.c:2359–2360], “`read_le32(buf)`”, e compara com `0xCEFAEDFE` [src/extract.c:2362–2363] ou `0xCFFAEDFE` [src/extract.c:2408–2409]. As assinaturas registradas são os bytes `CE FA ED FE` e `CF FA ED FE` [src/state.c:375–379]; lidos como *little endian*, eles produzem respectivamente `0xFEEDFACE` e `0xFEEDFACF`, portanto não passam nessas comparações. A função de leitura realmente usa ordem *little endian* [src/helpers.c:351–354], “`read_le32 … FOREMOST_LITTLE_ENDIAN`”. Para mudar a conclusão, seria necessária correção ou explicação verificável da divergência, seguida de extrações FAT e *thin* 32/64 bits reconhecidas por analisador Mach-O.

### C4 — ELF 32/64 bits: depende de execução

O artigo promete os dois tamanhos e delimitação pelos cabeçalhos de programa [artigo.pdf:p.6, §3, “ELF”]. O código confere a assinatura e a classe [src/extract.c:2158–2169], “`0x7F 'E' 'L' 'F'`” e “`EI_CLASS`”; há ramos de gravação para ELF32 [src/extract.c:2232–2236] e ELF64 [src/extract.c:2298–2302]. Isso **não comprova** arquivos estruturalmente legíveis. Para mudar o estado, observar extração de entradas ELF32 e ELF64 conhecidas e verificar a estrutura e os limites dos arquivos resultantes com analisador ELF, documentando as entradas.

### C5 — VirusTotal: depende de execução

O artigo descreve consulta pelo hash e anotação do resultado [artigo.pdf:p.7, §4.1], “query VirusTotal’s API” e “annotate the `audit.txt`”. O README explica `-x` e `VT_API_KEY` [README.md:89–107]. O código calcula SHA-256, consulta e registra rótulo [src/dir.c:274–295], “`sha_checksum … "sha256"`”, “`vt_check_hash`” e “`vt_label`”. Falta uma execução documentada com chave válida, hash, resposta e registro correspondente. Há ainda risco de interpretação: sem chave, a consulta retorna contagens zeradas [src/vt_query.c:139–143] e a saída pode ser rotulada “Clean (0)” [src/dir.c:280–282], embora nenhuma detecção tenha sido consultada. Para mudar o estado, observar consulta válida associada ao hash do arquivo extraído, resultado no registro e, sem chave, aviso e carving sem consulta. As contagens não precisam coincidir com a figura [reivindicacoes.md:Critério de reprodução].

### C6 — execução da Figura 2: não reproduzível com o pacote

A figura especifica [artigo.pdf:p.8, Fig.2], “`./foremost-ng -v -x evidence2.dd`”, e mostra 12 extrações ELF, script, EXE e ZIP, com offsets e coluna VT; por exemplo, `00004352.elf` no offset `2228224` e `00399884.exe` no offset `204740608`. O arquivo **`evidence2.dd` não consta do índice completo** [artefato.txt:ÍNDICE], e o README não o identifica nem instrui a reproduzir a figura [README.md:74–107]. Sem essa entrada, não há como confrontar os arquivos e offsets exigidos [reivindicacoes.md:Critério de reprodução], “Em C6, comparam-se os arquivos e offsets da Fig. 2”. Para mudar a decisão, seria preciso fornecer a imagem exata, sua identificação de integridade e o procedimento; então observar a execução e comparar nomes, tipos e offsets com a figura.

**Decisão R: Não atribuir.** C2 e C3 apresentam divergências estáticas nas reivindicações completas; C6 carece da entrada indispensável. Além disso, faltam no README as instruções por reivindicação e a descrição do processo dos autores exigidas oficialmente. **Confiança de que o comitê oficial atribuiu R: 5/100.** A avaliação continua limitada ao pacote, sem execução nem respostas dos autores.

## D. Lacunas e riscos

- O índice não contém imagens de teste ou `evidence2.dd` [artefato.txt:ÍNDICE]; o artigo remete genericamente a amostras externas [artigo.pdf:p.7, §4], “Carving test samples can be downloaded”, sem identificar quais produziram a Figura 2. Isso impede comparação fiel sem material adicional.
- O Dockerfile usa base móvel e clona o repositório remoto [Dockerfile:1–10], “`ubuntu:latest`” e “`git clone`”; sua construção futura não fica vinculada à versão `bb812a22…` examinada.
- Há discrepância no nome do registro: o artigo menciona `recovery.log` [artigo.pdf:p.7, §4.2], enquanto o código define `audit.txt` [src/main.h:162], “`AUDIT_FILE_NAME "audit.txt"`”. Uma reprodução precisaria esclarecer qual arquivo comparar.
- C7 foi apenas inspecionada, **fora da regra de R** [reivindicacoes.md:Regra para o selo R]. O artigo descreve callbacks por parser [artigo.pdf:p.3, §2], enquanto o código despacha por uma cadeia de testes de tipo [src/extract.c:2624–2687]; isso merece esclarecimento próprio, sem alterar diretamente a decisão de R.

```json
{"F":{"decisao":"Não atribuir","confianca":20,"evidencias":["instrucoes-oficiais.md:Funcional (F)","README.md:21-85","Dockerfile:1-10","src/Makefile:100-101"]},"R":{"decisao":"Não atribuir","confianca":5,"evidencias":["instrucoes-oficiais.md:Reprodutível (R)","reivindicacoes.md:Regra para o selo R","src/extract.c:2598-2604","src/extract.c:2359-2363","src/extract.c:2408-2409","src/helpers.c:351-354","artefato.txt:ÍNDICE","artigo.pdf:p.8, Fig.2"],"por_reivindicacao":{"C1":"depende_execucao","C2":"nao_reproduzivel","C3":"nao_reproduzivel","C4":"depende_execucao","C5":"depende_execucao","C6":"nao_reproduzivel"}}}
```
