ROTEIRO DE VERIFICAÇÃO F/R: Foremost-NG, versão bb812a22cb06ef87b5a2d877dfb6f40eb12d460d

Nada foi executado. É o plano da próxima etapa, escrito só a partir de artigo.pdf, artefato.txt, instrucoes-oficiais.md e reivindicacoes.md.

O que os autores documentam para obter, instalar e usar a ferramenta:
- Artigo, p.6: git clone; cd foremost-ng; make; sudo make install.
- README.md:23-34: tarball, cd …/src, make, sudo make install. Para Linux, o README não lista dependências.
- Dockerfile:3-10: apt-get install gcc make git libssl-dev libcurl4-openssl-dev; make && make install em src.
- VT_API_KEY: README.md:99-101 e artigo, p.7.
- Exemplos de uso: artigo §4.1. Execução da Fig. 2: artigo, p.8. Amostras: dftt.sourceforge.net (artigo, p.7).

O artefato não traz imagens de teste. Por isso, todo passo que monta ou valida uma amostra está marcado [NÃO DOCUMENTADO], com a justificativa.

REGRAS GERAIS
- Não alterar o código-fonte em nenhuma hipótese. Se algo der erro ou travar, o erro é registrado e não corrigido.
- Cada execução grava a saída com `2>&1 | tee`. A pasta de saída (-o) tem de ser nova, porque dir.c:120-126 aborta se ela existir e não estiver vazia.
- Downloads que não vêm do repositório dos autores precisam de autorização prévia do coordenador: amostra do DFTT, amostras EVTX, eventual binário Mach-O e evidence2.dd.
- A chave do VirusTotal é exportada pelo operador humano no shell. Eu não digito a chave, ela não vai para os logs e eu não rodo `env` nem `set` com a evidência aberta.
- Os validadores são instalados só depois da compilação (P8), para não esconderem dependências que faltem ao procedimento dos autores.
- Variáveis usadas em todos os passos:
  `export AV=$HOME/aval EV=$HOME/aval/evid T=$HOME/aval/testes O=$HOME/aval/out; export SRC=$AV/foremost-ng-bb812a22/src`

1. REQUISITOS DO AMBIENTE

Hardware:
- x86_64 (amd64). É obrigatório para `gcc -m32` (C4) e para os pacotes multilib.
- 2 ou mais vCPU.
- 4 GB de RAM ou mais. O motor lê blocos de 100 MB (main.h:230, engine.c:383-384), e clang/llvm também consomem memória.
- 10 GB livres em disco ou mais: evidence2.dd tem cerca de 2,8 GB; os pacotes, cerca de 1,5 GB; e as saídas podem crescer porque a leitura do código indicou risco de extração excessiva em EVTX e Mach-O.
- Rede com acesso a: espelhos apt, github.com, sourceforge.net, www.virustotal.com, e às fontes das amostras aprovadas.

Software:
- Ubuntu 24.04 limpo, usuário com sudo.
- Dependências dos autores, documentadas só no Dockerfile:5: gcc, make, git, libssl-dev, libcurl4-openssl-dev.
- Validadores [NÃO DOCUMENTADO]: file, xxd, binutils (readelf), gcc-multilib, clang, llvm (llvm-lipo, llvm-objdump), lld, python3, python3-venv, python-evtx (pip), ca-certificates, curl.
- Chave da API do VirusTotal, fornecida pelo operador, só para C5 e C6.

2. PREPARAÇÃO E COMPILAÇÃO

P1. Selo F (registro do ambiente) [NÃO DOCUMENTADO]
- Justificativa: o parecer precisa descrever o ambiente (instrucoes-oficiais.md:10-11).
- Diretório: ~
- Comando: `mkdir -p $EV $T $O && { date -u; uname -a; cat /etc/os-release; nproc; free -h; df -h $HOME; } > $EV/P1_ambiente.txt`
- Esperado pelos autores: não há.
- Evidência: P1_ambiente.txt.
- Sucesso: Ubuntu 24.04, x86_64, recursos dentro dos mínimos acima.
- Falha: arquitetura diferente de x86_64.
- Interrupção: se não for x86_64, seguir só com F e C1, C2, C3 e C5, e marcar C4 de 32 bits como não verificável.

P2. Selo F (dependências dos autores)
- Documentado só no Dockerfile:3-5, não no README.
- Diretório: ~
- Comando: `sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev 2>&1 | tee $EV/P2_apt.log; dpkg -l gcc make git libssl-dev libcurl4-openssl-dev > $EV/P2_versoes.txt; gcc --version >> $EV/P2_versoes.txt`
- Esperado pelos autores: os pacotes são instalados (Dockerfile).
- Evidência: P2_apt.log e P2_versoes.txt.
- Sucesso: código de saída 0 e os 5 pacotes com status "ii".
- Falha: pacote inexistente ou erro do apt.
- Interrupção: se o apt falhar, parar tudo, porque não há compilador.

