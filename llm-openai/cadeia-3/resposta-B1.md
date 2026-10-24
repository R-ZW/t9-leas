# Roteiro de execução para F e R

Este roteiro usa apenas os procedimentos e resultados descritos em `artigo.pdf`, `artefato.txt`, `instrucoes-oficiais.md` e `reivindicacoes.md` do pacote da cadeia 3. **Ainda não executei nenhum passo.** `[NÃO DOCUMENTADO]` identifica uma preparação ou verificação necessária para a avaliação, mas sem procedimento completo fornecido pelos autores. Nesses pontos, o roteiro interrompe a reivindicação se faltar a entrada ou o método de validação; não substituirei amostras por outras escolhidas por mim.

## Ambiente e condições de início

O ambiente previsto é Ubuntu 24.04 em Docker, com usuário comum e `sudo`. O README documenta compilação em Linux com `make` e `sudo make install` [README.md:31–35]. O Dockerfile dos autores instala `gcc`, `make`, `git`, `libssl-dev` e `libcurl4-openssl-dev` [Dockerfile:3–6]. **Versões dessas dependências, CPU e RAM mínimas não foram especificadas** [README.md:21–68; Dockerfile:1–10]. Ubuntu 24.04 é a condição desta etapa; o Dockerfile usa `ubuntu:latest` [Dockerfile:1].

A Figura 2 usa uma imagem de **2.845.109.643 bytes**, além de espaço para código e extrações [artigo.pdf:p.8, Fig.2]. `[NÃO DOCUMENTADO]` É necessário conferir espaço livre antes de obtê-la. O pacote não fornece `disk.img`, `memory.dump`, `evidence2.dd`, chave `VT_API_KEY` nem amostras identificadas para cada formato [artefato.txt:ÍNDICE]. A ausência de qualquer entrada exigida interrompe o teste correspondente, sem ser tratada como falha observada do programa.

### P1 — Conferir recursos do contêiner `[NÃO DOCUMENTADO]`

- **Selo/reivindicação:** preparação para F e R.
- **Diretório:** `/tmp`.
- **Comando exato:** `df -B1 /tmp && uname -m`
- **Resultado esperado segundo os autores:** não há requisito numérico de hardware documentado; a Figura 2 declara entrada de 2.845.109.643 bytes [artigo.pdf:p.8, Fig.2].
- **Evidência a salvar:** arquitetura e espaço livre exibidos.
- **Sucesso:** há espaço para a imagem, repositório e arquivos extraídos.
- **Falha:** não se aplica a uma reivindicação do programa.
- **Interrupção:** espaço insuficiente; não iniciar uma extração cujo resultado possa ser truncado.

### P2 — Instalar as dependências indicadas

- **Selo/reivindicação:** F e R, preparação.
- **Diretório:** `/tmp`.
- **Comando exato:** `sudo apt-get update && sudo apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev`
- **Resultado esperado segundo os autores:** as dependências listadas no Dockerfile ficam disponíveis [Dockerfile:3–6]. **`[NÃO DOCUMENTADO]`** O prefixo `sudo` adapta o `RUN` do Dockerfile, executado como administrador, ao usuário comum do contêiner.
- **Evidência a salvar:** saída integral do gerenciador de pacotes e versões instaladas exibidas por ele.
- **Sucesso:** todas as instalações terminam sem erro.
- **Falha:** pacote necessário não instala.
- **Interrupção:** indisponibilidade de rede, repositório de pacotes ou `sudo`; não inferir que o código compila.

### P3 — Obter o código pelo procedimento do artigo

- **Selo/reivindicação:** F e R, preparação.
- **Diretório:** `/tmp`.
- **Comando exato:** `git clone https://github.com/cristianzsh/foremost-ng.git`
- **Resultado esperado segundo os autores:** repositório `foremost-ng` disponível [artigo.pdf:p.6, §4].
- **Evidência a salvar:** saída do clone.
- **Sucesso:** clone concluído.
- **Falha:** repositório não pode ser obtido.
- **Interrupção:** se o endereço não estiver acessível, não substituir por outro repositório.

### P4 — Fixar a versão avaliada `[NÃO DOCUMENTADO]`

