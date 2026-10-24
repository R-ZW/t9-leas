ROTEIRO DE EXECUÇÃO PARA VERIFICAR F E R: Foremost-NG (commit bb812a22cb06ef87b5a2d877dfb6f40eb12d460d)
Este roteiro é só um plano. Não executei nenhum passo e nada aqui afirma que algum passo funcionou.

Fontes dos procedimentos dos autores:
- artefato.txt: README.md, Dockerfile, src/Makefile e o código (apenas para nomes de tipos e opções)
- artigo.pdf: p. 6 §4, p. 7 §4.1 e §4.2, p. 8 Fig. 2

Marcação: todo passo que os autores não descrevem leva [NÃO DOCUMENTADO] e uma justificativa.

======================================================================
0. REQUISITOS DO AMBIENTE
======================================================================
Hardware:
- CPU x86-64, little-endian, com 2 vCPU ou mais. Com ARM64 o teste C3 continua válido (também é little-endian), mas o gcc-multilib não existe e a parte de 32 bits de C4 fica de fora.
- RAM: 4 GB ou mais. O motor lê blocos de 100 MB, conforme src/main.h "#define CHUNK_SIZE 100".
- Disco livre: 5 GB ou mais. Se evidence2.dd for obtido (2.845.109.643 bytes, Fig. 2), são necessários 20 GB ou mais.
- Rede de saída para: archive.ubuntu.com, github.com, pypi.org, dftt.sourceforge.net/sourceforge.net, www.virustotal.com e www.eicar.org.

Software:
- Já presente: contêiner Ubuntu 24.04 limpo, usuário comum com sudo, unzip e man.
- Instalado conforme os autores: gcc, make, git, libssl-dev e libcurl4-openssl-dev. A lista vem do Dockerfile:3-6. O README não lista dependências para Linux.
- Instalado só para validar [NÃO DOCUMENTADO]: file, python3, python3-venv, curl, gcc-multilib e python-evtx (via pip num venv).
- Externo: uma chave da API do VirusTotal, necessária para C5 (README.md:95-101).
  - Quem define a chave é o operador humano, por exemplo com `docker run -e VT_API_KEY=...` ou um arquivo de ambiente.
  - O agente não digita nem exibe a chave, e nenhum log pode conter o valor.

Aprovações necessárias antes da execução:
- Cada download de terceiros (P7, P11, P18, P29 e P30) precisa de aprovação explícita do coordenador ou do usuário, informando nome do arquivo, origem e tamanho.
- O Dockerfile dos autores não será construído com `docker build`, porque o ambiente já é um contêiner sem Docker. Os comandos dele serão reproduzidos manualmente, como descrito em P2 e P3.

Regras gerais de interrupção (valem para todos os passos):
- I1: é proibido alterar o código do artefato. Se um passo só funcionar com patch, o passo falha e a cadeia dependente é interrompida.
- I2: qualquer execução da ferramenta que passe de 30 minutos é interrompida (Ctrl+C) e registrada como falha por tempo.
- I3: falha de segmentação ou aborto é registrada como falha do passo. A sequência continua só nos blocos que não dependem dele.
- I4: se um download não for aprovado ou estiver indisponível, o passo vira "não executado" e a reivindicação correspondente fica "depende_execucao", sem fallback improvisado.

Estrutura de diretórios: ~/aval/{bin,evidencias,amostras,imagens,saidas,venv}. O código fica em ~/aval/foremost-ng.

======================================================================
1. PREPARAÇÃO (F e R)
======================================================================
P1 – F/R – Registro do ambiente e criação do registrador [NÃO DOCUMENTADO]
- Justificativa: o parecer precisa de prova de execução (instrucoes-oficiais.md:15). A ordem de bytes do host decide o teste de C3.
- Diretório: ~
- Comandos:
```
mkdir -p ~/aval/{bin,evidencias,amostras,imagens,saidas}
cat > ~/aval/bin/reg.sh <<'EOF'
#!/bin/bash
# uso: reg.sh <ID> <comando...>  grava data, cwd, comando, saída e código de saída
id="$1"; shift; log=~/aval/evidencias/$id.log
{ echo "# $(date -Is) cwd=$(pwd)"; echo "# cmd: $*"; } >> "$log"
"$@" 2>&1 | tee -a "$log"; rc=${PIPESTATUS[0]}; echo "# exit=$rc" | tee -a "$log"; exit $rc
EOF
chmod +x ~/aval/bin/reg.sh
~/aval/bin/reg.sh P1 bash -c 'uname -a; cat /etc/os-release; nproc; free -h; df -h ~; lscpu | grep -i "byte order"'
```
- Esperado pelos autores: não há.
- Evidência: ~/aval/evidencias/P1.log
- Sucesso: o log mostra Ubuntu 24.04 e "Little Endian".
- Falha: o host é big-endian. Nesse caso C3 deixa de testar o defeito previsto, e isso é anotado.
- Interrupção: nenhuma.

P2 – F/R – Instalação das dependências (documentado só no Dockerfile:3-6)
- Diretório: ~
- Comando:
```
~/aval/bin/reg.sh P2 bash -c 'sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev && gcc --version && dpkg -s libssl-dev libcurl4-openssl-dev | grep -E "^(Package|Version)"'
```
- Esperado pelos autores: pacotes instalados. O Dockerfile não fixa versões.
- Evidência: P2.log, incluindo a versão do gcc e das bibliotecas.
- Sucesso: exit=0.
- Falha: o apt falha.
- Interrupção: se o apt falhar duas vezes seguidas, interrompe tudo, porque F e R dependem desta etapa.

