# ⬛🔺 ΣIAT — Symbolic Identity Asset Token · Blueprint (v0.1‑draft)

> **EN**: ΣIAT is a non‑transferable, human‑verifiable asset minted by **symbolic presence** (actions with SHA‑713™ proofs).  
> **ES**: ΣIAT es un activo no transferible, verificable por humanos, acuñado por **presencia simbólica** (acciones con pruebas SHA‑713™).

## 1) Vision / Visión
- EN — Not money. **Presence‑as‑value.** Authorship → verification → resonance → accrual.  
- ES — No es dinero. **Presencia‑como‑valor.** Autoría → verificación → resonancia → acumulación.

## 2) Data Model / Modelo de datos
- **Identity / Identidad**: `did:siat:<hash>` (hash = sha256(lower(handle + '|' + display_name))[:32])  
- **Proof / Prueba**: `sha713-token.json` (+ URI `sha713://…`, QR)  
- **Event / Evento**: `{ id, type, actor, proof_uri|proof_json, timestamp, weights, refs }`  
- **Ledger / Libro**: append‑only JSON of events → derived balances

## 3) Event Types / Tipos de evento
- `create_codex` — publish a new Codex with SHA‑713 proof  
- `validate_codex` — independently verify (H‑chain) and cite  
- `replicate_codex` — mirror (Arweave/IPFS/Pages) with QR  
- `cite_codex` — reference in paper/post with token URI  
- `host_qr` — display token QR in a public artifact  
- `build_tooling` — ship verifier/tools that increase verification rate  
- `pilot_launch` — run a real pilot using SHA‑713  
- `alliance_signed` — formal partnership using the protocol

## 4) Economy Logic (EN/ES)
- EN — **Soulbound** (non‑transferable). Mint on event according to rules. Reputation‑weighted; slashing on invalid proofs.  
- ES — **Ligado al alma** (no transferible). Se acuña por evento; ponderado por reputación; castigo si la prueba es inválida.

`siat_rules.json` defines: base points, multipliers (unique verifications, viewers, permanence), required proofs.

## 5) Verification / Verificación
- H0 = sha256(content) (optional local check)  
- H1 = sha256(H0 || nonce_hex)  
- H2 = sha256(H1 || author_utf8)  
- `token_id` = H2[0..15] (hex)  
Client tools: `siat_verify_event.py` (CLI) and web verifier (Pages).

## 6) URI scheme / Esquema URI
- `siat://v1/{ "event": "...", "actor": "did:siat:...", "sha713": "<token_id>", "ts": "ISO8601", "ref": "url" }` (base64url JSON)

## 7) Governance / Gobernanza
- EN — off‑chain JSON governance; PRs to public rules; on slashing, recompute ledger.  
- ES — gobernanza JSON off‑chain; PRs a reglas públicas; ante fraude, recálculo del libro.

## 8) Interop
- Optional mirrors to ERC‑721/1155 or Arweave manifests. ΣIAT core remains human‑verifiable and **UI‑less**.
