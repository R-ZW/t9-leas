# Registro factual da execução — cadeia 1

## Escopo e ambiente observado

Todos os comandos de instalação, preparação, extração e validação foram executados **dentro** de `t9-openai-c1`, por `docker exec t9-openai-c1 bash -lc '<comando>'`. Este registro não decide os selos F ou R. Os arquivos de saída citados estão nesta pasta `execucao`; os arquivos grandes de trabalho permaneceram no contêiner.

| Item | Valor observado | Evidência |
|---|---|---|
| Sistema | Ubuntu 24.04.2 LTS; kernel `6.18.54.1-microsoft-standard-WSL2` | `E-ambiente.log` |
| Compilação | GCC `13.3.0`, GNU Make `4.3`, Git `2.43.0`, OpenSSL `3.0.13` | `E-ambiente.log`, `E-pacotes-observados.log` |
| Bibliotecas de desenvolvimento | `libssl-dev` `3.0.13-0ubuntu3.5`; `libcurl4-openssl-dev` `8.5.0-2ubuntu10.6` | `E-pacotes-observados.log` |
| Verificadores adicionais | Python `3.12.3`, `file` `5.45`, binutils `2.42`, libevtx-utils `20181227` | `E-pacotes-observados.log` |
| Revisão executada | `bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` | `P4-checkout.log` |
| ZIP disponibilizado | 7.252.858 bytes; SHA-256 `955c770e29893527f789e11afc28dcc6b83d7af4a64f14b416e39f554b388e0a` | `E-artefato-zip.log` |
| Chave VT | Presente no ambiente; valor não exibido nem salvo | `P14-VT-key-presence.log` |

O contêiner inicial não tinha compilador, Python nem o executável `curl`. P1–P2 instalaram as dependências listadas no Dockerfile; verificadores adicionais foram instalados em X1 e X2. A existência de `VT_API_KEY` foi testada sem imprimir seu valor.

## Entradas e downloads

`disk.img` e `memory.dump` foram **criados pelo revisor**, byte a byte idênticos, com 5.242.880 bytes e SHA-256 `68a0f593fa71c67b9d402efdf9fa7ca35107442cf4a1f03720ed7b025826d5a0`. Contêm EVTX públicos, um ELF64 do próprio Ubuntu, um ELF32 construído para o teste, scripts positivos e só com comentários, e Mach-O `fat`/`thin` construídos para o teste. Seus offsets e hashes individuais constam de `P8-input-manifest.txt`. Não são dados dos autores.

| Download | URL e identificação | Tamanho e SHA-256 registrado |
|---|---|---|
| Repositório dos autores | `https://github.com/cristianzsh/foremost-ng.git`, checkout `bb812a22...` | Pack Git recebido: 7.346.023 bytes; `b401a815267657f3e7b9461063c313d2c9ff0b8bf9eacbda6bb7a190decb4e66` |
| Repositório de amostras EVTX | `https://github.com/williballenthin/python-evtx.git`, commit `c0007441657899c39180de10a2be1a0e43dbeaf9` | Pack Git recebido: 450.422 bytes; `424ba643e1385cea0cd801dd0e594508c77efc90fb45c2d7add73d9a8fae0c0e` |
| `issue_38.evtx` desse repositório | `tests/data/issue_38.evtx` no commit acima | 69.632 bytes; `becab64455866f8fae5583fbaa5dab901115e4397ea7abe14f37ad732d5d7eb9` |
| `security.evtx` desse repositório | `tests/data/security.evtx` no commit acima | 2.166.784 bytes; `5f29a03cf8c1b4bfbd82c4074ccc81ecfe85d7ee15375afc352ed5025c9a4d8d` |
| ZIP EICAR | `https://secure.eicar.org/eicar_com.zip` | 184 bytes; `2546dcffc5ad854d4ddc64fbf056871cd5a00f2471cb7a5bfd4ac23b6e9eedad` |

As medidas dos packs Git e os commits constam de `E-downloads-git.log`; as medidas das amostras, de `P8-evtx-hashes.txt` e `X3-eicar-download.log`. O ZIP EICAR não foi copiado para a pasta de evidências. A imagem da Figura 2, `evidence2.dd`, não foi fornecida.