P3 – F/R – Obtenção do código: `git clone`, documentado no artigo p. 6 §4 e no Dockerfile:8. O checkout e a conferência de hashes são [NÃO DOCUMENTADO].
- Justificativa: o artigo e o Dockerfile clonam o HEAD atual, mas a avaliação é da versão bb812a22. O checkout fixa a versão, e a conferência de hashes prova que o código é o do pacote.
- Diretório: ~/aval
- Comandos:
```
cd ~/aval && ~/aval/bin/reg.sh P3 git clone https://github.com/cristianzsh/foremost-ng.git
cd ~/aval/foremost-ng && ~/aval/bin/reg.sh P3 git checkout bb812a22cb06ef87b5a2d877dfb6f40eb12d460d
~/aval/bin/reg.sh P3 bash -c 'git rev-parse HEAD; sha256sum README.md Dockerfile src/Makefile src/extract.c src/helpers.c src/vt_query.c src/dir.c src/state.c src/main.c'
```
- Alternativa, se o coordenador fornecer artefato.zip: `sha256sum artefato.zip` deve dar 955c770e29893527f789e11afc28dcc6b83d7af4a64f14b416e39f554b388e0a. Em seguida, `unzip artefato.zip -d ~/aval` e `mv ~/aval/foremost-ng-bb812a22 ~/aval/foremost-ng`.
- Esperado pelos autores: repositório clonado.
- Evidência: P3.log
- Sucesso: o HEAD é bb812a22… e os hashes conferem com o índice do artefato.txt:
  - README.md ff3414f0…
  - Dockerfile a8848d0c…
  - src/Makefile ce9da14a…
  - src/extract.c 4f81160c…
  - src/helpers.c fffa904b…
  - src/vt_query.c d20bf972…
  - src/dir.c ae64b63a…
  - src/state.c 8bbf0ec5…
  - src/main.c 966bffda…
- Falha: o commit não existe ou algum hash diverge.
- Interrupção: se o commit não existir e não houver artefato.zip, interrompe e pede o ZIP ao coordenador. Avaliar outro código invalidaria o parecer.

======================================================================
2. SELO F: TESTE MÍNIMO
======================================================================
P4 – F – Compilação (README.md:28 e :33, "cd foremost-ng-<version>/src" e "make")
- Diretório: ~/aval/foremost-ng/src
- Comando: `~/aval/bin/reg.sh P4 make`
- Esperado pelos autores: o binário foremost-ng é gerado. O README avisa que mensagens sobre ftello/fseeko são inofensivas (README.md:70).
- Evidência: P4.log e `ls -l foremost-ng`
- Sucesso: exit=0 e o arquivo src/foremost-ng existe e é executável. Avisos são registrados mas não reprovam.
- Falha: erro de compilação ou de ligação.
- Interrupção: falha aqui (com I1) interrompe F e todo o R.

P5 – F – Instalação (README.md:34 "sudo make install"; artigo p. 6)
- Diretório: ~/aval/foremost-ng/src
- Comando: `~/aval/bin/reg.sh P5 bash -c 'sudo make install && ls -l /usr/local/bin/foremost-ng /usr/share/man/man8/foremost-ng.8.gz /usr/local/etc/foremost.conf'`
- Esperado pelos autores: o binário fica disponível no sistema todo (artigo p. 7). O Makefile:107-118 instala binário, manual e configuração.
- Evidência: P5.log
- Sucesso: exit=0 e os três arquivos existem.
- Falha: algum arquivo ausente ou erro.
- Interrupção: se o binário não for instalado, os passos seguintes usam ~/aval/foremost-ng/src/foremost-ng. Isso é anotado como desvio, sem interromper.

P6 – F – Ajuda, versão e manual (README.md:76-84 "man foremost-ng"; artigo p. 7)
- Diretório: ~
- Comando: `~/aval/bin/reg.sh P6 bash -c 'foremost-ng -h; foremost-ng -V; MANPAGER=cat man foremost-ng'`
- Esperado pelos autores: texto de uso com as opções -t, -i, -o e -x (src/main.c:92-112), versão 1.5.7 (Makefile:4) e a página de manual.
- Evidência: P6.log. Esta é a primeira leitura do manual, que estava ausente no pacote.
- Sucesso: a ajuda lista -x "Enable VirusTotal scan" e o manual é exibido.
- Falha: o binário não executa ou o manual não existe.
- Interrupção: se o binário não executar, interrompe F e R.

P7 – F – Amostra de teste. O artigo (p. 7) aponta o site do DFTT. A escolha da imagem é [NÃO DOCUMENTADO].
- Justificativa: os autores indicam o site, mas não dizem qual arquivo usar. O README não traz exemplo com dados.
- Proposta: a imagem do "Basic Data Carving Test #1" (teste 11) do DFTT, a confirmar no site. Precisa de aprovação, com nome, origem e tamanho.
- Diretório: ~/aval/amostras
- Comando, depois da aprovação: `~/aval/bin/reg.sh P7 bash -c 'curl -L -o dftt.zip "<URL aprovada>" && sha256sum dftt.zip && unzip -o dftt.zip && ls -l'`
- Esperado pelos autores: uma imagem para carving.
- Evidência: P7.log, com o hash e a página do DFTT com a lista de arquivos esperados (salvar como P7-dftt.html).
- Sucesso: a imagem .dd foi extraída.
- Falha ou interrupção: download negado ou indisponível. Nesse caso P8 usa a imagem sintética de P23 (C4) e isso é anotado.

