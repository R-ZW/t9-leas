## A. Materiais examinados

Examinei somente `artigo.pdf`, `artefato.txt`, `instrucoes-oficiais.md` e `reivindicacoes.md`, todos no pacote indicado. A análise foi apenas de leitura: não compilei nem executei o artefato. O arquivo de instruções informa ser um **resumo fiel para leitura offline**, e não uma transcrição literal da página oficial [instrucoes-oficiais.md:Natureza deste arquivo].

## B. Selo Funcional (F)

O critério fornecido exige que o artefato seja executável, permita observar funcionalidades e que o README informe “dependências, versões de dependências/linguagens/ambiente, ambiente de execução, instalação, execução e pelo menos um exemplo mínimo”. Exige também que o revisor **execute** o artefato e apresente “prova de execução e saídas” [instrucoes-oficiais.md:Funcional (F)].

| Critério | Estado nesta análise | Evidência |
|---|---|---|
| Ser executável e permitir observar funcionalidades | **Só verificável por execução** | Há alvo de compilação `all` [src/Makefile:65-70: “all: $(SYS) goals”], mas código e instruções não provam funcionamento. |
| README informar dependências | **Não atendido** | O README menciona `curl` para BSD e OpenSSL para macOS [README.md:37-54: “Make sure curl is installed”; “brew install openssl@3”]. GCC, Make e bibliotecas de desenvolvimento aparecem no Dockerfile, não no README [Dockerfile:3-5: “gcc make git libssl-dev libcurl4-openssl-dev”]. |
| README informar versões de dependências, linguagens e ambiente | **Não atendido** | Há `openssl@3`, mas não versões para as demais dependências ou ambiente [README.md:50-54; Dockerfile:1: “FROM ubuntu:latest”]. |
| README informar ambiente e instalação | **Atendido na documentação** | Descreve Linux, BSD, macOS e compilação cruzada para Windows, com comandos de construção [README.md:21-67: “make”; “sudo make install”; “make mac”; “make cross”]. |
| README informar execução | **Atendido na documentação**, em nível genérico | Apresenta a sintaxe `foremost-ng [options] [image_or_device]` [README.md:74-84]. |
| README trazer pelo menos um exemplo mínimo | **Não atendido** | A seção de uso contém apenas a sintaxe com parâmetros genéricos e remete à página de manual; não fornece entrada concreta e comando completo [README.md:74-85: “foremost-ng [options] [image_or_device]”]. |
| Revisor executar e apresentar prova e saídas | **Só verificável por execução** | A instrução diz que “ler código ou README, por si só, não constitui prova de funcionamento” [instrucoes-oficiais.md:Funcional (F)]. Esta etapa proíbe a execução. |

**Decisão F: Não atribuir.** Há falhas documentais em requisitos obrigatórios do README, independentemente da execução ainda não observada. **Confiança de que o comitê oficial atribuiu F: 15/100**; não há decisão oficial entre os materiais examinados.

Para rever a decisão, seria preciso completar no README as dependências e versões e acrescentar um exemplo mínimo reproduzível. Depois, a execução teria de mostrar compilação, processamento da entrada do exemplo e saídas recuperadas observáveis. Uma execução bem-sucedida, sozinha, não supriria as lacunas obrigatórias do README.

## C. Selo Reprodutível (R)

As instruções exigem reproduzir as “principais reivindicações do artigo”; a documentação deve ensinar a executá-las e descrever como os autores chegaram aos resultados. O revisor deve executar os experimentos e confrontar os resultados com o artigo, inclusive figuras e tabelas pertinentes [instrucoes-oficiais.md:Reprodutível (R)]. A regra específica do pacote determina que **C1 a C6** precisam ser reproduzidas; C7 é arquitetural e fica fora da regra do selo [reivindicacoes.md:Regra para o selo R: “R é atribuído se C1 a C6 forem reproduzidas”].

