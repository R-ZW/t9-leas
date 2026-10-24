# Roteiro para a próxima etapa — selos F e R

**Estado:** roteiro preparado; nenhum comando foi executado. Usarei o commit `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` indicado em [artefato.txt:cabeçalho]. Os comandos de avaliação vêm do README, Dockerfile ou artigo. Marco **[NÃO DOCUMENTADO]** toda preparação ou verificação necessária para a qual os autores não dão procedimento.

## Ambiente e limites antes de começar

O contêiner terá Ubuntu 24.04, internet e usuário comum com `sudo`, `unzip` e `man`, conforme a condição desta etapa. Os autores indicam Ubuntu sem versão fixada (`ubuntu:latest`) e instalam `gcc`, `make`, `git`, `libssl-dev` e `libcurl4-openssl-dev` [Dockerfile:1-6]. O README também indica `make` e `sudo make install` para Linux [README.md:31-35]. **[NÃO DOCUMENTADO]** Os autores não especificam CPU, RAM, espaço livre nem versões dessas dependências. A Figura 2 identifica `evidence2.dd` com 2.845.109.643 bytes [artigo.pdf:p.8, Fig. 2]; será necessário espaço para essa imagem e para os arquivos extraídos, mas não há capacidade mínima oficial.

Os nomes `disk.img`, `memory.dump` e `evidence2.dd` abaixo são os nomes usados nos exemplos do artigo [artigo.pdf:pp.7-8, §4.1–4.2 e Fig. 2]. Nenhum desses dados aparece no índice completo do pacote [artefato.txt:ÍNDICE]. A indicação de que amostras *podem* ser baixadas de `https://dftt.sourceforge.net` não identifica arquivo, hash ou composição que reproduza cada reivindicação [artigo.pdf:p.7, §4]. **Não substituirei uma entrada ausente por outra como se fosse a entrada dos autores.**

Em cada execução, salvarei a saída do terminal, o código de saída, os nomes e tamanhos dos arquivos produzidos e o log de recuperação que o programa gerar. Essa coleta é um procedimento da revisão, **[NÃO DOCUMENTADO]** pelos autores. “Interromper” abaixo significa não emitir conclusão positiva para o passo dependente; uma saída incorreta após execução é registrada como **falha**, não descartada.

## Preparação

**P1 — F e R; diretório `/tmp`; comando `sudo apt-get update`.** Procedimento baseado em `apt-get update` [Dockerfile:3]. O uso de `sudo` adapta o Dockerfile, que executa como root, ao usuário comum **[NÃO DOCUMENTADO]**. Esperado: índices de pacotes atualizados. Salvar: saída e código de saída. Sucesso: código zero. Falha: erro do gerenciador. Interrupção: indisponibilidade de rede ou repositórios impede P2.

**P2 — F e R; diretório `/tmp`; comando `sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev`.** Pacotes fornecidos pelos autores [Dockerfile:4-6]; `sudo env` é adaptação **[NÃO DOCUMENTADO]**. Esperado: compilador, ferramentas e bibliotecas instalados. Salvar: saída e código de saída. Sucesso: instalação concluída. Falha: pacote não instalável. Interrupção: sem essas dependências, não seguir para compilação.

**P3 — F e R; diretório `/tmp`; comando `git clone https://github.com/cristianzsh/foremost-ng.git`.** Comando indicado no artigo [artigo.pdf:p.6, §4] e repositório usado no Dockerfile [Dockerfile:8]. Esperado: árvore em `/tmp/foremost-ng`. Salvar: saída e identificação da árvore obtida. Sucesso: clone concluído. Falha: clone incompleto. Interrupção: repositório inacessível.

**P4 — F e R; diretório `/tmp/foremost-ng`; comando `git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` — [NÃO DOCUMENTADO].** Os autores mandam clonar, mas não mandam fixar essa revisão; fixá-la é necessário para avaliar a mesma versão descrita em [artefato.txt:cabeçalho]. Esperado: árvore no commit indicado. Salvar: saída e identificador do commit. Sucesso: checkout desse commit. Falha: commit indisponível. Interrupção: não avaliar um HEAD diferente como se fosse o pacote.

**P5 — F e R; diretório `/tmp/foremost-ng/src`; comando `make`.** Procedimento do README [README.md:31-35]. Esperado: binário `foremost-ng`. Salvar: saída da compilação, código de saída e presença do binário. Sucesso: compilação concluída com binário produzido. Falha: erro de compilação ou linkedição. Interrupção: sem binário, não seguir para testes de execução.

