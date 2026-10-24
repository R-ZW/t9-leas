AVALIAÇÃO ANALÍTICA: selos F e R, Foremost-NG (SBSeg 2025), versão bb812a22cb06ef87b5a2d877dfb6f40eb12d460d

Esta avaliação foi feita só por leitura. Não compilei nem executei o artefato, e nada do que segue afirma que algo funcionou.

A. MATERIAIS EXAMINADOS

- D:\Lab-artefatos\t9-trabalho\claude-c3\pacote\instrucoes-oficiais.md: lido por inteiro.
- D:\Lab-artefatos\t9-trabalho\claude-c3\pacote\reivindicacoes.md: lido por inteiro.
- D:\Lab-artefatos\t9-trabalho\claude-c3\pacote\artigo.pdf: as 8 páginas, inclusive as Figuras 1 e 2.
- D:\Lab-artefatos\t9-trabalho\claude-c3\pacote\artefato.txt: lido por inteiro nas linhas 1–2100 e 4205 até o fim. Isso cobre o índice, .gitignore, Dockerfile, LICENSE, README.md, src/Makefile, api.c, cli.c, config.c, dir.c, engine.c, extract.h, foremost.conf, helpers.c, main.c, main.h, ole.h, state.c, vt_query.c e vt_query.h. Do src/extract.c li o início (extract_zip), extract_exe (linhas 3890–4040 do arquivo único), extract_elf, extract_macho, extract_evtx, extract_script e o despachante extract_file. Não li os parsers legados (pdf, cpp, htm, ole, mov, wmv, riff, bmp, gif, mpg, mp4, png, jpeg, generic, reg e rar), que não pertencem a C1–C6.
- Arquivos binários que aparecem só no índice e não puderam ser examinados (evidência ausente): src/foremost-ng.8.gz (página de manual citada pelo README), screenshots/foremost-ng-01.png, screenshots/foremost-ng-02.png e windows_dlls/*.

Observação: o artefato não traz nenhuma imagem de disco nem amostra de teste. O índice (artefato.txt:9-49) lista apenas código, configuração, DLLs e capturas de tela.

B. SELO FUNCIONAL (F)

B.1 Critérios oficiais aplicáveis
[instrucoes-oficiais.md:15] "O artefato precisa ser executável e permitir a observação de funcionalidades. O README deve informar dependências, versões de dependências/linguagens/ambiente, ambiente de execução, instalação, execução e pelo menos um exemplo mínimo. O revisor deve executar o artefato e apresentar prova de execução e saídas no parecer. Ler código ou README, por si só, não constitui prova de funcionamento."

B.2 Situação de cada critério

F1. Executável, com funcionalidades observáveis: só verificável por execução.
- O código e o build parecem completos: [artefato.txt → src/Makefile:56] "SRC = main.c state.c helpers.c config.c cli.c engine.c dir.c extract.c api.c vt_query.c". O alvo Linux é [src/Makefile:69-70] "linux: CC += -D__LINUX ...".
- Risco: [src/main.c:222-223] "if (load_config_file(s)) { fatal_error(s, "Unable to load the config file");". Se não houver foremost.conf no diretório atual nem em /usr/local/etc ([src/config.c:223]), o programa aborta. Isso só aparece quando se executa fora de src/ sem ter feito make install.

F2. Dependências: não atendido para Linux no README.
- Para Linux, o README só diz [README.md:31-34] "### Linux / make / sudo make install". Ele cita curl apenas para BSD [README.md:39] e openssl@3 apenas para macOS [README.md:52-54].
- O código exige cabeçalhos de OpenSSL e libcurl: [src/vt_query.c:13-14] "#include <openssl/evp.h> / #include <curl/curl.h>" e [src/Makefile:46] "LINK_OPT += -lssl -lcrypto -lcurl".
- Os pacotes necessários só aparecem no Dockerfile, que o README não menciona: [Dockerfile:5] "gcc make git libssl-dev libcurl4-openssl-dev".

F3. Versões de dependências, linguagem e ambiente: não atendido.
- O README não informa nenhuma versão, exceto "openssl@3" para macOS [README.md:54].
- O Dockerfile usa uma imagem sem versão fixa [Dockerfile:1] "FROM ubuntu:latest" e clona o HEAD do GitHub, não o commit avaliado [Dockerfile:8] "RUN git clone https://github.com/cristianzsh/foremost-ng.git".

F4. Ambiente de execução: atendido em parte.
- [README.md:3] "`foremost-ng` is a Linux-based file recovery tool". Há seções para Linux, BSD, macOS e compilação cruzada para Windows [README.md:31-68].

F5. Instalação: atendido, com ressalvas.
- [README.md:27-28] "tar xzvf foremost-ng-<version>.tar.gz / cd foremost-ng-<version>/src". O README parte de um tarball, mas não diz onde obtê-lo.
- As instruções do artigo estão erradas para este repositório: [artigo.pdf:p.6 §4] "cd foremost-ng / make". O índice mostra que só existe src/Makefile [artefato.txt:16], sem Makefile na raiz.

F6. Execução: atendido em parte.
- O README dá só a sintaxe geral e manda consultar a man page: [README.md:79] "man foremost-ng" e [README.md:84] "foremost-ng [options] [image_or_device]". A man page é binária e não pôde ser examinada (evidência ausente).
- As opções aparecem no código: [src/main.c:121] getopt "o:b:c:t:s:i:k:hqmQTadvVwx" e a ajuda em [src/main.c:92-112].

F7. Pelo menos um exemplo mínimo: não atendido no README.
- O README não traz nenhum comando concreto com entrada e saída esperada, e o repositório não inclui dados de teste (índice, artefato.txt:9-49).
- O artigo traz exemplos ([artigo.pdf:p.7 §4.1] "foremost-ng -t evtx,elf,exe -i disk.img") e indica amostras externas ([artigo.pdf:p.7] "Carving test samples can be downloaded from https://dftt.sourceforge.net"), mas o critério se refere ao README.

F8. Prova de execução e saídas no parecer: só verificável por execução.

B.3 Decisão para F: Não atribuir.
Pela regra pedida, há evidência documental de que critérios obrigatórios do README não são atendidos: faltam versões (F3) e exemplo mínimo (F7), e as dependências de Linux estão incompletas (F2). Mesmo sem essas falhas, a decisão máxima seria Indeterminado, porque F1 e F8 exigem execução. As falhas são documentais e fáceis de corrigir, e o comitê pode tê-las relevado na fase de resposta dos autores [instrucoes-oficiais.md:11].

B.4 Confiança de que o comitê atribuiu F: 55/100.
É uma ferramenta C simples, que compila com make e tem Dockerfile, e qualquer imagem de disco serve para observar a extração. Por outro lado, o README é fraco nos itens exigidos.

B.5 O que precisaria ser observado na execução para mudar a decisão (para Atribuir)
- Compilação sem erros em um ambiente declarado (por exemplo, Ubuntu com libssl-dev e libcurl4-openssl-dev), a partir de src/ e do commit bb812a22.
- Execução de um exemplo mínimo, como `foremost-ng -v -t elf,script,exe -i <imagem> -o out`, gerando subdiretórios por formato, arquivos nomeados <bloco>.<sufixo> e um audit.txt com a tabela ID/Name/Size/Offset/Comment/VT.
- Que o comitê considere as lacunas do README sanáveis (ou que os autores as corrijam na resposta).

C. SELO REPRODUTÍVEL (R)

C.1 Critérios oficiais aplicáveis
[instrucoes-oficiais.md:19] "O revisor deve conseguir reproduzir as principais reivindicações do artigo. A documentação do artefato deve trazer instruções de execução dessas reivindicações e descrever o processo usado pelos autores para chegar aos resultados publicados. O revisor deve executar os experimentos e confrontar os resultados com os do artigo, incluindo figuras/tabelas pertinentes".
Regra fixada: [reivindicacoes.md:17] "R é atribuído se C1 a C6 forem reproduzidas."
Critério de reprodução: [reivindicacoes.md:21] "Em C6, comparam-se os arquivos e offsets da Fig. 2. As contagens do VirusTotal mudam com o tempo".

C.2 Critérios gerais
- R1, instruções de execução das reivindicações: não atendido. O README não tem nenhuma seção de experimentos. A própria tabela de reivindicações marca a coluna "O README indica como reproduzir?" como "parcial" para C1–C5 e "não" para C6 [reivindicacoes.md:7-12].
- R2, descrição do processo usado pelos autores: não atendido. Nada descreve como foi produzido evidence2.dd nem qual era o seu conteúdo.
- R3, dados necessários: não atendido para C6, porque evidence2.dd não está no artefato (índice, artefato.txt:9-49) nem é identificado no artigo. Para C1–C5 não há amostras incluídas, mas o revisor pode montar as próprias.
- R4, execução e confronto com o artigo: só verificável por execução.

C.3 Avaliação por reivindicação

C1, EVTX (assinatura ElfFile, chunks de 64 KiB, log extraído): depende de execução.
- Implementação: [src/extract.c:2474] "if (memcmp(buf, "ElfFile\0\0", 8) != 0)" e [src/extract.c:2479] "chunk_count = htoi(&buf[0x18], FOREMOST_LITTLE_ENDIAN);". O tamanho é [2489] "full_size = (uint64_t)chunk_count * 65536ULL;", e o corte acontece no próximo cabeçalho [2494-2505]. O tipo é registrado em [src/state.c:381] e [src/state.c:688-694] (-t evtx).
- Lacunas: não há amostra EVTX e não há instrução de teste.
- Risco técnico (observação minha, sem respaldo no pacote): pelo que sei do formato EVTX, o deslocamento 0x18 guarda o identificador do próximo registro, e a contagem de chunks fica em 0x2A. Além disso, o cálculo ignora o cabeçalho de 4 KiB do arquivo. O resultado provável é extrair dados demais até o limite do buffer ([2486-2487] "full_size = buflen") ou cortar o arquivo. Se o .evtx extraído continua legível precisa ser verificado na execução.

C2, scripts (shebang, mínimo de 32 bytes, mais que comentários): depende de execução.
- Implementação compatível com o artigo: [src/extract.c:2521] "const uint64_t MIN_SCRIPT_SIZE = 32;", o laço de caracteres imprimíveis [2547-2554], a rejeição de corpo só com comentários [2600-2612] "if (*p != '#') { ... found_real = 1;" e o registro do tipo [src/state.c:384, 695-697].
- Os arquivos saem com sufixo ".script", não ".sh" como diz o artigo [artigo.pdf:p.7 §4.2]. A Fig. 2 é coerente com o código ("00005492.script").
- Não há amostra incluída.

C3, Mach-O fat e thin: depende de execução.
- Fat: [src/extract.c:2327] reconhece a assinatura CAFEBABE e calcula o tamanho por "arch_fileoff + arch_size" [2342-2347].
- Thin de 32 bits: LC_SEGMENT [2387-2394]. Thin de 64 bits: LC_SEGMENT_64 [2433-2441]. Os tipos são registrados em [src/state.c:372-379].
- Riscos:
  - [src/helpers.c:360-361] "uint64_t read_le64(...) { return htoi(buf, ...)": a função lê só 32 bits.
  - Pelo formato segment_command_64 (conhecimento meu, não do pacote), os deslocamentos +32 e +40 correspondem a vmsize e fileoff, e não a fileoff e filesize. O provável é extrair um pouco além do fim do binário.
  - Há só o limite por buflen, sem max_len [2448]. Binários Mach-O big-endian (thin) não são reconhecidos.
- Não há amostra incluída.

C4, ELF de 32 e 64 bits delimitado pelos cabeçalhos de programa: depende de execução.
- Implementação: [src/extract.c:2172] "if (ei_data != 1) { return ...". Só ELF little-endian é aceito; o artigo não diz isso.
- O tamanho é o maior fim entre os segmentos PT_LOAD [2213-2219 e 2279-2285].
- Risco: a tabela de cabeçalhos de seção, que fica no fim do arquivo, não entra no cálculo. O artigo diz que o arquivo extraído "retains ... symbol information" [artigo.pdf:p.6], mas é possível que o readelf -S acuse um arquivo truncado. O critério esperado, "estruturalmente legível", tem de ser verificado com um analisador ELF.
- Não há amostra incluída.

C5, VirusTotal (-x e VT_API_KEY, consulta por hash, resultado registrado): depende de execução, que exige uma chave da API.
- A opção -x existe [src/main.c:131]. O hash SHA-256 e a consulta ficam em [src/dir.c:275-282] "sha_checksum(fn, "sha256", sha256); vt = vt_check_hash(sha256);". A URL e o cabeçalho estão em [src/vt_query.c:21, 164], e o rótulo vai para o audit [src/dir.c:292-295].
- Sem chave: [src/vt_query.c:140-142] "Error: VT_API_KEY environment variable is not set." e retorno antes da consulta. A extração continua, como diz o artigo, mas o audit registra "Clean (0)" em vez de indicar que a consulta foi pulada.
- Chave inválida, arquivo desconhecido ou falha de parsing também resultam em "Clean (0)" ou "Clean (-1)" sem nenhum aviso (vt_query.c:137, 176-189). Isso contradiz [artigo.pdf:p.7] "If the API key is missing or invalid ... will emit a warning".
- O parsing depende de ordem e espaçamento exatos do JSON: [src/vt_query.c:180] sscanf com o padrão "\"last_analysis_stats\": {\"malicious\": %d, \"suspicious\": %*d, \"undetected\": %d".
- O hash não é gravado em nenhum log. O artigo promete "recovery.log ... hash values" [artigo.pdf:p.7 §4.2], mas o código só gera audit.txt [src/main.h:162]. Para associar hash e resultado, o revisor teria de calcular o hash por fora.

C6, Fig. 2 (`./foremost-ng -v -x evidence2.dd`): não reprodutível.
- Falta o dado necessário. evidence2.dd (2.845.109.643 bytes, segundo a Fig. 2 [artigo.pdf:p.8]) não está no artefato (índice, artefato.txt:9-49), não tem origem identificada e não há instrução de reprodução [reivindicacoes.md:12] "não".
- Pela leitura, a Fig. 2 é coerente com o código:
  - Os nomes são bloco/512, por exemplo offset 2228224 → "00004352.elf", seguindo [src/dir.c:214, 239-241].
  - O cabeçalho da tabela corresponde a [src/engine.c:175-177].
  - Os rótulos "Clean (n)" e "Malicious (n)" correspondem a [src/dir.c:280-282].
  - A versão 1.5.7 confere com [src/Makefile:4].
- Mesmo assim, sem a imagem, os arquivos e offsets não podem ser comparados.

C7, arquitetura extensível (fora da regra de R; só inspeção):
- O despachante é uma cadeia de if/else por tipo [src/extract.c:2628-2697], e os tipos são registrados em init_all e set_search_def [src/state.c:321-714].
- Para incluir um parser é preciso editar o despachante, o que contradiz [artigo.pdf:p.3] "does not require modifying the dispatcher logic itself".
- Não existe um callback de validação separado, como sugere a Fig. 1.

C.4 Decisão para R: Não atribuir.
A regra exige C1 a C6. C6 falha por falta do dado necessário, que é o exemplo explícito de "Não atribuir" na regra pedida. Além disso, a documentação não traz instruções de reprodução nem o processo dos autores (R1, R2).

C.5 Confiança de que o comitê atribuiu R: 15/100.

C.6 O que precisaria ser observado para mudar a decisão
- Disponibilização de evidence2.dd, ou de um conjunto equivalente documentado, com instruções de reprodução. Depois, uma execução cujos arquivos e offsets coincidam com a Fig. 2: 4 ELF, 1 script, 5 EXE e 2 ZIP nos offsets mostrados.
- C1: um .evtx extraído de imagem conhecida e aberto sem erro por uma ferramenta de eventos (python-evtx, EvtxECmd ou o Visualizador de Eventos), com o tamanho conferido.
- C2: scripts bash, python e powershell com shebang extraídos com a linha do interpretador e o corpo intactos; fragmentos com menos de 32 bytes ou só com comentários descartados.
- C3: binários Mach-O fat e thin (32 e 64 bits) extraídos e reconhecidos por file, otool ou lipo, com o tamanho conferido.
- C4: ELF de 32 e 64 bits extraídos e legíveis por readelf -h -l (e, se possível, -S).
- C5: com uma chave válida, o rótulo no audit.txt coerente com a consulta manual do mesmo SHA-256 no VirusTotal; sem chave, aviso emitido e extração concluída.

D. LACUNAS E RISCOS

1. Evidência ausente:
   - Não há dados de teste no artefato.
   - evidence2.dd não está disponível.
   - A man page (foremost-ng.8.gz) e as capturas de tela são binárias e não puderam ser examinadas.
   - Não há registro de execução pelos autores além da Fig. 2.
2. README: faltam versões, exemplo mínimo e dependências de Linux. As dependências só aparecem no Dockerfile, que usa ubuntu:latest e clona o HEAD do repositório, e não o commit avaliado.
3. Divergências entre o artigo e o código:
   - Instalação: o artigo manda rodar make na raiz, mas o Makefile está em src/.
   - Saída: o artigo fala em recovery.log com hashes e arquivos .sh; o código gera audit.txt sem hashes e arquivos .script.
   - Aviso de chave inválida: o artigo promete, o código não emite.
   - Despachante: o artigo diz que incluir um parser não exige alterá-lo; no código, exige.
4. Riscos técnicos que só a execução confirma:
   - Campo usado como contagem de chunks no EVTX (0x18) e ausência do cabeçalho de 4 KiB no cálculo do tamanho.
   - Deslocamentos de LC_SEGMENT_64 e read_le64 lendo só 32 bits (Mach-O).
   - ELF sem a tabela de seções.
   - Parsing frágil do JSON do VirusTotal.
   - Rótulo "Clean (0)" ambíguo: não distingue arquivo limpo de falha, chave ausente ou arquivo desconhecido.
   - Arquivos que cruzam o limite do bloco de leitura de 100 MB são cortados (limite por buflen).
   As observações sobre os formatos EVTX, Mach-O e ELF vêm do meu conhecimento técnico, não do pacote.
5. Variação externa: as contagens do VirusTotal mudam com o tempo e dependem da cota da API, o que afeta C5 e a coluna VT da Fig. 2. A regra já aceita essa diferença.
6. Processo: a decisão oficial pode ter levado em conta a resposta dos autores [instrucoes-oficiais.md:11], que não consta do pacote.

{"F": {"decisao": "Não atribuir", "confianca": 55, "evidencias": ["instrucoes-oficiais.md:15", "artefato.txt:README.md:31-34", "artefato.txt:README.md:79-84", "artefato.txt:Dockerfile:1-8", "artefato.txt:src/Makefile:46", "artefato.txt:src/vt_query.c:13-14", "artefato.txt:src/main.c:222-223", "artefato.txt:índice (linhas 9-49)", "artigo.pdf:p.6 §4", "artigo.pdf:p.7 §4.1"]},
 "R": {"decisao": "Não atribuir", "confianca": 15, "evidencias": ["instrucoes-oficiais.md:19", "reivindicacoes.md:12", "reivindicacoes.md:17", "artigo.pdf:p.8 Fig. 2", "artefato.txt:índice (linhas 9-49)", "artefato.txt:src/extract.c:2474-2516", "artefato.txt:src/extract.c:2519-2622", "artefato.txt:src/extract.c:2314-2455", "artefato.txt:src/extract.c:2147-2309", "artefato.txt:src/dir.c:275-295", "artefato.txt:src/vt_query.c:136-198", "artefato.txt:src/helpers.c:360-361"],
       "por_reivindicacao": {"C1": "depende_execucao", "C2": "depende_execucao", "C3": "depende_execucao", "C4": "depende_execucao", "C5": "depende_execucao", "C6": "nao_reproduzivel"}}}