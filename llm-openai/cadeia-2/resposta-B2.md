Reli o [registro factual](<D:\user\unipampa\8º Semestre\LEAS\atividades\t9\t9-leas\llm-openai\cadeia-2\execucao\registro-factual.md>) e as evidências citadas abaixo. Os ensaios D2/D3 são **controles complementares**; não os trato como reprodução dos experimentos dos autores.

| Passos relevantes | Relação com a avaliação analítica | Evidência |
|---|---|---|
| P1–P6, X1–X2 | **Confirma** a identidade da versão e mostra que ela compilou e foi instalada. Resolve a dúvida de execução, mas não a falta de informações obrigatórias no README. | [P5-make-tentativa1.txt], [P6-make-install.txt] |
| P7–P8 | **Não altera** a decisão F. A entrada dos autores faltava; com uma entrada D2, houve recuperação idêntica de um script de 40 bytes. Isso prova uma funcionalidade mínima observada, sem suprir dependências, versões e exemplo mínimo no README. | [P7-disk-img.txt], [P8-audit.txt], [X6-F-comparacao.txt] |
| P9 e X40–X42 | **Confirma parcialmente** C1: um EVTX público foi recuperado byte a byte. O controle D2 com 64 KiB acrescentados mostrou que a saída também incluiu essa cauda, contrariando a delimitação reivindicada. Não substitui um experimento dos autores. | [X10-C1-cmp.txt], [X42-C1-cauda-resultados.txt] |
| P10 e X14–X16 | **Confirma** a ressalva analítica sobre C2. O script com corpo foi recuperado, mas o arquivo contendo apenas shebang e comentário também foi recuperado. | [X12-C2-resultados.txt], [X16-C2-negativo-resultados.txt] |
| P11 e X23–X26 | **Confirma** a ressalva analítica sobre C3. O Mach-O *fat* foi recuperado; os controles *thin* de 32 e 64 bits terminaram com “0 FILES EXTRACTED”. | [X21-C3-fat-resultados.txt], [X24-C3-thin32-audit.txt], [X26-C3-thin64-audit.txt] |
| P12 e X32–X33 | **Não altera** a decisão R. Ambos os ELF foram extraídos e `readelf` leu seus segmentos, mas acusou cabeçalhos de seção além do fim dos arquivos recuperados. A integridade completa de C4 permanece sem demonstração nos dados dos autores. | [X31-C4-elf32-readelf.txt], [X33-C4-elf64-resultados.txt] |
| P13–P16 e X36 | **Confirma** a lacuna de C5, sem concluir o teste com um hash que tenha resultado de detecção. O registro mostrou `Clean (0)` para um hash cuja consulta direta retornou HTTP 404; sem chave, houve aviso e carving, mas novamente `Clean (0)`. | [X35-C5-com-chave-resultados.txt], [X36-vt-hash-resposta.txt], [P16-C5-sem-chave-execucao.txt], [X37-C5-sem-chave-resultados.txt] |
| P17–P18 | **Confirma** o impedimento já identificado para C6. `evidence2.dd` estava ausente e o comando da Figura 2 não foi executado. | [P17-evidence2-presenca.txt] |
| P19 | **Não altera** R: C7 é arquitetural e está fora da regra de atribuição. | [P19-C7-inspecao.txt] |

**F — Não atribuir; mudou: não.** A compilação e o teste mínimo elevam a evidência de funcionamento. Persistem, porém, requisitos obrigatórios do README sem atendimento: dependências e versões completas e um exemplo mínimo [instrucoes-oficiais.md:Funcional (F); README.md:21-85]. A confiança de que o comitê oficial atribuiu F sobe de **15 para 25/100** pela execução observada, sem mudar a decisão fundamentada na documentação.

**R — Não atribuir; mudou: não.** O pacote continua sem instruções e processo específicos para reproduzir C1–C6, e a entrada indispensável para comparar a Figura 2 permanece ausente [instrucoes-oficiais.md:Reprodutível (R); reivindicacoes.md:Regra para o selo R; registro-factual.md:C6]. Os controles D2/D3 reforçam problemas em C1–C3, mas não substituem os dados dos autores. A confiança de que o comitê oficial atribuiu R cai de **3 para 1/100**.

Não uso **Indeterminado** para nenhum selo porque há falhas em critérios obrigatórios já documentadas. Para resolver as incertezas restantes por reivindicação, faltam especialmente a imagem exata `evidence2.dd` para C6 e, para C5, uma entrada com hash que tenha resposta de detecção verificável no VirusTotal. C4 ainda carece de validação completa com entradas identificadas pelos autores.

```json
{
  "F": {
    "decisao": "Não atribuir",
    "confianca": 25,
    "mudou": false,
    "evidencias": [
      "instrucoes-oficiais.md:Funcional (F)",
      "README.md:21-85",
      "registro-factual.md:P5-P8",
      "P8-audit.txt",
      "X6-F-comparacao.txt"
    ]
  },
  "R": {
    "decisao": "Não atribuir",
    "confianca": 1,
    "mudou": false,
    "evidencias": [
      "instrucoes-oficiais.md:Reprodutível (R)",
      "reivindicacoes.md:Regra para o selo R",
      "registro-factual.md:C1-C6",
      "X42-C1-cauda-resultados.txt",
      "X16-C2-negativo-resultados.txt",
      "X24-C3-thin32-audit.txt",
      "X26-C3-thin64-audit.txt",
      "P17-evidence2-presenca.txt"
    ],
    "por_reivindicacao": {
      "C1": "nao_reproduzivel",
      "C2": "nao_reproduzivel",
      "C3": "nao_reproduzivel",
      "C4": "depende_execucao",
      "C5": "depende_execucao",
      "C6": "nao_reproduzivel"
    }
  }
}
```