**P6 — F e R; diretório `/tmp/foremost-ng/src`; comando `sudo make install`.** Procedimento do README [README.md:31-35]. Esperado: ferramenta, configuração e manual instalados conforme [src/Makefile:107-118]. Salvar: saída e código de saída. Sucesso: instalação concluída. Falha: erro de instalação. Interrupção: se falhar, não usar o comando instalado `foremost-ng` nos passos seguintes.

**P7 — F; diretório `/tmp/foremost-ng/src`; comando `man foremost-ng`.** Consulta indicada em [README.md:74-80]. Esperado: manual acessível; isto verifica documentação instalada, **não** funcionamento do carver. Salvar: registro de acesso ou erro. Sucesso: manual abre. Falha: manual ausente. Interrupção: a falha não impede testar o binário local, mas impede afirmar instalação completa.

**P8 — F e R/C1–C5; diretório `/tmp/foremost-ng/src`; comando: nenhum — porta de entrada [NÃO DOCUMENTADO].** Antes das invocações, é necessário obter entradas identificadas e verificar que `disk.img` e `memory.dump` contêm, respectivamente, os formatos que serão testados. Também é necessário tornar graváveis os diretórios escolhidos com `-o`. Os autores não fornecem os arquivos, seus hashes, nem comandos para preparar essas condições [artigo.pdf:p.7, §4.1; artefato.txt:ÍNDICE]. Salvar: origem, hash e descrição de cada entrada que venha a ser fornecida. Sucesso: entradas e destino de saída definidos sem ambiguidade. Falha: entrada fornecida não contém o caso alegado. Interrupção: sem entrada apropriada, **não executar** P9–P13 e P15 como supostos testes dessas reivindicações.

## Teste mínimo F

**P9 — F; diretório `/tmp/foremost-ng/src`; comando `foremost-ng -i disk.img -o /temp/output/carved`.** É o exemplo de execução dos autores [artigo.pdf:p.7, §4.1]. Esperado: diretório de saída, subdiretórios por formato e arquivos recuperados [artigo.pdf:p.7, §4.2]. Salvar: saída do terminal, código de saída, log e arquivos extraídos. Sucesso: o comando termina e produz ao menos um arquivo reconhecível da entrada conhecida, com registro correspondente. Falha: erro, nenhuma recuperação apesar de entrada conhecida, ou arquivo ilegível. Interrupção: falta de `disk.img` ou impossibilidade de escrever em `/temp/output/carved`. A preparação desse caminho é **[NÃO DOCUMENTADO]**; não presumir que existe no Ubuntu limpo.

## R por reivindicação

**P10 — C1, EVTX; diretório `/tmp/foremost-ng/src`; comando `foremost-ng -t evtx,elf,exe -i disk.img -o /temp/output/c1`.** O uso de `-t evtx,elf,exe` vem do exemplo dos autores; o nome `c1` apenas separa as saídas de avaliações distintas [artigo.pdf:p.7, §4.1]. Esperado: `.evtx` recuperado a partir de assinatura `ElfFile` e chunks de 64 KiB [artigo.pdf:p.6, §3]. Salvar: terminal, log com offset e `.evtx`. Sucesso: arquivo extraído e legível por analisador de eventos. Falha: ausência, truncamento ou ilegibilidade diante de entrada EVTX conhecida. Interrupção: ausência dessa entrada. O artigo menciona ferramentas de análise de eventos, mas não dá uma ferramenta nem comando de validação **[NÃO DOCUMENTADO]**.

**P11 — C2, scripts; diretório `/tmp/foremost-ng/src`; comando `foremost-ng -i disk.img -o /temp/output/c2`.** O modo padrão percorre os parsers registrados [artigo.pdf:p.7, §4.1]. Esperado: scripts Bash, Python ou PowerShell com shebang, pelo menos 32 bytes e corpo além de comentários [artigo.pdf:p.6, §3]. Salvar: terminal, log e scripts extraídos. Sucesso: amostras conhecidas dos três tipos saem com diretiva e corpo legíveis, e entrada só com comentários não é aceita. Falha: perda de uma amostra válida ou aceitação de apenas comentários. Interrupção: amostras positivas e negativa não fornecidas; sua construção e composição são **[NÃO DOCUMENTADO]**.

**P12 — C3, Mach-O; diretório `/tmp/foremost-ng/src`; comando `foremost-ng -i disk.img -o /temp/output/c3`.** Usa o modo padrão indicado pelos autores [artigo.pdf:p.7, §4.1]. Esperado: Mach-O `fat` e `thin` completos [artigo.pdf:p.6, §3]. Salvar: terminal, log, arquivos `.macho` e identificação das amostras de origem. Sucesso: recuperação reconhecível de pelo menos um `fat` e dos casos `thin` reivindicados. Falha: ramo ausente, saída truncada ou arquivo não reconhecível. Interrupção: falta das amostras. O artigo não fornece comando nem ferramenta para conferir a estrutura Mach-O **[NÃO DOCUMENTADO]**; o risco de endianness encontrado em [src/extract.c:2359-2363,2408-2409] torna especialmente necessária a observação dos `thin`.

