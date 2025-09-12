#!/usr/bin/env bash
# new_acta.sh  —  Create a notarized SHA-713 Acta in one shot
# Usage:
#   ./scripts/new_acta.sh "TITLE" "1.0.0" src/Acta.md docs/Acta_v1.0.0.pdf
set -euo pipefail

title="${1:?TITLE missing}"
version="${2:?VERSION missing (e.g., 1.0.0)}"
src_md="${3:?SRC .md missing}"
out_pdf="${4:?OUT .pdf missing}"

# paths
out_base="$(basename "${out_pdf%.pdf}")"                 # e.g., Acta_v1.0.0
dist="dist"; docs="docs"; mani_dir="manifests"; scripts="scripts"
mkdir -p "$dist" "$docs" "$mani_dir"

# deps (best effort)
command -v shasum >/dev/null || { echo "shasum not found"; exit 1; }
command -v gpg     >/dev/null || { echo "gpg not found";     exit 1; }
command -v jq      >/dev/null || { echo "jq not found";      exit 1; }

# 0) Build PDF (Pandoc optional)
if [ -f "$src_md" ]; then
  if command -v pandoc >/dev/null; then
    pandoc "$src_md" -o "$out_pdf" \
      --metadata title="$title — $version" --pdf-engine=xelatex || {
      echo "pandoc failed; ensure LaTeX engine is available"; exit 1; }
  else
    echo "pandoc not present — ensure $out_pdf already exists"
    [ -f "$out_pdf" ] || { echo "Missing $out_pdf"; exit 1; }
  fi
else
  echo "Missing source markdown: $src_md"; exit 1
fi

# 1) Hash
sha_file="$dist/${out_base}.sha256"
shasum -a 256 "$out_pdf" | tee "$sha_file"
hash=$(cut -d' ' -f1 "$sha_file")

# 2) Firma GPG (detached ascii)
asc_file="$dist/${out_base}.pdf.asc"
gpg --armor --detach-sign --output "$asc_file" "$out_pdf"

# 3) QR con el hash (opcional)
qr_file="$dist/${out_base}_qr.png"
python3 - <<PY
import qrcode, sys
h=open("$sha_file").read().split()[0]
qrcode.make(f"sha256:{h}").save("$qr_file")
print("QR saved:", "$qr_file")
PY

# 4) MANIFEST-713 (create or update)
mani="$mani_dir/MANIFEST-713_${version}.json"
if [ -f "$mani" ]; then
  tmp=$(mktemp)
  jq --arg h "$hash" --arg pdf "$out_pdf" \
     '.outputs = [{"path":$pdf,"sha256":$h}]' "$mani" > "$tmp" && mv "$tmp" "$mani"
else
  cat > "$mani" <<JSON
{
  "version": "$version",
  "created_utc": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "bundle": "$title",
  "inputs": [{"path":"$src_md","sha256":"(optional)"}],
  "outputs": [{"path":"$out_pdf","sha256":"$hash"}],
  "model": {"name": "gpt-5.0", "build": "2025-08-xx"},
  "decision_path": "logits_summary:…",
  "signature": "gpg: see $asc_file",
  "log_proof": "(optional: merkle_inclusion / OTS / TX)",
  "notes": "Not opinion. Proof."
}
JSON
fi

# 5) Commit + tag firmado + push
git add "$out_pdf" "$sha_file" "$asc_file" "$qr_file" "$mani"
git commit -m "release($title): $version — PDF+SHA256+ASC+QR+MANIFEST"
git tag -s "v$version" -m "$title $version"
git push origin main --tags
git tag -v "v$version" || { echo "WARNING: tag verification failed locally"; }

echo
echo "✔ SHA-713 Acta sealed:"
printf "  • PDF      : %s\n" "$out_pdf"
printf "  • SHA-256  : %s\n" "$hash"
printf "  • SIG      : %s\n" "$asc_file"
printf "  • QR       : %s\n" "$qr_file"
printf "  • MANIFEST : %s\n" "$mani"
