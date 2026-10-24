AVALIAÇÃO ANALÍTICA – SBSeg 2025, selos F e R – Foremost-NG (commit bb812a22cb06ef87b5a2d877dfb6f40eb12d460d)

Esta avaliação foi feita só pela leitura dos arquivos. Não compilei nem executei o artefato, e nada aqui afirma que algo funcionou. Nas citações de código uso o formato caminho:linha original, como pede o cabeçalho de artefato.txt. Os trechos do artigo, que tem direitos autorais, estão parafraseados e indicados por página e seção.

======================================================================
A. MATERIAIS EXAMINADOS
======================================================================
Abri estes arquivos em D:\Lab-artefatos\t9-trabalho\claude-c1\pacote:
- instrucoes-oficiais.md: lido inteiro.
- reivindicacoes.md: lido inteiro.
- artigo.pdf: lido inteiro, páginas 1 a 8, pelo texto extraído. A primeira tentativa de renderizar as páginas falhou porque o pdftoppm não está instalado; a leitura sem renderização funcionou, e o conteúdo da Fig. 2 veio legível.
- artefato.txt: lido inteiro, linhas 1 a 7330. Inclui o índice, README.md, Dockerfile, LICENSE, .gitignore, src/Makefile e todos os arquivos .c, .h e foremost.conf. As partes de OLE, ZIP, PDF, JPEG e outros formatos antigos de extract.c foram só localizadas, porque não pesam em C1 a C6.

Desvio de procedimento: no início usei uma vez a ferramenta de shell para rodar `wc -l` e `head -150` sobre artefato.txt. Eram comandos só de leitura, mas a instrução pedia apenas ferramentas de leitura de arquivo. Depois disso usei só Read e Grep. Não abri nenhum outro arquivo, não naveguei na web e não usei memória.

