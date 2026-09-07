from __future__ import annotations

from playwright.sync_api import sync_playwright

import pylage as pl
from pylage.ENGINE.runtime import Runtime


def test_reduced_motion_preference_disables_spinner_animation():
    spinner = pl.Spinner()

    runtime = Runtime(
        pl.Stack(spinner),
        title="PyLage Reduced Motion Browser Test",
        output="test_output/reduced_motion_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            try:
                page = browser.new_page(reduced_motion="reduce")
                page.goto(url)

                spinner_locator = page.locator(".pylage-spinner")
                assert spinner_locator.count() == 1

                animation_duration = spinner_locator.evaluate(
                    "element => getComputedStyle(element).animationDuration"
                )
                animation_iteration_count = spinner_locator.evaluate(
                    "element => getComputedStyle(element).animationIterationCount"
                )

                duration_seconds = float(animation_duration.rstrip("s"))

                assert duration_seconds == 0.00001
                assert animation_iteration_count == "1"

            finally:
                browser.close()

    finally:
        runtime.stop()