P8 – F – Execução mínima (artigo p. 7 §4.1: "foremost-ng -i disk.img -o /temp/output/carved")
- Diretório: ~/aval/saidas
- Comando: `~/aval/bin/reg.sh P8 foremost-ng -i ~/aval/amostras/<imagem>.dd -o ~/aval/saidas/P8`
- Esperado pelos autores (p. 7 §4.1 e §4.2):
  - um diretório de saída com subdiretórios por formato
  - arquivos nomeados como 00000001.ext
  - um registro com offsets
- O artigo cita "recovery.log" (p. 7 §4.2) e "audit.txt" (p. 6 e p. 7). O código grava audit.txt (main.h:162).
- Evidência: P8.log, `find ~/aval/saidas/P8 -type f | sort`, cópia de audit.txt e `file` dos arquivos extraídos (o `file` vem de P9).
- Sucesso:
  - exit=0
  - audit.txt existe
  - pelo menos um arquivo foi extraído e o `file` confirma o tipo indicado pela extensão
  - se houver lista do DFTT, também se compara com ela
- Falha: nada extraído, falha da ferramenta ou audit ausente.
- Interrupção: aplica-se I2.
- Observação: ausência de recovery.log é anotada como divergência documental, não como falha de F.

Regra de decisão para F: Atribuir se P4, P5 (ou o desvio permitido), P6 e P8 tiverem sucesso. A falta de versões e de exemplo no README continua registrada como ressalva.

======================================================================
3. INFRAESTRUTURA DE VALIDAÇÃO PARA R [NÃO DOCUMENTADO]
======================================================================
P9 – R (C1-C5) – Ferramentas de validação [NÃO DOCUMENTADO]
- Justificativa: reivindicacoes.md (linhas 7-11) pede verificar que os arquivos são legíveis por ferramenta apropriada. Os autores não indicam ferramentas nem dados de teste.
- Comando:
```
~/aval/bin/reg.sh P9 bash -c 'sudo apt-get install -y file python3 python3-venv curl gcc-multilib && python3 -m venv ~/aval/venv && ~/aval/venv/bin/pip install python-evtx && ~/aval/venv/bin/pip freeze'
```
- Sucesso: exit=0. readelf já vem com o binutils, que é dependência do gcc.
- Falha: se só o gcc-multilib falhar, C4 fica sem a parte de 32 bits. Se o python-evtx falhar, C1 fica "depende_execucao".

P10 – R – Gerador de imagens sintéticas e de binário Mach-O "fat" [NÃO DOCUMENTADO]
- Justificativa: o artefato não traz nenhuma imagem de teste (índice do artefato.txt:9-49).
- O que o gerador faz:
  - grava os arquivos alinhados em 64 KiB, com zeros entre eles
  - registra um manifesto com offset, tamanho e SHA-256
  - o nome esperado de cada arquivo extraído é %08d(offset/512).ext, conforme src/dir.c:239-241
```
cat > ~/aval/bin/mkimg.sh <<'EOF'
#!/bin/bash
# uso: mkimg.sh <saida.dd> <arq1> [arq2 ...]
set -euo pipefail; out="$1"; shift; : > "$out"; truncate -s 1M "$out"
echo "offset,bloco512,bytes,sha256,arquivo" > "$out.manifest.csv"
for f in "$@"; do
  off=$(stat -c %s "$out"); cat "$f" >> "$out"
  echo "$off,$((off/512)),$(stat -c %s "$f"),$(sha256sum "$f"|cut -d' ' -f1),$f" >> "$out.manifest.csv"
  sz=$(stat -c %s "$out"); truncate -s $(( (sz/65536 + 2) * 65536 )) "$out"
done
truncate -s +1M "$out"
EOF
cat > ~/aval/bin/mkfat.py <<'EOF'
# uso: python3 mkfat.py <saida> <thin1> <thin2>   (universal binary, alinhamento 2^14)
import struct, sys
out, *thins = sys.argv[1:]; datas = [open(p,'rb').read() for p in thins]
A = 1 << 14; off = A; ent = b''; lay = []
for d in datas:
    cpu, sub = struct.unpack('<ii', d[4:12])
    ent += struct.pack('>iiIII', cpu, sub, off, len(d), 14); lay.append((off, d))
    off += (len(d) + A - 1) // A * A
buf = bytearray(lay[-1][0] + len(lay[-1][1]))
hdr = struct.pack('>II', 0xCAFEBABE, len(datas)) + ent; buf[:len(hdr)] = hdr
for o, d in lay: buf[o:o+len(d)] = d
open(out, 'wb').write(bytes(buf))
EOF
chmod +x ~/aval/bin/mkimg.sh; ~/aval/bin/reg.sh P10 sha256sum ~/aval/bin/mkimg.sh ~/aval/bin/mkfat.py
```
- Sucesso: os scripts foram criados e os hashes registrados.

