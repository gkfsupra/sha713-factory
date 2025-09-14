# sealed_lineage proposal

This bundle proposes an optional `sealed_lineage` block for `.fuo` files to embed
verifiable lineage metadata.

Included:
- `proposals/0001-sealed_lineage.md` – rationale and specification
- `schema/sealed_lineage.schema.json` – Draft-07 JSON Schema
- `examples/robot_sim2real.fuo.json` – example `.fuo` file with lineage data
- `scripts/verify_fuo_lineage.py` – local/CI verifier for SHA-256 and GPG
- `.github/workflows/fuo_lineage_check.yml` – GitHub Actions example

Quick verify:
```bash
python3 scripts/verify_fuo_lineage.py examples/robot_sim2real.fuo.json --workdir .
```
