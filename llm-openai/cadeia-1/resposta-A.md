## A. Materiais examinados

Examinei exclusivamente `artigo.pdf`, `artefato.txt`, `instrucoes-oficiais.md` e `reivindicacoes.md`, na versão do pacote indicada. **Não compilei nem executei o artefato.** As decisões abaixo avaliam a documentação e o código fornecidos; não representam um resultado de execução nem a decisão histórica do comitê.

## B. Selo F — Funcional

| Critério oficial | Avaliação documental | Evidência |
|---|---|---|
| Ser executável e permitir observar funcionalidades | **Só verificável por execução.** Há código e alvo de compilação, sem prova de que compilam ou funcionam. | [instrucoes-oficiais.md:§Funcional (F)] “precisa ser executável e permitir a observação de funcionalidades”; [src/Makefile:65-70] `all: $(SYS) goals`. |
| README informar dependências, versões e ambiente | **Não atendido.** Há instruções por plataforma, mas faltam versões fixadas das dependências e uma descrição suficiente do ambiente para repetir a instalação. | [instrucoes-oficiais.md:§Funcional (F)] “dependências, versões de dependências/linguagens/ambiente, ambiente de execução”; [README.md:21-35] “Linux” seguido de `make` e `sudo make install`; [Dockerfile:1] `FROM ubuntu:latest`; [Dockerfile:4-6] lista pacotes sem versões. |
| README informar instalação, execução e exemplo mínimo | **Parcial; critério não atendido integralmente.** A instalação está descrita. Para execução, há somente sintaxe com parâmetros genéricos, sem entrada e comando completos de um exemplo mínimo. | [instrucoes-oficiais.md:§Funcional (F)] “instalação, execução e pelo menos um exemplo mínimo”; [README.md:31-35] `make` / `sudo make install`; [README.md:74-85] `foremost-ng [options] [image_or_device]`. |
| Revisor executar e apresentar prova e saídas | **Só verificável por execução.** Nenhuma saída do artefato foi produzida nesta avaliação. | [instrucoes-oficiais.md:§Funcional (F)] “deve **executar** o artefato e apresentar prova de execução e saídas”; “Ler código ou README, por si só, não constitui prova de funcionamento.” |

**Decisão F: Não atribuir.** Há falha documental em requisitos obrigatórios do README; uma execução bem-sucedida, isoladamente, não supriria essa falha. **Confiança de que o comitê oficial atribuiu F: 15/100.** Essa é uma estimativa, pois o pacote não contém parecer, resposta dos autores ou decisão oficial.

**Para mudar a decisão:** seria necessário completar o README com dependências e versões, ambiente e um exemplo mínimo executável; depois, observar compilação, execução desse exemplo, arquivos recuperados e saídas registradas no parecer.

## C. Selo R — Reprodutível

Os critérios oficiais são: reproduzir as “principais reivindicações do artigo”, ter na documentação “instruções de execução dessas reivindicações” e a descrição do “processo usado pelos autores”, e **executar** os experimentos para confrontar saídas com figuras e tabelas do artigo [instrucoes-oficiais.md:§Reprodutível (R)]. A regra fornecida exige **C1 a C6**; C7 é estrutural e não entra no cálculo [reivindicacoes.md:§Regra para o selo R] “R é atribuído se C1 a C6 forem reproduzidas”.

