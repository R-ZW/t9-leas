# Registro factual — cadeia 3, execução de F e R

Data: 24/10/2026. Todo teste do artefato ocorreu em t9-openai-c3. Este registro descreve observações e não decide selos. D0 = procedimento dos autores sem alteração; D1 = ajuste de ambiente; D2 = passo ou entrada propostos pelo revisor; D3 = teste externo com dados de terceiros. Passos não previstos no roteiro estão marcados [FORA DO ROTEIRO]. Os logs citados estão neste mesmo diretório. A variável VT_API_KEY estava presente; seu valor não foi impresso nem salvo. O artefato e a conferência externa enviaram somente hashes à API VT, nenhum arquivo.

## Ambiente observado

Ubuntu 24.04.2 LTS, x86_64, 16 CPUs visíveis; memória indicada por free: 7,6 GiB totais e 6,8 GiB disponíveis no momento da medição. P1 encontrou 1.024.113.041.408 bytes livres em /tmp. GCC 13.3.0; GNU Make 4.3; Git 2.43.0; libssl-dev 3.0.13-0ubuntu3.5; libcurl4-openssl-dev 8.5.0-2ubuntu10.6. Ferramentas adicionais de validação: Clang 18.1.3, GNU readelf 2.42, file 5.45, Python 3.12.3, curl 8.5.0, python-evtx 0.8.1 e hexdump 3.3. Evidências: ambiente-versoes.txt, ambiente-dependencias.txt, ambiente-recursos.txt.

O ZIP fornecido em /home/revisor/artefato.zip tem 7.252.858 bytes e SHA-256 955c770e29893527f789e11afc28dcc6b83d7af4a64f14b416e39f554b388e0a; seu comentário indica o commit bb812a22cb06ef87b5a2d877dfb6f40eb12d460d. O clone foi fixado nesse mesmo commit. O arquivo tar gerado por git archive HEAD do clone tem 15.626.240 bytes e SHA-256 f6d097f67737ca66bb4f6affabe83e864724b0bdc36b65d4792e9624eaf7a84d. Evidências: ambiente-versoes.txt, p3-proveniencia.txt, p4-versao.txt.

## Passos do roteiro

