#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from common import save_result, summarize, wait_http


def get_counter(page, framework):
    btn = page.get_by_role(
        "button",
        name="Increment",
    )
    btn.wait_for(timeout=30000)

    if framework == "pylage":
        root = btn.locator("xpath=..")
        counter = root.locator(":scope > div").nth(0)

    elif framework == "nicegui":
        root = btn.locator("xpath=..")
        counter = root.locator(":scope > div").nth(1)

    elif framework == "streamlit":
        heading = page.get_by_role(
            "heading",
            name="Counter",
        )
        counter = heading.locator(
            "xpath=following::p[1]"
        )

    elif framework == "reflex":
        heading = page.get_by_role(
            "heading",
            name="Counter",
        )
        counter = heading.locator(
            "xpath=following::p[1]"
        )

    else:
        raise ValueError(
            f"Unsupported framework: {framework}"
        )

    counter.wait_for(timeout=30000)

    return btn, counter


def measure(url, framework, samples, warmup):
    from playwright.sync_api import expect, sync_playwright

    wait_http(url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        t0 = time.perf_counter()

        page.goto(
            url,
            wait_until="domcontentloaded",
        )

        btn, counter = get_counter(
            page,
            framework,
        )

        current = int(
            counter.inner_text().strip()
        )

        startup_ms = (
            time.perf_counter() - t0
        ) * 1000.0

        def one_increment():
            nonlocal counter

            current = int(
                counter.inner_text().strip()
            )
            expected = str(current + 1)

            t1 = time.perf_counter()

            btn.click()

            expect(counter).to_have_text(
                expected,
                timeout=5000,
            )

            t2 = time.perf_counter()

            return (t2 - t1) * 1000.0

        for _ in range(warmup):
            one_increment()

        latencies = []

        for _ in range(samples):
            latencies.append(
                one_increment()
            )

        browser.close()

    return summarize(
        latencies,
        startup_ms,
    )


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--name",
        required=True,
        choices=[
            "pylage",
            "nicegui",
            "streamlit",
            "reflex",
        ],
    )

    ap.add_argument(
        "--url",
        required=True,
    )

    ap.add_argument(
        "--samples",
        type=int,
        default=50,
    )

    ap.add_argument(
        "--warmup",
        type=int,
        default=20,
    )

    args = ap.parse_args()

    data = measure(
        args.url,
        args.name,
        args.samples,
        args.warmup,
    )

    data.update(
        {
            "framework": args.name,
            "url": args.url,
            "scenario": "counter",
            "warmup": args.warmup,
            "completion": "counter_value_incremented",
        }
    )

    path = save_result(
        args.name,
        data,
    )

    print("Saved", path)
    print(
        f"startup_ms={data['startup_ms']:.2f} "
        f"p50={data['p50_ms']:.2f} "
        f"p95={data['p95_ms']:.2f}"
    )


if __name__ == "__main__":
    main()
