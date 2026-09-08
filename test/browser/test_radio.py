from playwright.sync_api import expect, sync_playwright

from pylage.ENGINE import Column, Input, RadioGroup, State, Text
from pylage.ENGINE.runtime import Runtime


def test_browser_radio_group_state_binding():
    selected = State("python")
    received = []

    def handle_change(payload):
        received.append(payload)

    python_radio = Input(
        input_type="radio",
        name="language",
        value="python",
    )

    javascript_radio = Input(
        input_type="radio",
        name="language",
        value="javascript",
    )

    rust_radio = Input(
        input_type="radio",
        name="language",
        value="rust",
    )

    group = RadioGroup(
        python_radio,
        javascript_radio,
        rust_radio,
        value=selected,
        on_change=handle_change,
    )

    selected_text = Text(selected)

    app = Column(
        group,
        selected_text,
    )

    runtime = Runtime(
        app,
        title="PyLage B4 Radio Browser Test",
        output=(
            "test_output/"
            "b4_radio_browser/"
            "index.html"
        ),
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            python_locator = page.locator(
                f'[data-pylage-id="{python_radio.id}"]'
            )

            javascript_locator = page.locator(
                f'[data-pylage-id="{javascript_radio.id}"]'
            )

            rust_locator = page.locator(
                f'[data-pylage-id="{rust_radio.id}"]'
            )

            selected_locator = page.locator(
                f'[data-pylage-id="{selected_text.id}"]'
            )

            expect(python_locator).to_be_checked()
            expect(javascript_locator).not_to_be_checked()
            expect(rust_locator).not_to_be_checked()
            expect(selected_locator).to_have_text("python")

            javascript_locator.check()

            for _ in range(50):
                if selected.value == "javascript":
                    break

                page.wait_for_timeout(100)

            assert selected.value == "javascript"

            assert received
            assert received[-1]["value"] == "javascript"
            assert received[-1]["checked"] is True

            expect(javascript_locator).to_be_checked()
            expect(python_locator).not_to_be_checked()
            expect(selected_locator).to_have_text(
                "javascript"
            )

            rust_locator.check()

            for _ in range(50):
                if selected.value == "rust":
                    break

                page.wait_for_timeout(100)

            assert selected.value == "rust"

            assert received[-1]["value"] == "rust"
            assert received[-1]["checked"] is True

            expect(rust_locator).to_be_checked()
            expect(javascript_locator).not_to_be_checked()
            expect(selected_locator).to_have_text("rust")

            browser.close()

    finally:
        runtime.stop()


def test_browser_radio_group_programmatic_state_update():
    selected = State("python")

    python_radio = Input(
        input_type="radio",
        name="language",
        value="python",
    )

    javascript_radio = Input(
        input_type="radio",
        name="language",
        value="javascript",
    )

    group = RadioGroup(
        python_radio,
        javascript_radio,
        value=selected,
    )

    app = Column(group)

    runtime = Runtime(
        app,
        title="PyLage B4 Radio Programmatic Update",
        output=(
            "test_output/"
            "b4_radio_programmatic/"
            "index.html"
        ),
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            python_locator = page.locator(
                f'[data-pylage-id="{python_radio.id}"]'
            )

            javascript_locator = page.locator(
                f'[data-pylage-id="{javascript_radio.id}"]'
            )

            expect(python_locator).to_be_checked()
            expect(javascript_locator).not_to_be_checked()

            selected.set("javascript")

            for _ in range(50):
                if javascript_locator.is_checked():
                    break

                page.wait_for_timeout(100)

            expect(javascript_locator).to_be_checked()
            expect(python_locator).not_to_be_checked()

            browser.close()

    finally:
        runtime.stop()
