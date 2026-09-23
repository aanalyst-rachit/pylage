#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
OUT = ROOT / "REPORT.md"
rows = []
for path in sorted(RESULTS.glob("*.json")):
    d = json.loads(path.read_text(encoding="utf-8"))
    rows.append((d.get("framework", path.stem), d.get("startup_ms"), d.get("p50_ms"), d.get("p95_ms"), d.get("n")))
lines = ["# Counter benchmark", "", "| Framework | Startup (ms) | P50 (ms) | P95 (ms) | N |", "|---|---:|---:|---:|---:|"]
for name, s, p50, p95, n in rows:
    lines.append(f"| {name} | {s:.2f} | {p50:.2f} | {p95:.2f} | {n} |")
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Wrote", OUT)
