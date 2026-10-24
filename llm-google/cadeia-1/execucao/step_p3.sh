#!/bin/bash
set -e
exec > /home/revisor/evidencias/tree_artifact.txt 2>&1
cd /home/revisor
rm -rf foremost-ng
mkdir -p foremost-ng
unzip -q artefato.zip -d foremost-ng
ls -laR foremost-ng