P3. Selos F e R (obter exatamente a versão avaliada)
Caminho A [NÃO DOCUMENTADO], usado se o coordenador fornecer artefato.zip. Justificativa: garantir o commit bb812a22, porque o Dockerfile e o artigo clonam o HEAD e o README cita um tarball sem URL.
- Diretório: $AV
- Comando: `sha256sum artefato.zip | tee $EV/P3_zip.txt; unzip -z artefato.zip >> $EV/P3_zip.txt; unzip -q artefato.zip -d $AV; sha256sum $AV/foremost-ng-bb812a22/README.md $SRC/Makefile >> $EV/P3_zip.txt`

Caminho B, documentado no artigo p.6, exceto o checkout:
- Comando: `cd $AV && git clone https://github.com/cristianzsh/foremost-ng.git 2>&1 | tee $EV/P3_clone.log && cd foremost-ng && git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d && git rev-parse HEAD >> $EV/P3_clone.log`
- O checkout é [NÃO DOCUMENTADO]: serve para fixar a versão avaliada.
- Se o caminho B for a fonte, fazer `export SRC=$AV/foremost-ng/src`.

Para os dois caminhos:
- Evidência: P3_zip.txt e/ou P3_clone.log.
- Sucesso:
  - zip com sha256 955c770e29893527f789e11afc28dcc6b83d7af4a64f14b416e39f554b388e0a e comentário bb812a22…, ou HEAD igual a bb812a22…;
  - README.md com sha256 ff3414f0…, e src/Makefile com ce9da14a… (índice do artefato.txt).
- Falha: hashes divergentes, ou commit inexistente.
- Interrupção: se nenhum dos dois caminhos produzir a versão exata, parar e reportar.

P4. Selo F (procedimento do artigo, p.6: "cd foremost-ng; make")
- Diretório: raiz do clone, ou $AV/foremost-ng-bb812a22 se só houver o zip.
- Comando: `make 2>&1 | tee $EV/P4_make_raiz.log; echo "rc=$?" >> $EV/P4_make_raiz.log`
- Esperado pelos autores: compilação.
- Previsão pela leitura: o índice só tem src/Makefile, então o make deve falhar com "No targets specified and no makefile found".
- Evidência: P4_make_raiz.log.
- Sucesso: binário gerado.
- Falha: não há Makefile. Registrar como divergência entre artigo e repositório.
- Interrupção: não. Seguir para P5.

P5. Selo F (compilação segundo o README: cd …/src, make)
- Referências: README.md:28 e 33; Dockerfile:9-10.
- Diretório: $SRC
- Comando: `make 2>&1 | tee $EV/P5_make.log; echo "rc=$?" >> $EV/P5_make.log; ls -l foremost-ng >> $EV/P5_make.log`
- Esperado pelos autores: o binário foremost-ng.
- Evidência: P5_make.log, com os avisos de compilação.
- Sucesso: código de saída 0 e o executável src/foremost-ng existe.
- Falha: erro de compilação ou de ligação.
- Interrupção: se falhar, parar F e R e registrar o erro sem corrigir o código.

P6. Selo F (instalação: sudo make install)
- Referências: README.md:34; artigo, p.6-7.
- Diretório: $SRC
- Comando: `sudo make install 2>&1 | tee $EV/P6_install.log; ls -l /usr/local/bin/foremost-ng /usr/share/man/man8/foremost-ng.8.gz /usr/local/etc/foremost.conf >> $EV/P6_install.log; command -v foremost-ng >> $EV/P6_install.log`
- Esperado pelos autores: "the foremost-ng binary is available system-wide" (artigo, p.7).
- Evidência: P6_install.log.
- Sucesso: os 3 arquivos instalados e foremost-ng no PATH.
- Falha: erro no install.
- Interrupção: não. Nesse caso, usar $SRC/foremost-ng com `-c $SRC/foremost.conf`.

P7. Selo F (Dockerfile)
- Não executável neste ambiente, porque não há Docker dentro do contêiner.
- Registrar que os passos do Dockerfile foram reproduzidos manualmente em P2 e P5-P6, e que o Dockerfile usa ubuntu:latest e o HEAD do repositório, não o commit avaliado.
- Evidência: nota no parecer.

P8. Validadores (R; F só em P11) [NÃO DOCUMENTADO]
- Justificativa: os resultados esperados em reivindicacoes.md exigem "ferramenta de análise de eventos", "ferramenta apropriada" e "analisador ELF", e o artefato não traz amostras.
- Diretório: ~
- Comando: `sudo DEBIAN_FRONTEND=noninteractive apt-get install -y file xxd binutils gcc-multilib clang llvm lld python3 python3-venv ca-certificates curl 2>&1 | tee $EV/P8_valid.log && python3 -m venv $AV/venv && $AV/venv/bin/pip install python-evtx 2>&1 | tee -a $EV/P8_valid.log; dpkg -l file clang llvm lld gcc-multilib > $EV/P8_versoes.txt; $AV/venv/bin/pip show python-evtx >> $EV/P8_versoes.txt`
- Evidência: P8_valid.log e P8_versoes.txt.
- Sucesso: tudo instalado.
- Falha: pacote indisponível.
- Interrupção: sem python-evtx, a validação de C1 cai para a verificação de cabeçalho; sem clang/llvm, C3 fica não verificável.

