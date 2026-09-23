#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"


def load_results(scenario):
    rows = []

    for path in sorted(RESULTS.glob("*.json")):
        try:
            data = json.loads(
                path.read_text(encoding="utf-8")
            )
        except Exception:
            continue

        if data.get("scenario") != scenario:
            continue

        rows.append(data)

    return rows


def write_report(scenario, output):
    rows = load_results(scenario)

    title = (
        "Counter benchmark"
        if scenario == "counter"
        else "Form benchmark"
    )

    lines = [
        f"# {title} (v2)",
        "",
        "| Framework | Startup (ms) | P50 (ms) | P95 (ms) | Mean (ms) | N |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for data in rows:
        lines.append(
            f"| {data.get("framework", "unknown")} "
            f"| {data.get("startup_ms", 0):.2f} "
            f"| {data.get("p50_ms", 0):.2f} "
            f"| {data.get("p95_ms", 0):.2f} "
            f"| {data.get("mean_ms", 0):.2f} "
            f"| {data.get("n", 0)} |"
        )

    output.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("Wrote", output)


if __name__ == "__main__":
    write_report(
        "counter",
        ROOT / "REPORT.md",
    )

    write_report(
        "form",
        ROOT / "REPORT_FORM.md",
    )