| Passo | Comando exato principal | Resultado esperado segundo autores | Resultado observado e código de saída | Evidência | Status | Desvio |
|---|---|---|---|---|---|---|
| P1 | cd /tmp && df -B1 /tmp && uname -m | Recurso suficiente para a imagem da Figura 2; sem mínimo numérico publicado. | 1.024.113.041.408 bytes livres, x86_64; código 0. Primeira chamada Docker do host: permissão negada, código 1; repetição autorizada: código 0, sem repetir o teste no contêiner. | p1-ambiente.txt | sucesso | D1 |
| P2 | sudo apt-get update && sudo apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev | Dependências listadas no Dockerfile disponíveis. | Instalação concluída; código 0. | p2-apt.txt | sucesso | D1 |
| P3 | cd /tmp && git clone https://github.com/cristianzsh/foremost-ng.git | Código disponível. | Clone concluído; código 0. | p3-clone.txt; p3-proveniencia.txt | sucesso | D0 |
| P4 | cd /tmp/foremost-ng && git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d && git rev-parse HEAD | Fixar a versão do pacote, passo não especificado pelos autores. | HEAD igual a bb812a22cb06ef87b5a2d877dfb6f40eb12d460d; código 0. | p4-versao.txt | sucesso | D2 |
| P5 | cd /tmp/foremost-ng/src && make | Compilar foremost-ng. | Executável gerado; código 0, com dois avisos sobre retorno de realpath ignorado. | p5-build-1.txt | sucesso | D0 |
| P6 | cd /tmp/foremost-ng/src && sudo make install; man -P cat foremost-ng | Instalação e manual acessível. | Instalação código 0; manual código 0. O pager cat é ajuste não interativo. | p6-install.txt; p6-man.txt | sucesso | D1 |
| P7 | cd /tmp/foremost-ng/src && foremost-ng -i disk.img -o /temp/output/carved | Extração mínima em subdiretório por formato. | Entrada sintética de 55 bytes, SHA-256 b719e05bec2455cd800edffa89b2cb697f7bc0f42b3dcbe9069ee350adb0deb4; código 0. Um script de 50 bytes foi extraído no offset 4, VT N/A. | p7-fixture.txt; p7-f-minimo.txt; p7-saidas.txt | sucesso | D2 |
| P8 / C1 | foremost-ng -t evtx,elf,exe -i /tmp/c1-disk.img -o /temp/output/c1-carved | EVTX recuperado e legível, delimitado pelos chunks. | Código 0; EVTX no offset 4. Original 2.166.784 bytes; extraído 2.166.785 bytes; cmp código 1, com um byte adicional. Leitor python-evtx contou 2.261 registros em ambos, código 0. | p8-fixture-c1.txt; p8-c1-exec.txt; p8-c1-saidas.txt; p8-evtx-reader-original-3.txt; p8-evtx-reader-carved-3.txt | falha | D3 |
| P9 / C2 | Para cada name em bash, python, pwsh, comments, short: foremost-ng -i /tmp/c2-$name.img -o /temp/output/c2-$name | Recuperar scripts válidos com shebang e corpo, mínimo 32 bytes; rejeitar apenas comentários. | Cinco comandos retornaram código 0. Bash 49 B, Python 51 B e PowerShell 61 B foram extraídos exatamente (cmp 0); short 17 B teve 0 extrações; comments 56 B, apenas shebang e comentário, gerou script de 54 B. | p9-fixtures-c2.txt; p9-c2-*.txt; p9-c2-comparacao.txt; arquivos p9-c2-*.script | falha | D2 |
| P10 / C3 | Para cada name em thin32, thin64, fat: foremost-ng -i /tmp/c3-$name.img -o /temp/output/c3-$name | Recuperar Mach-O fat e thin. | Três comandos retornaram código 0. Fat: um arquivo de 8.688 B, byte a byte idêntico ao original (cmp 0), reconhecido como universal i386/x86_64. Thin32 e thin64: 0 arquivos extraídos. | p10-fixtures-c3.txt; p10-c3-*.txt; p10-c3-validacao.txt | falha | D2 |
| P11 / C4 | Para cada bits em 32, 64: foremost-ng -i /tmp/c4-elf$bits.img -o /temp/output/c4-elf$bits | Recuperar ELF32 e ELF64 estruturalmente legíveis. | Ambos os comandos código 0 e um ELF por entrada. ELF32: 4.448 B de origem, 4.105 B extraídos; ELF64: 4.616 B de origem, 4.108 B extraídos. readelf -h -l retornou 0; readelf -S imprimiu erro de leitura das tabelas de seções, embora seu código fosse 0. | p11-fixtures-c4.txt; p11-c4-*.txt; p11-c4-validacao.txt; p11-c4-elf*-readelf-*.txt | falha | D2 |
| P12 / C5 | cd /tmp/foremost-ng/src && foremost-ng -x -t elf -i memory.dump -o ./carved-files | Consultar VT pelo hash do ELF extraído e registrar resultado. | Código 0; ELF extraído com SHA-256 32b15e73281f86af25cfeb6d6fb2b94d818f0b656fd20e489071e54b7c2783e8, rótulo Clean (0). Consulta independente ao mesmo hash: HTTP 404, NotFoundError. | p12-fixture-c5.txt; p12-c5-exec.txt; p12-c5-saidas.txt; p12-vt-check.txt; p12-vt-api.json | inconclusivo | D2 |
| P13 / C6 | ./foremost-ng -v -x evidence2.dd | 12 linhas de extração com tipos e offsets da Figura 2. | Não executado: evidence2.dd ausente do ZIP e do diretório de execução (verificações com código 1); autores não forneceram imagem. | p13-c6-bloqueio.txt | bloqueado | D0 |
| P14 / C7 | Nenhum comando experimental indicado. | Inspeção arquitetural; C7 fora da regra de R. | Nenhum experimento executado nesta etapa. | — | não executado | D2 |

