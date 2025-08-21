
# SHA-713 Minimal Package (Demo)
**see → reason → do → seal** with a tamper-evident JSONL ledger.

## Files
- `sha713_core.py` — core sealing/verification + ALI metric
- `ingest_cv.py` — demo ingest simulating detections and actions
- `viewer.py` — tiny HTML/JSON viewer for quick <30s replay

## Quick start
1) Run `python ingest_cv.py` to generate `out/ledger.jsonl`
2) Run `python viewer.py` to produce `out/viewer.html`
3) Open the HTML to replay the trace; check ALI in `trace_summary.json`

## Notes
- Signing uses HMAC-SHA256 (easy to swap for ed25519 later).
- Ledger is append-only (JSON Lines). Each block chains `hash(prev + canonical(record))`.
- ALI = % of objects with full `see, reason, do` lineage.
- TtT target is <30 seconds for a human to verify one trace.

— Giankoof · GKF IA™ · SHA-713