P9. Script de montagem de imagens (R: C1 a C5) [NÃO DOCUMENTADO]
- Justificativa: o artigo e o artefato não fornecem imagens, exceto evidence2.dd, que está ausente.
- Diretório: $T
- Comando: criar $T/monta.sh com:
```
#!/bin/bash
# uso: monta.sh IMG TAM_MB arquivo:bloco ...  (bloco de 512 B, ordem crescente)
set -e; img=$1; tam=$2; shift 2; rm -f "$img"; truncate -s ${tam}M "$img"
m="$img.manifesto.tsv"; printf "bloco\toffset\tarquivo\tbytes\tsha256\n" > "$m"; fim=0
for p in "$@"; do f=${p%:*}; b=${p##*:}; s=$(stat -c%s "$f")
  [ $((b*512)) -ge $fim ] || { echo "SOBREPOSICAO em $f"; exit 1; }
  dd if="$f" of="$img" bs=512 seek="$b" conv=notrunc status=none; fim=$((b*512+s))
  printf "%s\t%s\t%s\t%s\t%s\n" "$b" $((b*512)) "$f" "$s" "$(sha256sum "$f"|cut -d' ' -f1)" >> "$m"
done; sha256sum "$img" >> "$m"
```
  Depois: `chmod +x $T/monta.sh; cp $T/monta.sh $EV/`
- Esperado pelos autores: não há.
- Evidência: o próprio script e os manifestos (.tsv).
- Sucesso: o script cria imagens e manifestos sem erro de sobreposição.
- Falha ou interrupção: corrigir o script, que é meu e não do artefato.

3. TESTE MÍNIMO (selo F)

P10. Selo F (uso, ajuda e versão)
- Referências: README.md:84; artigo, p.7.
- Diretório: $AV
- Comando: `{ foremost-ng; echo "rc=$?"; foremost-ng -h; echo "rc=$?"; foremost-ng -V; echo "rc=$?"; } > $EV/P10_uso.txt 2>&1`
- Esperado pelos autores: sintaxe "foremost-ng [options] [image_or_device]".
- Evidência: P10_uso.txt.
- Sucesso: a ajuda lista -t, -i, -o, -x e -v, e -V imprime 1.5.7 (Makefile:4).
- Falha: travamento ou nenhuma saída.
- Interrupção: se o programa travar, parar F.

P11. Selo F (página de manual)
- Referências: README.md:79; artigo, p.7.
- Diretório: $AV
- Comando: `man foremost-ng | col -b > $EV/P11_man.txt 2>&1; echo "rc=$?" >> $EV/P11_man.txt`
- Esperado pelos autores: documentação das opções.
- Evidência: P11_man.txt. É a primeira vez que a man page será lida, porque no pacote ela é binária.
- Sucesso: a página existe e descreve as opções.
- Falha: "No manual entry".
- Interrupção: não.

P12. Selo F (exemplo mínimo com amostra do DFTT)
- Referências: artigo, p.7, "Carving test samples … dftt.sourceforge.net"; comando no formato do §4.1.
- A escolha da imagem é [NÃO DOCUMENTADO]: os autores não dizem qual amostra usar. Proposta: uma imagem da série "Basic Data Carving" do DFTT, com autorização prévia do download.
- Diretório: $T/dftt
- Comando: baixar o arquivo, registrar URL, tamanho e sha256 em $EV/P12_fonte.txt, unzip, e então `foremost-ng -i <imagem> -o $O/F_dftt 2>&1 | tee $EV/P12_run.log; ls -lR $O/F_dftt > $EV/P12_arvore.txt; cp $O/F_dftt/audit.txt $EV/P12_audit.txt; file $O/F_dftt/*/* > $EV/P12_file.txt`
- Esperado pelos autores (artigo §4.1-4.2): uma pasta de saída com subpastas por formato, arquivos nomeados NNNNNNNN.ext e um audit.txt com tabela.
- Evidência: os quatro arquivos citados, mais o gabarito do DFTT, se houver.
- Sucesso: código de saída 0; audit.txt com a tabela ID/Name/Size/Offset/Comment/VT; pelo menos um arquivo extraído cujo tipo o `file` confirma. Comparar com o gabarito, se existir.
- Falha: travamento, nenhum arquivo ou audit.txt vazio.
- Interrupção: se o download não for autorizado ou estiver indisponível, usar como exemplo mínimo a imagem mista de P26 e registrar a substituição.

4. BLOCOS DE REPRODUÇÃO (selo R)

C1. EVTX

