Reli o [registro factual](<D:\user\unipampa\8º Semestre\LEAS\atividades\t9\t9-leas\llm-openai\cadeia-1\execucao\registro-factual.md>) e as evidências citadas. Os testes D2 e D3 são **complementares**: mostram comportamentos da versão avaliada, mas não substituem as entradas nem os resultados dos autores.

| Passos | Relação com a avaliação analítica |
|---|---|
| P1–P4 | **Não alteram** os selos: prepararam o ambiente e fixaram o commit correto [P4-checkout.log]. |
| P5–P6, P9 | **Confirmam** execução básica: `make` e instalação terminaram, e o teste mínimo produziu arquivos e `audit.txt` [P5-make-attempt1.log; P9-output-inventory.log]. Resolvem a incerteza sobre executar *alguma* funcionalidade, mas não suprem as informações obrigatórias ausentes do README. |
| P7 | **Não altera** a lacuna do README: o manual abriu, mas o critério exige dependências, versões e exemplo mínimo no README [P7-man.log; README.md:21–35,74–85]. |
| P8 e X1 | **Não alteram** a reprodução dos autores: as entradas foram obtidas de terceiros ou construídas pelo revisor [registro-factual.md:Entradas e downloads]. |
| P10 e X2 | **Confirmam parcialmente** C1: `evtxinfo` leu os dois EVTX. **Contradizem** a delimitação precisa reivindicada: ambos saíram maiores que as origens, embora preservem seus bytes iniciais [P10-C1-evtxinfo.log; P10-C1-bytes.log]. |
| P11 | **Confirma** o risco identificado no código: os três scripts positivos saíram, mas também saiu, byte a byte, o script que continha só comentários [P11-C2-validate.log]. |
| P12 | **Confirma** a falha analítica dos ramos `thin`: apenas o Mach-O `fat` apareceu [P12-C3-validate.log; src/extract.c:2359–2363,2408–2409]. |
| P13 | **Contradiz** a expectativa ainda pendente para C4: o ELF32 saiu íntegro; o ELF64 saiu menor e `readelf` apontou cabeçalhos de seção além do fim do arquivo [P13-C4-validate.log; P13-C4-readelf64-sections.log]. |
| P14–P15 e X4 | **Não demonstram** o resultado VT dos autores: com chave, os dois hashes ELF receberam HTTP 404 na conferência direta, enquanto o log marcou `Clean (0)` [P15-C5-output.log; P15-C5-direct-api.log]. |
| P16–P17 | **Confirmam** aviso e recuperação sem chave; também registram `Clean (0)` na coluna VT nessa condição [P17-C5-no-key.log; P17-C5-output.log]. |
| X3 | **Confirma**, como teste externo D3, uma consulta VT positiva: o ZIP EICAR foi recuperado integralmente, e `Malicious (61)` coincidiu com a API. Não reproduz o exemplo ELF ou a Figura 2 dos autores [X3-eicar-output.log; X3-eicar-direct-api.log]. |
| P18–P19 | **Confirmam** a lacuna decisiva de C6: `evidence2.dd` não estava disponível e o comando da Figura 2 não foi executado [P18-C6-blocked.log]. |
| P20 | **Confirma** a inspeção estrutural de C7; C7 permanece fora da regra de R [P20-C7-inspection.log; reivindicacoes.md:§Regra para o selo R]. |

**F — Não atribuir; decisão não mudou.** A execução agora prova funcionalidade mínima, mas o README continua sem versões de dependências/ambiente e sem exemplo mínimo completo, exigidos por [instrucoes-oficiais.md:§Funcional (F)]. Minha estimativa de que o comitê oficial atribuiu F sobe de **15 para 25/100** pela execução observada. O resultado oficial e eventuais esclarecimentos dos autores não estão nos materiais.

**R — Não atribuir; decisão não mudou.** A regra exige C1–C6 reproduzidas [reivindicacoes.md:§Regra para o selo R]. C6 não pode ser confrontada com a Figura 2 sem `evidence2.dd`; isso é falha de um requisito obrigatório pela regra de decisão, não motivo para deixar o selo indeterminado. A incompatibilidade `thin` de C3, já visível no código, recebeu confirmação complementar em P12. A documentação também continua sem o processo dos autores e instruções por reivindicação [instrucoes-oficiais.md:§Reprodutível (R); README.md:74–107]. Minha estimativa de atribuição oficial cai de **3 para 1/100**.

Para as reivindicações ainda marcadas `depende_execucao`, falta especificamente **uma entrada identificada dos autores e seu procedimento de comparação**; os ensaios D2/D3 não fornecem isso. Em C6 falta a própria `evidence2.dd`. Essas lacunas não tornam a decisão **global** indeterminada, pois já há critérios obrigatórios não atendidos.

```json
{
  "F": {
    "decisao": "Não atribuir",
    "confianca": 25,
    "evidencias": [
      "instrucoes-oficiais.md:§Funcional (F)",
      "README.md:21-35",
      "README.md:74-85",
      "P5-make-attempt1.log:linkedição",
      "P9-output-inventory.log:arquivos e audit.txt"
    ],
    "mudou": false
  },
  "R": {
    "decisao": "Não atribuir",
    "confianca": 1,
    "evidencias": [
      "instrucoes-oficiais.md:§Reprodutível (R)",
      "reivindicacoes.md:§Regra para o selo R",
      "src/extract.c:2359-2363",
      "src/extract.c:2408-2409",
      "P12-C3-validate.log:saída Mach-O",
      "P13-C4-validate.log:ELF64",
      "P18-C6-blocked.log:ausência de evidence2.dd"
    ],
    "por_reivindicacao": {
      "C1": "depende_execucao",
      "C2": "nao_reproduzivel",
      "C3": "nao_reproduzivel",
      "C4": "nao_reproduzivel",
      "C5": "depende_execucao",
      "C6": "nao_reproduzivel"
    },
    "mudou": false
  }
}
```
