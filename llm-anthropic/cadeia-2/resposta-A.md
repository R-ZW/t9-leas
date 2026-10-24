AVALIAÇÃO ANALÍTICA: Foremost-NG (SBSeg 2025), selos F e R
Não executei nem compilei o artefato. Tudo abaixo vem da leitura dos arquivos. Quando digo que algo "falharia", é uma previsão feita a partir do código, não algo que eu tenha observado rodando.

Resultado: **F = Não atribuir** e **R = Não atribuir**. Em F, o motivo são lacunas na documentação. Em R, falta o dado da Fig. 2 e há um defeito no parser de Mach-O "thin".

======================================================================
A. MATERIAIS EXAMINADOS
======================================================================
Abri somente os quatro arquivos de D:\Lab-artefatos\t9-trabalho\claude-c2\pacote:

1. instrucoes-oficiais.md: li inteiro.
2. reivindicacoes.md: li inteiro.
3. artigo.pdf: li as 8 páginas, com texto e imagem de cada página, inclusive a Fig. 2.
4. artefato.txt: li o índice (linhas 9–49) e, por inteiro, .gitignore, Dockerfile, LICENSE, README.md, src/Makefile, src/api.c, src/cli.c, src/vt_query.c, src/vt_query.h e src/main.c.
   - Li trechos de src/config.c (load_config_file), src/dir.c (write_to_disk), src/engine.c (laço de busca, linhas 243–367), src/extract.c (linhas 2137–2697: ELF, Mach-O, EVTX, script e o despachante), src/helpers.c (htos/htoi/htoll e read_le*/read_be32), src/main.h (macros e protótipos) e src/state.c (init_all, set_search_def, partes de 327–714).
   - Não li inteiras as outras partes de extract.c (parsers antigos) e de state.c.
   - O artefato.txt só lista no índice, sem conteúdo, os arquivos binários: screenshots/*.png, src/foremost-ng.8.gz (página de manual) e windows_dlls/*.dll. Registro esse conteúdo como evidência ausente.

Nota sobre as citações:
- Trechos do código e do README são transcritos. O LICENSE (MIT) permite.
- O artigo é citado por página e seção, em paráfrase. Fiz uma única citação literal curta.

======================================================================
B. SELO FUNCIONAL (F)
======================================================================
B.1 Critérios oficiais aplicáveis
[instrucoes-oficiais.md:15]: "O artefato precisa ser executável e permitir a observação de funcionalidades. O README deve informar dependências, versões de dependências/linguagens/ambiente, ambiente de execução, instalação, execução e pelo menos um exemplo mínimo. O revisor deve executar o artefato e apresentar prova de execução e saídas no parecer. Ler código ou README, por si só, não constitui prova de funcionamento."

Daí saem estes critérios:
- F1: dependências
- F2: versões
- F3: ambiente
- F4: instalação
- F5: execução
- F6: exemplo mínimo
- F7: executável, com funcionalidades observáveis
- F8: prova de execução

B.2 Situação de cada critério

**F1 – Dependências: parcialmente atendido.**
- [artefato.txt: README.md:39–43]: "Make sure ```curl``` is installed:" (só na seção BSD). [README.md:52–54]: "brew install openssl@3" (só no macOS).
- A seção Linux [README.md:31–35] traz apenas "make / sudo make install". Não cita libssl-dev nem libcurl-dev, embora o Makefile faça a ligação com elas: [src/Makefile:46] "LINK_OPT += -lssl -lcrypto -lcurl".
- O Dockerfile lista as dependências: [Dockerfile:5] "gcc make git libssl-dev libcurl4-openssl-dev". Mas o README não menciona o Dockerfile.

**F2 – Versões de dependências, linguagem e ambiente: não atendido.**
- O README não traz nenhuma versão de gcc, OpenSSL, libcurl ou sistema operacional.
- O Dockerfile não fixa versões: [Dockerfile:1] "FROM ubuntu:latest".
- O Dockerfile também clona o HEAD do GitHub, e não o commit avaliado (bb812a22): [Dockerfile:8] "RUN git clone https://github.com/cristianzsh/foremost-ng.git /opt/foremost-ng".
- O único número de versão é o da própria ferramenta: [src/Makefile:4] "VERSION = 1.5.7".

**F3 – Ambiente de execução: parcialmente atendido.**
- Plataformas citadas: [README.md:31, 37, 50, 62] "### Linux", "### BSD", "### macOS", "### Cross compiling for Windows". Faltam as versões do sistema e os requisitos de hardware.

**F4 – Instalação: atendido na documentação.**
- [README.md:27–28]: "tar xzvf foremost-ng-<version>.tar.gz" / "cd foremost-ng-<version>/src". [README.md:33–34]: "make" / "sudo make install".
- Inconsistência: o artigo, na p. 6, §4, manda rodar `make` na raiz do repositório. Pelo índice, porém, o único Makefile fica em src/ [artefato.txt:16] "src/Makefile". O README está correto e o artigo não.

**F5 – Execução: parcialmente atendido.**
- [README.md:76–84]: "For full details, refer to the manual page: man foremost-ng" e "Basic syntax: foremost-ng [options] [image_or_device]".
- A página de manual é binária e foi omitida [artefato.txt:25] "src/foremost-ng.8.gz | 2914 | binário (omitido)". Evidência ausente.
- As opções estão no código: [src/main.c:121] getopt "o:b:c:t:s:i:k:hqmQTadvVwx".

**F6 – Exemplo mínimo: não atendido no README.**
- O README traz só a sintaxe genérica (README.md:84). Não há exemplo concreto com arquivo de entrada nem dados de teste. O índice (artefato.txt:9–49) não contém imagem ou amostra alguma.
- O artigo traz exemplos concretos (p. 7, §4.1) e aponta amostras no site dftt.sourceforge.net, mas não diz qual arquivo usar.

**F7 – Executável, com funcionalidades observáveis: só verificável por execução.**
- O código é coerente com uma aplicação de linha de comando que compila. O alvo padrão é [src/Makefile:65] "all: $(SYS) goals", e o ponto de entrada é [src/main.c:197] "int main(int argc, char **argv)".
- O arquivo de configuração tem fallback: [src/config.c:223] "/usr/local/etc/foremost.conf".

**F8 – Prova de execução: só verificável por execução.**
- Pelo critério oficial, ler o código não basta.

B.3 Decisão para F: **NÃO ATRIBUIR**
- Pela regra fixada, F2 (versões) e F6 (exemplo mínimo no README) são exigências obrigatórias ("O README deve informar…") e não estão atendidas. F1 e F5 estão só parcialmente atendidos.
- Essas falhas são leves e fáceis de corrigir. O artefato parece simples de compilar (C, make, duas bibliotecas comuns) e há um Dockerfile.
- Um comitê que leve em conta os exemplos do artigo (§4.1) e a resposta dos autores poderia atribuir F depois de executar.

B.4 Confiança de que o comitê oficial atribuiu F: **60**

B.5 O que mudaria a decisão em uma execução
- Para Atribuir:
  - Compilar com `make` em src/ (ou pelo Dockerfile) sem erros. Atenção a compiladores recentes, por exemplo GCC 14 do ubuntu:latest.
  - Rodar `foremost-ng -h` e conferir a ajuda descrita em src/main.c:92–112.
  - Rodar `foremost-ng -t elf,script -i <imagem> -o out` sobre uma imagem montada pelo revisor e observar out/audit.txt e os subdiretórios por tipo.
  - Registrar as versões efetivas de gcc, OpenSSL e libcurl.
- Para manter Não atribuir: falha de compilação, falha de execução, ou a exigência de que o README documente versões e um exemplo.

======================================================================
C. SELO REPRODUTÍVEL (R): POR REIVINDICAÇÃO
======================================================================
C.1 Critérios oficiais aplicáveis
[instrucoes-oficiais.md:19]: "O revisor deve conseguir reproduzir as principais reivindicações do artigo. A documentação do artefato deve trazer instruções de execução dessas reivindicações e descrever o processo usado pelos autores para chegar aos resultados publicados. O revisor deve executar os experimentos e confrontar os resultados com os do artigo, incluindo figuras/tabelas pertinentes".

Daí saem estes critérios:
- R1: instruções de execução para cada reivindicação
- R2: descrição do processo que gerou os resultados publicados
- R3: reprodução observada, comparada com figuras e tabelas

Regra local [reivindicacoes.md:17]: "R é atribuído se C1 a C6 forem reproduzidas." Critério de reprodução [reivindicacoes.md:21]: "Em C6, comparam-se os arquivos e offsets da Fig. 2."

R1: parcial em C1–C5 e ausente em C6 e C7, conforme a coluna do próprio reivindicacoes.md (linhas 7–13). O README não tem seção de experimentos.
R2: **não atendido**. Nenhum arquivo descreve como foi gerada ou obtida a imagem evidence2.dd da Fig. 2. Ela não aparece no índice (artefato.txt:9–49).
R3: só verificável por execução.

C.2 Por reivindicação

**C1 – EVTX ("ElfFile", chunks de 64 KiB): DEPENDE DE EXECUÇÃO, com risco.**
- A assinatura está registrada: [src/state.c:381] `init_builtin(state, EVTX, "evtx", "ElfFile\0\0", NULL, 8, 0, 100 * MEGABYTE, TRUE);`. O tipo também é aceito em -t [src/state.c:688].
- Verificação e cálculo do tamanho:
  - [src/extract.c:2474] `if (memcmp(buf, "ElfFile\0\0", 8) != 0)`
  - [src/extract.c:2478–2479] `// Read chunk_count at offset 0x18` / `chunk_count = htoi(&buf[0x18], ...)`
  - [src/extract.c:2489] `full_size = (uint64_t)chunk_count * 65536ULL;`
  - O corte vai até o próximo cabeçalho [2494–2505].
- Bate com o artigo (p. 6, §3, item EVTX).
- Risco de corretude: esta parte usa conhecimento do formato EVTX, não evidência do pacote. No cabeçalho EVTX, o deslocamento 0x18 guarda o identificador do próximo registro, e a contagem de chunks fica em 0x2A. Além disso, o cálculo não soma o bloco de cabeçalho de 4 KiB. Na prática, o tamanho tende a ser limitado pelo buffer ou pelo próximo "ElfFile". O .evtx extraído pode sair maior ou truncado, e só a execução mostra se uma ferramenta de eventos consegue lê-lo.
- Não há amostra EVTX no artefato.

**C2 – Scripts por shebang, ≥ 32 bytes, com mais que comentários: DEPENDE DE EXECUÇÃO. O código corresponde bem à descrição.**
- [src/state.c:384] `init_builtin(state, SCRIPT, "script", "#!", ...)`
- [src/extract.c:2521] `const uint64_t MIN_SCRIPT_SIZE = 32;`
- [src/extract.c:2549] `if (isprint(c) || c == '\n' || c == '\r' || c == '\t')`
- [src/extract.c:2601–2603] `if (*p != '#') { // Found something other than whitespace or '#' -> valid body`
- Bate com o artigo (p. 6, §3, item Script Files).
- Pequenas divergências:
  - A extensão gerada é ".script", não ".sh" como diz o artigo na p. 7, §4.2. A Fig. 2 mostra ".script", o que concorda com o código.
  - Caracteres fora do ASCII interrompem o carving.
  - Não há detecção de "Unicode signatures" (p. 2). Isso não faz parte de C2.

**C3 – Mach-O fat e thin: NÃO REPRODUTÍVEL na parte "thin". É uma previsão analítica forte e deve ser confirmada em execução.**
- Fat: implementado, com leitura big-endian da tabela fat_arch: [src/extract.c:2327] `if (buf[0] == 0xCA && buf[1] == 0xFE && buf[2] == 0xBA && buf[3] == 0xBE)` e [2333] `read_be32(&buf[4])`.
- Thin: os cabeçalhos registrados são os bytes CE FA ED FE e CF FA ED FE [src/state.c:375, 378]. O código lê assim:
  - [src/extract.c:2360] `uint32_t magic_le = read_le32(buf);`
  - [src/extract.c:2363] `if (magic_le == 0xCEFAEDFE)`
  - [src/extract.c:2409] `if (magic_le == 0xCFFAEDFE)`
- O read_le32 usa htoi, que só troca a ordem dos bytes em host big-endian:
  - [src/helpers.c:353–354] `uint32_t read_le32(unsigned char *buf) { return htoi(buf, FOREMOST_LITTLE_ENDIAN);`
  - [src/helpers.c:273–274] `if ((endian == FOREMOST_BIG_ENDIAN && BYTE_ORDER == LITTLE_ENDIAN) || (endian == FOREMOST_LITTLE_ENDIAN && BYTE_ORDER == BIG_ENDIAN))`
- Em host little-endian (x86-64 ou ARM64 comuns), os bytes CE FA ED FE viram 0xFEEDFACE, e CF FA ED FE vira 0xFEEDFACF. Nenhum dos dois é igual às constantes comparadas.
- Resultado: a função cai em [2454] `return foundat + needle->header_len;` e nenhum Mach-O thin é gravado.
- O resultado esperado da reivindicação ("fat e thin", reivindicacoes.md:9) não seria atingido na parte thin.

**C4 – ELF de 32 e 64 bits pelos program headers: DEPENDE DE EXECUÇÃO.**
- Assinatura [src/state.c:369]. Lógica de 32/64 bits e união dos PT_LOAD em [src/extract.c:2168–2176] `unsigned char ei_class = buf[4];` e em [2213] `if (p_type_32 == 1 /* PT_LOAD */)` e [2279], com gravação em [2303] `needle->suffix = "elf";`. O tipo é aceito em -t [src/state.c:447].
- Bate com o artigo (p. 6, item ELF).
- Riscos:
  - O tamanho é o fim do último PT_LOAD. A tabela de cabeçalhos de seção e as seções que não são carregadas (.symtab, .strtab), em geral no fim do arquivo, ficariam de fora. Isso contraria a afirmação do artigo de que as informações de símbolos são preservadas. Um `readelf -h` deve funcionar, mas `readelf -S` pode acusar truncamento.
  - O read_le64 usa htoi de 32 bits [src/helpers.c:360–361], o que é inofensivo para arquivos menores que 4 GiB.
  - Só ELF little-endian é tratado [src/extract.c:2172].

**C5 – VirusTotal com -x e VT_API_KEY: DEPENDE DE EXECUÇÃO e de recurso externo (chave pessoal do VirusTotal).**
- Ativação: [src/main.c:131] `case 'x': set_mode(s, mode_virustotal); break;`.
- Hash e consulta:
  - [src/dir.c:275–279] `if (get_mode(s, mode_virustotal)) { ... sha_checksum(fn, "sha256", sha256); vt = vt_check_hash(sha256);`
  - [src/vt_query.c:21] `#define VT_URL "https://www.virustotal.com/api/v3/files/"`
  - [src/vt_query.c:164] `"x-apikey: %s"`
- O resultado vai para o audit: [src/dir.c:292–295] `audit_msg(s, "%4d: %-20s %10s %12llu  %-24s  %-15s", ... nd->vt_label);`.
- O README documenta o recurso [README.md:89–101].
- Divergências e riscos:
  1. Sem chave, o código imprime o erro a cada arquivo, [src/vt_query.c:141] `"Error: VT_API_KEY environment variable is not set.\n"`, e devolve {0,0,0}. O audit então registra "Clean (0)" [src/dir.c:281], e não "consulta pulada" (artigo, p. 7, §4.1). A consulta HTTP de fato não acontece, então "carving sem consulta" se cumpre, mas o rótulo engana.
  2. O hash não é gravado no audit. O artigo, na p. 7, §4.2, promete um "recovery.log" com hashes, mas o código usa [src/main.h:162] `#define AUDIT_FILE_NAME "audit.txt"`. Para associar consulta e hash, o revisor teria de calcular o SHA-256 por conta própria.
  3. A leitura da resposta usa sscanf com formato JSON rígido [src/vt_query.c:180] `"\"last_analysis_stats\": {\"malicious\": %d, \"suspicious\": %*d, \"undetected\": %d"`. Ela depende da ordem e da formatação atuais da API. Se falhar, o rótulo sai "Clean (-1)".
  4. A verificação TLS está desligada [src/vt_query.c:167–168]. Isso é coerente com o artigo, p. 3.

**C6 – Fig. 2 (`./foremost-ng -v -x evidence2.dd`): NÃO REPRODUTÍVEL. Falta o dado.**
- O artigo (p. 7, §4.2, e p. 8, Fig. 2) mostra 12 arquivos (ELF, script, EXE, ZIP) com offsets, extraídos de "evidence2.dd" (2845109643 bytes).
- Esse arquivo não está no índice do artefato (artefato.txt:9–49). Nem o README nem o artigo dizem como obtê-lo ou gerá-lo. O artigo só aponta genericamente para dftt.sourceforge.net (p. 7).
- reivindicacoes.md:12 já registra que o README não indica como reproduzir ("não").
- A sintaxe com entrada posicional é suportada [src/main.c:241–252], mas os offsets da Fig. 2 não podem ser comparados sem a imagem. É o caso típico da regra "falta o dado necessário para uma reivindicação principal".

**C7 – Arquitetura extensível (fora da regra de R): inspeção mostra consistência parcial.**
- Há um registro de assinaturas [src/state.c:366–385, init_builtin] e um laço genérico de busca [src/engine.c:248–337].
- O despachante, porém, é uma cadeia if/else por tipo [src/extract.c:2680–2687] `} else if (needle->type == ELF) { return extract_elf(...)`. Um parser novo exige mudar o despachante, o set_search_def e o enum em main.h. Isso contraria a frase do artigo (p. 3) de que adicionar parsers "does not require modifying the dispatcher logic".
- C7 não tem experimento e não entra na decisão. Por isso ficou fora do bloco JSON, cujos valores não se aplicam a uma reivindicação sem experimento.

C.3 Decisão para R: **NÃO ATRIBUIR**
- C6 não tem o dado de entrada (evidence2.dd) nem a descrição do processo (R2).
- Há evidência no código de que a parte thin de C3 não funciona em hosts little-endian.
- A documentação não traz instruções por reivindicação (R1 parcial ou ausente).

C.4 Confiança de que o comitê oficial atribuiu R: **25**
Um comitê leniente poderia aceitar a reprodução qualitativa sobre amostras do DFTT e não testar Mach-O thin.

C.5 O que mudaria a decisão em uma execução
- C6 só pode virar "reproduzível" se os autores fornecerem evidence2.dd, ou uma receita para gerá-lo, e os nomes e offsets da Fig. 2 coincidirem. Sem isso, R continua Não atribuir.
- C3: carregar uma imagem com um Mach-O thin x86_64 (bytes CF FA ED FE) e outro fat, e conferir se out/macho/ recebe os dois. Se o thin for extraído em host x86-64, a previsão acima está errada e C3 vira dependente apenas da validação com `otool`/`file`.
- C1: extrair um .evtx de uma imagem com logs conhecidos e abri-lo com um parser de EVTX (python-evtx, EvtxECmd ou o Visualizador de Eventos), comparando o tamanho com o original.
- C2: extrair scripts bash, python e pwsh com shebang e conferir a linha do interpretador e o corpo. Conferir também que scripts com menos de 32 bytes ou só com comentários são descartados.
- C4: extrair ELF de 32 e de 64 bits e rodar `readelf -h -l -S`, observando se há truncamento da tabela de seções.
- C5: com VT_API_KEY válida, rodar `-x` sobre um arquivo de hash conhecido e malicioso (por exemplo, EICAR) e conferir "Malicious (n)". Sem a chave, observar o aviso e o rótulo "Clean (0)". Conferir também se o sscanf lê o JSON atual da API.

======================================================================
D. LACUNAS E RISCOS
======================================================================
1. **Dado ausente.** Não há evidence2.dd nem amostra alguma no artefato (artefato.txt:9–49). Isso bloqueia C6 e obriga o revisor a montar suas próprias entradas para C1–C5.
2. **README sem versões nem exemplo concreto** (README.md:21–108). O Dockerfile não fixa versões ("ubuntu:latest") e clona o HEAD, não o commit bb812a22 avaliado (Dockerfile:1, 8). O revisor pode acabar avaliando um código diferente do pacote.
3. **Defeito provável no Mach-O thin** (src/extract.c:2360/2363/2409 junto com src/helpers.c:269–284): a comparação usa constantes com bytes invertidos.
4. **Possível campo errado no cabeçalho EVTX** (src/extract.c:2478–2489): offset 0x18 e ausência do cabeçalho de 4 KiB. É uma análise baseada no formato EVTX, a confirmar.
5. **ELF cortado no último PT_LOAD** (src/extract.c:2216–2232, 2282–2298): pode perder os cabeçalhos de seção e os símbolos.
6. **Divergências entre artigo e código:**
   - recovery.log com hashes (artigo, p. 7) contra audit.txt sem hash (main.h:162; dir.c:292–295)
   - "00000002.sh" (p. 7) contra a extensão "script" (state.c:384)
   - `make` na raiz (p. 6) contra o Makefile em src/
   - "aviso e pula as consultas" (p. 7) contra "Error…" mais "Clean (0)" por arquivo (vt_query.c:141; dir.c:281)
7. **Dependência externa:** C5 exige uma conta e chave do VirusTotal, com limites de taxa. As contagens mudam com o tempo (reivindicacoes.md:21), e a leitura por sscanf é frágil (vt_query.c:180).
8. **Evidências ausentes:** a página de manual (src/foremost-ng.8.gz) e as capturas (screenshots/*.png) são binárias e foram omitidas no artefato.txt, e o vídeo citado no artigo (p. 7) está fora do pacote. Não pude verificar se trazem exemplos ou resultados.
9. **Riscos de compilação** com compiladores recentes, por exemplo GCC 14 em ubuntu:latest. Não verifiquei, porque não executei nada.

{"F": {"decisao": "Não atribuir", "confianca": 60, "evidencias": ["instrucoes-oficiais.md:15", "artefato.txt:README.md:31-35", "artefato.txt:README.md:82-85", "artefato.txt:Dockerfile:1", "artefato.txt:Dockerfile:5", "artefato.txt:Dockerfile:8", "artefato.txt:src/Makefile:46", "artefato.txt:src/Makefile:65", "artefato.txt:índice linhas 9-49", "artigo.pdf:p.6 §4"]},
 "R": {"decisao": "Não atribuir", "confianca": 25, "evidencias": ["instrucoes-oficiais.md:19", "reivindicacoes.md:12", "reivindicacoes.md:17", "artefato.txt:índice linhas 9-49", "artigo.pdf:p.8 Fig. 2", "artefato.txt:src/extract.c:2360-2409", "artefato.txt:src/helpers.c:269-284", "artefato.txt:src/helpers.c:353-354", "artefato.txt:src/extract.c:2478-2489", "artefato.txt:src/extract.c:2519-2622", "artefato.txt:src/extract.c:2147-2309", "artefato.txt:src/dir.c:274-295", "artefato.txt:src/vt_query.c:136-186", "artefato.txt:src/main.h:162"],
       "por_reivindicacao": {"C1": "depende_execucao", "C2": "depende_execucao", "C3": "nao_reproduzivel", "C4": "depende_execucao", "C5": "depende_execucao", "C6": "nao_reproduzivel"}}}