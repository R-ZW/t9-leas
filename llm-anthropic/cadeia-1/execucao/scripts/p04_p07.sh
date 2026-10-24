set -u
source /home/revisor/evidencias/scripts/run.sh
cd ~/aval
# P4 (Dockerfile:3-6)
run P4 sudo apt-get update
run P4 sudo DEBIAN_FRONTEND=noninteractive apt-get install -y gcc make git libssl-dev libcurl4-openssl-dev
run P4 bash -c 'gcc --version | head -1; make --version | head -1; dpkg-query -W gcc make libssl-dev libcurl4-openssl-dev'
# P5 (artigo p.6: make na raiz)
cd ~/aval/src-art/foremost-ng-bb812a22
run P5 make
# P6 (README:28,33)
cd ~/aval/src-art/foremost-ng-bb812a22/src
run P6 make
run P6 bash -c 'ls -l foremost-ng && ./foremost-ng -V'
# P7 (README:34)
run P7 sudo make install
run P7 bash -c 'command -v foremost-ng; ls -l /usr/local/bin/foremost-ng /usr/share/man/man8/foremost-ng.8.gz /usr/local/etc/foremost.conf'
