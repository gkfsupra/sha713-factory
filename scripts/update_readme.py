#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_readme.py — GKF IA™ · SHA-713™
Genera/actualiza tabla de verificación en README.md con hashes SHA-256 y QR.
Reemplaza el bloque entre <!-- SHA713:TABLE:BEGIN --> y <!-- SHA713:TABLE:END -->
"""

from pathlib import Path
import hashlib
import sys

OUTPUT_DIR = Path("output")
README = Path("README.md")
BEGIN = "<!-- SHA713:TABLE:BEGIN -->"
END   = "<!-- SHA713:TABLE:END -->"

# extensiones a hashear; puedes ajustar
HASH_EXTS = {".pdf", ".zip", ".md", ".json"}


def sha256_of(file: Path) -> str:
    h = hashlib.sha256()
    with file.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def guess_qr_for(file: Path) -> Path | None:
    """
    Regla: si existe un PNG con el mismo stem + '_qr.png' o '<stem>.png' en output/,
    lo enlazamos; si no, dejamos '(embed pending)'.
    """
    candidates = [OUTPUT_DIR / f"{file.stem}_qr.png", OUTPUT_DIR / f"{file.stem}.png"]
    for c in candidates:
        if c.exists():
            return c
    return None


def build_table(rows: list[tuple[str, str, str]]) -> str:
    header = (
        "## 🔒 Tabla de Verificación\n\n"
        "| Archivo | SHA-256 Hash | QR |\n"
        "|---|---|---|\n"
    )
    body = "\n".join(
        f"| `{path}` | `{h}` | {qr} |" for path, h, qr in rows
    )
    return header + body + "\n"


def main() -> int:
    if not README.exists():
        print("ERROR: README.md no existe en el repo.", file=sys.stderr)
        return 2

    if not OUTPUT_DIR.exists():
        print("WARN: 'output/' no existe; tabla quedará vacía.", file=sys.stderr)

    # Construimos filas
    rows: list[tuple[str, str, str]] = []
    if OUTPUT_DIR.exists():
        for f in sorted(OUTPUT_DIR.rglob("*")):
            if f.is_file() and f.suffix.lower() in HASH_EXTS:
                h = sha256_of(f)
                qr = guess_qr_for(f)
                qr_md = f"![QR]({qr.as_posix()})" if qr else "(embed pending)"
                rows.append((f.as_posix(), h, qr_md))

    # Si no hay filas, deja una línea informativa
    if not rows:
        rows.append(("—", "—", "(no artifacts)"))

    table_md = build_table(rows)

    # Leemos README y reemplazamos bloque
    content = README.read_text(encoding="utf-8")
    if BEGIN not in content or END not in content:
        # Inserta bloque al final si faltan marcadores
        new_content = f"{content.rstrip()}\n\n{BEGIN}\n{table_md}{END}\n"
    else:
        pre, rest = content.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        new_content = f"{pre}{BEGIN}\n{table_md}{END}{post}"

    if new_content != content:
        README.write_text(new_content, encoding="utf-8")
        print("README actualizado con tabla SHA-713.")
        return 0

    print("README sin cambios.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