## Passos do roteiro

Na coluna **desvio**, D0 é procedimento dos autores sem alteração, D1 é ajuste de ambiente, D2 é passo ou entrada proposta pelo revisor, e D3 é teste com dados de terceiros. Em passos com procedimento dos autores mas entrada do revisor, a classificação reflete a entrada. Um redirecionamento para arquivo de evidência não altera o comando avaliado.

| Passo | Comando exato executado | Resultado esperado | Resultado observado, trecho e código | Evidência | Status | Desvio |
|---|---|---|---|---|---|---|
| P1 | `sudo apt-get update` | Índices apt atualizados | `Fetched 64.9 MB`; código 0 | `P1-apt-update.log` | sucesso | D1 |
| P2 | `sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev` | Dependências instaladas | `Setting up gcc`; código 0 | `P2-apt-install.log` | sucesso | D1 |
| P3 | `cd /tmp && git clone https://github.com/cristianzsh/foremost-ng.git` | Fonte obtida | `Cloning into 'foremost-ng'`; código 0 | `P3-git-clone.log`, `E-downloads-git.log` | sucesso | D0 |
| P4 | `cd /tmp/foremost-ng && git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d` | Versão do pacote fixada | `HEAD is now at bb812a2`; código 0 | `P4-checkout.log` | sucesso | D2 |
| P5 | `cd /tmp/foremost-ng/src && make` | Binário compilado | Linkou `foremost-ng -lssl -lcrypto -lcurl`; código 0; houve avisos sobre retorno de `realpath` | `P5-make-attempt1.log` | sucesso | D0 |
| P6 | `cd /tmp/foremost-ng/src && sudo make install` | Binário, configuração e manual instalados | Instalação em `/usr/local/bin`, `/usr/local/etc` e `/usr/share/man/man8`; código 0 | `P6-make-install.log` | sucesso | D0 |
| P7 | `cd /tmp/foremost-ng/src && man foremost-ng` | Manual legível | Título `FOREMOST-NG(8)` e sinopse exibidos; código 0 | `P7-man.log` | sucesso | D0 |
| P8a | `git clone --depth 1 https://github.com/williballenthin/python-evtx.git /tmp/python-evtx` | Entrada EVTX conhecida | Clone concluído, commit `c000744...`, seis EVTX encontrados; código 0 | `P8-evtx-source.log`, `P8-evtx-hashes.txt` | sucesso | D3 |
| P8b | `python3 - << "PY"` com o corpo literal de `P8-generate-heredoc.py` e terminador `PY` | Entradas nos offsets declarados | Imagens de 5.242.880 bytes e 11 componentes identificados; código 0 | `P8-generate-heredoc.py`, `P8-generate.log`, `P8-input-manifest.txt`, `P8-input-validation.log` | sucesso | D2 |
| P8c | `sudo mkdir -p /temp/output && sudo chown revisor:revisor /temp/output` | Destino de saída gravável | `/temp/output` pertence a `revisor`; código 0 | `P8-output-dir.log` | sucesso | D1 |
| P9 | `cd /tmp/foremost-ng/src && foremost-ng -i disk.img -o /temp/output/carved` | Ao menos uma recuperação e log | `[INFO] Processing finished`; código 0; foram listados scripts, ELF, Mach-O, EVTX e `audit.txt` | `P9-minimal-F.log`, `P9-output-inventory.log`, `P9-audit.txt` | sucesso | D2 |
| P10 | `cd /tmp/foremost-ng/src && foremost-ng -t evtx,elf,exe -i disk.img -o /temp/output/c1` | EVTX recuperados e legíveis | Concluiu com código 0; `evtxinfo` abriu os dois extraídos com código 0; saídas de 126.976 e 5.111.808 bytes excedem as origens de 69.632 e 2.166.784 bytes | `P10-C1.log`, `P10-C1-evtxinfo.log`, `P10-C1-bytes.log`, `P10-audit.txt`, `P10-00000008.evtx` | sucesso | D3 |
| P11 | `cd /tmp/foremost-ng/src && foremost-ng -i disk.img -o /temp/output/c2` | Três scripts positivos; rejeição de só comentários | Comando terminou com código 0; quatro scripts foram extraídos byte a byte, inclusive `only-comments.script` de 72 bytes | `P11-C2.log`, `P11-C2-validate.log`, `P11-script-files/`, `P11-audit.txt` | falha | D2 |
| P12 | `cd /tmp/foremost-ng/src && foremost-ng -i disk.img -o /temp/output/c3` | Mach-O `fat` e dois `thin` | Comando terminou com código 0; apenas `00008224.macho` (`fat`, 160 bytes) apareceu e coincide byte a byte com a origem; nenhum dos dois `thin` apareceu | `P12-C3.log`, `P12-C3-validate.log`, `P12-macho-files/`, `P12-audit.txt` | falha | D2 |
| P13 | `cd /tmp/foremost-ng/src && foremost-ng -t evtx,elf,exe -i disk.img -o /temp/output/c4` | ELF32 e ELF64 legíveis | Comando terminou com código 0; ELF32 saiu íntegro, 128 bytes; ELF64 saiu com 24.596 de 26.936 bytes, e `readelf -S` emitiu `Reading 1920 bytes extends past end of file for section headers` | `P13-C4.log`, `P13-C4-validate.log`, `P13-C4-readelf64-sections.log`, `P13-elf-files/`, `P13-audit.txt` | falha | D2 |
| P14 | `if [ -n "${VT_API_KEY:-}" ]; then echo "VT_API_KEY=present"; else echo "VT_API_KEY=absent"; fi` | Chave VT disponível | `VT_API_KEY=present`; código 0; valor não impresso | `P14-VT-key-presence.log` | sucesso | D1 |
| P15 | `cd /tmp/foremost-ng/src && foremost-ng -x -t elf -i memory.dump -o ./carved-files` | Hashes consultados e resultado VT registrado | Comando terminou com código 0; dois ELF registrados como `Clean (0)`; consulta independente dos mesmos hashes retornou HTTP 404 para ambos | `P15-C5-with-key.log`, `P15-C5-output.log`, `P15-C5-direct-api.log`, `P15-audit.txt` | inconclusivo | D2 |
| P16 | `unset VT_API_KEY` no mesmo shell de P17 | Condição sem chave | `VT_API_KEY=absent`; código 0 | `P16-unset-VT.log` | sucesso | D2 |
| P17 | `cd /tmp/foremost-ng/src && foremost-ng -x -t elf -i memory.dump -o ./carved-files-no-key` | Aviso, carving sem consulta | Duas mensagens `VT_API_KEY environment variable is not set`, dois ELF extraídos; código 0; coluna VT ainda disse `Clean (0)` | `P17-C5-no-key.log`, `P17-C5-output.log`, `P17-audit.txt` | sucesso | D2 |
| P18 | `unzip -Z1 /home/revisor/artefato.zip | grep -i "evidence2.dd"` e `test -f /tmp/foremost-ng/src/evidence2.dd` | Imagem original disponível | Ambos os testes de presença foram negativos; `ZIP=evidence2.dd absent`, `WORKTREE=evidence2.dd absent`; a indisponibilidade pública e a ausência de resposta dos autores foram informadas na tarefa | `P18-C6-blocked.log` | bloqueado | D2 |
| P19 | `cd /tmp/foremost-ng/src && ./foremost-ng -v -x evidence2.dd` | Tabela e offsets da Figura 2 | Não executado, pois P18 não forneceu a imagem | `P18-C6-blocked.log` | não executado | D0 |
| P20 | `cd /tmp/foremost-ng/src && sed -n "369,385p" state.c` e `sed -n "2624,2630p;2678,2687p" extract.c` | Registro e despachante inspecionáveis | Trechos mostram `init_builtin` para ELF, Mach-O, EVTX e script, e despacho `extract_*`; código 0 | `P20-C7-inspection.log` | sucesso | D2 |

