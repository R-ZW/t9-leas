Executei o roteiro no contêiner `t9-claude-c1` (Ubuntu 24.04.2, x86_64). O registro completo está em `D:\Lab-artefatos\t9-trabalho\claude-c1\execucao\registro-factual.md`. Não decidi os selos.

**Preparação e teste mínimo (F)**
- O `artefato.zip` confere: o SHA-256 bate e o commit é bb812a22.
- O `make` na raiz, como manda o artigo, falhou com "no makefile found" (exit=2).
- O `make` em `src/` (README), com as dependências do Dockerfile, compilou com 2 avisos. O `sudo make install` instalou o binário, a man page e o `foremost.conf`.
- `-h`, `-V` (1.5.7) e `man` funcionam. O manual não cita os formatos evtx, elf, macho e script.
- No teste mínimo (`-i img -o dir`) saíram os 2 arquivos esperados: `.elf` e `.script`. O script é idêntico ao original. O ELF saiu sem a tabela de seções.

**C1 – EVTX:** extraído nos dois testes, com prefixo idêntico ao original, e o python-evtx leu o mesmo número de registros (394 e 1601). Os tamanhos não batem com os originais:
- na primeira amostra, 25.886.720 B, que é o valor do deslocamento 0x18 (395) × 65536;
- na segunda, a extração foi até o fim da imagem.

**C2 – Scripts:** os scripts bash, python e pwsh saíram idênticos, com extensão `.script`. O de 18 B foi ignorado. O de 66 B só com comentários foi extraído, o que fere o critério do roteiro.

**C3 – Mach-O:** o fat saiu idêntico. Nenhum thin foi extraído: nem os objetos x86_64, arm64 e i386, nem dois executáveis compilados em Go (este último teste está marcado como fora do roteiro).

**C4 – ELF:** ELF32 e ELF64 foram extraídos. O readelf lê o cabeçalho e os segmentos, os arquivos são prefixos idênticos dos originais e executam, mas faltam as tabelas de seções. Os comandos `-t evtx,elf,exe` e o modo padrão do artigo se comportaram como descrito.

**C5 – VirusTotal**
- Com a chave válida, o ZIP EICAR extraído (idêntico ao original) recebeu `Malicious (62)`. A consulta direta à API pelo mesmo hash também deu malicious 62. O ELF recebeu `Clean (0)`, e a API responde NotFoundError para esse hash.
- Sem chave, apareceu um aviso por arquivo, e mesmo assim os dois arquivos ficaram rotulados `Clean (0)`.
- Com chave inválida, não houve aviso e os dois ficaram `Clean (0)`, inclusive o EICAR.
- Nenhuma execução gerou `recovery.log`, e o hash não aparece no audit.txt.

**C6 – Fig. 2:** `evidence2.dd` não existe no artefato. P43 e P44 ficaram bloqueados.

**Fora do roteiro:** P8b (resto do manual), P15b (hashes dos pacotes do pip), P19b (segunda amostra EVTX) e P27b (Mach-O ligados via Go), cada um com justificativa no registro. Todos os passos estão classificados de D0 a D3.

**Evidências**
- Ficam em `execucao\`: logs em `logs\Pn.log`, scripts executados em `scripts\` e saídas em `saidas\` (os audit.txt e um manifesto SHA-256).
- O pacote completo de saídas ficou só no contêiner porque contém o EICAR.
- A chave do VirusTotal não aparece em nenhum arquivo; conferi com `grep` (0 ocorrências).