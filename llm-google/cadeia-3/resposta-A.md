# Avaliação Analítica de Artefatos — SBSeg 2025 (Tarefa 9: Foremost-NG)

## A. Materiais examinados

Nesta etapa de avaliação analítica pré-execução, foram examinados exclusivamente os arquivos disponibilizados no pacote (`D:\t9-trabalho\gemini-c3\pacote`):
1. **`instrucoes-oficiais.md`** (21 linhas): Consolidação oficial dos critérios de avaliação do SBSeg 2025 para os selos Funcional (F) e Reprodutível (R).
2. **`reivindicacoes.md`** (22 linhas): Relação das reivindicações principais C1 a C7 fixadas para a ferramenta Foremost-NG, acompanhada das regras para avaliação do selo R.
3. **`artigo.pdf`** (8 páginas): Artigo completo *"Foremost-NG: An Open-Source Toolkit for Advanced File Carving and Analysis"* (Anais Estendidos do SBSeg 2025: SF).
4. **`artefato.txt`** (7.331 linhas): Pacote único correspondente ao commit `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` do repositório, contendo índice estrutural e código-fonte completo (incluindo `README.md`, `Dockerfile`, `src/Makefile`, código-fonte em C e cabeçalhos).

---

## B. Selo Funcional (F)

### 1. Critérios oficiais aplicáveis
> *"O artefato precisa ser executável e permitir a observação de funcionalidades. O README deve informar dependências, versões de dependências/linguagens/ambiente, ambiente de execução, instalação, execução e pelo menos um exemplo mínimo. O revisor deve **executar** o artefato e apresentar prova de execução e saídas no parecer. Ler código ou README, por si só, não constitui prova de funcionamento."* [instrucoes-oficiais.md:15]

### 2. Análise dos critérios segundo a documentação
- **Executabilidade e observação de funcionalidades:** *Só verificável por execução*. O código-fonte C e arquivos de build existem, mas o funcionamento efetivo requer compilação e teste dinâmico.
- **Dependências:** *Não atendido / Parcialmente atendido na documentação*. O `README.md` documenta explicitamente pacotes adicionais para BSD (`curl`) e macOS (`openssl@3`), bem como o compilador `MinGW` para Windows, mas omite completamente as dependências necessárias para compilar em ambiente Linux padrão (`gcc`, `make`, `libssl-dev`, `libcurl4-openssl-dev`). Essas dependências só são encontradas ao inspecionar o `Dockerfile` (`apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev`) [Dockerfile:4-5 / artefato.txt:113-115].
- **Versões de dependências, linguagens e ambiente:** *Não atendido*. O `README.md` não informa versões mínimas ou recomendadas do GCC, Make, libcurl ou OpenSSL (com exceção da versão de brew `openssl@3` no macOS). Cita apenas uma observação sobre versões legadas da biblioteca C ("*On systems with glibc < 2.2.0, you may see harmless warnings about ftello and fseeko*") [README.md:70 / artefato.txt:218].
- **Ambiente de execução:** *Atendido na documentação*. O `README.md` especifica suporte a plataformas Linux, BSD, macOS e compilação cruzada para Windows [README.md:31-68 / artefato.txt:179-216].
- **Instalação:** *Atendido na documentação*. O `README.md` documenta os comandos de descompactação e compilação (`make`, `sudo make install`, `make unix`, `make mac`, `make cross`) [README.md:25-66 / artefato.txt:173-214].
- **Execução:** *Atendido na documentação*. O `README.md` detalha a sintaxe genérica de invocação (`foremost-ng [options] [image_or_device]`), orienta a consulta do manual (`man foremost-ng`) e descreve a ativação do VirusTotal com `-x` [README.md:74-108 / artefato.txt:222-256].
- **Exemplo mínimo:** *Não atendido*. O `README.md` apresenta apenas a assinatura genérica de comando, sem disponibilizar um comando concreto com parâmetros completos (como `foremost-ng -i <arquivo> -o <pasta>`) e sem fornecer qualquer arquivo de teste ou imagem de disco de demonstração junto ao repositório.

### 3. Evidências citadas
- [instrucoes-oficiais.md:15]: *"O artefato precisa ser executável e permitir a observação de funcionalidades. O README deve informar dependências, versões de dependências/linguagens/ambiente, ambiente de execução, instalação, execução e pelo menos um exemplo mínimo. O revisor deve executar o artefato e apresentar prova de execução e saídas no parecer. Ler código ou README, por si só, não constitui prova de funcionamento."*
- [README.md:31-35 / artefato.txt:179-183]: *"### Linux\n```bash\nmake\nsudo make install\n```"* (ausência de menção às bibliotecas `libssl-dev` e `libcurl-dev`).
- [README.md:82-85 / artefato.txt:230-233]: *"Basic syntax:\n```bash\nforemost-ng [options] [image_or_device]\n```"* (apenas sintaxe esquemática, sem exemplo mínimo concreto ou dados de teste).
- [Dockerfile:3-6 / artefato.txt:112-115]: *"RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev"*.

