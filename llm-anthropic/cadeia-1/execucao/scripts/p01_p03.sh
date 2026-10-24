set -u
mkdir -p ~/aval/{dados,img,out}
source /home/revisor/evidencias/scripts/run.sh
# P2
run P2 bash -c 'cat /etc/os-release; uname -m; nproc; free -h; df -h $HOME; id'
# P3 (artefato fornecido em /home/revisor/artefato.zip)
cp /home/revisor/artefato.zip ~/aval/artefato.zip
cd ~/aval
run P3 sha256sum artefato.zip
run P3 unzip -z artefato.zip
run P3 unzip -q artefato.zip -d ~/aval/src-art
run P3 ls -la ~/aval/src-art/foremost-ng-bb812a22 ~/aval/src-art/foremost-ng-bb812a22/src
