from playwright.sync_api import expect, sync_playwright

import pylage as pl
from pylage.ENGINE.runtime import Runtime


def test_browser_datepicker_state_binding():
    value = pl.State("2026-09-03")

    datepicker = pl.datepicker(
        value=value,
        min="2026-01-01",
        max="2026-12-31",
    )

    app = pl.Stack(datepicker)

    runtime = Runtime(
        app,
        title="PyLage DatePicker Browser Binding",
        output="test_output/datepicker_browser_binding/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            datepicker_locator = page.locator("input[type=date]")

            expect(datepicker_locator).to_have_value("2026-09-03")

            datepicker_locator.evaluate(
                "(el) => { el.value = '2026-09-15'; el.dispatchEvent(new Event('input', {bubbles: true})); }"
            )

            for _ in range(50):
                if value.value == "2026-09-15":
                    break
                page.wait_for_timeout(100)

            assert value.value == "2026-09-15"
            expect(datepicker_locator).to_have_value("2026-09-15")

            browser.close()
    finally:
        runtime.stop()


def test_browser_datepicker_state_binding_preserves_custom_on_input():
    value = pl.State("2026-09-03")
    received = []

    def handle_input(payload):
        received.append(payload)

    datepicker = pl.datepicker(
        value=value,
        on_input=handle_input,
    )

    app = pl.Stack(datepicker)

    runtime = Runtime(
        app,
        title="PyLage DatePicker Custom Input Binding",
        output="test_output/datepicker_browser_custom_input/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            datepicker_locator = page.locator("input[type=date]")

            expect(datepicker_locator).to_have_value("2026-09-03")

            datepicker_locator.evaluate(
                "(el) => { el.value = '2026-10-01'; el.dispatchEvent(new Event('input', {bubbles: true})); }"
            )

            for _ in range(50):
                if value.value == "2026-10-01":
                    break
                page.wait_for_timeout(100)

            assert value.value == "2026-10-01"
            assert received
            assert received[-1]["value"] == "2026-10-01"

            browser.close()
    finally:
        runtime.stop()