Itens não disponíveis, que registro como evidência ausente:
- src/foremost-ng.8.gz, a página de manual citada no README como documentação de uso. É binária e foi omitida.
- screenshots/*.png, que também são binários e foram omitidos.
- A imagem evidence2.dd usada na Fig. 2.
- O vídeo e o site DFTT citados no artigo.

======================================================================
B. SELO FUNCIONAL (F)
======================================================================
Critérios oficiais, conforme instrucoes-oficiais.md:15: o artefato precisa ser executável e permitir observar suas funcionalidades. O README deve informar dependências, versões de dependências, linguagens e ambiente, ambiente de execução, instalação, execução e ao menos um exemplo mínimo. O revisor deve executar e mostrar prova; ler código ou README não basta.

F1. Ser executável e permitir observar funcionalidades: só verificável por execução.
- O código tem um fluxo completo de ponta a ponta:
  - [src/main.c:226-228] `set_search_def(s, "all", 0);` é o padrão quando não se passa -t.
  - [src/engine.c:381-412] lê a entrada em blocos e chama search_chunk.
  - [src/dir.c:209-300] write_to_disk grava o arquivo recuperado e escreve no audit.
- Prova de execução: não há, porque a execução não foi feita.

F2. Dependências no README: não atendido para Linux, a plataforma principal.
- [README.md:3] declara "a Linux-based file recovery tool".
- [README.md:31-35] diz só `make` / `sudo make install` e não cita bibliotecas.
- [src/Makefile:46] `LINK_OPT += -lssl -lcrypto -lcurl` mostra que OpenSSL e libcurl são obrigatórias.
- As dependências aparecem só no Dockerfile, que o README não menciona: [Dockerfile:5] `gcc make git libssl-dev libcurl4-openssl-dev`.
- Para BSD e macOS há indicação parcial: [README.md:39-42] curl; [README.md:52-54] `brew install openssl@3`.

F3. Versões de dependências, linguagem e ambiente: não atendido.
- Não há versão de gcc, OpenSSL, libcurl nem de sistema operacional.
- [Dockerfile:1] `FROM ubuntu:latest` não fixa versão.
- [Dockerfile:8] `git clone https://github.com/cristianzsh/foremost-ng.git` clona a HEAD, não o commit avaliado.
- A única nota de versão é sobre glibc: [README.md:70] "On systems with glibc < 2.2.0, you may see harmless warnings".

F4. Ambiente de execução: atendido.
- [README.md:31, 37, 50, 62] trazem seções para Linux, BSD, macOS e compilação cruzada para Windows.

F5. Instalação: atendido.
- [README.md:25-34] `cd foremost-ng-<version>/src`, `make`, `sudo make install`. O artigo repete isso na p. 6, §4.

F6. Execução: atendido só em parte.
- [README.md:84] traz apenas a sintaxe genérica `foremost-ng [options] [image_or_device]`.
- [README.md:79] remete a `man foremost-ng`, cujo conteúdo está ausente (binário).
- As opções aparecem em [src/main.c:92-112] (usage) e em exemplos do artigo na p. 7, §4.1, mas não no README.

F7. Exemplo mínimo: não atendido.
- O README não tem nenhum comando concreto com arquivo de entrada.
- O índice de artefato.txt mostra que o repositório não traz nenhum dado de exemplo.
- O artigo, na p. 7, só remete a amostras externas do DFTT e a um vídeo, sem indicar qual amostra usar nem o resultado esperado.

F8. Prova de execução e saídas no parecer: só verificável por execução (não realizada).

Decisão para F: NÃO ATRIBUIR.
Pela regra pedida, há evidência documental de que critérios obrigatórios do README não são atendidos: versões (F3), exemplo mínimo (F7) e dependências em Linux (F2). Isso não depende de execução. Não há, porém, sinal de que o software deixe de funcionar: o fluxo central parece coerente e os exemplos do artigo (§4.1) compensam parte da lacuna. Por isso a falha é de documentação e poderia ser corrigida na fase de resposta dos autores.

Confiança de que o comitê oficial atribuiu F: 60.
Uma ferramenta em C que compila com `make` costuma receber F de comitês que executam com uma imagem qualquer. As lacunas encontradas costumam virar pedidos de ajuste, não reprovação.

O que precisaria ser observado na execução para mudar a decisão para Atribuir. Isso só vale se o comitê aceitar as seções do artigo como complemento do README, ou se os autores corrigirem o README.
1. Compilação sem erros no commit avaliado, com `make` em uma distribuição Linux após instalar libssl-dev e libcurl4-openssl-dev.
2. `foremost-ng -h` mostrando as opções, e `man foremost-ng` disponível depois do `make install`.
3. Uma execução sobre uma imagem qualquer, por exemplo do DFTT, gerando output/ com audit.txt, subdiretórios por tipo e arquivos recuperados que abrem nas ferramentas próprias de cada formato.

======================================================================
C. SELO REPRODUTÍVEL (R), POR REIVINDICAÇÃO
======================================================================
Critérios oficiais, conforme instrucoes-oficiais.md:19:
- R-a: a documentação traz instruções para executar as reivindicações principais.
- R-b: a documentação descreve o processo usado pelos autores para chegar aos resultados publicados.
- R-c: o revisor executa e confronta os resultados com o artigo, incluindo figuras e tabelas.

Regra local, em reivindicacoes.md:17: "R é atribuído se C1 a C6 forem reproduzidas". C7 não entra.

Situação geral dos critérios:
- R-a: não atendido. reivindicacoes.md (coluna "O README indica como reproduzir?") marca C1 a C5 como "parcial" e C6 como "não". O README não tem seção de experimentos nem de reivindicações; [README.md:74-85] traz só a sintaxe geral.
- R-b: não atendido. Nada descreve como evidence2.dd foi criada ou obtida, nem qual ambiente e quais passos produziram a Fig. 2. Não há scripts nem dados no repositório (índice de artefato.txt).
- R-c: só verificável por execução, e no caso da Fig. 2 impossível, porque falta a entrada.

C1. EVTX (assinatura ElfFile, chunks de 64 KiB): DEPENDE DE EXECUÇÃO, com risco alto.
- Implementação:
  - [src/state.c:381] `init_builtin(state, EVTX, "evtx", "ElfFile\0\0", NULL, 8, ...)`.
  - [src/extract.c:2474] `if (memcmp(buf, "ElfFile\0\0", 8) != 0)`.
  - [src/extract.c:2479] `chunk_count = htoi(&buf[0x18], FOREMOST_LITTLE_ENDIAN);`.
  - [src/extract.c:2489] `full_size = (uint64_t)chunk_count * 65536ULL;`.
  - [src/extract.c:2492-2508] corta no próximo cabeçalho ElfFile, se houver.
- Risco pelo conhecimento do formato EVTX, que não dá para verificar nos arquivos fornecidos: o deslocamento 0x18 do cabeçalho EVTX guarda o identificador do próximo registro, não o número de chunks. Além disso, o tamanho calculado ignora o bloco de cabeçalho de 4 KiB. O recorte pode sair maior (até o fim do buffer ou do próximo ElfFile) ou truncado. O artigo, na p. 6, §3, diz que o parser lê o número de chunks.
- Documentação: não há exemplo nem amostra EVTX. O comando `-t evtx,elf,exe` aparece só no artigo, p. 7, §4.1.
- O que observar na execução: rodar sobre uma imagem com um .evtx conhecido e verificar se o arquivo extraído abre em uma ferramenta de eventos (python-evtx, EvtxECmd ou o Visualizador de Eventos) com os mesmos registros do original.

C2. Scripts com shebang, mínimo de 32 bytes, mais que comentários: DEPENDE DE EXECUÇÃO, e o código está coerente com o artigo.
- Implementação:
  - [src/state.c:384] `init_builtin(state, SCRIPT, "script", "#!", ...)`.
  - [src/extract.c:2521] `const uint64_t MIN_SCRIPT_SIZE = 32;`.
  - [src/extract.c:2547-2554] varre até o primeiro caractere não imprimível.
  - [src/extract.c:2600-2612] exige conteúdo além de comentários.
- Divergências menores:
  - A extensão gerada é `.script`, enquanto o artigo (p. 7, §4.2) usa `00000002.sh` como exemplo. A Fig. 2 mostra `.script`.
  - A varredura com isprint corta scripts que têm UTF-8 fora do ASCII.
  - Scripts PowerShell sem shebang não são cobertos.
- O que observar na execução: um script com mais de 32 bytes, embutido numa imagem, sendo extraído com a linha `#!` e o corpo legível; um script só com comentários não deve ser extraído.

C3. Mach-O fat e thin: NÃO REPRODUZÍVEL pela evidência de código. A parte thin falha; a parte fat depende de execução.
- Os cabeçalhos de busca são os bytes em disco de binários little-endian:
  - [src/state.c:375] `"\xCE\xFA\xED\xFE"`.
  - [src/state.c:378] `"\xCF\xFA\xED\xFE"`.
- No parser:
  - [src/extract.c:2360] `uint32_t magic_le = read_le32(buf);`, com read_le32 definida como `htoi(buf, FOREMOST_LITTLE_ENDIAN)` em [src/helpers.c:353-355].
  - Em host little-endian, htoi não inverte os bytes ([src/helpers.c:273-274]). Os bytes CF FA ED FE viram 0xFEEDFACF e os bytes CE FA ED FE viram 0xFEEDFACE.
  - Só que o código compara com os valores invertidos: [src/extract.c:2363] `if (magic_le == 0xCEFAEDFE)` e [src/extract.c:2409] `if (magic_le == 0xCFFAEDFE)`.
  - Por isso, nos cabeçalhos thin registrados, as duas comparações falham e a função cai em [src/extract.c:2454] `return foundat + needle->header_len;` sem gravar nada.
- Conclusão: em x86-64 ou arm64, o carving de Mach-O thin, citado explicitamente no artigo (p. 6, §3), não deve ocorrer.
- O ramo fat ([src/extract.c:2327-2357], magic CAFEBABE lido como big-endian) é plausível. Esse mesmo magic coincide com arquivos .class do Java, o que pode gerar falsos positivos.
- O que reverteria essa conclusão: uma execução com um Mach-O thin de 64 bits (por exemplo, binário arm64 ou x86_64 de uma única arquitetura) dentro de uma imagem gerando `output/macho/*.macho` reconhecido por `file` ou `otool`.

C4. ELF de 32 e 64 bits delimitado pelos cabeçalhos de programa: DEPENDE DE EXECUÇÃO.
- Implementação:
  - [src/extract.c:2176-2239] trata ELF32 e [src/extract.c:2240-2306] trata ELF64.
  - Usa a união dos segmentos PT_LOAD: [src/extract.c:2213] `if (p_type_32 == 1 /* PT_LOAD */)`.
  - Só little-endian: [src/extract.c:2172] `if (ei_data != 1)`.
- Riscos:
  - read_le64 lê só 32 bits: [src/helpers.c:360-362] `return htoi(...)`. Não afeta arquivos pequenos.
  - O recorte termina no último PT_LOAD. A tabela de seções, que normalmente fica no fim do arquivo, tende a ficar de fora, o que contradiz a retenção de símbolos dita no artigo (p. 6). Um analisador ELF deve ler o cabeçalho e os segmentos, mas pode reclamar das seções.
  - Com `-t elf`, o tamanho máximo é 2 MB ([src/state.c:447-453]); no modo padrão "all", é 50 MB ([src/state.c:369]).
- O que observar na execução: um ELF32 e um ELF64 embutidos numa imagem gerando `.elf` em que `readelf -h -l` lê cabeçalho e segmentos corretamente.

C5. VirusTotal com `-x` e VT_API_KEY: DEPENDE DE EXECUÇÃO e de recurso externo (uma chave do VT, que não está no artefato).
- Implementação:
  - [src/main.c:131] `case 'x': set_mode(s, mode_virustotal);`.
  - [src/dir.c:275-283] calcula o SHA-256 do arquivo gravado e chama `vt_check_hash(sha256)`.
  - [src/vt_query.c:21] `VT_URL "https://www.virustotal.com/api/v3/files/"`.
  - [src/vt_query.c:164] envia o cabeçalho `x-apikey`.
  - [src/vt_query.c:180] faz um sscanf rígido sobre `last_analysis_stats`.
  - [src/dir.c:292-295] grava a coluna VT no audit.txt.
  - Documentação: [README.md:89-108].
- Divergências:
  - Sem chave, o código imprime `Error: VT_API_KEY environment variable is not set.` a cada arquivo ([src/vt_query.c:140-142]). Ele não pula a consulta de forma global e rotula o arquivo como `Clean (0)`, porque [src/dir.c:280-282] usa o VTResult zerado.
  - Com chave inválida, não há aviso, e a ausência de `last_analysis_stats` também resulta em `Clean (0)`. O artigo (p. 7, §4.1) diz que o programa emite aviso e pula as consultas.
  - O rótulo "Clean (n)" mostra o número de motores que não detectaram, e um hash desconhecido também aparece como "Clean (0)".
  - Não existe recovery.log com hashes, que o artigo promete na p. 7, §4.2. Uma busca por "recovery.log" no artefato não acha nada. O hash não é gravado em lugar nenhum.
  - O artigo diz que o hash pode ser SHA-1 ou SHA-256; o código usa só SHA-256.
- O que observar na execução: com uma chave válida e um arquivo de hash conhecidamente malicioso, a coluna VT mostrando `Malicious (n)` com n > 0 coerente com o site do VT. Sem chave, conferir o aviso e se a extração continua.

C6. Exemplo da Fig. 2 (`./foremost-ng -v -x evidence2.dd`): NÃO REPRODUZÍVEL.
- A entrada evidence2.dd, que pela Fig. 2 tem cerca de 2 GB (2845109643 bytes), não está no repositório (índice de artefato.txt). O artigo não diz onde obtê-la, e o README não fala dela.
- reivindicacoes.md:12 marca "não" para C6, e reivindicacoes.md:21 exige comparar os arquivos e offsets da Fig. 2. Essa comparação é impossível sem o dado.
- O que teria de ser observado: só com a imagem disponibilizada pelos autores. A execução teria de listar os 12 arquivos da Fig. 2 (elf, script, exe, zip) nos mesmos offsets, por exemplo 2228224 e 914484119.

C7. Arquitetura (não entra na regra; apenas inspecionada): parcialmente divergente.
- O "despachante" é uma cadeia if/else por tipo: [src/extract.c:2628-2694]. Os parsers são registrados à mão em [src/state.c:321-403] e [src/state.c:408-714]. Não existe uma interface uniforme com callback de validação separado.
- Para adicionar um formato é preciso alterar extract_file, init_all e set_search_def. Isso contradiz o artigo (p. 3), que afirma não ser necessário mexer no despachante.

Decisão para R: NÃO ATRIBUIR.
Os motivos são três: R-a e R-b não são atendidos na documentação; falta o dado necessário para C6, uma reivindicação principal; e o código indica que C3 (Mach-O thin) falha. Mesmo que C1, C2, C4 e C5 se confirmassem na execução, a regra C1 a C6 não fecharia.

Confiança de que o comitê oficial atribuiu R: 20.
Um comitê tolerante poderia ter atribuído R com amostras próprias, já que a ferramenta e suas funções básicas podem ser observadas. Mesmo assim, faltam o dado e o processo da Fig. 2.

O que precisaria ser observado na execução para mudar a decisão:
- Em primeiro lugar, os autores teriam de disponibilizar evidence2.dd ou uma imagem equivalente com instruções, e a execução teria de reproduzir os arquivos e offsets da Fig. 2.
- Mach-O thin teria de ser extraído na prática, o que desmentiria a análise de C3.
- Um EVTX extraído teria de abrir corretamente numa ferramenta de eventos.
- A coluna VT teria de aparecer coerente com uma chave válida.

======================================================================
D. LACUNAS E RISCOS
======================================================================
1. Dados ausentes: o repositório não traz nenhuma imagem de teste. evidence2.dd (Fig. 2) não está disponível e não há instruções para obtê-la.
2. README sem dependências de Linux, sem versões e sem exemplo mínimo. O Dockerfile usa `ubuntu:latest` e clona a HEAD do GitHub, então não reproduz o commit avaliado.
3. Página de manual (src/foremost-ng.8.gz) binária: o conteúdo da documentação de uso referida no README não pôde ser verificado.
4. Defeito provável no Mach-O thin: comparação de magic invertida em [src/extract.c:2363] e [src/extract.c:2409] frente a [src/helpers.c:353-355]. Precisa ser confirmado por execução.
5. EVTX: o tamanho é calculado a partir do deslocamento 0x18 ([src/extract.c:2479]). Pelo formato, esse campo não é o número de chunks, o que traz risco de recorte errado. Precisa ser confirmado por execução.
6. VirusTotal:
   - depende de chave externa e de um serviço que muda com o tempo;
   - o sscanf rígido depende do formato exato do JSON;
   - a verificação SSL está desativada ([src/vt_query.c:167-168]);
   - sem chave ou com chave inválida, o arquivo recebe "Clean (0)" em vez de a consulta ser pulada;
   - não há recovery.log nem registro de hash;
   - no modo `-w` a consulta ao VT nunca ocorre, porque [src/dir.c:222-231] retorna antes dela.
7. ELF: o recorte só pelos PT_LOAD tende a perder a tabela de seções; read_le64 lê só 32 bits.
8. Divergências entre artigo e código: extensão `.sh` contra `.script`; SHA-1 ou SHA-256 contra só SHA-256; arquitetura "plug-in" contra uma cadeia if/else.
9. Limite desta avaliação: as conclusões são analíticas, tiradas da leitura de código. Nenhuma compilação nem execução foi feita, e os pontos 4, 5 e 7 podem ser desmentidos pela execução.

{"F": {"decisao": "Não atribuir", "confianca": 60, "evidencias": ["instrucoes-oficiais.md:15", "README.md:3", "README.md:31-35", "README.md:84", "README.md:79", "Dockerfile:1", "Dockerfile:5", "Dockerfile:8", "src/Makefile:46", "src/main.c:226-228", "src/dir.c:209-300", "artefato.txt:índice (sem dados de exemplo; foremost-ng.8.gz binário)", "artigo.pdf:p.6-7 §4"]},
 "R": {"decisao": "Não atribuir", "confianca": 20, "evidencias": ["instrucoes-oficiais.md:19", "reivindicacoes.md:12", "reivindicacoes.md:17", "reivindicacoes.md:21", "artigo.pdf:p.8 Fig. 2", "artefato.txt:índice (evidence2.dd ausente)", "src/extract.c:2360", "src/extract.c:2363", "src/extract.c:2409", "src/helpers.c:353-355", "src/extract.c:2479", "src/extract.c:2521", "src/extract.c:2213", "src/dir.c:275-283", "src/vt_query.c:140-142", "src/vt_query.c:180", "README.md:89-108"],
       "por_reivindicacao": {"C1": "depende_execucao", "C2": "depende_execucao", "C3": "nao_reproduzivel", "C4": "depende_execucao", "C5": "depende_execucao", "C6": "nao_reproduzivel"}}}