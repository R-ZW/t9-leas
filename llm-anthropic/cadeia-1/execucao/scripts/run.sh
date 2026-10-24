# Funcao de registro (P1). Evidencias em /home/revisor/evidencias/logs/Pn.log
EVID=/home/revisor/evidencias/logs
mkdir -p "$EVID"
run(){ id="$1"; shift; log="$EVID/$id.log"; printf '### %s | %s\n' "$(date -Is)" "$*" >> "$log"; "$@" 2>&1 | tee -a "$log"; rc=${PIPESTATUS[0]}; echo "exit=$rc" | tee -a "$log"; return $rc; }
