#!/usr/bin/env bash
# Usage: ./scripts/post_seal.sh posts/2025-09-11-openai-github.md
set -euo pipefail
src="${1:?post .md required}"
base="$(basename "${src%.md}")"                     # 2025-09-11-openai-github
pdf="docs/posts/${base}.pdf"
sha="dist/posts/${base}.sha256"
asc="dist/posts/${base}.pdf.asc"
qr="dist/posts/${base}_qr.png"
mani="manifests/posts/MANIFEST-713_${base}.json"

mkdir -p docs/posts dist/posts manifests/posts

# 1) Build PDF (Pandoc recomendado; o exporta tu editor a $pdf)
if command -v pandoc >/dev/null; then
  pandoc "$src" -o "$pdf" --metadata title="$base" --pdf-engine=xelatex
else
  echo "pandoc no encontrado; asegúrate de generar $pdf"; [ -f "$pdf" ]
fi

# 2) Hash + Firma + QR
shasum -a 256 "$pdf" | tee "$sha"
HASH=$(cut -d' ' -f1 "$sha")
gpg --armor --detach-sign --output "$asc" "$pdf"
python3 - <<PY
import qrcode,pathlib
h=pathlib.Path("$sha").read_text().split()[0]
qrcode.make(f"sha256:{h}").save("$qr")
print("QR listo:", "$qr")
PY

# 3) MANIFEST-713
cat > "$mani" <<JSON
{
  "bundle": "POST-$base",
  "created_utc": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "inputs": [{"path":"$src","sha256":"(optional)"}],
  "outputs": [{"path":"$pdf","sha256":"$HASH"}],
  "model": {"name": "gpt-5.0", "build": "2025-08-xx"},
  "decision_path": "logits_summary:…",
  "signature": "gpg: see $asc",
  "notes": "Not opinion. Proof."
}
JSON

# 4) Inserta ShortHash (8) al final del .md (si hay marcador)
SH8=${HASH:0:8}
if grep -q "ShortHash (8):" "$src"; then
  sed -i'' -e "s/ShortHash (8): .*/ShortHash (8): $SH8/" "$src" || true
fi

git add "$src" "$pdf" "$sha" "$asc" "$qr" "$mani"
git commit -m "post($base): sealed — PDF+SHA256+ASC+QR+MANIFEST"
echo "OK: $base -> $HASH (ShortHash: $SH8)"