### 4. Decisão analítica para F
- **Decisão:** **Indeterminado**.
- **Justificativa:** Conforme estipulado nas regras analíticas, a decisão é "Indeterminado" quando nenhum critério inviabiliza aprioristicamente a execução, mas a decisão final depende de verificação prática. O código-fonte em C está completo no repositório, o `Makefile` define os alvos de compilação adequadamente e há um `Dockerfile` funcional. No entanto, por determinação expressa das instruções oficiais, "ler código ou README, por si só, não constitui prova de funcionamento", sendo indispensável executar o utilitário para validar sua operabilidade.

### 5. Confiança
- **Confiança de atribuição pelo comitê oficial:** **85 / 100**.
- **Justificativa:** A ferramenta é um utilitário CLI clássico em C, cuja estrutura de compilação e código está íntegra. Em ambiente com as dependências instaladas (conforme o Dockerfile), a probabilidade de compilar sem erros graves e executar extrações sob demanda é muito alta, permitindo aos revisores comprovar as funcionalidades na etapa experimental.

### 6. Observações necessárias na execução para mudar a decisão
- **Para atribuir F:** Demonstrar a compilação bem-sucedida do executável `foremost-ng`; comprovar que o binário responde às opções de linha de comando (`-h`, `-v`, `-V`); e verificar a extração funcional de arquivos a partir de uma fonte de dados de teste, com geração do diretório de saída e do arquivo `audit.txt`.
- **Para reprovar F:** Constatar erros fatais de compilação não documentados com a cadeia padrão de ferramentas ou falhas de execução críticas (como *segmentation fault* / travamentos sistemáticos ao carregar dados).

---

## C. Selo Reprodutível (R)

### 1. Critérios oficiais aplicáveis
> *"O revisor deve conseguir reproduzir as **principais reivindicações do artigo**. A documentação do artefato deve trazer instruções de execução dessas reivindicações e descrever o processo usado pelos autores para chegar aos resultados publicados. O revisor deve executar os experimentos e confrontar os resultados com os do artigo, incluindo figuras/tabelas pertinentes, resumindo a comparação no parecer."* [instrucoes-oficiais.md:19]
> *"O README não marca reivindicações a reproduzir. Por isso, valem as reivindicações principais desta lista: **C1 a C6**. **R é atribuído se C1 a C6 forem reproduzidas.** C7 é uma contribuição arquitetural, sem experimento associado no artigo; ela pode ser inspecionada, mas não entra na regra de R."* [reivindicacoes.md:17]

### 2. Avaliação detalhada por reivindicação

#### C1: Recuperação de logs de eventos do Windows (EVTX)
- **Definição:** Reconhecimento da assinatura `ElfFile`, delimitação dos blocos de 64 KiB e extração do log [artigo.pdf: p. 1; p. 2; p. 6, §3; p. 7, §4.1].
- **Evidência no código:** Função `extract_evtx` em `src/extract.c:2460-2516` [artefato.txt:4528-4585], que valida `ElfFile\0\0`, lê `chunk_count` no offset `0x18`, computa `chunk_count * 65536` e grava em disco com sufixo `evtx`.
- **Documentação de reprodução:** Parcial. O README e o artigo indicam apenas a sintaxe genérica `-t evtx`. Não há arquivos de teste EVTX no repositório.
- **Classificação analítica:** `depende_execucao` (a lógica do parser está implementada no código, mas a validação de extração e integridade depende de execução com dados de teste).

#### C2: Recuperação de scripts (Bash, Python, PowerShell)
- **Definição:** Identificação via shebang (`#!`) e texto legível, com tamanho mínimo de 32 bytes e descarte de arquivos que contenham apenas comentários [artigo.pdf: p. 1; p. 2; p. 6, §3].
- **Evidência no código:** Função `extract_script` em `src/extract.c:2519-2621` [artefato.txt:4587-4690], que impõe `MIN_SCRIPT_SIZE = 32`, varre caracteres imprimíveis até delimitadores e valida que o corpo após a primeira quebra de linha contenha caracteres além de `#` e espaços.
- **Documentação de reprodução:** Parcial (sintaxe geral suportada via `-t script`, sem amostras de teste no artefato).
- **Classificação analítica:** `depende_execucao` (lógica implementada; comprovação depende de execução dinâmica).

