
"""
ingest_cv.py — demo adapter that simulates detections and writes a SHA-713 ledger
Run:
  python ingest_cv.py
Outputs:
  /mnt/data/sha713_pkg/out/ledger.jsonl
"""
import json, random
from pathlib import Path
from sha713_core import Ledger, Signer

OUT = Path("/mnt/data/sha713_pkg/out/ledger.jsonl")
SECRET = b"demo-key-sha713-avantix"
signer = Signer(SECRET)
ledger = Ledger(OUT)

RULES = {
    "detector": {"min_conf": 0.80},
    "reasoner": {"min_track_conf": 0.85, "min_velocity": 0.8},
    "action": {"alert_threshold": 1},
}

random.seed(713)

def see(camera_id: str, obj_id: int):
    import random
    conf = round(random.uniform(0.75, 0.97), 2)
    det = {"step":"see","camera":camera_id,"obj_id":obj_id,
           "bbox":[random.randint(100,500), random.randint(100,500), 64, 64],
           "confidence":conf,"rule_min_conf":RULES["detector"]["min_conf"]}
    det["decision"] = "accept" if conf >= RULES["detector"]["min_conf"] else "reject"
    return det

def reason(prev_det: dict):
    import random
    vel = round(random.uniform(0.6, 1.0), 2)
    track_conf = round(max(prev_det["confidence"], vel - 0.05), 2)
    decision = "track" if (track_conf >= RULES["reasoner"]["min_track_conf"] and vel >= RULES["reasoner"]["min_velocity"]) else "discard"
    return {"step":"reason","obj_id":prev_det["obj_id"],"track_conf":track_conf,
            "velocity_score":vel,"rule_min_track_conf":RULES["reasoner"]["min_track_conf"],
            "rule_min_velocity":RULES["reasoner"]["min_velocity"],"decision":decision}

def do(reason_out: dict):
    alert = 1 if reason_out["decision"] == "track" else 0
    return {"step":"do","obj_id":reason_out["obj_id"],"action":"alert" if alert else "none",
            "alert_count":alert,"rule_alert_threshold":RULES["action"]["alert_threshold"]}

# fresh run
if OUT.exists(): OUT.unlink()
OUT.parent.mkdir(parents=True, exist_ok=True)

for oid in [101, 102, 103]:
    r1 = see("cam-A", oid); ledger.append_record(r1, signer)
    if r1["decision"] == "accept":
        r2 = reason(r1); ledger.append_record(r2, signer)
        r3 = do(r2);     ledger.append_record(r3, signer)

ok, n, err = ledger.verify(signer)
ali = 0.0
try:
    from sha713_core import compute_ali
    ali = compute_ali(ledger)
except Exception:
    pass

print(json.dumps({"ok": ok, "blocks": n, "error": err, "ALI_percent": ali}, indent=2))
print(f"Ledger → {OUT}")