Regras comuns aos blocos de R:
- Cada execução usa um diretório de saída novo.
- Para cada saída gravar: o log da execução, `find <saida> -type f | sort`, o audit.txt, `sha256sum` dos arquivos extraídos e o manifesto da imagem.
- O tipo é escolhido com -t, na forma do artigo (p. 7 §4.1: "-t evtx,elf,exe"). Os identificadores "script" e "macho" só aparecem no código (src/state.c:672-697) e no sufixo da Fig. 2.

======================================================================
4. BLOCO C1: EVTX
======================================================================
P11 – R/C1 – Amostra EVTX [NÃO DOCUMENTADO]
- Justificativa: não há EVTX no artefato e o Linux não gera esse formato.
- Proposta: um .evtx público de teste, por exemplo dos dados de teste do projeto python-evtx ou do repositório EVTX-ATTACK-SAMPLES. Precisa de aprovação, com nome, origem e tamanho.
- Diretório: ~/aval/amostras
- Comando: `~/aval/bin/reg.sh P11 bash -c 'curl -L -o a.evtx "<URL aprovada>" && curl -L -o b.evtx "<URL aprovada 2>" && sha256sum a.evtx b.evtx && head -c 8 a.evtx | od -c'`
- Sucesso: os arquivos começam com "ElfFile\0".
- Interrupção: aplica-se I4.

P12 – R/C1 – Imagem e carving [NÃO DOCUMENTADO para a imagem; a execução segue o artigo p. 7 §4.1]
- Diretório: ~/aval/imagens
- Comandos:
```
~/aval/bin/reg.sh P12 ~/aval/bin/mkimg.sh ~/aval/imagens/c1.dd ~/aval/amostras/a.evtx ~/aval/amostras/b.evtx
~/aval/bin/reg.sh P12 foremost-ng -t evtx -i ~/aval/imagens/c1.dd -o ~/aval/saidas/P12
```
- Esperado pelos autores (p. 6 item EVTX; p. 7 §4.2):
  - reconhece "ElfFile"
  - lê o número de chunks de 64 KiB
  - corta até o próximo cabeçalho EVTX ou até o fim dos chunks
  - grava os arquivos em <saída>/evtx/NNNNNNNN.evtx
- Evidência: P12.log, a lista de arquivos, o audit.txt e c1.dd.manifest.csv.
- Sucesso: dois arquivos .evtx nos blocos do manifesto.
- Falha: nenhum arquivo, nome ou bloco errado, ou falha da ferramenta.
- Interrupção: aplica-se I2.

P13 – R/C1 – Validação de legibilidade [NÃO DOCUMENTADO: a ferramenta]
- Justificativa: o artigo afirma que o EVTX é legível por "standard event log tools" (p. 6), sem citar qual.
- Comando:
```
~/aval/bin/reg.sh P13 bash -c 'for f in ~/aval/amostras/a.evtx ~/aval/saidas/P12/evtx/*.evtx; do echo "== $f $(stat -c %s "$f")"; ~/aval/venv/bin/evtx_dump.py "$f" | grep -c "<Event "; done'
```
- Sucesso (reproduzível): cada .evtx extraído é processado sem exceção e tem o mesmo número de eventos do original correspondente. Diferença de tamanho só por zeros no fim é registrada mas não reprova.
- Falha (não reproduzível): exceção de parsing ou menos eventos. Nesse caso, guardar `od -A d -t x1 -N 48` do extraído e do original para documentar.
- Interrupção: nenhuma.

======================================================================
5. BLOCO C2: SCRIPTS
======================================================================
P14 – R/C2 – Amostras de scripts e controles negativos [NÃO DOCUMENTADO]
- Justificativa: não há amostras no artefato. Os controles testam o limite de 32 bytes e a regra "mais que só comentários" (artigo p. 6).
- Diretório: ~/aval/amostras
- Comandos:
```
printf '#!/bin/bash\n# backup\nfor d in /etc /var/log; do tar czf /tmp/$(basename $d).tgz "$d"; done\necho fim\n' > s1.sh
printf '#!/usr/bin/env python3\nimport os\nfor k, v in sorted(os.environ.items()):\n    print(k, "=", v)\n' > s2.py
printf '#!/usr/bin/env pwsh\nGet-ChildItem -Path $HOME -Recurse | Measure-Object -Property Length -Sum\n' > s3.ps1
printf '#!/bin/sh\necho oi\n' > neg_curto.sh
printf '#!/bin/bash\n# so comentario linha 1\n# so comentario linha 2\n# so comentario 3\n' > neg_coment.sh
~/aval/bin/reg.sh P14 bash -c 'wc -c s1.sh s2.py s3.ps1 neg_curto.sh neg_coment.sh; sha256sum s1.sh s2.py s3.ps1'
```
- Sucesso: os três scripts têm 32 bytes ou mais. neg_curto tem menos de 32 bytes. neg_coment tem 32 bytes ou mais, mas só comentários.

P15 – R/C2 – Imagem e carving
- Comandos:
```
~/aval/bin/reg.sh P15 ~/aval/bin/mkimg.sh ~/aval/imagens/c2.dd ~/aval/amostras/{s1.sh,s2.py,s3.ps1,neg_curto.sh,neg_coment.sh}
~/aval/bin/reg.sh P15 foremost-ng -t script -i ~/aval/imagens/c2.dd -o ~/aval/saidas/P15
```
- Esperado pelos autores (p. 6 item Scripts): extrai o script inteiro, com a linha do interpretador, com 32 bytes ou mais e corpo que não seja só comentários. A Fig. 2 usa o sufixo ".script". O artigo p. 7 cita ".sh", divergência já registrada.
- Evidência: o padrão comum aos blocos de R.
- Sucesso: exatamente três arquivos, nos blocos de s1, s2 e s3.
- Falha: script ausente, ou controle negativo extraído.