### Passos adicionais e tentativas registradas

Todos os passos desta tabela são **[FORA DO ROTEIRO]**. Foram necessários para preparar ou validar entradas sem procedimentos completos dos autores. Nenhum repetiu uma extração P9–P13 concluída.

| Passo | Comando exato ou operação | Motivo, resultado observado e código | Evidência | Status | Desvio |
|---|---|---|---|---|---|
| X1 | `sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y python3 file binutils` | Preparar entradas controladas e validar tipos; código 0 | `X1-extra-tools.log` | sucesso | D1 |
| X2a | `PYTHONPATH=/tmp/python-evtx python3 - << "PY"` com o corpo de `X2-evtx-python-validate-heredoc.py` e terminador `PY` | Primeira validação C1 falhou: `ModuleNotFoundError: No module named 'hexdump'`; código 1 | `X2-evtx-python-validate-heredoc.py`, `P10-C1-validate.log` | falha | D3 |
| X2b | `sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y python3-hexdump` | Tentativa de corrigir X2a: pacote inexistente no apt; código 100 | `X2-hexdump-install.log` | falha | D1 |
| X2c | `apt-cache search libevtx` | Localizou `libevtx-utils`; código 0 | `X2-libevtx-search.log` | sucesso | D1 |
| X2d | `sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y libevtx-utils` | Instalou validador alternativo; código 0 | `X2-libevtx-install.log` | sucesso | D1 |
| X2e | `evtxinfo <arquivo>` para as duas origens e duas saídas de P10 | Todas abriram com código 0; contagens de registros respectivas 1/1 e 2261/2261 | `P10-C1-evtxinfo.log` | sucesso | D3 |
| X3a | `python3 - << "PY"` com o corpo de `X3-eicar-download-heredoc.py` e terminador `PY` | Download direto do ZIP de teste: HTTP 200, 184 bytes, SHA-256 registrado; código 0 | `X3-eicar-download-heredoc.py`, `X3-eicar-download.log` | sucesso | D3 |
| X3b | `python3 - << "PY"` com o corpo de `X3-eicar-image-heredoc.py` e terminador `PY` | Imagem de 1.048.576 bytes; SHA-256 `fc7c9685ba83d01cd7c676a39a9ed31d912f962cc6fd23e22b4f5ed3ef867f68`; código 0 | `X3-eicar-image-heredoc.py`, `X3-eicar-image.log` | sucesso | D2 |
| X3c | `cd /tmp/foremost-ng/src && foremost-ng -x -t zip -i eicar.img -o ./carved-eicar` | Recuperou ZIP idêntico de 184 bytes e registrou `Malicious (61)`; código 0 | `X3-eicar-carve.log`, `X3-eicar-output.log`, `X3-eicar-audit.txt` | sucesso | D3 |
| X3d | `python3 - << "PY"` com o corpo de `X3-eicar-direct-api-heredoc.py` e terminador `PY` | Consulta só por hash do ZIP extraído: HTTP 200, `malicious: 61`; código 0; chave não salva | `X3-eicar-direct-api-heredoc.py`, `X3-eicar-direct-api.log` | sucesso | D3 |
| X4 (após P15) | `python3 - << "PY"` com o corpo de `P15-direct-api-heredoc.py` e terminador `PY` | Conferência por hash dos dois ELF: HTTP 404 para ambos; código 0; chave não salva | `P15-direct-api-heredoc.py`, `P15-C5-direct-api.log` | sucesso | D2 |

