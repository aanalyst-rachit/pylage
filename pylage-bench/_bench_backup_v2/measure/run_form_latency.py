#!/usr/bin/env python3
"""Measure form: load + fill fields + submit visible update."""
from __future__ import annotations

import argparse
import statistics
import time
from pathlib import Path

import json
from playwright.sync_api import sync_playwright
import urllib.request


RESULTS = Path(__file__).resolve().parent.parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def percentile(values, p):
    s = sorted(values)
    if not s:
        return float("nan")
    k = max(0, min(len(s) - 1, int(round((p / 100.0) * (len(s) - 1)))))
    return s[k]


def wait_http(url, timeout=60.0):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1.5) as r:
                if r.status < 500:
                    return
        except Exception as e:
            last = e
            time.sleep(0.3)
    raise RuntimeError(f"not ready {url} {last}")


def one_submit_cycle(page, i: int):
    # Fill fields (best-effort across frameworks)
    # Prefer placeholder / label / role
    name_val = f"User{i}"
    email_val = f"user{i}@example.com"

    # text inputs: first two textboxes often name/email
    boxes = page.get_by_role("textbox")
    count = boxes.count()
    if count >= 1:
        boxes.nth(0).fill(name_val)
    if count >= 2:
        boxes.nth(1).fill(email_val)

    # checkbox terms
    try:
        page.get_by_role("checkbox").first.check(timeout=1000)
    except Exception:
        pass

    t1 = time.perf_counter()
    page.get_by_role("button", name="Submit").click()
    # wait until Saved or new row text appears
    try:
        page.get_by_text("Saved").wait_for(timeout=5000)
    except Exception:
        try:
            page.get_by_text(name_val).wait_for(timeout=5000)
        except Exception:
            page.wait_for_timeout(30)
    t2 = time.perf_counter()
    return (t2 - t1) * 1000.0


def measure(url, samples=30, warmup=5):
    wait_http(url)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        t0 = time.perf_counter()
        page.goto(url, wait_until="domcontentloaded")
        page.get_by_role("button", name="Submit").wait_for(timeout=60000)
        startup_ms = (time.perf_counter() - t0) * 1000.0

        for i in range(warmup):
            one_submit_cycle(page, 1000 + i)

        latencies = []
        for i in range(samples):
            latencies.append(one_submit_cycle(page, i + 1))

        browser.close()

    return {
        "startup_ms": startup_ms,
        "n": len(latencies),
        "mean_ms": statistics.mean(latencies),
        "p50_ms": statistics.median(latencies),
        "p95_ms": percentile(latencies, 95),
        "samples_ms": latencies,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--samples", type=int, default=30)
    ap.add_argument("--warmup", type=int, default=5)
    args = ap.parse_args()
    data = measure(args.url, args.samples, args.warmup)
    data["framework"] = args.name
    data["url"] = args.url
    data["scenario"] = "complex_form"
    path = RESULTS / f"form_{args.name}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("Saved", path)
    print(f"startup={data['startup_ms']:.2f} p50={data['p50_ms']:.2f} p95={data['p95_ms']:.2f}")


if __name__ == "__main__":
    main()
