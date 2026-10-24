# Parecer de Avaliação Pós-Execução — SBSeg 2025 (Etapa B2)

**Artefato:** Foremost-NG: An Open-Source Toolkit for Advanced File Carving and Analysis  
**Versão analisada (commit):** `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d`  
**Base factual:** `registro-factual.md` e evidências geradas em `D:\t9-trabalho\gemini-c2\execucao\`  

---

## 1. Confronto entre a Execução Experimental e a Avaliação Analítica (Passo a Passo)

- **P1 (Instalação de Dependências - D1):** *Confirma a avaliação analítica.* Todas as dependências documentadas no `Dockerfile` e `README.md` (`gcc 13.3.0`, `make 4.3`, `git`, `libssl-dev`, `libcurl4-openssl-dev`) foram instaladas no Ubuntu 24.04 sem conflitos de pacotes (`01_apt_install.log`), confirmando a exequibilidade do ambiente.
- **P2 (Obtenção do Código-Fonte - D0):** *Confirma a avaliação analítica.* O arquivo `artefato.zip` no contêiner continha a árvore completa de fontes C idêntica à de `artefato.txt`.
- **P3 e P4 (Compilação e Instalação - D0):** *Confirma a avaliação analítica e resolve a indeterminação do Selo F.* O binário `foremost-ng` foi compilado limpo com gcc (`make clean && make`), gerando o binário ELF 64-bit de 86 KB (`03_make_build.log`), e instalado com sucesso em `/usr/local/bin` (`04_make_install.log`).
- **P5 (Comandos Informativos e Man Page - D0):** *Confirma a avaliação analítica.* Os comandos de versão (`foremost-ng -V`), menu de ajuda (`foremost-ng -h`) e manual do sistema (`man foremost-ng`) funcionaram perfeitamente (`05_version.txt`, `05_help.txt`, `05_man.txt`).
- **P6 e P7 (Teste Funcional Mínimo - D2 e D0):** *Confirma a avaliação analítica e comprova a funcionalidade.* O Foremost-NG processou a imagem de teste `test_f.img`, criou a estrutura de diretórios e registrou o log `audit.txt` (`07_audit_f.txt`), extraindo com sucesso o arquivo script.
- **P8 e P9 (EVTX / Reivindicação C1 - D2 e D0):** *Confirma a avaliação analítica.* O parser nativo identificou a assinatura `ElfFile\0\0`, delimitou exatamente o chunk de 64 KiB e extraiu `00000001.evtx` (64 KiB), reconhecido pelo utilitário `file` como `MS Windows 10-11 Event Log` (`09_audit_c1.txt`). *(Tratado como evidência complementar por utilizar entrada sintética D2).*
- **P10 e P11 (Scripts / Reivindicação C2 - D2 e D0):** *Confirma a avaliação analítica.* Foram recuperados com sucesso scripts Bash, Python e PowerShell íntegros em `output_c2/script/` (`11_audit_c2.txt`), preservando shebang e corpo. Revelou-se que o filtro de comentários da linha 2601 de `src/extract.c` é permissivo a linhas de comentários contendo letras normais. *(Evidência complementar D2).*
- **P12 e P13 (Mach-O / Reivindicação C3 - D2 e D0):** *Contradiz parcialmente a avaliação analítica.* O parser recuperou com sucesso o binário universal Mach-O FAT (`0xCAFEBABE`, 8 KiB), validado por `file` como `Mach-O universal binary`. Todavia, constatou-se no código (`src/extract.c:2408`) um bug de comparação de endianness (`magic_le == 0xCFFAEDFE` versus `0xFEEDFACF`), impedindo o carving de binários Thin Mach-O na imagem de teste. *(Evidência complementar D2).*
- **P14 e P15 (ELF / Reivindicação C4 - D2 e D0):** *Confirma a avaliação analítica.* O parser extraiu com precisão os 24.520 bytes correspondentes à união dos segmentos de carga `PT_LOAD` do binário ELF64 `/bin/true`, validado estruturalmente por `readelf -h` (`15_audit_c4.txt`). *(Evidência complementar D2).*
- **P16 e P17 (VirusTotal / Reivindicação C5 - D0):** *Confirma a avaliação analítica.* Com a chave `VT_API_KEY` (confirmada mascarada), a ferramenta calculou o SHA-256 e consultou a API v3 da plataforma via libcurl, preenchendo a coluna `VT` do `audit.txt` com `Clean (0)` (`17_audit_c5.txt`). Sem a chave, emitiu o aviso previsto no artigo e prosseguiu o carving.
- **P18 e P19 (Figura 2 / Reivindicação C6 - D0):** *Confirma categoricamente a avaliação analítica.* A busca no contêiner constatou que `evidence2.dd` não existe (`18_find_evidence2.log`). O comando oficial `foremost-ng -v -x evidence2.dd` falhou imediatamente com código 1 (`19_exec_c6_fig2.log`), confirmando que o experimento publicado não é reproduzível por ausência do dataset de 2 GB.

---

## 2. Decisão Final dos Selos

### Selo Funcional (F): ATRIBUIR
- **Decisão:** **Atribuir**.
- **Mudou em relação à Etapa A:** **Sim (`mudou: true`)**.
- **Justificativa:** Na Etapa A, o selo F foi classificado como *Indeterminado* porque as diretrizes oficiais estipulam que a leitura de código e documentação não comprova execução. Na Etapa E, o código-fonte foi compilado sem qualquer intervenção no código C, instalado no sistema operacional através das instruções dos autores, executou com sucesso os comandos de ajuda/versão e realizou carving funcional ponta a ponta sobre imagens de disco, gerando a estrutura de diretórios e o log de auditoria `audit.txt`. O artefato atende plenamente a todos os requisitos de funcionalidade.
- **Confiança:** **100 / 100** de que o comitê oficial atribuiu o selo F.

### Selo Reprodutível (R): NÃO ATRIBUIR
- **Decisão:** **Não atribuir**.
- **Mudou em relação à Etapa A:** **Não (`mudou: false`)**.
- **Justificativa:**
  - A regra fixada em `reivindicacoes.md:17` estabelece: *"R é atribuído se C1 a C6 forem reproduzidas."*
  - A reivindicação C6 requer a reprodução exata do experimento publicado na Figura 2 (`./foremost-ng -v -x evidence2.dd`), comparando os 12 arquivos e respectivos offsets.
  - O dataset de 2 GB `evidence2.dd` não foi fornecido no pacote, não está disponível no contêiner e o comando oficial falhou com erro de arquivo inexistente (código 1).
  - Conforme a diretriz de avaliação, passos classificados como D2 (testes com dados sintéticos propostos pelo revisor para C1 a C4) constituem apenas evidência complementar de funcionamento do código e não representam a reprodução dos experimentos dos autores.
  - Adicionalmente, identificou-se em C3 uma falha de lógica no parser de binários Thin Mach-O (`src/extract.c:2408`).
  - Como um critério mandatório falhou por ausência do dataset indispensável para C6, o selo R não pode ser concedido.
- **Classificação por reivindicação:**
  - `C1`: `reproduzivel` (parser EVTX operacional com chunk de 64 KiB, comprovado em D2).
  - `C2`: `reproduzivel` (extração de scripts Bash, Python e PowerShell comprovada em D2).
  - `C3`: `nao_reproduzivel` (Mach-O FAT funciona, mas Thin Mach-O falha por bug de endianness em `src/extract.c:2408`).
  - `C4`: `reproduzivel` (extração de segmentos `PT_LOAD` de ELF64 comprovada em D2).
  - `C5`: `reproduzivel` (consulta REST à API VirusTotal e preenchimento da coluna VT comprovados em D0).
  - `C6`: `nao_reproduzivel` (arquivo `evidence2.dd` ausente, comando falha com código 1; impossível reproduzir a Figura 2).
- **Confiança:** **10 / 100** de que o comitê oficial atribuiu o selo R (convicção de que o comitê não atribuiu R pela falta de `evidence2.dd`).

---

```json
{
  "F": {
    "decisao": "Atribuir",
    "mudou": true,
    "confianca": 100,
    "evidencias": [
      "registro-factual.md:P3",
      "registro-factual.md:P4",
      "registro-factual.md:P5",
      "registro-factual.md:P7",
      "03_make_build.log:1-17",
      "07_audit_f.txt:1-21"
    ]
  },
  "R": {
    "decisao": "Não atribuir",
    "mudou": false,
    "confianca": 10,
    "evidencias": [
      "registro-factual.md:P18",
      "registro-factual.md:P19",
      "registro-factual.md:C3",
      "registro-factual.md:C6",
      "18_find_evidence2.log:1-2",
      "19_exec_c6_fig2.log:1-6"
    ],
    "por_reivindicacao": {
      "C1": "reproduzivel",
      "C2": "reproduzivel",
      "C3": "nao_reproduzivel",
      "C4": "reproduzivel",
      "C5": "reproduzivel",
      "C6": "nao_reproduzivel"
    }
  }
}
```