# Proposal 0001: sealed_lineage

## Motivation
`.fuo` files can optionally embed verifiable lineage of referenced artifacts.

## Specification
Add an optional top-level `sealed_lineage` object with:
- `file` (string): relative path to the artifact.
- `sha256` (string): hex-encoded SHA-256 of the file.
- `timestamp` (string): UTC timestamp in [RFC3339](https://www.rfc-editor.org/rfc/rfc3339) format.
- `signature` (string, optional): OpenPGP detached signature file name.
- `signature_url` (string, optional): URL where the signature can be retrieved.

## Security Considerations
SHA-256 guarantees integrity of the referenced file. An optional OpenPGP
signature allows authenticity checks when a corresponding public key is
available.