P13. Selo R, C1 (amostras) [NÃO DOCUMENTADO]
- Justificativa: não há .evtx no artefato e um contêiner Linux não gera esse tipo de log.
- Diretório: $T/c1
- Comando: com autorização, baixar 2 arquivos .evtx públicos de fonte aprovada pelo coordenador e salvá-los como e1.evtx e e2.evtx; registrar URL e sha256 em $EV/P13_fonte.txt. Depois: `for f in e1 e2; do $AV/venv/bin/evtx_dump.py $f.evtx > $f.ref.xml; grep -c '<Event ' $f.ref.xml; done > $EV/P13_ref.txt; xxd -l 128 e1.evtx >> $EV/P13_ref.txt`
- Esperado pelos autores: não há.
- Sucesso: os originais são lidos e a contagem de registros fica anotada.
- Falha: os originais não são legíveis. Nesse caso, trocar de amostra.
- Interrupção: sem amostra autorizada, C1 fica "depende_execucao (não verificado)".

P14. Selo R, C1 (imagens de teste) [NÃO DOCUMENTADO]
- Diretório: $T/c1
- Comando: `B2=$((2048 + ($(stat -c%s e1.evtx)+511)/512)); $T/monta.sh img_A.dd 64 e1.evtx:2048; $T/monta.sh img_B.dd 64 e1.evtx:2048 e2.evtx:$B2; cp *.tsv $EV/`
- Caso A: um EVTX isolado, seguido de zeros.
- Caso B: dois EVTX em sequência, para testar "locates the next EVTX header" (artigo, p.6).
- Sucesso: os manifestos são gerados.

P15. Selo R, C1 (extração)
- Diretório: $T/c1
- Comando: `for c in A B; do foremost-ng -v -t evtx -i img_$c.dd -o $O/C1_$c 2>&1 | tee $EV/P15_$c.log; cp $O/C1_$c/audit.txt $EV/P15_${c}_audit.txt; ls -l $O/C1_$c/evtx >> $EV/P15_$c.log; done`
- Esperado pelos autores (artigo, p.6-7): `$O/C1_A/evtx/00002048.evtx`; em B, também `$(printf %08d $B2).evtx`.
- Evidência: os logs e os audit.txt.
- Sucesso: os arquivos esperados existem.
- Falha: nenhum .evtx gerado.
- Interrupção: se o programa travar, registrar e passar a C2.

P16. Selo R, C1 (validação) [NÃO DOCUMENTADO: validador externo exigido por reivindicacoes.md:7]
- Diretório: $T/c1
- Comando: para cada arquivo extraído X, com o original correspondente Y:
  `stat -c%s X Y; cmp -n $(stat -c%s Y) X Y; xxd -l 64 X; $AV/venv/bin/evtx_dump.py X > X.xml; echo rc=$?; grep -c '<Event ' X.xml`
  Gravar tudo em $EV/P16_valida.txt.
- Esperado pelos autores: "The resulting EVTX file can then be parsed with standard event log tools" (artigo, p.6).
- Sucesso:
  - cada .evtx começa com "ElfFile", tem o mesmo prefixo do original (cmp sem diferença no comprimento do original) e é lido pelo python-evtx sem exceção;
  - a contagem de registros é igual à da referência.
  - Registrar também o tamanho extraído contra o original. Isso documenta a parte "delimita os chunks de 64 KiB". Uma diferença de tamanho conta como divergência parcial, mesmo que o arquivo seja legível.
- Falha: erro de leitura ou menos registros que o original.
- Interrupção: não.

C2. Scripts

P17. Selo R, C2 (amostras) [NÃO DOCUMENTADO]
- Diretório: $T/c2
- Comando: criar com printf:
  - s1.sh: `#!/bin/bash\n# teste C2\nfor i in 1 2 3; do echo "linha $i"; done\n`
  - s2.py: `#!/usr/bin/env python3\nimport sys\nprint("ola", sys.version)\n`
  - s3.ps1: `#!/usr/bin/env pwsh\nWrite-Output "ola"\nGet-Date\n`
  - controle negativo n1.sh, só comentários e mais de 32 bytes: `#!/bin/sh\n# comentario 1\n# comentario 2\n# fim\n`
  - controle negativo n2.sh, com menos de 32 bytes: `#!/bin/sh\necho a\n`
  Depois: `$T/monta.sh img_c2.dd 8 s1.sh:100 s2.py:200 s3.ps1:300 n1.sh:400 n2.sh:500; cp *.tsv $EV/`
- Sucesso: manifesto gerado.

P18. Selo R, C2 (extração)
- Diretório: $T/c2
- Comando: `foremost-ng -v -t script -i img_c2.dd -o $O/C2 2>&1 | tee $EV/P18.log; cp $O/C2/audit.txt $EV/P18_audit.txt; ls -l $O/C2/script >> $EV/P18.log`
- Esperado pelos autores (artigo, p.6): scripts com pelo menos 32 bytes e com mais que comentários são extraídos com a diretiva do interpretador. A Fig. 2 usa o sufixo ".script"; o §4.2 diz ".sh".
- Evidência: P18.log e P18_audit.txt.
- Sucesso: existem 00000100, 00000200 e 00000300 com sufixo .script, e não existem 00000400 nem 00000500.
- Falha: falta um positivo ou aparece um negativo.
- Interrupção: não.

