#!/usr/bin/env bash
set -euo pipefail
file="robot_movement.log"
echo ">> SHA-256:"
shasum -a 256 "$file"
if [ -f "Giankoof_GPG.asc" ]; then
  echo ">> GPG verify:"
  gpg --verify Giankoof_GPG.asc "$file" || true
else
  echo ">> No signature found (Giankoof_GPG.asc)."
fi