## Passos adicionais e tentativas

- [FORA DO ROTEIRO] D1 — P7: criei /temp/output e uma disk.img sintética com NUL inicial, script Bash e sentinela NUL. Foi necessário porque os autores não forneceram disk.img. Resultado e hash em p7-fixture.txt. A extração em p7-saidas.txt foi examinada após o comando do artigo.
- [FORA DO ROTEIRO] D3 — C1: clonei https://github.com/williballenthin/python-evtx.git, commit c0007441657899c39180de10a2be1a0e43dbeaf9. Arquivo tar de git archive HEAD: 6.871.040 bytes, SHA-256 2157c8869ff580b5370ff3090d5f783428bf9decab2acc539f6ba3fd76250106. A amostra usada, tests/data/security.evtx no mesmo commit, tem 2.166.784 bytes e SHA-256 5f29a03cf8c1b4bfbd82c4074ccc81ecfe85d7ee15375afc352ed5025c9a4d8d; URL identificável: https://github.com/williballenthin/python-evtx/blob/c0007441657899c39180de10a2be1a0e43dbeaf9/tests/data/security.evtx. Evidências: p8-download-evtx.txt, p8-fixture-c1.txt.
- [FORA DO ROTEIRO] D3 — Leitor EVTX: a primeira tentativa falhou por ausência de Python (código 1); instalei Python, e a segunda falhou por ausência de hexdump (códigos 1/1); instalei python-evtx 0.8.1 em venv, e a terceira falhou por não abrir o objeto com contexto (códigos 1/1); a quarta, com contexto, contou 2.261 registros no original e no extraído (códigos 0/0). Evidências: p8-python-install.txt, p8-evtx-reader-original.txt, p8-evtx-reader-carved.txt, p8-python-deps.txt, p8-evtx-install.txt, p8-evtx-reader-*-2.txt e p8-evtx-reader-*-3.txt. A tentativa de instalar o venv antes da retomada não chegou a executar por limite da ferramenta; a execução efetiva após a retomada consta em p8-evtx-install.txt.
- [FORA DO ROTEIRO] D2 — C2: gerei cinco imagens curtas com shebangs Bash/Python/PowerShell e casos negativos; comando de criação, tamanhos e hashes em p9-fixtures-c2.txt. As saídas pequenas foram copiadas como p9-c2-*.script.
- [FORA DO ROTEIRO] D2 — C3: instalei Clang, LLVM e file para gerar dois objetos Mach-O thin com target Apple e reuni-os com llvm-lipo-18 em um fat. Cada um foi reconhecido pela ferramenta file antes da extração. Tamanhos e hashes em p10-fixtures-c3.txt; instalação em p10-tools-install.txt.
- [FORA DO ROTEIRO] D2 — C4: montei e liguei executáveis ELF32 e ELF64 mínimos; os fontes pequenos c4-32.s e c4-64.s, tamanhos, hashes e cabeçalhos em p11-fixtures-c4.txt. As cópias dos ELF extraídos e os relatórios readelf constam como p11-c4-*.
- [FORA DO ROTEIRO] D2 — C5 sem chave: env -u VT_API_KEY foremost-ng -x -t elf -i memory.dump -o ./carved-files-nokey retornou 0, exibiu “VT_API_KEY environment variable is not set.”, extraiu um ELF e registrou Clean (0). Evidências: p12-c5-sem-chave.txt e p12-c5-sem-chave-audit.txt.
- [FORA DO ROTEIRO] D3 — C5 com amostra pública: tentativa de baixar https://secure.eicar.org/eicar.com.zip falhou, curl código 22, sem arquivo aproveitável (p12-download-eicar.txt). O endereço alternativo https://secure.eicar.org/eicar_com.zip baixou 184 bytes, SHA-256 2546dcffc5ad854d4ddc64fbf056871cd5a00f2471cb7a5bfd4ac23b6e9eedad (p12-download-eicar-2.txt). O ZIP foi inserido em imagem sintética de 186 bytes e recuperado byte a byte, SHA-256 idêntico. O comando foremost-ng -x -i /tmp/c5-eicar.img -o /temp/output/c5-eicar retornou 0 e registrou Malicious (61). Consulta independente por hash retornou HTTP 200 e last_analysis_stats.malicious = 61; nenhum arquivo foi enviado à API. Evidências: p12-eicar-fixture.txt, p12-c5-eicar-exec.txt, p12-c5-eicar-audit.txt, p12-vt-eicar-check.txt, p12-vt-eicar-api.json, p12-vt-eicar-stats.txt.
- [FORA DO ROTEIRO] D1 — Instalei curl para a conferência independente da API (p12-curl-install.txt). Registrei versões e recursos em ambiente-*.txt e a proveniência do clone em p3-proveniencia.txt.