P19. Selo R, C2 (validação)
- Diretório: $T/c2
- Comando: `for p in s1.sh:100 s2.py:200 s3.ps1:300; do f=${p%:*}; b=${p##*:}; cmp $O/C2/script/$(printf %08d $b).script $f && echo "$f IGUAL"; head -1 $O/C2/script/$(printf %08d $b).script; done > $EV/P19.txt 2>&1`
- Sucesso: os 3 positivos são idênticos aos originais (o preenchimento com zeros funciona como sentinela) e a primeira linha é o shebang.
- Falha: arquivo truncado, ou corpo ilegível.
- Registrar a sufixação (.script ou .sh) como divergência entre texto e código, sem que isso conte como falha de C2.

C3. Mach-O

P20. Selo R, C3 (amostras) [NÃO DOCUMENTADO]
- Justificativa: não há Mach-O no artefato e o Ubuntu não tem SDK da Apple.
- Diretório: $T/c3
- Comando: criar h.c sem includes: `int puts(const char*); static const char m[4096]="foremost-ng"; int main(void){puts(m);return 0;}`. Depois:
  `clang -target x86_64-apple-macos11 -c h.c -o t64.o; clang -target arm64-apple-macos11 -c h.c -o t64a.o; clang -target i386-apple-macos10.6 -c h.c -o t32.o; llvm-lipo -create t64.o t64a.o -output fat.o`
- Tentativa opcional de gerar executável: `ld64.lld -arch x86_64 -platform_version macos 11.0 11.0 -e _main -o t64.exe t64.o`. Se falhar, registrar a falha.
- Opcional, com autorização: um executável Mach-O público, fat e thin, de fonte aprovada.
- Gravar `file *; llvm-objdump --macho --private-headers <cada>` em $EV/P20_ref.txt.
- Sucesso: ter pelo menos um fat, um thin de 32 bits e um thin de 64 bits.
- Interrupção: sem clang/llvm, C3 fica não verificado.
- Limitação a registrar: arquivos-objeto (MH_OBJECT) são Mach-O válidos, mas não são executáveis.

P21. Selo R, C3 (imagem e extração)
- Diretório: $T/c3
- Comando: `$T/monta.sh img_c3.dd 16 fat.o:100 t32.o:1000 t64.o:2000 [t64.exe:3000]; foremost-ng -v -t macho -i img_c3.dd -o $O/C3 2>&1 | tee $EV/P21.log; cp img_c3.dd.manifesto.tsv $O/C3/audit.txt $EV/`
- Esperado pelos autores (artigo, p.6): Mach-O fat e thin extraídos, "whether fat or thin, is written out".
- Sucesso: arquivos 00000100.macho, 00001000.macho e 00002000.macho (e 00003000.macho, se houver o executável).
- Falha: algum deles ausente.
- Interrupção: não.

P22. Selo R, C3 (validação)
- Diretório: $T/c3
- Comando: para cada par (extraído X, original Y): `file X; llvm-objdump --macho --private-headers X; stat -c%s X Y; cmp -n $(stat -c%s Y) X Y`. Para o fat, também `llvm-lipo -info X`. Gravar em $EV/P22.txt.
- Esperado (reivindicacoes.md:9): "reconhecível por ferramenta apropriada".
- Sucesso: o `file` e o llvm-objdump reconhecem o mesmo tipo e arquitetura do original, sem erro, e o prefixo é idêntico. Registrar o excesso de tamanho, se houver.
- Falha: não reconhecido, ou erro de leitura.

C4. ELF

P23. Selo R, C4 (amostras) [NÃO DOCUMENTADO]
- Diretório: $T/c4
- Comando: criar h.c: `#include <stdio.h>\nint main(void){puts("ola foremost-ng");return 0;}`. Depois:
  `gcc -O0 -o e64 h.c; gcc -m32 -O0 -o e32 h.c; cp /usr/bin/ls ls64; for f in e64 e32 ls64; do readelf -h -l -S $f; done > $EV/P23_ref.txt`
- Sucesso: e32 é ELF32 e e64 e ls64 são ELF64.
- Interrupção: sem gcc-multilib, a parte de 32 bits fica não verificada.

P24. Selo R, C4 (imagem e extração), no formato do exemplo "-t elf" do §4.1
- Diretório: $T/c4
- Comando: `$T/monta.sh img_c4.dd 16 e64:100 e32:1000 ls64:2000; foremost-ng -v -t elf -i img_c4.dd -o $O/C4 2>&1 | tee $EV/P24.log; cp img_c4.dd.manifesto.tsv $O/C4/audit.txt $EV/`
- Esperado pelos autores (artigo, p.6-7): .elf de 32 e 64 bits delimitados pelos segmentos PT_LOAD.
- Sucesso: arquivos 00000100.elf, 00001000.elf e 00002000.elf.
- Falha: algum ausente.
- Interrupção: não.

