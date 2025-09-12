#!/usr/bin/env bash
set -euo pipefail
PDF="docs/Acta_Publica_SHA713.pdf"
OUT="dist/Acta_Publica_SHA713"
MANI="manifests/MANIFEST-713_v1.0.json"

mkdir -p dist

# 1) Hash
shasum -a 256 "$PDF" | tee "${OUT}.sha256"
HASH=$(cut -d' ' -f1 "${OUT}.sha256")

# 2) Firma GPG (detached, ASCII)
gpg --armor --detach-sign --output "${OUT}.pdf.asc" "$PDF"

# 3) QR con el hash
python3 - << 'PY'
import qrcode, pathlib
h = pathlib.Path("dist/Acta_Publica_SHA713.sha256").read_text().split()[0]
qrcode.make(f"sha256:{h}").save("dist/Acta_Publica_SHA713_qr.png")
PY

# 4) Inyecta hash en MANIFEST (si existe), o crea base
if [ -f "$MANI" ]; then
  tmp=$(mktemp)
  jq --arg h "$HASH" '.outputs[0].sha256=$h' "$MANI" > "$tmp" && mv "$tmp" "$MANI"
else
  cat > "$MANI" <<JSON
{
  "version": "1.0",
  "created_utc": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "bundle": "SHA-713 Public Act v1.0",
  "inputs": [{"path":"src/Acta_Publica_SHA713.md","sha256":"(fill-if-needed)"}],
  "outputs": [{"path":"docs/Acta_Publica_SHA713.pdf","sha256":"$HASH"}],
  "model": {"name": "gpt-5.0", "build": "2025-08-xx"},
  "decision_path": "logits_summary:…",
  "signature": "(see dist/Acta_Publica_SHA713.pdf.asc)",
  "log_proof": "(optional: merkle_inclusion)",
  "notes": "Not opinion. Proof."
}
JSON
fi

echo "SHA-713 seal complete:"
echo "  PDF: $PDF"
echo "  SHA256: $HASH"
echo "  SIG: ${OUT}.pdf.asc"
echo "  QR:  ${OUT}.qr.png"
echo "  MANIFEST: $MANI"
