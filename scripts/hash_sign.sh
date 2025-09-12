#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <pdf-file>" >&2
  exit 1
fi

PDF="$1"
BASENAME=$(basename "$PDF" .pdf)
mkdir -p dist

# Compute SHA-256
shasum -a 256 "$PDF" | tee "dist/${BASENAME}.sha256"
HASH=$(cut -d' ' -f1 "dist/${BASENAME}.sha256")

# Create QR code
python3 - <<PY
import qrcode, pathlib
h = pathlib.Path("dist/${BASENAME}.sha256").read_text().split()[0]
qrcode.make(f"sha256:{h}").save("dist/${BASENAME}_qr.png")
print("QR listo: dist/${BASENAME}_qr.png")
PY

# GPG signature
if command -v gpg >/dev/null 2>&1; then
  gpg --armor --detach-sign --output "dist/${BASENAME}.pdf.asc" "$PDF"
else
  echo "gpg not found, skipping signature" >&2
fi

printf "SHA256: %s\n" "$HASH"
