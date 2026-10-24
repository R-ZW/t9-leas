# Registro factual — cadeia 2

Data: 24/10/2026. Não há decisão sobre selos neste registro. Todas as ações de execução ocorreram no contêiner t9-openai-c2, invocadas por docker exec t9-openai-c2 bash -lc. Os comandos na tabela são os comandos centrais executados dentro de bash -lc; as saídas foram capturadas com tee nos arquivos indicados. Arquivos do artefato e os testes não foram executados no host.

## Ambiente observado

| Item | Observação | Evidência |
|---|---|---|
| Sistema | Ubuntu 24.04.2 LTS, x86_64, 16 CPUs visíveis, 7,6 GiB de RAM, 952 GiB livres | X38-ambiente-final.txt |
| Ferramentas | GCC 13.3.0, Make 4.3, Git 2.43.0, Python 3.12.3, file 5.45, OpenSSL 3.0.13, libssl-dev 3.0.13-0ubuntu3.5, libcurl4-openssl-dev 8.5.0-2ubuntu10.6 | X38-ambiente-final.txt |
| Artefato | ZIP de 7.252.858 bytes, SHA-256 955c770e29893527f789e11afc28dcc6b83d7af4a64f14b416e39f554b388e0a; commit bb812a22cb06ef87b5a2d877dfb6f40eb12d460d; binário versão 1.5.7. A compilação usou o ZIP extraído. | X45-artefato-proveniencia.txt; P4-git-checkout.txt; X3-versoes.txt |
| VirusTotal | Variável VT_API_KEY presente, sem valor exibido ou salvo. Consultas feitas apenas por hash, sem envio de arquivos. | P14-chave-presenca.txt; X36-consultar-vt-hash.py |

Desvios: D0 = procedimento dos autores sem alteração; D1 = ajuste de ambiente; D2 = entrada ou teste do revisor; D3 = dado ou verificação externa. Todos os passos X são [FORA DO ROTEIRO]. Os diretórios de P8 a P19 foram /home/revisor/artefato-extraido/foremost-ng-bb812a22/src. Os arquivos de evidência mencionados estão em /home/revisor/evidencias.

## Tabela de passos

