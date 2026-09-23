#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

from playwright.sync_api import sync_playwright

from common import save_result, summarize, wait_http


def one_submit_cycle(page, i: int):
    name_val = f"User{i}"
    email_val = f"user{i}@example.com"
    expected_row = f"{name_val} | {email_val}"

    boxes = page.get_by_role("textbox")

    count = boxes.count()

    if count < 2:
        raise RuntimeError(
            f"Expected at least 2 textboxes, found {count}"
        )

    boxes.nth(0).fill(name_val)
    boxes.nth(1).fill(email_val)

    t1 = time.perf_counter()

    page.get_by_role(
        "button",
        name="Submit",
    ).click()

    # Completion signal is the newly-created unique row.
    page.get_by_text(
        expected_row,
        exact=True,
    ).wait_for(timeout=5000)

    t2 = time.perf_counter()

    return (t2 - t1) * 1000.0


def measure(url, samples=30, warmup=5):
    wait_http(url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        t0 = time.perf_counter()

        page.goto(
            url,
            wait_until="domcontentloaded",
        )

        page.get_by_role(
            "button",
            name="Submit",
        ).wait_for(timeout=60000)

        page.get_by_role(
            "textbox",
        ).nth(0).wait_for(timeout=5000)

        page.get_by_role(
            "textbox",
        ).nth(1).wait_for(timeout=5000)

        startup_ms = (
            time.perf_counter() - t0
        ) * 1000.0

        for i in range(warmup):
            one_submit_cycle(
                page,
                1000 + i,
            )

        latencies = []

        for i in range(samples):
            latencies.append(
                one_submit_cycle(
                    page,
                    i + 1,
                )
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
    )

    ap.add_argument(
        "--url",
        required=True,
    )

    ap.add_argument(
        "--samples",
        type=int,
        default=30,
    )

    ap.add_argument(
        "--warmup",
        type=int,
        default=5,
    )

    args = ap.parse_args()

    data = measure(
        args.url,
        args.samples,
        args.warmup,
    )

    data.update(
        {
            "framework": args.name,
            "url": args.url,
            "scenario": "form",
            "warmup": args.warmup,
            "completion": "unique_submitted_row_visible",
        }
    )

    path = save_result(
        f"form_{args.name}",
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
