# POSE713_REPRO.md — Cold Demo (1‑2‑3)

**Goal:** Reproduce SHA‑713™ Proof of Symbolic Execution without prior context.

## 1) Hash Verification
- macOS/Linux:
```bash
shasum -a 256 README_SUPRA.md AX-TRACK-LINKEDIN-POST.md MANIFEST-713.json QR_PAYLOAD_SHA713.txt
```
- Windows PowerShell:
```powershell
Get-FileHash README_SUPRA.md -Algorithm SHA256
Get-FileHash AX-TRACK-LINKEDIN-POST.md -Algorithm SHA256
Get-FileHash MANIFEST-713.json -Algorithm SHA256
Get-FileHash QR_PAYLOAD_SHA713.txt -Algorithm SHA256
```

## 2) QR Payload Check
- Scan `QR_SHA713.png` (or use the JSON in `QR_PAYLOAD_SHA713.txt`).
- Confirm it resolves/matches `MANIFEST-713.json` → `sha256` values.

## 3) Voice Trigger (Echo‑Forge 713)
- Play encoded sample (not included); or run `echo_forge.py` with a seed phrase.
- In `forge_listener.js`, confirm **trigger event** emits and logs (Ω‑Mesh node).

**Pass/Fail:** Green badge in CI + QR payload match + event log present.

**Seal:** SHA‑713™ · 2025-09-10