**P13 — C4, ELF; diretório `/tmp/foremost-ng/src`; comando `foremost-ng -t evtx,elf,exe -i disk.img -o /temp/output/c4`.** Exemplo de seleção dos autores [artigo.pdf:p.7, §4.1]. Esperado: `.elf` de 32 e 64 bits delimitados pelos cabeçalhos de programa [artigo.pdf:p.6, §3]. Salvar: terminal, log, offsets e arquivos `.elf`. Sucesso: ambos os tipos são extraídos e estruturalmente legíveis. Falha: ausência ou estrutura inválida para entrada conhecida. Interrupção: falta de amostras das duas classes. Os autores não indicam comando de análise estrutural **[NÃO DOCUMENTADO]**.

**P14 — C5, preparação de VirusTotal; diretório `/tmp/foremost-ng/src`; comando `export VT_API_KEY=<YOUR_VT_API_KEY>`.** É a forma mostrada pelos autores [artigo.pdf:p.7, §4; README.md:89-107]. Esperado: chave válida disponível ao processo, sem divulgá-la nas evidências. Salvar: somente confirmação de presença da variável, nunca seu valor. Sucesso: chave fornecida pelo avaliador e válida. Falha: chave recusada. Interrupção: sem chave, não realizar a parte de consulta real de P15; prosseguir separadamente para o comportamento sem chave de P16–P17.

**P15 — C5, consulta com chave; diretório `/tmp/foremost-ng/src`; comando `foremost-ng -x -t elf -i memory.dump -o ./carved-files`.** Exemplo dos autores [artigo.pdf:p.7, §4.1]. Esperado: hash dos ELF recuperados, consulta ao VirusTotal e anotação da detecção no log. Salvar: terminal, hash, resposta ou contagem registrada, log e ELF correspondente; ocultar a chave. Sucesso: consulta associada ao hash do arquivo extraído e resultado registrado. Falha: resultado sem associação ao arquivo, erro de API não tratado como tal, ou nenhum ELF diante de entrada conhecida. Interrupção: ausência de `memory.dump`, chave válida ou conectividade. As contagens atuais não precisam coincidir com as de 2025 [reivindicacoes.md:§Critério de reprodução].

**P16 — C5, retirar chave; diretório `/tmp/foremost-ng/src`; comando `unset VT_API_KEY` — [NÃO DOCUMENTADO].** O artigo reivindica comportamento sem chave, mas não dá o comando para criar essa condição [artigo.pdf:p.7, §4.1]. Esperado: variável ausente apenas no shell de teste. Salvar: confirmação sem expor segredo. Sucesso: condição sem chave estabelecida. Falha: variável ainda disponível ao processo. Interrupção: não usar P17 como teste do caso sem chave se a condição não puder ser assegurada.

**P17 — C5, execução sem chave; diretório `/tmp/foremost-ng/src`; comando `foremost-ng -x -t elf -i memory.dump -o ./carved-files-no-key`.** Repete o exemplo de P15 com outro destino, para separar resultados. Esperado segundo os autores: aviso, carving preservado e consultas VT puladas [artigo.pdf:p.7, §4.1]. Salvar: terminal, log e ELF extraído. Sucesso: aviso e arquivo recuperado sem consulta. Falha: carving interrompido ou resultado apresentado como consulta válida sem chave. Interrupção: `memory.dump` ausente ou saída indisponível.

**P18 — C6, entrada da Figura 2; diretório `/tmp/foremost-ng/src`; comando: nenhum — porta de entrada [NÃO DOCUMENTADO].** É indispensável obter **o mesmo** `evidence2.dd`; o pacote não o contém [artigo.pdf:p.8, Fig. 2; artefato.txt:ÍNDICE]. Esperado: imagem identificada, de 2.845.109.643 bytes conforme a figura. Salvar: procedência, tamanho e hash da imagem recebida. Sucesso: identidade do dado demonstrada. Falha: imagem diferente apresentada como equivalente. Interrupção: sem esse dado, não executar P19 como reprodução da Figura 2.

