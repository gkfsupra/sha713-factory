# SHA-256 / PoSE-713 (GKF IA™) — Minimal README

**EN:** PoSE-713™ is **not** a new cryptographic hash function. It is a **verification layer** built **on top of NIST SHA-2** (e.g., SHA-256). It binds **identity + context + time** to a standard hash using the **7-1-3 rule**: **7 context fields · 1 canonical digest · 3 verifiers** (time/nonce/author), packaged as **JSON + QR**.

**ES:** PoSE-713™ **no** es un algoritmo de hash nuevo. Es una **capa de verificación** **sobre** NIST SHA-2 (p. ej., SHA-256). Une **identidad + contexto + tiempo** a un hash estándar con la **regla 7-1-3**: **7 campos de contexto · 1 digest canónico · 3 verificadores** (tiempo/nonce/autor), empaquetado como **JSON + QR**.

---

## Spec (concise)

- **Base**: `algo_base = "sha-256"` (or `"sha-512"`).
- **7 context fields**: `artifact_id, subject, issuer, issued_at, repo_or_url, version, notes`.
- **1 canonical digest**: SHA-256 of the primary artifact (file/document).
- **3 verifiers**:
  - `nonce` (unique, random)
  - `proof_713 = SHA256( sha256 + "." + nonce + "." + issued_at )`
  - `author_sig` (optional PGP/Ed25519 signature over the JSON)

**Important:** Always include the line: “**Built on SHA-256 (NIST SHA-2)**” in your README/whitepaper.

---

## Local verification (3 steps)

**Linux/macOS (bash):**
1) Compute base hash:
   ```bash
   sha256sum artifact_sample.txt
   ```
2) Recompute proof:
   ```bash
   export SHA256=<hash>
   export NONCE=<nonce>
   export ISSUED_AT=<iso8601>
   echo -n "${SHA256}.${NONCE}.${ISSUED_AT}" | sha256sum
   ```
3) Compare with `proof_713` in the JSON.

**Windows PowerShell:**
1) Base hash:
   ```powershell
   Get-FileHash .\artifact_sample.txt -Algorithm SHA256
   ```
2) Proof:
   ```powershell
   $SHA256="<hash>"; $NONCE="<nonce>"; $ISSUED_AT="<iso8601>"
   $bytes = [System.Text.Encoding]::UTF8.GetBytes("$SHA256.$NONCE.$ISSUED_AT")
   $stream = New-Object System.IO.MemoryStream(,$bytes)
   (Get-FileHash -Algorithm SHA256 -InputStream $stream).Hash.ToLower()
   ```
3) Compare with `proof_713`.

---

## Quick verifier (Python)

Use `verify_713.py`:
```bash
python3 verify_713.py --json example_pose713.json --artifact artifact_sample.txt
```

- It recomputes the artifact SHA-256 and the `proof_713` string; prints PASS/FAIL.

---

## QR

- The recommended QR payload is the **entire JSON** (compact form) or a short link to a public JSON.
- Verifiers should be able to **recompute** `proof_713` client-side using the JSON.

---

## Security & Scope

- PoSE-713 **does not replace** SHA-256; it **binds context** to a hash.
- Do **not** claim novel cryptography; claim **portable evidence**.
- Signing (`author_sig`) is **optional**, yet recommended for strong provenance.

---

## Example files included

- `artifact_sample.txt`
- `example_pose713.json`
- `verify_713.py`
- `FAQ_POSE-713_GKF.md`

**Giankoof · GKF IA™ — SHA-256/PoSE-713**. Presence → Code → Evidence → Legacy.
