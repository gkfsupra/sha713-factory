
"""
viewer.py — quick trace viewer
Run:
  python viewer.py
Creates:
  /mnt/data/sha713_pkg/out/trace_summary.json
  /mnt/data/sha713_pkg/out/viewer.html
"""
import json
from pathlib import Path
from sha713_core import Ledger, iter_blocks, compute_ali, Signer

OUT_LEDGER = Path("/mnt/data/sha713_pkg/out/ledger.jsonl")
OUT_DIR = OUT_LEDGER.parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

signer = Signer(b"demo-key-sha713-avantix")
ledger = Ledger(OUT_LEDGER)

# Build summary
steps = {}
blocks = list(iter_blocks(ledger))
for blk in blocks:
    rec = blk["record"]
    oid = str(rec.get("obj_id","-"))
    steps.setdefault(oid, []).append(rec.get("step"))

summary = {
    "blocks": len(blocks),
    "ALI_percent": compute_ali(ledger),
    "objects": steps
}
(Path(OUT_DIR/"trace_summary.json")).write_text(json.dumps(summary, indent=2))

# Tiny HTML
html = f"""<!doctype html>
<html><head><meta charset='utf-8'/>
<title>SHA-713 Trace Viewer</title>
<style>
body{{background:#0b1020;color:#eaeaea;font-family:system-ui,Arial;margin:2rem;}}
.card{{border:1px solid #0ff3;padding:1rem;border-radius:12px;margin-bottom:1rem;}}
h1{{color:#7df;}} code{{color:#aff;}}
.badge{{display:inline-block;padding:.2rem .5rem;border:1px solid #7df;border-radius:8px;margin-right:.5rem}}
</style>
</head><body>
<h1>SHA-713 Trace Viewer</h1>
<div class="badge">Blocks: {summary['blocks']}</div>
<div class="badge">ALI: {summary['ALI_percent']}%</div>
{''.join(f"<div class='card'><b>Object {oid}</b><br/>Steps: {' → '.join(steps)}</div>" for oid,steps in summary['objects'].items())}
<p><small>Ledger: {OUT_LEDGER}</small></p>
</body></html>"""
(Path(OUT_DIR/"viewer.html")).write_text(html)

print("Wrote:", OUT_DIR/"trace_summary.json")
print("Wrote:", OUT_DIR/"viewer.html")