Os corpos literais dos comandos Python executados por here-doc foram copiados para os arquivos `*-heredoc.py` nesta pasta **depois da execução**, apenas para registrar os comandos; esses arquivos não foram executados como scripts. A consulta independente de P15 usou o corpo de `P15-direct-api-heredoc.py`.

As consultas independentes de P15 e X3d enviaram somente o SHA-256 por URL à API VirusTotal. Nenhum arquivo foi enviado à API. Em P15, foram consultados os hashes `6cc0b9b0da246ee2f8f6cecc4f007ada981bc88cc61fe2fab74494768d44ad9f` e `d0cd2bec3dc342c1c1fd5e8f858034cc600ae753`; ambos retornaram HTTP 404 (`P15-C5-direct-api.log`).

## C1 — EVTX: fatos observados

- As entradas públicas foram identificadas por `file` como EVTX (`P8-input-validation.log`). `issue_38.evtx` tinha 69.632 bytes e `security.evtx`, 2.166.784 bytes (`P8-evtx-hashes.txt`).
- P10 produziu dois `.evtx` nos offsets 4.096 e 131.072. Os tamanhos foram 126.976 e 5.111.808 bytes. Em ambos, os bytes iniciais até o tamanho da origem coincidiram (`PREFIX_RC=0`), mas o SHA-256 do arquivo completo diferiu (`P10-C1-bytes.log`).
- `evtxinfo` abriu origens e extrações com código 0. Para a primeira amostra, relatou 1 registro e 38 recuperados; para a segunda, 2.261 registros e 30 recuperados, tanto na origem quanto na saída (`P10-C1-evtxinfo.log`).

