import json, os, subprocess, pathlib
from datetime import datetime
import qrcode

REPO_OWNER = "gkfsupra"
REPO_NAME  = "sha713-factory"
base = pathlib.Path("docs/whois-713")
manifest = json.load(open(base/"MANIFEST_WHOIS713.json", "r", encoding="utf-8"))
pdf_hash = next(f["sha256"] for f in manifest["files"] if f["path"]=="WHOIS_713_PROOF.pdf")
page_url = f"https://{REPO_OWNER}.github.io/{REPO_NAME}/whois-713/"

payload = {
    "codex": "WHOIS-713",
    "sha256_pdf": pdf_hash,
    "msg": "Yo no fui tendencia. Fui protocolo.",
    "url": page_url,
    "timestamp": datetime.utcnow().isoformat()+"Z"
}

out_qr_dir = base/"qr"
out_voice_dir = base/"voice"
out_qr_dir.mkdir(parents=True, exist_ok=True)
out_voice_dir.mkdir(parents=True, exist_ok=True)

# Save payload
with open(out_qr_dir/"qr_whois713_payload.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# Generate QR PNG
img = qrcode.make(json.dumps(payload, ensure_ascii=False))
img.save(out_qr_dir/"qr_whois713.png")

# Generate voice (es-ES or es-la)
text = "Yo no fui tendencia. Fui protocolo."
wav = out_voice_dir/"giankoof_protocolo.wav"
mp3 = out_voice_dir/"giankoof_protocolo.mp3"
subprocess.run(["espeak-ng", "-v", "es-la", "-s", "140", "-w", str(wav), text], check=True)
# Embed hash metadata and convert to mp3
subprocess.run([
    "ffmpeg","-y","-i",str(wav),
    "-metadata","comment=firma_SHA256="+pdf_hash,
    str(mp3)
], check=True)

print("QR + voice generated:", out_qr_dir, out_voice_dir)