#### C3: Recuperação de binários Mach-O fat e thin
- **Definição:** Identificação de cabeçalhos universais FAT (`0xCAFEBABBE`) e thin (`0xCEFAEDFE` / `0xCFFAEDFE`), determinando o tamanho total a partir da tabela de arquiteturas ou dos comandos de carga `LC_SEGMENT` / `LC_SEGMENT_64` [artigo.pdf: p. 1; p. 2; p. 6, §3].
- **Evidência no código:** Função `extract_macho` em `src/extract.c:2314-2455` [artefato.txt:4382-4523], contemplando parsing das estruturas Mach-O para delimitação do arquivo.
- **Documentação de reprodução:** Parcial (sintaxe geral descrita, mas sem binários Mach-O de teste no repositório).
- **Classificação analítica:** `depende_execucao`.

#### C4: Recuperação de executáveis ELF de 32 e 64 bits
- **Definição:** Identificação do número mágico ELF (`\x7fELF`), tratamento de 32 e 64 bits e cálculo da extensão máxima com base nos segmentos `PT_LOAD` dos program headers [artigo.pdf: p. 1; p. 2; p. 6, §3; p. 7, §4.1].
- **Evidência no código:** Função `extract_elf` em `src/extract.c:2147-2309` [artefato.txt:4215-4377], validando `buf[0..3] == "\x7fELF"`, `ei_data == 1` (little-endian), e somando `p_offset + p_filesz` dos cabeçalhos com `p_type == 1`.
- **Documentação de reprodução:** Parcial (exemplos `-t elf` no artigo e manual, sem arquivo de teste no artefato).
- **Classificação analítica:** `depende_execucao`.

#### C5: Enriquecimento pelo VirusTotal
- **Definição:** Cálculo de hash criptográfico (SHA-256) dos arquivos esculpidos, consulta à API pública v3 do VirusTotal via libcurl com chave da variável `VT_API_KEY` (usando flag `-x`), e registro da quantidade de motores que classificaram o artefato como malicioso ou não detectado [artigo.pdf: p. 1; pp. 2–3, §2; p. 7, §4-4.1; p. 8, Fig. 2].
- **Evidência no código:** Módulo `src/vt_query.c:31-197` [artefato.txt:7106-7272] (funções `get_api_key`, `sha_checksum`, `vt_check_hash`), integrado em `src/dir.c:274-283` [artefato.txt:1564-1574] e documentado detalhadamente no `README.md:89-108` [artefato.txt:237-256].
- **Documentação de reprodução:** Atendido na documentação quanto à sintaxe (`-x`) e configuração de ambiente (`export VT_API_KEY=<chave>`).
- **Classificação analítica:** `depende_execucao` (depende de conectividade e resposta do serviço remoto durante o teste prático).

#### C6: Exemplo de execução da Figura 2 (`evidence2.dd`)
- **Definição:** Reprodução exata do experimento demonstrado na Seção 4.2 e Figura 2 do artigo (`./foremost-ng -v -x evidence2.dd`), no qual uma imagem de disco de 2 GB (2.045.109.643 bytes) é processada, gerando um `audit.txt` com exatamente 12 artefatos recuperados (3 ELF, 1 script, 6 EXE e 2 ZIP) nos offsets precisos indicados na tabela (ex.: ELF em 2228224, script em 2811904, EXE em 204740608, ZIP em 914484119) [artigo.pdf: p. 7, §4.2; p. 8, Fig. 2].
- **Evidência no artefato:** **Evidência ausente**. O arquivo `evidence2.dd` **NÃO** acompanha o repositório do artefato (verificável no índice de arquivos [artefato.txt:9-50]). O `README.md` não faz nenhuma referência ao arquivo `evidence2.dd`, nem descreve onde obtê-lo ou como sintetizá-lo. Embora o artigo cite na Seção 4 que amostras podem ser baixadas de `https://dftt.sourceforge.net`, não especifica qual imagem corresponde a `evidence2.dd`.
- **Classificação analítica:** **`nao_reproduzivel`**. Falta o dado indispensável para reproduzir a reivindicação C6 e validar os resultados tabelados na Figura 2.

