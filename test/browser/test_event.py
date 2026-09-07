from playwright.sync_api import sync_playwright, expect

import pylage as ps
from pylage.ENGINE import Button, Card, Column, Heading, Text
from pylage.ENGINE.runtime import Runtime


def test_browser_event():
    print("=== PYLAGE BROWSER EVENT TEST ===")

    calls = []

    def clicked():
        calls.append("clicked")
        print("=== BROWSER EVENT RECEIVED ===")
        print("Calls:", calls)
        return "clicked"

    heading = Heading("Browser Event Test")

    button = Button(
        "Click me",
        on_click=clicked,
    )

    app = Column(
        heading,
        button,
    )

    runtime = Runtime(
        app,
        title="Browser Event Test",
        output="test_output/browser_event_output/index.html",
    )

    try:
        url = runtime.start()

        print("URL:", url)
        print("WebSocket:", runtime._websocket.url)
        print("Button ID:", button.id)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            button_locator = page.locator(
                f'[data-pylage-id="{button.id}"]'
            )

            expect(button_locator).to_have_text("Click me")

            print("Browser loaded: PASS")

            button_locator.click()

            page.wait_for_function(
                """() => window.__pylage_event_test_done === true"""
            ) if False else None

            # Poll Python-side callback without arbitrary long waits.
            for _ in range(50):
                if calls == ["clicked"]:
                    break
                page.wait_for_timeout(100)

            assert calls == ["clicked"]

            print("Browser click: PASS")
            print("WebSocket event → Python callback: PASS")
            print("Callback isolation: PASS")

            browser.close()

        print()
        print("=== BROWSER EVENT PASS ===")

    finally:
        runtime.stop()
        print("Runtime stopped.")


def test_browser_event_bubbles_to_parent_component():
    print("=== NESTED PARENT BROWSER EVENT TEST ===")

    calls = []

    def clicked():
        calls.append("clicked")

    card = Card(
        Text("Nested clickable content"),
        on_click=clicked,
    )

    app = Column(card)

    runtime = Runtime(
        app,
        title="Nested Parent Browser Event Test",
        output="test_output/nested_parent_browser_event_output/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            text_locator = page.locator(
                f'[data-pylage-id="{card.children[0].id}"]'
            )

            expect(text_locator).to_have_text("Nested clickable content")

            text_locator.click()

            for _ in range(50):
                if calls == ["clicked"]:
                    break
                page.wait_for_timeout(100)

            assert calls == ["clicked"]

            browser.close()

    finally:
        runtime.stop()
