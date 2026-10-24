#!/bin/bash
# uso: reg.sh <ID> <comando...>  grava data, cwd, comando, saída e código de saída
id="$1"; shift; log=/home/revisor/evidencias/$id.log
{ echo "# $(date -Is) cwd=$(pwd)"; echo "# cmd: $*"; } >> "$log"
"$@" 2>&1 | tee -a "$log"; rc=${PIPESTATUS[0]}; echo "# exit=$rc" | tee -a "$log"; exit $rc
