#!/usr/bin/env python3
"""Verify sealed_lineage block for a .fuo JSON file."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify sealed_lineage block")
    parser.add_argument('fuo', help='Path to .fuo.json file')
    parser.add_argument('--workdir', default='.', help='Base directory for file paths')
    args = parser.parse_args()

    data = json.load(open(args.fuo, 'r', encoding='utf-8'))
    lineage = data.get('sealed_lineage')
    if not lineage:
        print('no sealed_lineage block')
        return 1

    file_path = Path(args.workdir) / lineage['file']
    expected = lineage['sha256']
    actual = sha256sum(file_path)
    print(f"computed sha256: {actual}")
    if actual != expected:
        print(f"mismatch: expected {expected}")
        return 1

    signature = lineage.get('signature')
    if signature:
        sig_path = Path(args.workdir) / signature
        try:
            subprocess.run(['gpg', '--verify', str(sig_path), str(file_path)], check=True)
            print('signature verified')
        except Exception as exc:
            print(f'signature verification failed: {exc}')
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
