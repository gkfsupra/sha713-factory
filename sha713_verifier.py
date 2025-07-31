import argparse
import csv
import hashlib
import os
from datetime import datetime

LEDGER_FILE = 'ledger.csv'


def compute_hash(filepath):
    """Compute SHA-256 hash of the given file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def sign_file(filepath):
    """Sign a file by hashing it and appending to the ledger."""
    filehash = compute_hash(filepath)
    timestamp = datetime.utcnow().isoformat()
    exists = os.path.isfile(LEDGER_FILE)
    with open(LEDGER_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not exists:
            writer.writerow(['file', 'sha256', 'timestamp'])
        writer.writerow([filepath, filehash, timestamp])
    print(f'Signed {filepath}: {filehash}')


def verify_file(filepath):
    """Verify a file against the ledger."""
    if not os.path.isfile(LEDGER_FILE):
        print('Ledger not found. Nothing to verify against.')
        return
    filehash = compute_hash(filepath)
    with open(LEDGER_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['file'] == filepath and row['sha256'] == filehash:
                print(f'Verified {filepath} ✔')
                return
    print(f'Verification failed for {filepath} ✘')


def main():
    parser = argparse.ArgumentParser(description='SHA-256 file signer/verifier')
    subparsers = parser.add_subparsers(dest='command', required=True)

    sign_parser = subparsers.add_parser('sign', help='Sign a file and record in ledger')
    sign_parser.add_argument('file')

    verify_parser = subparsers.add_parser('verify', help='Verify a file against the ledger')
    verify_parser.add_argument('file')

    args = parser.parse_args()

    if args.command == 'sign':
        sign_file(args.file)
    elif args.command == 'verify':
        verify_file(args.file)


if __name__ == '__main__':
    main()
