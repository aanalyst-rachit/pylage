from playwright.sync_api import expect, sync_playwright

from pylage.ENGINE import Column, Option, Select, State, Text
from pylage.ENGINE.runtime import Runtime


def test_browser_select_state_binding():
    selected = State("india")
    received = []

    def handle_change(payload):
        received.append(payload)

    select = Select(
        Option("India", value="india"),
        Option("Japan", value="japan"),
        Option("Nepal", value="nepal"),
        value=selected,
        on_change=handle_change,
    )

    selected_text = Text(selected)

    app = Column(
        select,
        selected_text,
    )

    runtime = Runtime(
        app,
        title="PyLage B4 Select Browser State Binding",
        output="test_output/b4_select_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            select_locator = page.locator(
                f'[data-pylage-id="{select.id}"]'
            )
            selected_locator = page.locator(
                f'[data-pylage-id="{selected_text.id}"]'
            )

            expect(select_locator).to_have_value("india")
            expect(selected_locator).to_have_text("india")

            select_locator.select_option("japan")

            for _ in range(50):
                if selected.value == "japan":
                    break

                page.wait_for_timeout(100)

            assert selected.value == "japan"
            assert received
            assert received[-1]["value"] == "japan"
            assert received[-1]["selectedIndex"] == 1

            expect(select_locator).to_have_value("japan")
            expect(selected_locator).to_have_text("japan")

            selected.set("nepal")

            for _ in range(50):
                if select_locator.input_value() == "nepal":
                    break

                page.wait_for_timeout(100)

            expect(select_locator).to_have_value("nepal")
            expect(selected_locator).to_have_text("nepal")

            browser.close()

    finally:
        runtime.stop()