| Critério geral de R | Estado nesta análise | Evidência |
|---|---|---|
| Instruções para executar cada reivindicação principal | **Não atendido** | O README oferece sintaxe geral, sem entradas, comandos e verificações específicos para C1 a C6 [README.md:74-85]. Para VT, explica como definir a chave, mas não fornece um ensaio completo [README.md:89-107]. |
| Processo usado pelos autores para chegar aos resultados publicados | **Não atendido** | A Figura 2 mostra `./foremost-ng -v -x evidence2.dd` e uma tabela de resultados [artigo.pdf:p.8, Fig. 2], mas o README não identifica nem fornece `evidence2.dd` ou o procedimento para obter a mesma entrada [README.md:74-107; artefato.txt:índice, linhas 9-49]. |
| Execução e comparação com artigo, figuras e tabelas | **Só verificável por execução**, com impedimento para C6 | A comparação exigida está expressa nas instruções [instrucoes-oficiais.md:Reprodutível (R)]. Nenhuma execução ocorreu, e a entrada exata da Figura 2 não consta do índice completo do artefato [artefato.txt:linhas 5-6 e índice, linhas 9-49]. |

**Avaliação por reivindicação:**

| ID | Estado da documentação e do resultado | Evidência e observação necessária |
|---|---|---|
| **C1 — EVTX** | Instrução específica: **não atendido**. Recuperação: **só verificável por execução** (`depende_execucao`). | O artigo promete reconhecer `ElfFile` e delimitar chunks de 64 KiB [artigo.pdf:p.6, §3, “Windows Event Logs (EVTX)”]. O código confere `ElfFile\0\0`, calcula tamanho por `65536` e chama `write_to_disk` [src/extract.c:2473-2514]. Seria preciso observar um `.evtx` recuperado e legível por analisador de eventos, com entrada e saída identificadas. |
| **C2 — scripts** | Instrução específica: **não atendido**. A condição “mais que só comentários” está **não atendida no código** (`nao_reproduzivel` para a reivindicação completa). | O artigo exige shebang, ao menos 32 bytes e conteúdo além de comentários [artigo.pdf:p.6, §3, “Script Files”]. O código impõe 32 bytes [src/extract.c:2521, 2578-2580], porém, após uma linha iniciada por `#`, considera qualquer letra seguinte como conteúdo real: `if (*p != '#') ... found_real = 1` [src/extract.c:2598-2612]. Assim, um corpo composto apenas por uma linha `# comentário` pode passar nessa checagem. Para rever a conclusão, seria necessário observar que uma entrada válida é extraída **e** uma entrada de 32 bytes ou mais contendo somente comentários é rejeitada. |
| **C3 — Mach-O fat e thin** | Instrução específica: **não atendido**. A parte *thin* está **não atendida no código** (`nao_reproduzivel`). | O artigo exige ambos os tipos [artigo.pdf:p.6, §3, “Mach-O”]. O registro usa assinaturas *thin* `CE FA ED FE` e `CF FA ED FE` [src/state.c:375-379], mas o extrator lê esses bytes como inteiro little endian e compara com `0xCEFAEDFE` e `0xCFFAEDFE` [src/extract.c:2359-2363, 2408-2409; src/helpers.c:350-355]. Os bytes registrados produzem, respectivamente, `0xFEEDFACE` e `0xFEEDFACF`; portanto, não entram nos ramos *thin* indicados. Seria necessário observar a recuperação válida de amostras *fat* e *thin* de 32 e 64 bits e esclarecer essa divergência. |
| **C4 — ELF 32 e 64 bits** | Instrução específica: **não atendido**. Resultado: **só verificável por execução** (`depende_execucao`). | O artigo prevê arquivos ELF delimitados pelos cabeçalhos de programa [artigo.pdf:p.6, §3, “ELF”]. O código distingue classes 32/64, procura `PT_LOAD` e grava `.elf` [src/extract.c:2163-2176, 2212-2236, 2278-2302]. É preciso observar arquivos das duas classes extraídos e aceitos por um analisador ELF. |
| **C5 — VirusTotal** | Instrução específica do ensaio: **não atendido**. Consulta e correspondência ao arquivo: **só verificáveis por execução** (`depende_execucao`). | O README explica `-x` e `VT_API_KEY` [README.md:89-107]. O código calcula SHA-256 do arquivo gravado, consulta VT e escreve um rótulo no log [src/dir.c:274-295]. Sem chave, a função avisa e retorna sem consulta [src/vt_query.c:136-143], mas o chamador ainda formata o resultado zerado como `Clean (0)` [src/dir.c:279-282]; isso não comprova uma análise limpa. É preciso observar requisição associada ao hash correto, resultado registrado e, sem chave, carving com aviso e sem consulta. |
| **C6 — execução da Figura 2** | **Não atendido** (`nao_reproduzivel`) com o material fornecido. | A figura mostra `./foremost-ng -v -x evidence2.dd` e, por exemplo, `00004352.elf` no offset `2228224`, além de script, EXE, ZIP e coluna VT [artigo.pdf:p.8, Fig. 2]. `evidence2.dd` não aparece no índice exaustivo do artefato [artefato.txt:linhas 5-6 e índice, linhas 9-49]. Sem essa entrada, não há como confrontar os arquivos e offsets da figura. Seria preciso disponibilizar a imagem exata e observar a tabela correspondente. As contagens VT podem variar, conforme a regra do pacote [reivindicacoes.md:Critério de reprodução]. |
| **C7 — arquitetura** | **Fora da regra de R**; inspeção estática apenas. | Há registro de tipos e assinaturas [src/state.c:369-385] e um despachante central que chama funções de recuperação por tipo [src/extract.c:2624-2693]. Isso sustenta parte da arquitetura descrita [artigo.pdf:p.3, §2], mas o despacho é uma cadeia explícita de condições: acrescentar um novo tipo parece exigir alterá-la. C7 não altera a decisão de R [reivindicacoes.md:Regra para o selo R]. |