- **Selo/reivindicação:** F e R, controle de versão.
- **Diretório:** `/tmp/foremost-ng`.
- **Comando exato:** `git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d && git rev-parse HEAD`
- **Resultado esperado segundo os autores:** os comandos publicados fazem clone sem fixar commit [artigo.pdf:p.6, §4; Dockerfile:8]. O identificador desta avaliação está em [artefato.txt:cabeçalho], “`bb812a22cb06ef87b5a2d877dfb6f40eb12d460d`”.
- **Evidência a salvar:** hash impresso por `git rev-parse HEAD`.
- **Sucesso:** hash idêntico ao do pacote.
- **Falha:** a versão clonada difere e não pode ser fixada.
- **Interrupção:** commit indisponível no clone; não avaliar silenciosamente a versão corrente.

### P5 — Compilar

- **Selo/reivindicação:** F e R, preparação.
- **Diretório:** `/tmp/foremost-ng/src`.
- **Comando exato:** `make`
- **Resultado esperado segundo os autores:** construção do executável `foremost-ng` [README.md:25–35; src/Makefile:100–101].
- **Evidência a salvar:** saída integral da compilação e identificação do executável gerado.
- **Sucesso:** `make` termina sem erro e produz o executável.
- **Falha:** erro de compilação ou executável ausente.
- **Interrupção:** dependências ou versão incorretas; corrigir a preparação antes de atribuir uma falha ao código.

### P6 — Instalar e consultar a documentação

- **Selo/reivindicação:** F, instalação documentada.
- **Diretório:** `/tmp/foremost-ng/src`.
- **Comandos exatos:** `sudo make install` e, em seguida, `man foremost-ng`
- **Resultado esperado segundo os autores:** binário instalado e manual acessível [README.md:31–35, 74–80].
- **Evidência a salvar:** saída da instalação e disponibilidade do manual.
- **Sucesso:** instalação termina sem erro; o manual abre.
- **Falha:** instalação ou manual falham.
- **Interrupção:** falta de permissão de `sudo`. A abertura do manual, isoladamente, não prova funcionamento.

### P7 — Teste mínimo funcional

- **Selo/reivindicação:** F.
- **Diretório:** `/tmp/foremost-ng/src`.
- **Comando exato fornecido pelos autores:** `foremost-ng -i disk.img -o /temp/output/carved` [artigo.pdf:p.7, §4.1].
- **Resultado esperado segundo os autores:** arquivos recuperados em subdiretórios por formato e registro da extração [artigo.pdf:p.7, §4.1–4.2].
- **Evidência a salvar:** entrada usada e sua identificação, saída do terminal, diretório de extração, arquivos produzidos e registro (`audit.txt`, conforme [src/main.h:162]). O artigo também cita `recovery.log` [artigo.pdf:p.7, §4.2]; registrar a diferença se observada.
- **Sucesso:** com uma entrada conhecida que contenha arquivo recuperável, o comando termina e produz extração verificável.
- **Falha:** com entrada válida e ambiente pronto, o comando falha ou não produz a saída esperada.
- **Interrupção:** **`[NÃO DOCUMENTADO]`** `disk.img` não foi fornecido nem identificado pelo nome de uma amostra; os autores tampouco documentam sua preparação ou o conteúdo mínimo esperado. Não criar uma imagem substituta e não afirmar que F funcionou.

## R — reivindicações

Os passos P8–P11 usam a execução padrão de P7 **somente se** `disk.img` for identificado como contendo amostras conhecidas dos formatos correspondentes. O artigo afirma que todos os parsers registrados atuam no modo padrão [artigo.pdf:p.7, §4.1]. Reutilizar o resultado de P7 evita executar novamente no mesmo diretório de saída. A falta de amostra conhecida interrompe a reivindicação; ausência de extração em uma imagem de conteúdo desconhecido não demonstra falha.

### P8 — C1, EVTX

- **Diretório:** `/tmp/foremost-ng/src`. **Comando exato:** o de P7, `foremost-ng -i disk.img -o /temp/output/carved`. O artigo também oferece a execução restrita `foremost-ng -t evtx,elf,exe -i disk.img -o /temp/output/carved` [artigo.pdf:p.7, §4.1], a usar apenas em uma execução com saída ainda vazia.
- **Esperado:** arquivo `.evtx` delimitado por assinatura `ElfFile` e chunks de 64 KiB, legível por ferramenta de eventos [artigo.pdf:p.6, §3].
- **Evidência:** imagem identificada, arquivo extraído, offset e registro; resultado da leitura por ferramenta de eventos.
- **Sucesso:** extração completa e leitura válida da amostra conhecida.
- **Falha:** amostra EVTX válida é reconhecida incorretamente, truncada ou ilegível.
- **Interrupção:** **`[NÃO DOCUMENTADO]`** não há amostra EVTX identificada nem ferramenta de análise de eventos nomeada ou instalada pelos autores; registrar a evidência ausente antes de concluir legibilidade.