## Fatos por reivindicação

### C1 — EVTX
A imagem de terceiro continha security.evtx precedido por quatro bytes NUL e seguido por um byte NUL. O artefato extraiu um EVTX no offset 4; o original tinha 2.166.784 bytes e o extraído 2.166.785. cmp retornou 1 por um byte adicional ao final. O leitor python-evtx percorreu 2.261 registros em ambos os arquivos e terminou com código 0. Esta é uma amostra pública de terceiro, não a entrada dos autores.

### C2 — scripts
As imagens sintéticas Bash, Python e PowerShell produziram scripts de 49, 51 e 61 bytes, respectivamente, idênticos aos corpos das entradas (cmp 0). A entrada de 17 bytes não produziu arquivo. A imagem de 56 bytes composta por shebang e comentário, sem comando no corpo, produziu um script de 54 bytes. Todos os cinco processos do artefato terminaram com código 0.

### C3 — Mach-O
Clang e llvm-lipo geraram objetos válidos thin i386 (428 bytes), thin x86_64 (496 bytes) e fat de duas arquiteturas (8.688 bytes). O programa extraiu o fat exatamente (cmp 0); não extraiu nenhum dos dois thin. Os três processos retornaram código 0.

### C4 — ELF
Os executáveis ELF32 e ELF64 de origem tinham 4.448 e 4.616 bytes. Foram extraídos arquivos de 4.105 e 4.108 bytes, respectivamente, iguais aos prefixos das origens desse tamanho. file reconheceu ambos como ELF e apontou cabeçalhos de seções ausentes. readelf -h -l retornou 0 nos dois; readelf -S emitiu erro “Reading ... extends past end of file for section headers” nos dois, embora seu código de saída fosse 0.

### C5 — VirusTotal
Com VT_API_KEY presente, o comando dos autores sobre o ELF sintético extraiu o arquivo, calculou seu SHA-256 e registrou Clean (0). A consulta independente ao mesmo hash obteve HTTP 404 / NotFoundError. Sem VT_API_KEY, o programa exibiu aviso, continuou a extração e também registrou Clean (0). Num teste adicional com ZIP EICAR público de 184 bytes, a extração preservou o SHA-256; o programa registrou Malicious (61), e a consulta independente pelo mesmo hash retornou HTTP 200 com 61 detecções maliciosas. Não se enviaram arquivos ao VirusTotal.

### C6 — Figura 2
A entrada exata evidence2.dd não estava no ZIP nem no diretório da execução; as duas verificações retornaram código 1. O comando da Figura 2 não foi executado, e não há comparação observada com seus 12 arquivos e offsets.

Nenhuma conclusão sobre atribuição dos selos F ou R é feita neste registro.

[FORA DO ROTEIRO] D1 — Cópias adicionais de saídas: p7-script.script (50 B), p10-c3-fat.macho (8.688 B) e p8-c1-extraido.evtx (2.166.785 B); hashes em saidas-copiadas.txt.