## C2 — scripts: fatos observados

- `file` identificou as três entradas positivas como scripts Bash, Python e `pwsh`; a quarta entrada tinha shebang e apenas uma linha de comentário (`P8-input-validation.log`, `P8-input-manifest.txt`).
- P11 extraiu quatro arquivos `.script`. Cada arquivo coincidiu byte a byte com sua entrada (`CMP_RC=0`), inclusive o de 72 bytes contendo só comentários (`P11-C2-validate.log`).

## C3 — Mach-O: fatos observados

- `file` reconheceu as entradas como Mach-O universal, i386 `thin` e x86-64 `thin` (`P8-input-validation.log`).
- P12 gerou somente `00008224.macho`, de 160 bytes. Seu SHA-256 `b16e9cd13bae6435bdf72a645c40bd4c808e463ab2340ad384e08e16602cf8f6` coincide com o `fat` original. Não apareceu saída nos offsets das entradas `thin` 4.194.304 e 4.202.496 (`P12-C3-validate.log`, `P8-input-manifest.txt`).

## C4 — ELF: fatos observados

- A entrada ELF32 tinha 128 bytes e um cabeçalho de programa `LOAD`; a entrada ELF64, derivada de `/bin/true`, tinha 26.936 bytes e 30 cabeçalhos de seção (`P8-input-validation.log`).
- P13 extraiu o ELF32 com os mesmos 128 bytes e SHA-256 `6cc0b9b0da246ee2f8f6cecc4f007ada981bc88cc61fe2fab74494768d44ad9f`. O ELF64 extraído tinha 24.596 bytes e SHA-256 diferente da origem (`P13-C4-validate.log`).
- `file` descreveu o ELF64 extraído como tendo cabeçalhos de seção ausentes; `readelf -S` emitiu `Reading 1920 bytes extends past end of file for section headers` (`P13-C4-readelf64-sections.log`).

## C5 — VirusTotal: fatos observados

- Com a chave presente, P15 recuperou dois ELF e registrou `Clean (0)` para ambos. Uma consulta independente, somente pelos hashes desses arquivos, retornou HTTP 404 para cada um (`P15-C5-output.log`, `P15-C5-direct-api.log`).
- Sem a chave no shell de P17, o programa imprimiu duas vezes `VT_API_KEY environment variable is not set`, recuperou os dois ELF e também registrou `Clean (0)` na coluna VT (`P17-C5-no-key.log`, `P17-C5-output.log`).
- No teste externo X3, um ZIP EICAR público foi recuperado byte a byte no offset 4.096. O artefato registrou `Malicious (61)`. A consulta independente pelo mesmo SHA-256 retornou HTTP 200 e `malicious: 61` (`X3-eicar-output.log`, `X3-eicar-direct-api.log`). Esse teste usou ZIP e entrada de terceiro, enquanto o exemplo P15 dos autores selecionava ELF.

## C6 — Figura 2: fatos observados

- `evidence2.dd` não consta do ZIP disponibilizado nem do checkout (`P18-C6-blocked.log`). A tarefa informou que a imagem não foi encontrada publicamente e que os autores não responderam ao pedido.
- Por falta da entrada original, `./foremost-ng -v -x evidence2.dd` **não foi executado**. Não há saída desta etapa para comparar com os arquivos e offsets da Figura 2.

## Nota sobre C7

P20 apenas leu o registro de assinaturas e o despachante da revisão fixada (`P20-C7-inspection.log`). C7 não teve experimento nesta etapa e não integra a regra de reprodução C1–C6.