| Passo | Comando exato central | Esperado | Observado, com código de saída | Evidência | Status | Desvio |
|---|---|---|---|---|---|---|
| P1 | sudo apt-get update | Índices apt atualizados | Reading package lists; 0 | P1-apt-update.txt | sucesso | D1 |
| P2 | sudo apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev | Dependências instaladas | Pacotes configurados; 0 | P2-apt-install.txt | sucesso | D1 |
| P3 | cd /home/revisor && git clone https://github.com/cristianzsh/foremost-ng.git | Repositório dos autores clonado | Clone concluído; 0 | P3-git-clone.txt | sucesso | D0 |
| P4 | git -C /home/revisor/foremost-ng checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d | Commit fixado | HEAD at bb812a2; 0 | P4-git-checkout.txt | sucesso | D1 |
| X1 [FORA DO ROTEIRO] | sha256sum /home/revisor/artefato.zip | Conferir pacote fornecido | SHA-256 igual ao de artefato.txt; 0 | X1-zip-sha256.txt | sucesso | D1 |
| X2 [FORA DO ROTEIRO] | unzip -q /home/revisor/artefato.zip -d /home/revisor/artefato-extraido | Usar pacote exato | Extração sem erro; 0 | X2-unzip.txt | sucesso | D1 |
| P5 | cd /home/revisor/artefato-extraido/foremost-ng-bb812a22/src && make | Binário compilado | Ligação de foremost-ng concluída; avisos sobre realpath; 0 | P5-make-tentativa1.txt | sucesso | D0 |
| P6 | cd /home/revisor/artefato-extraido/foremost-ng-bb812a22/src && sudo make install | Binário instalado | Instalado em /usr/local/bin, com manual e configuração; 0 | P6-make-install.txt | sucesso | D0 |
| X3 [FORA DO ROTEIRO] | gcc --version; make --version; git --version; openssl version; foremost-ng -V | Registrar versões | Versões na seção Ambiente; 0 | X3-versoes.txt; X38-ambiente-final.txt | sucesso | D1 |
| P7a | test -r ./disk.img | Imagem legível | Ausente; 1 | P7-disk-img.txt | bloqueado | D2 |
| X4 [FORA DO ROTEIRO] | printf "#!/bin/sh\nprintf smoke-test-foremost-ng\n" > disk.img | Entrada mínima positiva | 40 bytes, SHA-256 d984f2d82ee4f328bd3ebd4effe6f7ca685d2a9e1216a2d3ecefdce7dc687f6e; 0 | X4-disk-img-revisor.dd; X4-disk-img-revisor-metadata.txt | sucesso | D2 |
| P7b | test -r ./disk.img | Entrada após ajuste | Presente; 0 | P7-disk-img-tentativa2.txt | sucesso | D2 |
| P8 | foremost-ng -i disk.img -o ./carved-f | Recuperação mínima | Um .script de 40 bytes, SHA igual à entrada, cmp=0; comando 0 | P8-F-execucao.txt; P8-audit.txt; X5-F-arquivos.txt; X6-F-comparacao.txt | sucesso | D2 |
| X7 [FORA DO ROTEIRO] | git clone --depth 1 https://github.com/williballenthin/python-evtx.git /home/revisor/dados-evtx | Obter EVTX público | Clone c0007441657899c39180de10a2be1a0e43dbeaf9; 0 | X7-evtx-clone.txt; X7-evtx-proveniencia.txt | sucesso | D3 |
| P9 | foremost-ng -t evtx,elf,exe -i disk.img -o ./carved-c1 | EVTX recuperado | Um .evtx de 2.166.784 bytes, SHA igual ao original e cmp=0; 0 | P9-C1-execucao.txt; P9-C1-audit.txt; X9-C1-resultados.txt; X10-C1-cmp.txt | sucesso | D3 |
| P10 | foremost-ng -i disk.img -o ./carved-c2 | Script com corpo recuperado | Um .script de 40 bytes, igual à entrada; 0 | P10-C2-execucao.txt; P10-C2-audit.txt; X12-C2-resultados.txt | sucesso | D2 |
| X14 [FORA DO ROTEIRO] | printf "#!/bin/sh\n# this-is-only-a-comment-with-enough-text\n" > comments-only.dd | Controle só com comentários | Entrada de 52 bytes; 0 | X14-C2-apenas-comentarios.dd; X14-C2-apenas-comentarios-metadata.txt | sucesso | D2 |
| X15 [FORA DO ROTEIRO] | foremost-ng -i comments-only.dd -o ./carved-c2-negativo | Rejeitar entrada só com comentários | Um .script de 52 bytes foi recuperado; comando 0 | X15-C2-negativo-execucao.txt; X16-C2-negativo-resultados.txt; X16-C2-negativo-audit.txt | falha do controle negativo | D2 |
| X17–X19 [FORA DO ROTEIRO] | sudo apt-get install -y python3 file; python3 /home/revisor/evidencias/X18-gerar-macho.py; file macho-fat.dd macho-thin32.dd macho-thin64.dd | Criar e identificar variantes Mach-O | file identificou universal, i386 thin e x86_64 thin; 128, 100 e 120 bytes; 0 | X17-instalar-ferramentas.txt; X18-gerar-macho.py; X19-macho-entradas.txt | sucesso | D1/D2 |
| P11 | foremost-ng -i disk.img -o ./carved-c3 | Recuperar Mach-O fat | Um .macho de 128 bytes com SHA igual à entrada; 0 | P11-C3-fat-execucao.txt; P11-C3-fat-audit.txt; X21-C3-fat-resultados.txt | sucesso para fat | D2 |
| X23 [FORA DO ROTEIRO] | foremost-ng -i macho-thin32.dd -o ./carved-c3-thin32 | Recuperar thin32 | 0 FILES EXTRACTED; comando 0 | X23-C3-thin32-execucao.txt; X24-C3-thin32-audit.txt | falha do controle thin32 | D2 |
| X25 [FORA DO ROTEIRO] | foremost-ng -i macho-thin64.dd -o ./carved-c3-thin64 | Recuperar thin64 | 0 FILES EXTRACTED; comando 0 | X25-C3-thin64-execucao.txt; X26-C3-thin64-audit.txt | falha do controle thin64 | D2 |
| X27–X28 [FORA DO ROTEIRO] | as --32 /home/revisor/evidencias/X27-elf32.s -o elf32.o; ld -m elf_i386 -o elf32.dd elf32.o; as --64 /home/revisor/evidencias/X27-elf64.s -o elf64.o; ld -m elf_x86_64 -o elf64.dd elf64.o | Construir ELF32 e ELF64 identificados | file e readelf identificaram ELF32 de 4.448 bytes e ELF64 de 4.616 bytes; 0 | X27-elf32.s; X27-elf64.s; X28-elf-entradas.txt | sucesso | D2 |
| P12 | foremost-ng -t evtx,elf,exe -i disk.img -o ./carved-c4 | ELF32 estruturalmente legível | .elf de 4.105 bytes, dois PT_LOAD; readelf emitiu erro sobre cabeçalhos de seção; carving 0 | P12-C4-elf32-execucao.txt; X30-C4-elf32-resultados.txt; X31-C4-elf32-readelf.txt | inconclusivo para integridade completa | D2 |
| X32 [FORA DO ROTEIRO] | foremost-ng -t evtx,elf,exe -i elf64.dd -o ./carved-c4-elf64 | ELF64 estruturalmente legível | .elf de 4.105 bytes, dois PT_LOAD; readelf emitiu erro sobre cabeçalhos de seção; 0 | X32-C4-elf64-execucao.txt; X33-C4-elf64-resultados.txt | inconclusivo para integridade completa | D2 |
| P13a | test -r ./memory.dump | Entrada legível | Ausente; 1 | P13-memory-dump-tentativa1.txt | bloqueado | D2 |
| X34 [FORA DO ROTEIRO] | cp elf64.dd memory.dump | Entrada ELF identificada | 4.616 bytes, SHA registrado; 0 | X34-C5-entrada.txt | sucesso | D2 |
| P13b | test -r ./memory.dump | Entrada após ajuste | Presente; 0 | P13-memory-dump-tentativa2.txt | sucesso | D2 |
| P14 | test -n "${VT_API_KEY:-}" | Chave presente, sem expor valor | Presente; 0 | P14-chave-presenca.txt | sucesso | D2 |
| P15 | foremost-ng -x -t elf -i memory.dump -o ./carved-vt | Registrar consulta por hash | ELF de SHA-256 4303231ef3b5bf8e5f655fa624b972b5cb6c055d8bf54350b7dcc73402d9af99; audit.txt mostrou Clean (0); 0 | P15-C5-com-chave-execucao.txt; X35-C5-com-chave-resultados.txt | inconclusivo para resultado de detecção | D2 |
| X36 [FORA DO ROTEIRO] | python3 /home/revisor/evidencias/X36-consultar-vt-hash.py | Conferir hash diretamente, sem upload | API respondeu HTTP 404 para o mesmo SHA-256; 0 | X36-consultar-vt-hash.py; X36-vt-hash-resposta.txt | sucesso da conferência | D3 |
| P16 | env -u VT_API_KEY foremost-ng -x -t elf -i memory.dump -o ./carved-vt-sem-chave | Aviso e carving sem chave | Aviso de chave ausente; ELF de 4.105 bytes; audit.txt também mostrou Clean (0); 0 | P16-C5-sem-chave-execucao.txt; X37-C5-sem-chave-resultados.txt | sucesso para aviso e carving | D2 |
| P17 | test -r ./evidence2.dd | Imagem da Figura 2 presente | Ausente; 1 | P17-evidence2-presenca.txt | bloqueado | D2 |
| P18 | ./foremost-ng -v -x evidence2.dd | Reproduzir tabela da Figura 2 | Não executado após P17; sem código | P17-evidence2-presenca.txt | não executado | D0 |
| P19 | grep -nE "init_builtin&#124;extract_file" state.c extract.c | Localizar registro e despacho | Entradas e função encontradas; 0 | P19-C7-inspecao.txt; X44-C7-despacho.txt | sucesso | D2 |
| X40–X42 [FORA DO ROTEIRO] | cp /home/revisor/dados-evtx/tests/data/security.evtx evtx-com-cauda.dd; dd if=/dev/zero bs=65536 count=1 >> evtx-com-cauda.dd; foremost-ng -t evtx -i evtx-com-cauda.dd -o ./carved-c1-cauda | Delimitar EVTX antes da cauda | Entrada e recuperado de 2.232.320 bytes; ambos incluem os 65.536 bytes anexados; 0 | X40-C1-cauda-entrada.txt; X41-C1-cauda-execucao.txt; X42-C1-cauda-resultados.txt | falha do controle de delimitação | D2 |
| X38/X43/X45 [FORA DO ROTEIRO] | Inventário de versões; du -sb e tar -cf - . &#124; sha256sum; stat e sha256sum do ZIP | Registrar proveniência | Versões, tamanhos, commits e hashes registrados; 0 | X38-ambiente-final.txt; X43-downloads-repositorios.txt; X45-artefato-proveniencia.txt | sucesso | D1 |

