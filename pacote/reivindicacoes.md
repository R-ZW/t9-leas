# Reivindicações principais — Foremost-NG (SBSeg 2025)

Lista fixada antes da avaliação a partir do artigo (`artigo.pdf`) e do artefato na versão `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` (`artefato.txt`). Páginas: numeração do PDF, de 1 a 8. Seções do README: títulos do `README.md` em `artefato.txt`.

| ID | Reivindicação | Onde está no artigo | Resultado esperado | O README indica como reproduzir? |
|---|---|---|---|---|
| C1 | Recuperação de logs de eventos do Windows (EVTX): o parser reconhece a assinatura `ElfFile`, delimita os chunks de 64 KiB e extrai o log | p. 1 (resumo); p. 2 (introdução); p. 6, §3, item "Windows Event Logs (EVTX)"; p. 7, §4.1 (exemplo `-t evtx,elf,exe`) | arquivo `.evtx` extraído, legível por ferramenta de análise de eventos | parcial: "Installation" e "Usage" (compilação e sintaxe geral) |
| C2 | Recuperação de scripts (Bash, Python, PowerShell) reconhecidos por shebang (`#!`) e conteúdo textual, com mínimo de 32 bytes e mais que só comentários | p. 1 (resumo); p. 2 (introdução); p. 6, §3, item "Script Files" | script extraído com a linha do interpretador e o corpo legível | parcial: "Installation" e "Usage" |
| C3 | Recuperação de binários Mach-O `fat` e `thin`, usando o cabeçalho universal ou os comandos de carga para determinar o tamanho | p. 1 (resumo); p. 2 (introdução); p. 6, §3, item "Mach-O (macOS/iOS Binaries)" | binário Mach-O extraído e reconhecível por ferramenta apropriada | parcial: "Installation" e "Usage" |
| C4 | Recuperação de executáveis ELF de 32 e 64 bits, delimitados pelos cabeçalhos de programa | p. 1 (resumo); p. 2 (introdução); p. 6, §3, item "ELF"; p. 7, §4.1 (exemplos `-t evtx,elf,exe` e `-x -t elf`) | arquivo `.elf` extraído e estruturalmente legível por analisador ELF | parcial: "Installation" e "Usage" |
| C5 | Enriquecimento pelo VirusTotal: com `-x` e `VT_API_KEY`, consulta a API pelo hash de cada arquivo recuperado e registra o resultado de detecção | p. 1 (resumo); pp. 2–3, §2; p. 7, §4 e §4.1; p. 8, Fig. 2 (coluna VT) | consulta associada ao hash do arquivo extraído, com o resultado de detecção registrado; sem chave, aviso e carving sem consulta (p. 7) | parcial: "VirusTotal API" e "Usage" |
| C6 | Exemplo de execução da Figura 2: `./foremost-ng -v -x evidence2.dd` | p. 7, §4.2; p. 8, Fig. 2 | tabela como a da Fig. 2, com arquivos ELF, script, EXE e ZIP, seus offsets e a coluna VT | não |
| C7 | Arquitetura de parsers extensível: despachante central e parsers com identificador, assinatura, validação e recuperação | p. 1 (resumo); pp. 2–3, §2 e Fig. 1; p. 8, §5 | organização do código correspondente à Fig. 1 | não |

## Regra para o selo R

O README não marca reivindicações a reproduzir. Por isso, valem as reivindicações principais desta lista: **C1 a C6**. **R é atribuído se C1 a C6 forem reproduzidas.** C7 é uma contribuição arquitetural, sem experimento associado no artigo; ela pode ser inspecionada, mas não entra na regra de R.

## Critério de reprodução

As reivindicações descrevem comportamentos, sem valores numéricos com tolerância declarada pelos autores. Uma reivindicação é reproduzida quando o resultado esperado da tabela é observado. Em C6, comparam-se os arquivos e offsets da Fig. 2. As contagens do VirusTotal mudam com o tempo e não precisam coincidir.
