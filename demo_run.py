
from ingest_cv import simulate_stream
from pathlib import Path
out = simulate_stream("sha713_demo/ledger.jsonl", n_objects=3)
Path("sha713_demo/README.txt").write_text(str(out))
print("Demo complete. Ledger at sha713_demo/ledger.jsonl")
