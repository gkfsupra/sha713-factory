# FAQ — SHA-256 / PoSE-713 (GKF IA™)

**Q: Is SHA-713 a new hash algorithm?**  
**A:** No. It is a **verification layer** on top of **SHA-256/SHA-512 (NIST SHA-2)**.

**P: ¿Es SHA-713 un algoritmo nuevo?**  
**R:** No. Es una **capa de verificación** sobre **SHA-256/SHA-512 (NIST SHA-2)**.

---

**Q: What problem does it solve?**  
**A:** It attaches human context (who/what/when/where/version/notes) to a standard hash and produces a **recomputable proof** (`proof_713`) so third parties can independently verify provenance and timing.

**P: ¿Qué problema resuelve?**  
**R:** Conecta el contexto humano (quién/qué/cuándo/dónde/versión/notas) a un hash estándar y genera una **prueba recomputable** (`proof_713`) para que terceros verifiquen procedencia y momento de emisión.

---

**Q: Why “7-1-3”?**  
**A:** **7 context fields** · **1 digest** · **3 verifiers** (time/nonce/author).

**P: ¿Por qué “7-1-3”?**  
**R:** **7 campos de contexto** · **1 digest** · **3 verificadores** (tiempo/nonce/autor).

---

**Q: How do I compute `proof_713`?**  
**A:** `proof_713 = SHA256( sha256 + "." + nonce + "." + issued_at )` (hex lowercase).

**P: ¿Cómo calculo `proof_713`?**  
**R:** `proof_713 = SHA256( sha256 + "." + nonce + "." + issued_at )` (hex minúsculas).

---

**Q: Is it secure?**  
**A:** It inherits the security of SHA-2 for collision/preimage properties. It **does not** add cryptographic novelty; it adds **portable, auditable context**. For stronger origin guarantees, sign the JSON (PGP/Ed25519).

**P: ¿Es seguro?**  
**R:** Hereda la seguridad de SHA-2 para colisiones/preimagen. **No** añade criptografía nueva; añade **contexto portátil y auditable**. Para mayor garantía de autoría, firme el JSON (PGP/Ed25519).

---

**Q: Can I use this in CI/CD?**  
**A:** Yes. Emit the JSON on each build/release, include the artifact SHA-256, and recompute `proof_713`. Publish the JSON alongside the artifact and expose a verification page.

**P: ¿Puedo usarlo en CI/CD?**  
**R:** Sí. Emite el JSON en cada build/release, incluye el SHA-256 del artefacto y recalcula `proof_713`. Publica el JSON junto al artefacto y expón una página de verificación.

---

**Q: Is it blockchain-related?**  
**A:** Optional. You may anchor the JSON hash to a chain, but PoSE-713 **does not require** blockchain.

**P: ¿Requiere blockchain?**  
**R:** Opcional. Puedes anclar el hash del JSON a una cadena, pero PoSE-713 **no lo requiere**.

---

**Q: Naming guidance to avoid confusion?**  
**A:** Use “**SHA-256/PoSE-713 (GKF IA™)**” and include the opening line: “**Built on SHA-256 (NIST SHA-2)**”.

**P: ¿Cómo evito confusiones de nombre?**  
**R:** Usa “**SHA-256/PoSE-713 (GKF IA™)**” e incluye la línea inicial: “**Built on SHA-256 (NIST SHA-2)**”.
