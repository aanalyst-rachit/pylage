from playwright.sync_api import expect, sync_playwright

import pylage as pl
from pylage.ENGINE.runtime import Runtime


def test_browser_slider_state_binding():
    value = pl.State(25)
    slider = pl.slider(
        value=value,
        min=0,
        max=100,
        step=5,
    )

    app = pl.Stack(slider)

    runtime = Runtime(
        app,
        title="PyLage Slider Browser Binding",
        output="test_output/slider_browser_binding/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            slider_locator = page.locator("input[type=range]")

            expect(slider_locator).to_have_value("25")

            slider_locator.evaluate(
                "(el) => { el.value = '75'; el.dispatchEvent(new Event('input', {bubbles: true})); }"
            )

            for _ in range(50):
                if value.value == "75":
                    break
                page.wait_for_timeout(100)

            assert value.value == "75"
            expect(slider_locator).to_have_value("75")

            browser.close()
    finally:
        runtime.stop()


def test_browser_slider_state_binding_preserves_custom_on_input():
    value = pl.State(25)
    received = []

    def handle_input(payload):
        received.append(payload)

    slider = pl.slider(
        value=value,
        min=0,
        max=100,
        step=5,
        on_input=handle_input,
    )

    app = pl.Stack(slider)

    runtime = Runtime(
        app,
        title="PyLage Slider Custom Input Binding",
        output="test_output/slider_browser_custom_input/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            slider_locator = page.locator("input[type=range]")

            slider_locator.evaluate(
                "(el) => { el.value = '80'; el.dispatchEvent(new Event('input', {bubbles: true})); }"
            )

            for _ in range(50):
                if value.value == "80":
                    break
                page.wait_for_timeout(100)

            assert value.value == "80"
            assert received
            assert received[-1]["value"] == "80"

            browser.close()
    finally:
        runtime.stop()