### P9 — C2, scripts

- **Diretório:** `/tmp/foremost-ng/src`. **Comando exato:** o de P7, `foremost-ng -i disk.img -o /temp/output/carved`.
- **Esperado:** scripts Bash, Python e PowerShell com `#!`, pelo menos 32 bytes e corpo além de comentários, legíveis após extração [artigo.pdf:p.6, §3].
- **Evidência:** entradas conhecidas, arquivos extraídos, respectivas linhas de intérprete e corpos, registro da extração.
- **Sucesso:** scripts válidos são recuperados e uma entrada composta somente por comentários não é aceita.
- **Falha:** script válido não é recuperado ou um arquivo de apenas comentários é aceito.
- **Interrupção:** **`[NÃO DOCUMENTADO]`** faltam amostras positivas e negativas e instruções para prepará-las. A condição negativa é necessária para verificar “mais que só comentários”, especialmente diante da lógica em [src/extract.c:2598–2604]; não inventar um corpus como se fosse o dos autores.

### P10 — C3, Mach-O

- **Diretório:** `/tmp/foremost-ng/src`. **Comando exato:** o de P7, `foremost-ng -i disk.img -o /temp/output/carved`.
- **Esperado:** recuperação de Mach-O `fat` e `thin` com tamanho determinado por cabeçalhos ou comandos de carga [artigo.pdf:p.6, §3].
- **Evidência:** entradas `fat` e `thin` identificadas, arquivos extraídos, offsets e reconhecimento estrutural.
- **Sucesso:** ambos os tipos são recuperados e reconhecidos.
- **Falha:** uma amostra válida de qualquer tipo não é recuperada corretamente.
- **Interrupção:** **`[NÃO DOCUMENTADO]`** faltam amostras identificadas e ferramenta de reconhecimento Mach-O indicada pelos autores. É essencial incluir `thin` por causa da divergência de constantes observada em [src/extract.c:2359–2363, 2408–2409].

### P11 — C4, ELF

- **Diretório:** `/tmp/foremost-ng/src`. **Comando exato:** o de P7, `foremost-ng -i disk.img -o /temp/output/carved`; alternativamente, o comando restrito do artigo citado em P8.
- **Esperado:** executáveis ELF de 32 e 64 bits delimitados pelos cabeçalhos de programa [artigo.pdf:p.6, §3].
- **Evidência:** entradas ELF32 e ELF64 identificadas, arquivos extraídos, offsets e resultado de analisador ELF.
- **Sucesso:** ambos os tipos são extraídos e estruturalmente legíveis.
- **Falha:** uma entrada ELF válida conhecida é truncada ou ilegível.
- **Interrupção:** **`[NÃO DOCUMENTADO]`** faltam amostras identificadas e comando de analisador ELF prescrito pelos autores.

### P12 — C5, VirusTotal

- **Diretório:** `/tmp/foremost-ng/src`.
- **Comandos exatos fornecidos:** `export VT_API_KEY=<YOUR_VT_API_KEY>` [artigo.pdf:p.7, §4] e `foremost-ng -x -t elf -i memory.dump -o ./carved-files` [artigo.pdf:p.7, §4.1]. O marcador da chave deve ser substituído **somente por uma chave válida disponibilizada para a avaliação**.
- **Esperado:** hash do ELF recuperado consultado na API e resultado de detecção registrado; sem chave, aviso e carving sem consulta [artigo.pdf:p.7, §4.1].
- **Evidência:** identificação de `memory.dump`, hash do arquivo extraído, registro e resultado da consulta, saída de aviso no caso sem chave. Guardar a chave fora das evidências divulgadas.
- **Sucesso:** consulta vinculada ao hash correto e detecção registrada; no ramo sem chave, nenhuma consulta é atribuída a resultado “limpo”.
- **Falha:** com chave válida e amostra conhecida, consulta ou vínculo do resultado falham.
- **Interrupção:** **`[NÃO DOCUMENTADO]`** não há `memory.dump`, chave nem resposta de referência no pacote. O README explica como configurar uma chave [README.md:89–107], mas não fornece credencial ou amostra. Se faltarem, não executar a variante com chave nem concluir C5.

### P13 — C6, Figura 2