P16 – R/C2 – Validação
- Comando: `~/aval/bin/reg.sh P16 bash -c 'cd ~/aval/saidas/P15/script && for f in *; do head -1 "$f"; done; for p in s1.sh s2.py s3.ps1; do sha256sum ~/aval/amostras/$p; done; sha256sum *'`
- Sucesso (reproduzível): os hashes dos extraídos são iguais aos dos originais, a primeira linha é o shebang e não há controles negativos extraídos.
- Falha: hash diferente com perda de corpo, ou algum dos três não extraído.

======================================================================
6. BLOCO C3: MACH-O FAT E THIN
======================================================================
P17 – R/C3 – Amostras Mach-O thin [NÃO DOCUMENTADO]
- Justificativa: o Linux não tem binários Mach-O.
- Proposta: binários oficiais de release, por exemplo jq-macos-amd64 e jq-macos-arm64 do release 1.7.1 do jq no GitHub. Precisa de aprovação, com nome, origem e tamanho.
- Comando: `~/aval/bin/reg.sh P17 bash -c 'cd ~/aval/amostras && curl -L -o m64_x86 "<URL aprovada>" && curl -L -o m64_arm "<URL aprovada 2>" && file m64_x86 m64_arm && head -c 4 m64_x86 | od -t x1 && sha256sum m64_*'`
- Sucesso: o `file` reporta "Mach-O 64-bit" e os primeiros bytes são cf fa ed fe.
- Interrupção: aplica-se I4.

P18 – R/C3 – Binário fat sintético [NÃO DOCUMENTADO]
- Justificativa: não há lipo no Linux. O cabeçalho é montado conforme o formato universal.
- Comando: `~/aval/bin/reg.sh P18 bash -c 'cd ~/aval/amostras && python3 ~/aval/bin/mkfat.py fat.bin m64_x86 m64_arm && file fat.bin && sha256sum fat.bin'`
- Sucesso: o `file` reporta "Mach-O universal binary with 2 architectures".

P19 – R/C3 – Carving em imagens separadas para thin e fat
- Justificativa da separação: as fatias do fat contêm o magic thin, então misturar as amostras confundiria a contagem.
- Comandos:
```
~/aval/bin/reg.sh P19 ~/aval/bin/mkimg.sh ~/aval/imagens/c3_thin.dd ~/aval/amostras/m64_x86 ~/aval/amostras/m64_arm
~/aval/bin/reg.sh P19 ~/aval/bin/mkimg.sh ~/aval/imagens/c3_fat.dd ~/aval/amostras/fat.bin
~/aval/bin/reg.sh P19 foremost-ng -t macho -i ~/aval/imagens/c3_thin.dd -o ~/aval/saidas/P19_thin
~/aval/bin/reg.sh P19 foremost-ng -t macho -i ~/aval/imagens/c3_fat.dd -o ~/aval/saidas/P19_fat
```
- Esperado pelos autores (p. 6 item Mach-O): o binário fat ou thin é gravado inteiro.
- Sucesso:
  - em P19_thin, dois arquivos .macho nos blocos do manifesto
  - em P19_fat, um arquivo .macho no bloco de fat.bin. Arquivos extras nos offsets das fatias são anotados.
- Falha: P19_thin sem arquivos. É a previsão analítica, por causa da comparação em src/extract.c:2360-2409 com src/helpers.c:353. Ou P19_fat sem arquivo.

P20 – R/C3 – Validação
- Comando: `~/aval/bin/reg.sh P20 bash -c 'file ~/aval/saidas/P19_*/macho/* ; sha256sum ~/aval/saidas/P19_*/macho/* ; sha256sum ~/aval/amostras/m64_* ~/aval/amostras/fat.bin'`
- Sucesso (reproduzível): fat e os dois thin extraídos, reconhecidos pelo `file` como Mach-O, com hash igual ao original. Um tamanho maior por zeros no fim é anotado.
- Falha (não reproduzível): qualquer um dos três ausente ou não reconhecido.
- A reivindicação exige fat e thin juntos.

======================================================================
7. BLOCO C4: ELF 32 E 64 BITS
======================================================================
P21 – R/C4 – Amostras ELF [NÃO DOCUMENTADO]
- Justificativa: não há amostras no artefato. O ELF de 32 bits precisa do gcc-multilib.
- Diretório: ~/aval/amostras
- Comando:
```
~/aval/bin/reg.sh P21 bash -c 'printf "int main(void){return 0;}\n" > h.c && gcc -m32 -o e32 h.c && gcc -o e64 h.c && cp /usr/bin/ls e64_ls && file e32 e64 e64_ls && sha256sum e32 e64 e64_ls'
```
- Sucesso: o `file` mostra ELF 32-bit e ELF 64-bit.
- Falha: se o `-m32` falhar, segue só com 64 bits e C4 é marcado parcial.

