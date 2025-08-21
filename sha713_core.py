
"""
SHA-713 Core — minimal, dependency-free
see → reason → do → seal  |  tamper-evident append-only ledger (JSONL)

Signing: HMAC-SHA256 (ed25519 interface stub included for future swap)
"""

from __future__ import annotations
import json, hashlib, hmac
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Tuple

def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="milliseconds") + "Z"

def canonical_bytes(obj: dict) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()

@dataclass
class Signer:
    """HMAC signer (plug-replaceable with ed25519 later)."""
    secret: bytes

    def sign(self, payload: bytes) -> str:
        return hmac.new(self.secret, payload, hashlib.sha256).hexdigest()

@dataclass
class Ledger:
    path: Path

    def _last_hash(self) -> str:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return "GENESIS"
        last = None
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last = line
        return json.loads(last)["hash"]

    def append_record(self, record: dict, signer: Signer) -> dict:
        prev = self._last_hash()
        canonical = canonical_bytes(record)
        block = {
            "ts": now_iso(),
            "prev": prev,
            "record": record,
            "hash": hashlib.sha256(canonical + prev.encode()).hexdigest(),
        }
        block["sig"] = signer.sign(canonical_bytes({
            "hash": block["hash"],
            "prev": block["prev"],
            "record": block["record"],
            "ts": block["ts"]
        }))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(block, ensure_ascii=False) + "\n")
        return block

    def verify(self, signer: Signer) -> Tuple[bool, int, str|None]:
        ok, n, err = True, 0, None
        prev = "GENESIS"
        with self.path.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if not line.strip(): 
                    continue
                blk = json.loads(line)
                canonical = canonical_bytes(blk["record"])
                expected_hash = hashlib.sha256(canonical + prev.encode()).hexdigest()
                if blk["hash"] != expected_hash:
                    return False, n, f"Hash mismatch at line {i}"
                signed = canonical_bytes({
                    "hash": blk["hash"],
                    "prev": blk["prev"],
                    "record": blk["record"],
                    "ts": blk["ts"]
                })
                if blk["sig"] != signer.sign(signed):
                    return False, n, f"Signature mismatch at line {i}"
                prev = blk["hash"]
                n += 1
        return ok, n, err

def compute_ali(ledger: Ledger) -> float:
    """ALI: % of objects with full see+reason+do lineage."""
    steps = {}
    with ledger.path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            rec = json.loads(line)["record"]
            oid = rec.get("obj_id")
            if oid is None: 
                continue
            steps.setdefault(str(oid), set()).add(rec.get("step"))
    total = len(steps) or 1
    full = sum(1 for s in steps.values() if {"see","reason","do"}.issubset(s))
    return round(100 * full / total, 1)

def iter_blocks(ledger: Ledger) -> Iterable[dict]:
    with ledger.path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)
