#!/usr/bin/env python3
# verify_713.py — local verifier for SHA-256 / PoSE-713 JSON

import argparse, json, hashlib, sys, os

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(description="Verify PoSE-713 JSON against an artifact file.")
    p.add_argument("--json", required=True, help="Path to PoSE-713 JSON")
    p.add_argument("--artifact", required=False, help="Path to the artifact file (optional). If provided, its SHA-256 must match the JSON.")
    args = p.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    sha256 = data.get("sha256")
    nonce = data.get("nonce")
    issued_at = data.get("issued_at")
    proof_713 = data.get("proof_713")

    if not all([sha256, nonce, issued_at, proof_713]):
        print("JSON missing required fields (sha256, nonce, issued_at, proof_713).", file=sys.stderr)
        sys.exit(2)

    # Optionally verify artifact
    if args.artifact:
        if not os.path.exists(args.artifact):
            print(f"Artifact not found: {args.artifact}", file=sys.stderr)
            sys.exit(2)
        calc_sha256 = sha256_file(args.artifact)
        if calc_sha256 != sha256:
            print("FAIL: Artifact sha256 does not match JSON sha256.")
            print(f"  JSON: {sha256}")
            print(f"  Calc: {calc_sha256}")
            sys.exit(1)
        else:
            print("OK: Artifact sha256 matches JSON.")

    # Verify proof_713
    recompute = hashlib.sha256(f"{sha256}.{nonce}.{issued_at}".encode("utf-8")).hexdigest()
    if recompute == proof_713:
        print("PASS: proof_713 recomputation matches.")
        sys.exit(0)
    else:
        print("FAIL: proof_713 differs from recomputation.")
        print(f"  JSON: {proof_713}")
        print(f"  Calc: {recompute}")
        sys.exit(1)

if __name__ == "__main__":
    main()