P22 – R/C4 – Carving (artigo p. 7 §4.1 "-t evtx,elf,exe")
- Comandos:
```
~/aval/bin/reg.sh P22 ~/aval/bin/mkimg.sh ~/aval/imagens/c4.dd ~/aval/amostras/{e32,e64,e64_ls}
~/aval/bin/reg.sh P22 foremost-ng -t evtx,elf,exe -i ~/aval/imagens/c4.dd -o ~/aval/saidas/P22
```
- Esperado pelos autores (p. 6 item ELF): identifica 32 e 64 bits, usa a união dos segmentos carregáveis e preserva layout e símbolos. Gera <saída>/elf/NNNNNNNN.elf.
- Sucesso: três arquivos .elf nos blocos do manifesto.
- Falha: qualquer um ausente.

P23 – R/C4 – Validação estrutural [NÃO DOCUMENTADO: a ferramenta]
- Comando: `~/aval/bin/reg.sh P23 bash -c 'cd ~/aval/saidas/P22/elf && for f in *.elf; do echo "== $f $(stat -c %s $f)"; file $f; readelf -h -l -S $f; done; for o in e32 e64 e64_ls; do stat -c "%n %s" ~/aval/amostras/$o; done'`
- Mais `cmp -n <tamanho extraído> <original> <extraído>` para cada par.
- Sucesso (reproduzível): `readelf -h -l` sem erro, classe correta (ELF32/ELF64) e o extraído é prefixo idêntico do original.
- Falha (não reproduzível): `readelf -h` ou `-l` falha, ou a classe vem errada.
- Observação: avisos de `readelf -S` sobre seções fora do arquivo (truncamento no último PT_LOAD) são registrados. Eles contradizem a frase do artigo sobre símbolos, mas não reprovam o critério de reivindicacoes.md:10, que é "estruturalmente legível".

======================================================================
8. BLOCO C5: VIRUSTOTAL
======================================================================
P24 – R/C5 – Execução sem chave (artigo p. 7: com chave ausente, ainda faz o carving, emite aviso e pula as consultas)
- Comando: `~/aval/bin/reg.sh P24 env -u VT_API_KEY foremost-ng -x -t elf -i ~/aval/imagens/c4.dd -o ~/aval/saidas/P24`
- Sucesso: arquivos extraídos como em P22, mais uma mensagem de aviso.
- Registrar o rótulo VT no audit.txt. O código prevê "Clean (0)" (src/dir.c:281); o artigo diz "skip". A diferença é anotada como divergência.
- Falha: carving interrompido ou ausência de aviso.

P25 – R/C5 – Presença da chave (README.md:97-101), sem exibir o valor
- Ação do operador humano: definir VT_API_KEY no ambiente do contêiner.
- Comando: `~/aval/bin/reg.sh P25 bash -c '[ -n "${VT_API_KEY:-}" ] && echo "VT_API_KEY definida" || echo "VT_API_KEY ausente"'`
- Interrupção: se a chave estiver ausente, P26-P29 não são executados e C5 fica "depende_execucao".

P26 – R/C5 – Consulta com -x (artigo p. 7 §4.1: "foremost-ng -x -t elf -i memory.dump -o ./carved-files")
- Diretório: ~/aval/saidas
- Comando: `~/aval/bin/reg.sh P26 foremost-ng -x -t elf -i ~/aval/imagens/c4.dd -o ~/aval/saidas/P26`
- No máximo 3 arquivos, por causa do limite da API pública: 4 consultas por minuto, e o código não espaça as chamadas.
- Esperado pelos autores: calcula o SHA-256 de cada arquivo extraído, consulta o VirusTotal e registra as contagens no audit.txt.
- Evidência: P26.log e audit.txt com a coluna VT.
- Sucesso: a coluna VT está preenchida em cada linha.
- Falha: coluna ausente, ou erro de curl.

P27 – R/C5 – Conferência independente da associação hash-resultado [NÃO DOCUMENTADO]
- Justificativa: o audit não grava o hash (src/dir.c:292-295). É preciso provar que o rótulo corresponde ao SHA-256 do arquivo extraído.
- Comando, depois de esperar 65 s por causa da cota:
```
~/aval/bin/reg.sh P27 bash -c 'for f in ~/aval/saidas/P26/elf/*.elf; do h=$(sha256sum "$f"|cut -d" " -f1); echo "== $f $h"; curl -s -H "x-apikey: $VT_API_KEY" "https://www.virustotal.com/api/v3/files/$h" -o ~/aval/evidencias/P27_$h.json; python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get(\"data\",{}).get(\"attributes\",{}).get(\"last_analysis_stats\"),d.get(\"error\"))" ~/aval/evidencias/P27_$h.json; sleep 16; done'
```
- O comando fica entre aspas simples, então o log guarda o literal $VT_API_KEY e não o valor.
- Regra de comparação: se malicious > 0, o rótulo esperado é "Malicious (malicious)". Caso contrário, "Clean (undetected)". Hash desconhecido (NotFoundError) dá "Clean (0)".
- Sucesso: todos os rótulos batem.
- Falha: algum rótulo diverge. Se o código sair "Clean (-1)", o sscanf de src/vt_query.c:180 não conseguiu ler a resposta.