**Decisão R: Não atribuir.** Além da falta de procedimento documentado e de `evidence2.dd` para C6, a leitura do código revela divergências diretas nas condições reivindicadas para C2 e C3. **Confiança de que o comitê oficial atribuiu R: 3/100**; a decisão oficial não consta dos materiais.

Para rever R, seriam necessários procedimentos e entradas identificadas para C1 a C6, inclusive a imagem exata de C6. A execução teria de produzir EVTX e ELF estruturalmente legíveis, aceitar scripts com corpo e rejeitar os compostos só de comentários, recuperar Mach-O *fat* e *thin*, registrar consultas VT ligadas aos hashes e reproduzir os arquivos e offsets da Figura 2.

## D. Lacunas e riscos

- Não há prova de compilação, execução ou validação estrutural dos arquivos extraídos nesta etapa [instrucoes-oficiais.md:Funcional (F); Reprodutível (R)].
- O índice completo não contém entradas de teste para as reivindicações nem `evidence2.dd`; o README também não descreve como preparar essas entradas [artefato.txt:índice, linhas 9-49; README.md:74-107].
- O Dockerfile usa `ubuntu:latest` e clona o repositório remoto sem fixar o commit, de modo que suas instruções não fixam o mesmo ambiente e código do pacote [Dockerfile:1, 8-10].
- O código de leitura de 64 bits chama uma função que retorna `unsigned int`, o que pode truncar offsets ou tamanhos grandes; o impacto concreto em C4 e C3 dependeria de entradas e execução [src/helpers.c:269-283, 357-361].
- A ausência de chave VT gera aviso, mas pode deixar `Clean (0)` no registro do arquivo, rótulo que não deve ser interpretado como resultado de consulta [src/vt_query.c:139-143; src/dir.c:274-295].

```json
{
  "F": {
    "decisao": "Não atribuir",
    "confianca": 15,
    "evidencias": [
      "instrucoes-oficiais.md:Funcional (F)",
      "README.md:21-67",
      "README.md:74-85",
      "Dockerfile:1-8"
    ]
  },
  "R": {
    "decisao": "Não atribuir",
    "confianca": 3,
    "evidencias": [
      "instrucoes-oficiais.md:Reprodutível (R)",
      "reivindicacoes.md:Regra para o selo R",
      "README.md:74-107",
      "src/extract.c:2598-2612",
      "src/state.c:375-379",
      "src/extract.c:2359-2363",
      "src/extract.c:2408-2409",
      "artigo.pdf:p.8, Fig. 2",
      "artefato.txt:índice, linhas 9-49"
    ],
    "por_reivindicacao": {
      "C1": "depende_execucao",
      "C2": "nao_reproduzivel",
      "C3": "nao_reproduzivel",
      "C4": "depende_execucao",
      "C5": "depende_execucao",
      "C6": "nao_reproduzivel"
    }
  }
}
```
