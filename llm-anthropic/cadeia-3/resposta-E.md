Segui o roteiro no contêiner `t9-claude-c3` das 15:46 às 16:02 UTC. Nenhum selo foi decidido. O registro completo está em `D:\Lab-artefatos\t9-trabalho\claude-c3\execucao\registro-factual.md`; logs, manifestos e hashes de cada passo estão na mesma pasta.

**Preparação e compilação**
- **Artefato:** confere. SHA-256 955c770e… e commit bb812a22, igual ao clone exceto pelos fins de linha (CRLF no zip).
- **Instalação do artigo (P4):** falha. `make` na raiz responde "No targets specified and no makefile found".
- **Instalação do README (P5–P6):** funciona. `make` em `src/` compila só com 2 avisos, e `sudo make install` instala binário, man page e configuração.

**Teste mínimo (F)**
- Ajuda, versão (1.5.7) e `man` funcionam. A man page não lista os formatos evtx, elf, macho nem script.
- Na imagem DFTT nº 11, citada pelos autores: 14 arquivos extraídos, 10 dos 15 do gabarito com MD5 idêntico.

**Fatos por reivindicação**

| Reivindicação | O que foi observado |
|---|---|
| C1 EVTX | Os 3 arquivos extraídos foram lidos pelo python-evtx com a mesma contagem de registros do original. Um EVTX isolado sai até o fim da imagem (66 MB contra 1,1 MB). Com dois EVTX seguidos, o primeiro sai idêntico ao original. |
| C2 Scripts | Bash, Python e PowerShell saem idênticos ao original. O controle com menos de 32 bytes foi rejeitado. O controle só com comentários **foi extraído**. |
| C3 Mach-O | Os dois universais (fat) saem idênticos ao original. **Nenhum thin** (i386, x86_64 objeto e x86_64 executável) foi extraído. Com `-a`, os cabeçalhos thin aparecem só como "Header dump". |
| C4 ELF | ELF32 e ELF64 extraídos sem a tabela de seções. `readelf -h -l` retorna rc=0, mas imprime erro sobre os cabeçalhos de seção. Os binários extraídos executam. |
| C5 VirusTotal | Sem chave: um aviso por arquivo e "Clean (0)". Chave inválida: **nenhum aviso** e "Clean (0)". Chave válida: os rótulos batem com a consulta direta por hash (EICAR "Malicious (65)", zcat "Clean (61)", ELF extraído desconhecido do VT → "Clean (0)"). O audit não registra hashes. |
| C6 Figura 2 | Bloqueado: evidence2.dd não está disponível. P32 e P33 não foram executados. |

No exemplo do artigo com `-t evtx,elf,exe`, a DLL zlib1.dll não foi extraída: todas as DLLs de `windows_dlls` são PE32+ (64 bits) e essa versão não as extrai. A Fig. 2 lista 6 arquivos .exe.

**Passos fora do roteiro (todos registrados)**
- **Validador EVTX:** o `evtx_dump` instalado pelo pip falha por erro de empacotamento, então escrevi `valida_evtx.py` usando a API da mesma biblioteca.
- **Executáveis Mach-O:** gerados na 2ª tentativa com `-undefined dynamic_lookup`.
- **Diagnósticos com `-a`:** feitos para Mach-O e para PE.
- **Amostras de C5:** troquei as DLLs previstas por zcat e EICAR, que o VT conhece e que são extraídos sem alteração. O EICAR é extraído por uma entrada de configuração minha (`c5.conf`).

A chave do VirusTotal não aparece em nenhum arquivo de evidência (checagem com `grep` retornou 0 arquivos).