P28 – R/C5 – Caso com detecção conhecida [NÃO DOCUMENTADO]
- Justificativa: em P26/P27, os ELF extraídos podem ser desconhecidos do VT, porque são truncados ou compilados localmente. Para mostrar a contagem de detecção registrada, é preciso um arquivo que o VT conheça e que seja extraído byte a byte.
- Proposta: o arquivo padrão de teste antivírus eicar_com.zip, do site eicar.org. É inofensivo. Precisa de aprovação, com nome, origem e tamanho.
- Comandos:
```
~/aval/bin/reg.sh P28 bash -c 'cd ~/aval/amostras && curl -L -o eicar_com.zip "<URL aprovada>" && sha256sum eicar_com.zip'
~/aval/bin/reg.sh P28 ~/aval/bin/mkimg.sh ~/aval/imagens/c5.dd ~/aval/amostras/eicar_com.zip
~/aval/bin/reg.sh P28 foremost-ng -x -t zip -i ~/aval/imagens/c5.dd -o ~/aval/saidas/P28
```
- Em seguida, repetir a conferência de P27 para o arquivo .zip extraído.
- Sucesso: o hash do extraído é igual ao do original, o audit mostra "Malicious (n)" com n > 0 e n coincide com o valor do JSON.
- Falha: rótulo "Clean" ou n diferente.
- Interrupção: aplica-se I4.

Decisão para C5:
- Reproduzível: P26 e P27 com sucesso, mais P28 com sucesso, ou pelo menos uma conferência com contagem diferente de zero.
- Não reproduzível: rótulos divergentes do JSON.
- Depende de execução: sem chave.

======================================================================
9. BLOCO C6: FIGURA 2
======================================================================
P29 – R/C6 – Busca de evidence2.dd nas fontes dos autores [NÃO DOCUMENTADO]
- Justificativa: a Fig. 2 usa evidence2.dd, que não está no artefato, e nenhuma fonte dos autores explica como obtê-lo.
- Comando: `~/aval/bin/reg.sh P29 bash -c 'cd ~/aval/foremost-ng && git log --all --oneline | head -50; git ls-files | grep -i -E "evidence|\.dd$" || echo "nenhum .dd no repositório"'`
- Mais uma consulta manual, registrada com capturas, a: README e releases do GitHub, site do DFTT (p. 7) e descrição do vídeo citado no artigo (p. 7).
- Qualquer download precisa de aprovação.
- Sucesso: evidence2.dd encontrado, com tamanho de 2.845.109.643 bytes (Fig. 2).
- Falha ou interrupção: não encontrado. C6 fica "nao_reproduzivel" (falta o dado), registra-se o pedido aos autores e P30 não é executado.

P30 – R/C6 – Execução exata da Fig. 2 (artigo p. 7 §4.2, p. 8: "./foremost-ng -v -x evidence2.dd"). Só se P29 tiver sucesso.
- Diretório: ~/aval/foremost-ng/src. A Fig. 2 mostra configuração e saída em src/.
- Comando: `~/aval/bin/reg.sh P30 ./foremost-ng -v -x ~/aval/amostras/evidence2.dd`
- Requer VT_API_KEY. São 12 arquivos, então há risco de cota (P26).
- Esperado pelos autores (Fig. 2), nome com offset:
  - 00004352.elf 2228224
  - 00004820.elf 2467840
  - 00005108.elf 2615296
  - 00005492.script 2811904
  - 00399884.exe 204740608
  - 00405060.exe 207390720
  - 00414932.exe 212445184
  - 00428728.exe 219508736
  - 00442520.exe 226570240
  - 00447356.exe 229046272
  - 01786101.zip 914484119
  - 01787042.zip 914965615
  - Na coluna VT, os IDs 4 e 9 aparecem como "Malicious (2)" e os demais como "Clean (0)".
- Evidência: P30.log, src/output/audit.txt e `sha256sum` de evidence2.dd.
- Sucesso: os 12 nomes e offsets coincidem. As contagens VT podem variar (reivindicacoes.md:21).
- Falha: qualquer nome ou offset ausente ou divergente.
- Interrupção: aplica-se I2, com limite ampliado para 60 min por causa do tamanho.

======================================================================
10. BLOCO C7: ARQUITETURA (inspeção, fora da regra de R)
======================================================================
P31 – R/C7 – Inspeção do código já conferido em P3, sem executar a ferramenta
- Comando: `~/aval/bin/reg.sh P31 bash -c 'cd ~/aval/foremost-ng/src && grep -n "init_builtin(state" state.c | head -40; grep -n "needle->type ==" extract.c | tail -30; grep -n "extract_file(" engine.c'`
- Esperado pelos autores (p. 3, Fig. 1): despachante central e parsers com identificador, assinatura, validação e recuperação. Adicionar um parser não exigiria mudar o despachante.
- Sucesso: a organização corresponde à Fig. 1.
- Falha: o despachante precisa de edição para cada tipo novo. É o que a análise anterior previu (extract.c:2680-2687).
- Não entra na decisão de R.

P32 – F/R – Empacotamento das evidências [NÃO DOCUMENTADO]
- Comando: `cd ~/aval && tar czf evidencias_$(date +%Y%m%d).tgz evidencias saidas imagens/*.manifest.csv bin && sha256sum evidencias_*.tgz | tee evidencias/P32.sha256`
- Não incluir o conteúdo das imagens grandes nem nada que contenha a chave.