- **Diretório:** `/tmp/foremost-ng/src`.
- **Comando exato:** `./foremost-ng -v -x evidence2.dd` [artigo.pdf:p.8, Fig.2].
- **Esperado:** 12 linhas: três `.elf`, um `.script`, seis `.exe` e dois `.zip`, nos offsets **2228224, 2467840, 2615296, 2811904, 204740608, 207390720, 212445184, 219508736, 226570240, 229046272, 914484119 e 914965615**, respectivamente [artigo.pdf:p.8, Fig.2]. As contagens atuais do VT podem variar [reivindicacoes.md:Critério de reprodução].
- **Evidência:** identidade e hash de `evidence2.dd`, saída integral, arquivos extraídos e registro; comparação linha a linha de nomes/tipos e offsets com a figura.
- **Sucesso:** arquivos e offsets correspondem à Figura 2, com coluna VT associada aos arquivos quando houver chave válida.
- **Falha:** com a imagem exata e ambiente pronto, há diferença de tipos, arquivos ou offsets.
- **Interrupção:** **`[NÃO DOCUMENTADO]`** `evidence2.dd` e seu hash não foram fornecidos [artefato.txt:ÍNDICE]; sem a imagem exata não há comparação válida. Sem chave válida, a coluna VT completa também fica inconclusiva.

### P14 — C7, arquitetura, fora da regra de R

- **Selo/reivindicação:** C7 é registrada para completude, mas não condiciona R [reivindicacoes.md:Regra para o selo R].
- **Diretório:** `/tmp/foremost-ng/src`.
- **Comando exato:** **`[NÃO DOCUMENTADO]` nenhum experimento ou comando de verificação foi fornecido** para comparar a arquitetura com a Figura 1.
- **Esperado:** despachante e parsers com identificador, assinatura, validação e recuperação [artigo.pdf:p.3, §2].
- **Evidência:** inspeção do código correspondente e da Figura 1; nenhum resultado de execução reivindicado.
- **Sucesso/falha:** registrar correspondências ou divergências arquiteturais, sem alterar a decisão de R.
- **Interrupção:** versão do código não confirmada em P4.

## Tempo estimado

Preparação, clone, compilação e instalação: **15–35 minutos**, se rede e pacotes estiverem disponíveis. Teste mínimo e C1–C5: **40–90 minutos**, desde que as entradas, chave e ferramentas de validação sejam fornecidas. C6, com imagem de 2,85 GB e consultas VT: **15–60 minutos ou mais**, conforme disco, rede e limites da API. **Total condicional: cerca de 1–3 horas.** Com o material atualmente descrito, a execução das reivindicações para nas entradas ausentes; o tempo efetivo seria apenas o de preparação.

## Quadro de todos os passos

| Passo | Selo/reivindicação | Comando ou ação | Condição de prosseguimento |
|---|---|---|---|
| P1 | F/R | `[NÃO DOCUMENTADO]` `df -B1 /tmp && uname -m` | Espaço para entrada e saída |
| P2 | F/R | `sudo apt-get update && sudo apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev` | Dependências instaladas |
| P3 | F/R | `git clone https://github.com/cristianzsh/foremost-ng.git` | Clone disponível |
| P4 | F/R | `[NÃO DOCUMENTADO]` `git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d && git rev-parse HEAD` | Hash idêntico ao pacote |
| P5 | F/R | `make` em `src` | Executável gerado |
| P6 | F | `sudo make install`; `man foremost-ng` | Instalação e manual acessíveis |
| P7 | F | `foremost-ng -i disk.img -o /temp/output/carved` | `disk.img` conhecido e disponível |
| P8 | R/C1 | Reusar P7; opção dos autores: `foremost-ng -t evtx,elf,exe -i disk.img -o /temp/output/carved` | EVTX conhecido e método de leitura |
| P9 | R/C2 | Reusar P7 | Scripts válidos e amostra só de comentários |
| P10 | R/C3 | Reusar P7 | Mach-O `fat` e `thin` conhecidos |
| P11 | R/C4 | Reusar P7; opção restrita de P8 | ELF32 e ELF64 conhecidos |
| P12 | R/C5 | `export VT_API_KEY=<YOUR_VT_API_KEY>`; `foremost-ng -x -t elf -i memory.dump -o ./carved-files` | Chave válida e `memory.dump` conhecido |
| P13 | R/C6 | `./foremost-ng -v -x evidence2.dd` | Imagem exata e chave para VT |
| P14 | C7, fora de R | `[NÃO DOCUMENTADO]` nenhum comando de experimento | Inspeção arquitetural apenas |