| Reivindicação | Avaliação | Evidência e resultado que faltaria observar |
|---|---|---|
| **C1 — EVTX** | **Depende de execução.** O README não dá entrada nem procedimento específico para EVTX; a existência do parser no código não prova a recuperação. | [artigo.pdf:p.6, §3] “ElfFile” e chunks de “64 KiB”; [src/extract.c:2473-2489] verifica `ElfFile` e calcula `chunk_count * 65536ULL`; [README.md:82-85] apenas sintaxe geral. Seria preciso extrair um `.evtx` de imagem conhecida e abri-lo em analisador de eventos. |
| **C2 — scripts** | **Depende de execução, com risco identificado no código.** Falta procedimento específico. A verificação de “mais que só comentários” examina caracteres após `#`, sem pular a linha de comentário; assim, texto de um comentário pode acionar `found_real`. | [artigo.pdf:p.6, §3] “shebang (#!)” e “at least 32 bytes”; [src/extract.c:2578-2580] mínimo de 32 bytes; [src/extract.c:2599-2612] `if (*p != '#')` define `found_real = 1`; [README.md:82-85] sintaxe geral. Seria preciso observar extração de Bash, Python e PowerShell com corpo legível **e** rejeição de uma entrada composta apenas de shebang e comentários. |
| **C3 — Mach-O `fat` e `thin`** | **Não reproduzível no estado documentado do código.** Além da falta de procedimento, os dois caminhos `thin` com assinaturas registradas têm uma comparação de endianness incompatível. | [artigo.pdf:p.6, §3] distingue cabeçalho “FAT (universal)” e “thin Mach-O”; [src/state.c:375-379] registra `CE FA ED FE` e `CF FA ED FE`; [src/helpers.c:350-354] `read_le32` lê little endian; [src/extract.c:2359-2363,2408-2409] compara o valor lido a `0xCEFAEDFE` e `0xCFFAEDFE`. Essas sequências, lidas em little endian, produzem respectivamente `0xFEEDFACE` e `0xFEEDFACF`, portanto não entram nos ramos `thin` mostrados. Para mudar a avaliação, seria necessária correção ou demonstração verificável de recuperação de amostras `fat` e `thin` reconhecíveis. |
| **C4 — ELF 32/64 bits** | **Depende de execução.** Há caminhos para as duas classes, mas o README não fornece amostras nem procedimento de validação. | [artigo.pdf:p.6, §3] “32-bit or 64-bit” e “program header table”; [src/extract.c:2176-2188] classe 32; [src/extract.c:2240-2253] classe 64; [src/extract.c:2234-2236,2300-2302] grava `.elf`. Seria preciso extrair ambos e verificar sua estrutura com um analisador ELF. |
| **C5 — VirusTotal** | **Depende de execução.** O README documenta `-x` e `VT_API_KEY`, mas não um experimento reproduzível com entrada, hash e resultado de referência. | [artigo.pdf:p.7, §4.1] exemplo com `-x` e anotação no log; [README.md:89-107] “`-x`” e `VT_API_KEY`; [src/dir.c:274-295] calcula SHA-256, consulta e registra a coluna VT. Seria preciso observar consulta associada ao hash de arquivo recuperado, registro do resultado e, sem chave, aviso e recuperação sem consulta. As contagens atuais não precisam igualar as publicadas [reivindicacoes.md:§Critério de reprodução]. |
| **C6 — execução da Figura 2** | **Não reproduzível com o pacote fornecido.** O dado necessário `evidence2.dd` não consta do índice completo, e o README não ensina a repetir esse caso. | [artigo.pdf:p.8, Fig. 2] `./foremost-ng -v -x evidence2.dd` e tabela com ELF, script, EXE, ZIP, offsets e VT; por exemplo, `00004352.elf` no offset `2228224`; [artefato.txt:ÍNDICE] identifica todos os arquivos do commit e não inclui `evidence2.dd`; [reivindicacoes.md:C6] “O README indica como reproduzir? não”. Para mudar a avaliação, seria preciso disponibilizar a imagem usada e confrontar arquivos e offsets extraídos com a figura. |
| **C7 — arquitetura extensível** | **Atendida por inspeção estrutural, fora da regra de R.** Não foi verificado comportamento em execução. | [reivindicacoes.md:§Regra para o selo R] “C7 ... não entra na regra de R”; [src/state.c:369-385] registra identificadores e assinaturas; [src/extract.c:2678-2687] despacha para parsers por tipo. |

**Decisão R: Não atribuir.** C3 apresenta uma incompatibilidade direta no caminho `thin`, e C6 carece da imagem indispensável para comparar a Figura 2. Além disso, o README não descreve o processo dos autores nem instruções por reivindicação [README.md:74-107; instrucoes-oficiais.md:§Reprodutível (R)]. **Confiança de que o comitê oficial atribuiu R: 3/100.**

## D. Lacunas e riscos

- A ausência de execução impede afirmar que compilação, extrações ou consultas VirusTotal funcionaram. Capturas incluídas no artefato são material documental, não prova produzida nesta revisão [artefato.txt:ÍNDICE; instrucoes-oficiais.md:§Funcional (F)].
- O pacote não fornece entradas controladas para C1 a C5 nem `evidence2.dd` para C6 [artefato.txt:ÍNDICE]. Para R, seria necessário observar todos os resultados C1–C6; em C6, comparar os **arquivos e offsets** da Figura 2, sem exigir igualdade das contagens mutáveis do VirusTotal [reivindicacoes.md:§Critério de reprodução].
- As instruções descrevem parecer inicial, resposta dos autores e decisão posterior [instrucoes-oficiais.md:§Contexto de revisão]. Esses documentos não estão entre os quatro materiais autorizados; por isso, as confianças numéricas não são uma afirmação sobre o resultado oficial conhecido.

```json
{
  "F": {
    "decisao": "Não atribuir",
    "confianca": 15,
    "evidencias": [
      "instrucoes-oficiais.md:§Funcional (F)",
      "README.md:21-35",
      "README.md:74-85",
      "Dockerfile:1-6"
    ]
  },
  "R": {
    "decisao": "Não atribuir",
    "confianca": 3,
    "evidencias": [
      "instrucoes-oficiais.md:§Reprodutível (R)",
      "reivindicacoes.md:§Regra para o selo R",
      "src/state.c:375-379",
      "src/helpers.c:350-354",
      "src/extract.c:2359-2363",
      "src/extract.c:2408-2409",
      "artigo.pdf:p.8, Fig. 2",
      "artefato.txt:ÍNDICE"
    ],
    "por_reivindicacao": {
      "C1": "depende_execucao",
      "C2": "depende_execucao",
      "C3": "nao_reproduzivel",
      "C4": "depende_execucao",
      "C5": "depende_execucao",
      "C6": "nao_reproduzivel"
    }
  }
}
```
