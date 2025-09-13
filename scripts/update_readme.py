#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys, json, datetime as dt

OUTPUT = Path("output")
README = Path("README.md")
BEGIN, END = "<!-- SHA713:TABLE:BEGIN -->", "<!-- SHA713:TABLE:END -->"
HASH_EXTS = {".pdf", ".zip", ".md", ".json"}

def h256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda: f.read(1024*1024), b""): h.update(ch)
    return h.hexdigest()

def qr_for(p: Path):
    cands = [OUTPUT/f"{p.stem}_qr.png", OUTPUT/f"{p.stem}.png"]
    return next((c for c in cands if c.exists()), None)

def build_table(rows):
    head = "## 🔒 Tabla de Verificación\n\n| Archivo | SHA-256 Hash | QR |\n|---|---|---|\n"
    body = "\n".join(f"| `{a}` | `{h}` | {qr} |" for a,h,qr in rows)
    return head + body + "\n"

def stamp_badge():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    payload = {
        "schemaVersion": 1,
        "label": "SHA-713 Seal",
        "message": dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "color": "gold"
    }
    (OUTPUT/"last_seal.json").write_text(json.dumps(payload), encoding="utf-8")

def main():
    if not README.exists(): sys.exit("README.md no existe")
    rows = []
    if OUTPUT.exists():
        for f in sorted(OUTPUT.rglob("*")):
            if f.is_file() and f.suffix.lower() in HASH_EXTS:
                h = h256(f)
                qr = qr_for(f)
                qr_md = f"![QR]({qr.as_posix()})" if qr else "(embed pending)"
                rows.append((f.as_posix(), h, qr_md))
    if not rows: rows = [("—","—","(no artifacts)")]
    table = build_table(rows)

    content = README.read_text(encoding="utf-8")
    if BEGIN in content and END in content:
        pre, rest = content.split(BEGIN,1); _, post = rest.split(END,1)
        content = f"{pre}{BEGIN}\n{table}{END}{post}"
    else:
        content = f"{content.rstrip()}\n\n{BEGIN}\n{table}{END}\n"
    README.write_text(content, encoding="utf-8")
    stamp_badge()
    print("README + badge actualizados.")

if __name__ == "__main__":
    main()

