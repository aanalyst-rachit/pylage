#!/usr/bin/env python3
from __future__ import annotations
import argparse, time
from common import save_result, summarize, wait_http

def measure(url, samples, warmup):
    from playwright.sync_api import sync_playwright
    wait_http(url)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        t0 = time.perf_counter()
        page.goto(url, wait_until="domcontentloaded")
        btn = page.get_by_role("button", name="Increment")
        btn.wait_for(timeout=30000)
        startup_ms = (time.perf_counter() - t0) * 1000.0
        for _ in range(warmup):
            btn.click()
            page.wait_for_timeout(30)
        latencies = []
        for _ in range(samples):
            t1 = time.perf_counter()
            btn.click()
            page.wait_for_timeout(20)
            t2 = time.perf_counter()
            latencies.append((t2 - t1) * 1000.0)
        browser.close()
    return summarize(latencies, startup_ms)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--samples", type=int, default=50)
    ap.add_argument("--warmup", type=int, default=20)
    args = ap.parse_args()
    data = measure(args.url, args.samples, args.warmup)
    data["framework"] = args.name
    data["url"] = args.url
    path = save_result(args.name, data)
    print("Saved", path)
    print(f"startup_ms={data['startup_ms']:.2f} p50={data['p50_ms']:.2f} p95={data['p95_ms']:.2f}")

if __name__ == "__main__":
    main()
