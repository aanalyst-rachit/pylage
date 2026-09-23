from __future__ import annotations
import json, statistics, time
from pathlib import Path
from typing import Any

RESULTS = Path(__file__).resolve().parent.parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

def percentile(values, p):
    s = sorted(values)
    if not s:
        return float("nan")
    k = max(0, min(len(s) - 1, int(round((p / 100.0) * (len(s) - 1)))))
    return s[k]

def summarize(latencies_ms, startup_ms):
    return {
        "startup_ms": startup_ms,
        "n": len(latencies_ms),
        "mean_ms": statistics.mean(latencies_ms) if latencies_ms else None,
        "p50_ms": statistics.median(latencies_ms) if latencies_ms else None,
        "p95_ms": percentile(latencies_ms, 95) if latencies_ms else None,
        "samples_ms": latencies_ms,
    }

def save_result(name, data):
    path = RESULTS / f"{name}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path

def wait_http(url, timeout=30.0):
    import urllib.request
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1.0) as r:
                if r.status < 500:
                    return
        except Exception as e:
            last = e
            time.sleep(0.2)
    raise RuntimeError(f"Server not ready: {url} ({last})")