## Downloads e origem das entradas

| Origem | Tamanho observado | SHA-256 ou identificador | Evidência |
|---|---:|---|---|
| https://github.com/cristianzsh/foremost-ng.git, checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d | 22.975.758 bytes no checkout | SHA-256 do fluxo tar do checkout: 2b5ea9d5dfcd200589e1e758fc6758c676000e9183b8ea30e942b5038300e70a | X43-downloads-repositorios.txt |
| https://github.com/williballenthin/python-evtx.git, checkout c0007441657899c39180de10a2be1a0e43dbeaf9 | 7.317.150 bytes no checkout | SHA-256 do fluxo tar do checkout: 9a72713c262ae85d0859eab676a4a0b1c350d04b054b264df24be7f8b5fa0675 | X43-downloads-repositorios.txt |
| security.evtx dentro do segundo checkout; URL do arquivo: https://raw.githubusercontent.com/williballenthin/python-evtx/c0007441657899c39180de10a2be1a0e43dbeaf9/tests/data/security.evtx | 2.166.784 bytes | 5f29a03cf8c1b4bfbd82c4074ccc81ecfe85d7ee15375afc352ed5025c9a4d8d | X7-evtx-proveniencia.txt |

security.evtx foi transferido como parte do clone, sem segunda transferência pela URL raw. As demais entradas de ensaio foram produzidas no contêiner. Seus bytes pequenos ou códigos-fonte constam em evidencias.

