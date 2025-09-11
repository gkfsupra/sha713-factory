import json, subprocess, pathlib
from datetime import datetime
import qrcode

base = pathlib.Path("docs/whois-713")
manifest = json.load(open(base/"MANIFEST_WHOIS713.json","r",encoding="utf-8"))
pdf_hash = next(f["sha256"] for f in manifest["files"] if f["path"]=="WHOIS_713_PROOF.pdf")
payload = {
    "codex":"WHOIS-713","sha256_pdf":pdf_hash,
    "msg":"Yo no fui tendencia. Fui protocolo.",
    "url":"https://gkfsupra.github.io/sha713-factory/whois-713/",
    "timestamp":datetime.utcnow().isoformat()+"Z"
}
(base/"qr").mkdir(parents=True, exist_ok=True)
(base/"voice").mkdir(parents=True, exist_ok=True)
with open(base/"qr"/"qr_whois713_payload.json","w",encoding="utf-8") as f:
    json.dump(payload,f,ensure_ascii=False,indent=2)
img = qrcode.make(json.dumps(payload,ensure_ascii=False))
img.save(base/"qr"/"qr_whois713.png")
wav = base/"voice"/"giankoof_protocolo.wav"
mp3 = base/"voice"/"giankoof_protocolo.mp3"
subprocess.run(["espeak-ng","-v","es-la","-s","140","-w",str(wav),"Yo no fui tendencia. Fui protocolo."],check=True)
subprocess.run(["ffmpeg","-y","-i",str(wav),"-metadata","comment=firma_SHA256="+pdf_hash,str(mp3)],check=True)
