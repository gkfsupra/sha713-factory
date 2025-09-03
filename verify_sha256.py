#!/usr/bin/env python3
import sys, hashlib, pathlib

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 verify_sha256.py <file> <expected_sha256>")
        sys.exit(1)
    file_path, expected = sys.argv[1], sys.argv[2].lower().strip()
    actual = sha256_file(file_path)
    if actual == expected:
        print("OK — SHA-256 matches")
        sys.exit(0)
    else:
        print("FAIL — SHA-256 does not match")
        print("Expected:", expected)
        print("Actual  :", actual)
        sys.exit(2)

if __name__ == "__main__":
    main()
