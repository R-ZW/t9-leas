# Resumo da Execução Prática (Etapa E)

A execução do roteiro experimental foi concluída dentro do contêiner Docker `t9-gemini-c1` (Ubuntu 24.04.2 LTS x86_64), e os resultados factuais detalhados foram documentados em `D:\t9-trabalho\gemini-c1\execucao\registro-factual.md`.

### Principais Ações Realizadas:
1. **Ambiente e Dependências (P1–P2):** O ambiente foi inspecionado, confirmando Ubuntu 24.04.2 LTS e a presença ativa da variável `VT_API_KEY` (mantida mascarada). As dependências `gcc`, `make`, `git`, `libssl-dev`, `libcurl4-openssl-dev`, `python3`, `file` e `binutils` foram instaladas via APT com sucesso.
2. **Compilação e Instalação (P3–P5):** O artefato `/home/revisor/artefato.zip` foi descompactado. A compilação via `make clean && make` gerou o binário ELF 64-bit `foremost-ng` (86 KB), que foi instalado com sucesso em `/usr/local/bin/foremost-ng`.
3. **Teste Mínimo Funcional (P6–P8):** As opções de linha de comando (`-V` e `-h`) funcionaram sem falhas, exibindo a versão 1.5.7 e menu de ajuda. O carving sobre uma imagem sintética mínima (`test_minimo.img`) extraiu com sucesso uma imagem PNG (`00002048.png`, 1x1, 67 B) e gerou o log `audit.txt`.
4. **Reivindicações C1 a C4 (P9–P16):**
   - **C1 (EVTX):** Extraiu log de eventos do Windows de 128 KiB (2 chunks de 64 KiB), validado pelo utilitário `file` como `MS Windows 10-11 Event Log`.
   - **C2 (Scripts):** Extraiu 3 scripts (Bash, POSIX shell e Python), delimitados por sentinela não imprimível, preservando a linha de interpretador (`#!`) e o corpo legível.
   - **C3 (Mach-O):** Extraiu binário Mach-O universal FAT (`0xCAFEBABE`) de 5120 bytes, validado pelo `file` como `Mach-O universal binary`. Identificou-se no código-fonte discrepância de endianness na rotina de busca de binários Mach-O thin de 64 bits.
   - **C4 (ELF):** Extraiu executável ELF de 64 bits (12304 bytes), com 13 cabeçalhos `PT_LOAD` íntegros validados por `readelf -l`. O binário extraído foi executado diretamente e retornou o código de saída 42 conforme projetado.
5. **Reivindicação C5 (VirusTotal - P17–P18):** Sem a chave `VT_API_KEY`, emitiu o aviso documentado e manteve o carving com `Clean (0)`. Com a chave ativa, calculou o SHA-256 e efetuou a consulta HTTPS à API do VirusTotal via libcurl sem erros. A funcionalidade da API e da chave foi adicionalmente confirmada com hash conhecido do EICAR (HTTP 200, 66 detecções).
6. **Reivindicação C6 (Figura 2 / `evidence2.dd` - P19–P20):** A busca por `evidence2.dd` confirmou que a imagem não existe no sistema nem acompanha o artefato. A execução do comando da Figura 2 (`./foremost-ng -v -x evidence2.dd`) falhou com erro de arquivo não encontrado (`[!] File not found or is a directory: evidence2.dd`), inviabilizando a reprodução da tabela e offsets publicados.

Todos os logs de execução, scripts (`step_p1.sh` a `step_p20.sh`), saídas e amostras recuperadas encontram-se salvos em `D:\t9-trabalho\gemini-c1\execucao`.