P25. Selo R, C4 (validação)
- Diretório: $T/c4
- Comando: para cada par: `file X; readelf -h -l X; echo rc=$?; readelf -S X 2>&1 | head; stat -c%s X Y; cmp -n $(stat -c%s X) X Y; chmod +x X && ./X` (este último só para e64 e e32). Gravar em $EV/P25.txt.
- Esperado (reivindicacoes.md:10): "estruturalmente legível por analisador ELF". O artigo também diz que o arquivo "retains … symbol information" (p.6).
- Sucesso: `readelf -h -l` sem erro, classe ELF32 ou ELF64 correta e prefixo idêntico ao original.
- Registrar à parte:
  - avisos do `readelf -S` (seções ou símbolos ausentes), que são divergência com a frase do artigo;
  - se o binário extraído executa e imprime "ola foremost-ng".
- Falha: erro no `readelf -h` ou `-l`, ou arquivo ausente.

P26. Selos F e R, C1/C4 (exemplo do §4.1: "-t evtx,elf,exe") [NÃO DOCUMENTADO: montagem da imagem]
- Diretório: $T
- Comando: `$T/monta.sh img_misto.dd 64 $T/c4/e64:100 $SRC/../windows_dlls/zlib1.dll:1000 $T/c1/e1.evtx:2048; foremost-ng -t evtx,elf,exe -i img_misto.dd -o $O/F_t 2>&1 | tee $EV/P26.log; ls -R $O/F_t >> $EV/P26.log`
- Adaptação: o caminho /temp/output/carved do artigo foi trocado por $O/F_t, porque o mkdir do programa não é recursivo (dir.c:65-79).
- Esperado pelos autores (artigo, p.7): "only the EVTX, ELF, and EXE modules will run", com subpastas por formato.
- Sucesso: só aparecem as subpastas evtx, elf e exe/dll com arquivos (as vazias são removidas por cleanup_output).
- Falha: aparecem outros formatos, ou falta algum dos três.

C5. VirusTotal

P27. Selo R, C5 (imagem) [NÃO DOCUMENTADO]
- As DLLs usadas vêm do próprio artefato e têm sha256 conhecido pelo índice: zlib1.dll 542ca2e3… e libbrotlidec.dll 6f59aae2…. Por isso, o hash do arquivo extraído pode ser conferido sem enviar a terceiros dados que não sejam públicos.
- Diretório: $T/c5
- Comando: `$T/monta.sh img_c5.dd 16 $SRC/../windows_dlls/zlib1.dll:100 $SRC/../windows_dlls/libbrotlidec.dll:1000 $T/c4/e64:2000; cp *.tsv $EV/`
- Sucesso: manifesto gerado.

P28. Selo R, C5 (sem chave)
- Diretório: $T/c5
- Comando: `env -u VT_API_KEY foremost-ng -x -t exe,elf -i img_c5.dd -o $O/C5_sem 2>&1 | tee $EV/P28.log; cp $O/C5_sem/audit.txt $EV/P28_audit.txt`
- Esperado pelos autores (artigo, p.7): "will still perform carving but will emit a warning and skip all VT lookups".
- Sucesso: arquivos extraídos e aviso emitido.
- Registrar o conteúdo da coluna VT do audit.txt.
- Falha: o programa aborta, ou não há aviso.
- Interrupção: não.

P29. Selo R, C5 (chave inválida)
- O valor fictício não é uma credencial.
- Diretório: $T/c5
- Comando: `VT_API_KEY=chave-invalida-teste foremost-ng -x -t exe,elf -i img_c5.dd -o $O/C5_inv 2>&1 | tee $EV/P29.log; cp $O/C5_inv/audit.txt $EV/P29_audit.txt`
- Esperado pelos autores (artigo, p.7): aviso e extração sem consulta.
- Sucesso: aviso emitido e extração concluída.
- Falha: nenhum aviso. Registrar o rótulo gravado no audit.
- Interrupção: não.

P30. Selo R, C5 (chave válida)
- O operador humano exporta VT_API_KEY no shell; eu não digito a chave.
- Diretório: $T/c5
- Comando: `foremost-ng -x -t exe -i img_c5.dd -o $O/C5_ok 2>&1 | grep -v -i apikey | tee $EV/P30.log; sha256sum $O/C5_ok/*/* > $EV/P30_hashes.txt; cp $O/C5_ok/audit.txt $EV/P30_audit.txt`
- Esperar 60 s ou mais. Depois, repetir no formato do exemplo do artigo: `foremost-ng -x -t elf -i img_c5.dd -o $O/C5_elf`.
- O operador consulta cada sha256 no VirusTotal (pela interface web) e registra malicious e undetected, com data e hora, em $EV/P30_ref.txt.
- Esperado pelos autores (artigo, p.3 e p.7): hash calculado, API consultada e audit anotado com as contagens malicious/undetected.
- Sucesso:
  - os hashes dos arquivos extraídos batem com o índice, para as DLLs;
  - para cada arquivo que o VirusTotal conhece, o rótulo segue a regra de dir.c:280-282: "Malicious (n)" com n = malicious, se malicious > 0; senão "Clean (n)" com n = undetected. Contagens próximas da referência são aceitas, por causa da variação temporal (reivindicacoes.md:21).
