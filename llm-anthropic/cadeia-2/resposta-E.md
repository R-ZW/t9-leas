Executei o roteiro (P1 a P32) dentro do contêiner `t9-claude-c2`, entre 15:47 e 16:00 UTC de 2026-10-24. O registro factual está em D:\Lab-artefatos\t9-trabalho\claude-c2\execucao\registro-factual.md. Os logs e hashes de cada passo estão na mesma pasta, com índice em SHA256SUMS.txt. Não decidi os selos.

**F (teste mínimo):**
- O artefato.zip confere com o índice: SHA-256 955c770e…, commit bb812a22, e os hashes dos arquivos batem.
- Instalei as dependências listadas no Dockerfile: gcc 13.3.0, OpenSSL 3.0.13, libcurl 8.5.0.
- `make` e `sudo make install` terminaram com exit 0, com dois avisos `-Wunused-result`.
- `-h`, `-V` (1.5.7) e `man foremost-ng` funcionaram. A seção de formatos do manual não lista elf, macho, evtx nem script.
- Na imagem DFTT #11 (MD5 conferido), a ferramenta extraiu 14 arquivos e gerou audit.txt. 10 dos 15 arquivos que o DFTT publica saíram com MD5 idêntico. Nenhum recovery.log foi gerado.

**R, por reivindicação** (fatos observados):
- **C1 (EVTX):** usei duas amostras públicas do python-evtx. Os dois arquivos foram extraídos maiores que os originais, com o início idêntico. Lidos pela biblioteca, deram as mesmas contagens dos originais: 1601 e 2261 registros, 9 e 26 chunks. O comando `evtx_dump` do pacote está quebrado, então usei um script que chama a biblioteca diretamente (marcado [FORA DO ROTEIRO]).
- **C2 (scripts):** os 3 scripts com shebang saíram com hash idêntico ao original. O controle com menos de 32 bytes não foi extraído. O controle que só tem comentários foi extraído.
- **C3 (Mach-O):**
  - Thin: com os binários do jq 1.7.1 para macOS, saíram 0 arquivos. Com `-a`, a ferramenta grava "(Header dump)" nos dois offsets, ou seja, encontra a assinatura mas não extrai o arquivo.
  - Fat: o universal binary montado por mim foi extraído com hash idêntico.
  - Mach-O de 32 bits não foi testado.
- **C4 (ELF):** os ELF de 32 e de 64 bits foram extraídos como prefixos idênticos dos originais e com a classe correta no `readelf -h -l`. Todos ficaram sem a tabela de seções ("extends past end of file for section headers"), e os símbolos FUNC no e64 caíram de 12 para 0.
- **C5 (VirusTotal):**
  - Sem chave: a extração acontece, aparece o aviso "VT_API_KEY … not set" e o audit registra "Clean (0)".
  - Com chave, nos 3 ELF: o audit registra "Clean (0)". Consultei a API pelo hash e ela devolveu 404 para os 3.
  - Com chave, no eicar_com.zip (extraído com hash idêntico): o audit registra "Malicious (62)", e a API confirma malicious=62.
  - O audit.txt não tem coluna de hash.
- **C6 (Fig. 2):** bloqueada. evidence2.dd não está no ZIP nem em nenhum commit do repositório.

**Desvios registrados:**
- `curl` e `file` foram instalados antes do previsto (em P7/P8, em vez de P9).
- O código avaliado é o do ZIP; o clone serviu só para confirmar que o commit existe.
- Dois passos [FORA DO ROTEIRO]: P13b (o script para o EVTX) e P20b (o diagnóstico com `-a`).
- Removi da pasta de evidências o tgz das saídas (13,5 MB). Ele continha o EICAR extraído, que iria parar no Windows. Mantive o hash de cada arquivo de saída em P32-saidas-sha256.txt.
- Não alterei o código do artefato, não enviei arquivos ao VirusTotal (só consultas por hash) e verifiquei que a chave não aparece em nenhum arquivo de evidência.