**P19 — C6, Figura 2; diretório `/tmp/foremost-ng/src`; comando `./foremost-ng -v -x evidence2.dd`.** Comando literal da figura [artigo.pdf:p.8, Fig. 2]. Esperado: tabela de 12 entradas, sendo três ELF, um script, seis EXE e dois ZIP, com offsets respectivamente `2228224`, `2467840`, `2615296`, `2811904`, `204740608`, `207390720`, `212445184`, `219508736`, `226570240`, `229046272`, `914484119` e `914965615` [artigo.pdf:p.8, Fig. 2]. Salvar: terminal, tabela/log e arquivos recuperados. Sucesso: arquivos e offsets correspondem à figura; contagens VT podem mudar [reivindicacoes.md:§Critério de reprodução]. Falha: arquivos ou offsets divergentes com a mesma imagem. Interrupção: falta da imagem ou, para avaliar a coluna VT, chave e rede. A figura não fornece a chave **[NÃO DOCUMENTADO]**.

**P20 — C7, arquitetura; diretório `/tmp/foremost-ng/src`; comando: nenhum — inspeção de código [NÃO DOCUMENTADO].** C7 não é experimento exigido para R [reivindicacoes.md:§Regra para o selo R]. A inspeção comparará o registro de identificadores e assinaturas [src/state.c:369-385] e o despachante [src/extract.c:2678-2687] com a arquitetura da Figura 1 [artigo.pdf:pp.2-3, §2]. Salvar: trechos de código e correspondência com a figura. Sucesso: componentes estruturais identificáveis. Falha: componente reivindicado ausente. Interrupção: fonte diferente do commit fixado. Nenhuma conclusão de funcionamento decorre desse passo.

## Tempo estimado

Com entradas e chave já disponíveis: **2 a 4 horas** para preparar, compilar, executar e examinar saídas; o processamento da imagem de aproximadamente 2,85 GB e limites da API podem ampliar esse tempo. **[NÃO DOCUMENTADO]** Os autores não fornecem tempos, requisitos de desempenho nem duração esperada. Sem `disk.img`, `memory.dump` e sobretudo `evidence2.dd`, o roteiro para nas portas de entrada indicadas, independentemente do tempo reservado.

## Tabela de todos os passos

| Passo | Selo/reivindicação | Diretório | Comando exato ou lacuna |
|---|---|---|---|
| P1 | F, R | `/tmp` | `sudo apt-get update` |
| P2 | F, R | `/tmp` | `sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev` |
| P3 | F, R | `/tmp` | `git clone https://github.com/cristianzsh/foremost-ng.git` |
| P4 | F, R | `/tmp/foremost-ng` | `git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` **[NÃO DOCUMENTADO]** |
| P5 | F, R | `/tmp/foremost-ng/src` | `make` |
| P6 | F, R | `/tmp/foremost-ng/src` | `sudo make install` |
| P7 | F | `/tmp/foremost-ng/src` | `man foremost-ng` |
| P8 | F, C1–C5 | `/tmp/foremost-ng/src` | Sem comando: entradas e saída gravável **[NÃO DOCUMENTADO]** |
| P9 | F | `/tmp/foremost-ng/src` | `foremost-ng -i disk.img -o /temp/output/carved` |
| P10 | C1 | `/tmp/foremost-ng/src` | `foremost-ng -t evtx,elf,exe -i disk.img -o /temp/output/c1` |
| P11 | C2 | `/tmp/foremost-ng/src` | `foremost-ng -i disk.img -o /temp/output/c2` |
| P12 | C3 | `/tmp/foremost-ng/src` | `foremost-ng -i disk.img -o /temp/output/c3` |
| P13 | C4 | `/tmp/foremost-ng/src` | `foremost-ng -t evtx,elf,exe -i disk.img -o /temp/output/c4` |
| P14 | C5 | `/tmp/foremost-ng/src` | `export VT_API_KEY=<YOUR_VT_API_KEY>` |
| P15 | C5 | `/tmp/foremost-ng/src` | `foremost-ng -x -t elf -i memory.dump -o ./carved-files` |
| P16 | C5 | `/tmp/foremost-ng/src` | `unset VT_API_KEY` **[NÃO DOCUMENTADO]** |
| P17 | C5 | `/tmp/foremost-ng/src` | `foremost-ng -x -t elf -i memory.dump -o ./carved-files-no-key` |
| P18 | C6 | `/tmp/foremost-ng/src` | Sem comando: obter `evidence2.dd` **[NÃO DOCUMENTADO]** |
| P19 | C6 | `/tmp/foremost-ng/src` | `./foremost-ng -v -x evidence2.dd` |
| P20 | C7, fora do cálculo de R | `/tmp/foremost-ng/src` | Sem comando: inspeção estrutural **[NÃO DOCUMENTADO]** |