- Falha: rótulo "Clean (0)" ou "Clean (-1)" para um arquivo que o VirusTotal conhece, ou nenhuma consulta feita.
- Interrupção:
  - sem chave fornecida: C5 fica verificado só nos caminhos de P28 e P29;
  - erro HTTP 429 (limite da API pública): esperar e repetir com no máximo 4 arquivos por minuto.

C6. Execução da Figura 2

P31. Selo R, C6 (obter evidence2.dd) [NÃO DOCUMENTADO]
- A imagem não está no artefato e o artigo não indica sua origem.
- Diretório: $T/c6
- Comando: pedir o arquivo ao coordenador ou aos autores; com autorização, baixar. Depois: `stat -c%s evidence2.dd; sha256sum evidence2.dd > $EV/P31.txt`
- Esperado pelos autores (Fig. 2): "Length: 2 GB (2845109643 bytes)".
- Sucesso: o tamanho é exatamente 2845109643 bytes.
- Falha: arquivo indisponível ou de tamanho diferente.
- Interrupção: sem a imagem, encerrar o bloco e classificar C6 como nao_reproduzivel. Não usar imagem substituta.

P32. Selo R, C6 (execução idêntica à Fig. 2)
- A chave é exportada pelo operador.
- Diretório: $SRC. A Fig. 2 mostra "Output directory: /tmp/foremost-ng/src/output".
- Comando: `test ! -e output && ./foremost-ng -v -x $T/c6/evidence2.dd 2>&1 | tee $EV/P32.log; cp output/audit.txt $EV/P32_audit.txt; ls -lR output > $EV/P32_arvore.txt`
- Esperado pelos autores: a tabela da Fig. 2, conforme minha transcrição da figura, a ser conferida no PDF. Formato: ID, nome, tamanho, offset, comentário, VT.

| ID | Nome | Tamanho | Offset | Comentário | VT |
|---|---|---|---|---|---|
| 0 | 00004352.elf | 57 KB | 2228224 | | Clean (0) |
| 1 | 00004820.elf | 57 KB | 2467840 | | |
| 2 | 00005108.elf | 1 KB | 2615296 | | |
| 3 | 00005492.script | 3 KB | 2811904 | | |
| 4 | 00399884.exe | 600 KB | 204740608 | 01/01/1970 | Malicious (2) |
| 5 | 00405060.exe | 52 KB | 207390720 | 01/01/1970 | |
| 6 | 00414932.exe | 2 MB | 212445184 | 01/01/2015 | |
| 7 | 00428728.exe | 2 MB | 219508736 | 01/01/2015 | |
| 8 | 00442520.exe | 536 KB | 226570240 | 01/01/1970 | |
| 9 | 00447356.exe | 600 KB | 229046272 | 01/01/1970 | Malicious (2) |
| 10 | 01786101.zip | 470 KB | 914484119 | | |
| 11 | 01787042.zip | 350 KB | 914965615 | | |

  Os demais itens da coluna VT aparecem como Clean (0).
- Evidência: P32.log, P32_audit.txt e P32_arvore.txt.
- Sucesso: a execução termina com audit.txt.
- Falha: travamento.
- Interrupção: se a execução passar de 2 h sem progresso, interromper e registrar.

P33. Selo R, C6 (comparação)
- Diretório: $EV
- Comando: extrair do P32_audit.txt as colunas Name, Size, Offset e Comment para $EV/P33_obtido.tsv; comparar com a transcrição da Fig. 2 em $EV/P33_fig2.tsv usando `diff`. Gravar o resultado em $EV/P33_diff.txt.
- Critério (reivindicacoes.md:21): comparar arquivos e offsets; as contagens do VirusTotal não precisam coincidir.
- Sucesso: os 12 nomes e offsets aparecem idênticos. Arquivos extras são registrados à parte.
- Falha: algum dos 12 falta ou tem offset diferente.

C7 não faz parte da regra de R (reivindicacoes.md:17). Fica para inspeção do código, sem passo de execução.

P34. Consolidação (F e R) [NÃO DOCUMENTADO]
- Diretório: $AV
- Comando: `sha256sum $EV/* > $AV/evid_SHA256SUMS.txt; tar czf $AV/evidencias.tgz -C $AV evid evid_SHA256SUMS.txt`
- Sucesso: pacote de evidências íntegro e sem a chave. Conferir com `grep -ri "x-apikey\|VT_API_KEY=" $EV`, que deve retornar só o valor fictício de P29.

5. TEMPO ESTIMADO