## C1 — EVTX

security.evtx tinha 2.166.784 bytes e SHA-256 5f29a03cf8c1b4bfbd82c4074ccc81ecfe85d7ee15375afc352ed5025c9a4d8d. P9 recuperou .evtx com mesmo tamanho e hash; cmp retornou 0. file identificou original e recuperado como Windows Event Log com 26 chunks. Após anexar 65.536 bytes de zeros à entrada, X41 recuperou .evtx de 2.232.320 bytes, incluindo essa cauda. Evidências: X9-C1-resultados.txt, X10-C1-cmp.txt, X39-C1-file.txt, X42-C1-cauda-resultados.txt.

## C2 — scripts

A entrada positiva de 40 bytes com shebang e comando foi recuperada integralmente como .script. A entrada de 52 bytes com shebang e somente uma linha de comentário também foi recuperada integralmente como .script. Evidências: X12-C2-resultados.txt, X13-C2-cmp.txt, X14-C2-apenas-comentarios.dd, X16-C2-negativo-resultados.txt.

## C3 — Mach-O

file identificou três entradas geradas como universal, i386 thin e x86_64 thin. O arquivo universal de 128 bytes foi recuperado com SHA igual ao original. Os dois comandos para entradas thin terminaram com código 0, mas cada audit.txt registrou 0 FILES EXTRACTED. Evidências: X19-macho-entradas.txt, X21-C3-fat-resultados.txt, X24-C3-thin32-audit.txt, X26-C3-thin64-audit.txt.

## C4 — ELF

file e readelf identificaram as entradas como ELF32 de 4.448 bytes e ELF64 de 4.616 bytes. Cada execução recuperou .elf de 4.105 bytes. readelf leu dois segmentos PT_LOAD em cada saída e emitiu erro de leitura de cabeçalhos de seção além do fim do arquivo. Evidências: X28-elf-entradas.txt, X30-C4-elf32-resultados.txt, X31-C4-elf32-readelf.txt, X33-C4-elf64-resultados.txt.

## C5 — VirusTotal

A chave estava presente em P15. O arquivo recuperado tinha SHA-256 4303231ef3b5bf8e5f655fa624b972b5cb6c055d8bf54350b7dcc73402d9af99 e audit.txt registrou Clean (0). A consulta direta posterior da API pelo mesmo hash retornou HTTP 404. Sem chave no processo P16, houve aviso de chave ausente, recuperação do mesmo ELF e registro Clean (0). Nenhum arquivo foi enviado ao VirusTotal. Evidências: P14-chave-presenca.txt, X35-C5-com-chave-resultados.txt, X36-vt-hash-resposta.txt, P16-C5-sem-chave-execucao.txt, X37-C5-sem-chave-resultados.txt.

## C6 — Figura 2

A checagem de evidence2.dd retornou 1 porque o arquivo estava ausente. A imagem também foi informada como indisponível para esta etapa. O comando da Figura 2 não foi executado; não há comparação observada dos arquivos e offsets da figura. Evidência: P17-evidence2-presenca.txt.

## C7 — inspeção fora da regra de R

P19 localizou registros de assinaturas em state.c e a função extract_file em extract.c. O trecho salvo de extract.c mostra ramificações para ELF, MACHO, EVTX e SCRIPT. Evidências: P19-C7-inspecao.txt; X44-C7-despacho.txt.