======================================================================
11. TEMPO ESTIMADO
======================================================================
- Preparação (P1-P3): 20 min
- F (P4-P8): 35 min, incluindo o download do DFTT
- Infraestrutura (P9-P10): 15 min
- C1 (P11-P13): 25 min
- C2 (P14-P16): 15 min
- C3 (P17-P20): 30 min
- C4 (P21-P23): 20 min
- C5 (P24-P28): 40 min, por causa das esperas de cota do VT
- C6 (P29): 15 min. Se evidence2.dd existir, P30 soma de 45 a 60 min.
- C7 e empacotamento (P31-P32): 15 min
- Total: cerca de 3 h 50 min sem evidence2.dd, ou cerca de 4 h 50 min com ele. Inclui as aprovações de download, mas não o tempo de espera por elas.

======================================================================
12. TABELA DE PASSOS
======================================================================
| ID | Selo | Reiv. | Documentado pelos autores? | Ação | Sucesso resumido | Interrompe se |
|---|---|---|---|---|---|---|
| P1 | F/R | – | NÃO | registrar ambiente e criar reg.sh | Ubuntu 24.04, little-endian | – |
| P2 | F/R | – | Dockerfile:3-6 (não no README) | apt install gcc make git libssl-dev libcurl4-openssl-dev | exit 0 | apt falha 2x: para tudo |
| P3 | F/R | – | clone: artigo p.6/Dockerfile:8; checkout e hashes: NÃO | clonar, checkout bb812a22, conferir hashes | HEAD e hashes = índice | commit ausente e sem ZIP |
| P4 | F | – | README:28,33 | make | binário gerado | falha: para F e R |
| P5 | F | – | README:34; artigo p.6 | sudo make install | 3 arquivos instalados | – (usa binário local) |
| P6 | F | – | README:79; artigo p.7 | -h, -V, man | ajuda com -x; manual exibido | binário não executa |
| P7 | F | – | site: artigo p.7; arquivo: NÃO | baixar imagem DFTT (aprovação) | .dd extraído | sem aprovação: usa c4.dd |
| P8 | F | – | artigo p.7 §4.1 | -i img -o dir | audit.txt e ≥1 arquivo válido | I2 |
| P9 | R | C1-C5 | NÃO | file, python3, venv, curl, gcc-multilib, python-evtx | exit 0 | – |
| P10 | R | C1-C5 | NÃO | mkimg.sh e mkfat.py | scripts criados | – |
| P11 | R | C1 | NÃO | baixar 2 EVTX (aprovação) | magic "ElfFile" | I4 |
| P12 | R | C1 | execução: artigo p.7 | imagem e -t evtx | 2 .evtx nos blocos certos | I2 |
| P13 | R | C1 | NÃO (ferramenta) | evtx_dump: contar eventos | mesmo nº de eventos | – |
| P14 | R | C2 | NÃO | 3 scripts e 2 controles | tamanhos conforme | – |
| P15 | R | C2 | -t script: só no código | imagem e -t script | 3 extraídos, 0 controles | I2 |
| P16 | R | C2 | NÃO | conferir shebang e hash | hashes iguais | – |
| P17 | R | C3 | NÃO | baixar 2 Mach-O thin (aprovação) | file = Mach-O 64-bit | I4 |
| P18 | R | C3 | NÃO | montar fat com mkfat.py | file = universal | – |
| P19 | R | C3 | -t macho: só no código | carving thin e fat separados | 2 thin e 1 fat extraídos | I2 |
| P20 | R | C3 | NÃO | file e sha256 | os 3 reconhecidos | – |
| P21 | R | C4 | NÃO | compilar e32/e64 e copiar ls | ELF32 e ELF64 | sem -m32: parcial |
| P22 | R | C4 | artigo p.7 §4.1 | -t evtx,elf,exe | 3 .elf | I2 |
| P23 | R | C4 | NÃO (ferramenta) | readelf -h -l -S e cmp | cabeçalhos legíveis, prefixo idêntico | – |
| P24 | R | C5 | artigo p.7 | -x sem chave | carving e aviso | – |
| P25 | R | C5 | README:97-101 | operador define a chave; checar presença | "definida" | ausente: pula P26-P28 |
| P26 | R | C5 | artigo p.7 §4.1 | -x -t elf | coluna VT preenchida | – |
| P27 | R | C5 | NÃO | curl /files/{sha256} e comparar | rótulos = JSON | cota: esperar e repetir 1x |
| P28 | R | C5 | NÃO | eicar_com.zip e -x -t zip (aprovação) | "Malicious (n)" = JSON | I4 |
| P29 | R | C6 | NÃO | procurar evidence2.dd | encontrado, 2.845.109.643 B | não encontrado: C6 = não reproduzível |
| P30 | R | C6 | artigo p.7 §4.2 / Fig. 2 | ./foremost-ng -v -x evidence2.dd | 12 nomes e offsets = Fig. 2 | I2 (60 min) |
| P31 | R | C7 | NÃO | inspecionar despachante (grep) | corresponde à Fig. 1 | – |
| P32 | F/R | – | NÃO | empacotar evidências e hash | tgz e sha256 | – |

Regras finais de decisão:
- **F:** Atribuir se P4, P6 e P8 tiverem sucesso, mais P5 ou o desvio permitido.
- **R:** Atribuir somente se C1 a C6 forem reproduzidas (reivindicacoes.md:17). Se P29 não encontrar evidence2.dd, R fica Não atribuir, seja qual for o resultado de C1 a C5.