#### C7: Arquitetura de parsers extensível (inspeção analítica complementar)
- **Definição:** Desacoplamento entre o despachante central e os módulos de parser através de uma interface uniforme e lista de registro dinâmico [artigo.pdf: p. 2-3, §2 e Fig. 1].
- **Evidência no código:** Ao contrário do alegado no artigo, o arquivo `src/extract.c:2628-2695` [artefato.txt:4696-4764] implementa um despachante estático estruturado em uma sequência rígida de comandos condicionais (`if (needle->type == JPEG) ... else if (needle->type == EVTX) ...`), sem tabela de despacho desacoplada. Conforme `reivindicacoes.md:17`, C7 é uma alegação arquitetural sem experimento associado e não integra o cômputo obrigatório de R.

### 3. Decisão analítica para R
- **Decisão:** **Não atribuir**.
- **Justificativa:** Conforme as regras oficiais de avaliação, o selo R só é concedido se todas as reivindicações principais obrigatórias (C1 a C6) puderem ser reproduzidas contra os resultados publicados [reivindicacoes.md:17; instrucoes-oficiais.md:19]. Pela regra analítica pré-execução: *"Não atribuir: há evidência de que um critério obrigatório não é atendido (por exemplo, falta o dado necessário para uma reivindicação principal)"*. Como o arquivo `evidence2.dd` não foi fornecido e a documentação não contém instruções para recriar o cenário da Figura 2, C6 é inviável de ser reproduzida, o que bloqueia terminantemente a concessão do selo R.

### 4. Confiança
- **Confiança de atribuição pelo comitê oficial:** **10 / 100**.
- **Justificativa:** Sem a disponibilização da imagem de disco forense `evidence2.dd` e sem instruções passo a passo para replicar a tabela da Figura 2, é virtualmente certo que o comitê oficial não atribuiu o selo Reprodutível.

### 5. Observações necessárias na execução para mudar a decisão de R
- Disponibilização do conjunto exato de dados de entrada (`evidence2.dd`) com 2.045.109.643 bytes;
- Execução do comando `./foremost-ng -v -x evidence2.dd` em bancada;
- Obtenção dos 12 arquivos esculpidos exatamente nos offsets reportados na Figura 2 e confirmação da anotação das estatísticas do VirusTotal no relatório de auditoria.

---

## D. Lacunas e riscos

1. **Ausência total de dados de teste e replicação:** O repositório não inclui nenhuma imagem de disco, dump de memória ou arquivos de teste sintéticos (mesmo de pequenas dimensões). Não há como confrontar os resultados experimentais da Figura 2 sem dados externos.
2. **Omissões no README.md:** O arquivo de instruções ignora as dependências essenciais de compilação em Linux (`libssl-dev`, `libcurl4-openssl-dev`) e omite comandos de exemplo completos e executáveis.
3. **Discrepância na nomenclatura do log de saída:** A Seção 4.2 do artigo (p. 7) afirma que o utilitário gera um arquivo chamado `recovery.log`, enquanto a Seção 3 (p. 6), a Figura 2 (p. 8) e o código-fonte (`AUDIT_FILE_NAME` em `src/main.h:162` [artefato.txt:5986]) produzem `audit.txt`.
4. **Discrepância arquitetural em relação ao artigo:** A arquitetura descrita na Figura 1 e Seção 2 do artigo (despachante dinâmico modular desacoplado) não corresponde ao código real de `src/extract.c`, que opera por encadeamento monolítico de condicionais `if/else`.
5. **Limitação de formatos binários:** O parser ELF limita-se exclusivamente a binários little-endian (`src/extract.c:2172`), ignorando executáveis big-endian sem tratamento explícito no relatório.
6. **Dependência de serviços externos e rede para o selo Funcional:** A flag `-x` depende de comunicação ativa com a API do VirusTotal e desabilita verificação SSL (`CURLOPT_SSL_VERIFYPEER = 0` em `src/vt_query.c:167` [artefato.txt:7242]), o que impõe riscos de cota e bloqueios em ambientes de teste estritamente isolados.

---

```json
{
  "F": {
    "decisao": "Indeterminado",
    "confianca": 85,
    "evidencias": [
      "instrucoes-oficiais.md:15",
      "README.md:21-85",
      "Dockerfile:3-6",
      "src/Makefile:1-120",
      "src/main.c:210-290"
    ]
  },
  "R": {
    "decisao": "Não atribuir",
    "confianca": 10,
    "evidencias": [
      "instrucoes-oficiais.md:19",
      "reivindicacoes.md:15-21",
      "artigo.pdf:p. 7-8",
      "artefato.txt:9-50",
      "README.md:1-119"
    ],
    "por_reivindicacao": {
      "C1": "depende_execucao",
      "C2": "depende_execucao",
      "C3": "depende_execucao",
      "C4": "depende_execucao",
      "C5": "depende_execucao",
      "C6": "nao_reproduzivel"
    }
  }
}
```