| Etapa | Passos | Tempo |
|---|---|---|
| Preparação e compilação | P1-P9 | 30-40 min |
| Teste mínimo F | P10-P12 | 20-30 min (inclui download do DFTT) |
| C1 | P13-P16 | 30 min |
| C2 | P17-P19 | 15 min |
| C3 | P20-P22 | 30-40 min |
| C4 | P23-P25 | 20 min |
| Exemplo do §4.1 | P26 | 10 min |
| C5 | P27-P30 | 30 min (inclui esperas por limite de taxa) |
| C6, se a imagem existir | P31-P33 | 60-90 min (download de 2,8 GB, varredura e 12 consultas VT a 4 por minuto) |
| Consolidação | P34 | 15 min |
| **Total** | | **cerca de 4,5 a 5,5 h com C6; cerca de 3,5 h sem C6** |

6. TABELA-RESUMO

| ID | Selo/Reiv. | Documentado pelos autores? | Ação | Sucesso |
|---|---|---|---|---|
| P1 | F | NÃO DOC | registrar ambiente | Ubuntu 24.04 x86_64 |
| P2 | F | Sim (só Dockerfile:3-5) | apt gcc make git libssl-dev libcurl4-openssl-dev | pacotes "ii" |
| P3 | F/R | A: NÃO DOC; B: artigo p.6 + checkout NÃO DOC | obter commit bb812a22 | hashes/commit conferem |
| P4 | F | Sim (artigo p.6) | make na raiz | binário gerado (previsão: falha) |
| P5 | F | Sim (README:28,33) | make em src | src/foremost-ng existe, rc=0 |
| P6 | F | Sim (README:34; artigo p.6) | sudo make install | binário, man e conf instalados |
| P7 | F | Sim (Dockerfile) | não executável aqui; registrar | nota no parecer |
| P8 | R (F em P11) | NÃO DOC | instalar validadores | ferramentas disponíveis |
| P9 | R | NÃO DOC | script monta.sh | imagens e manifestos |
| P10 | F | Sim (README:84) | uso, -h, -V | ajuda exibida e versão 1.5.7 |
| P11 | F | Sim (README:79) | man foremost-ng | página existe |
| P12 | F | Parcial (DFTT citado; imagem NÃO DOC) | -i img -o out em amostra DFTT | audit.txt e arquivos válidos |
| P13 | R C1 | NÃO DOC | obter EVTX e referência | originais legíveis |
| P14 | R C1 | NÃO DOC | imagens A e B | manifestos |
| P15 | R C1 | Sim (artigo p.6-7) | -t evtx | 00002048.evtx (+ 2º em B) |
| P16 | R C1 | NÃO DOC (validador) | python-evtx, cmp, tamanho | legível e mesma contagem de registros |
| P17 | R C2 | NÃO DOC | 3 scripts + 2 negativos | manifesto |
| P18 | R C2 | Sim (artigo p.6) | -t script | 3 positivos, 0 negativos |
| P19 | R C2 | NÃO DOC | cmp e head | idênticos, com shebang |
| P20 | R C3 | NÃO DOC | clang/llvm-lipo: fat, thin32, thin64 | amostras geradas |
| P21 | R C3 | Sim (artigo p.6) | -t macho | arquivos .macho nos blocos esperados |
| P22 | R C3 | NÃO DOC | file, llvm-objdump, lipo, cmp | reconhecidos e prefixo idêntico |
| P23 | R C4 | NÃO DOC | gcc 64 e -m32, ls | ELF32 e ELF64 de referência |
| P24 | R C4 | Sim (artigo p.6-7, -t elf) | -t elf | arquivos .elf nos blocos esperados |
| P25 | R C4 | NÃO DOC | readelf -h -l -S, cmp, execução | readelf sem erro, classe correta |
| P26 | F, R C1/C4 | Sim (artigo §4.1); imagem NÃO DOC | -t evtx,elf,exe | só esses formatos |
| P27 | R C5 | NÃO DOC | imagem com DLLs do artefato + ELF | manifesto |
| P28 | R C5 | Sim (artigo p.7) | -x sem chave | aviso e extração |
| P29 | R C5 | Sim (artigo p.7) | -x com chave inválida | aviso e extração |
| P30 | R C5 | Sim (README:89-108; artigo p.7) | -x com chave válida e conferência manual | rótulo coerente com o VT |
| P31 | R C6 | NÃO DOC | obter evidence2.dd | 2845109643 bytes |
| P32 | R C6 | Sim (Fig. 2) | ./foremost-ng -v -x evidence2.dd | execução termina com audit |
| P33 | R C6 | Sim (reivindicacoes.md:21) | diff com a Fig. 2 | 12 nomes e offsets iguais |
| P34 | F/R | NÃO DOC | hashes e pacote de evidências | íntegro e sem a chave |

Pontos que dependem do coordenador antes de executar:
- (a) fornecer artefato.zip ou autorizar o clone do GitHub;
- (b) autorizar os downloads do DFTT, das amostras EVTX e de um eventual Mach-O, indicando as fontes;
- (c) fornecer evidence2.dd ou confirmar que ele não está disponível;
- (d) providenciar que o operador humano exporte VT_API_KEY.