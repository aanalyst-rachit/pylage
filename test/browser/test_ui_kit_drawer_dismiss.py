from playwright.sync_api import expect, sync_playwright

from pylage.ENGINE import Column, Drawer, State, Text
from pylage.ENGINE.runtime import Runtime


def test_drawer_backdrop_click_dismisses_drawer_in_browser():
    open_state = State(False)

    def dismiss():
        open_state.set(False)

    drawer = Drawer(
        Text("Drawer content"),
        open=open_state,
        on_dismiss=dismiss,
    )

    app = Column(drawer)

    runtime = Runtime(
        app,
        title="PyLage Drawer Dismiss Browser Test",
        output="test_output/drawer_browser/dismiss.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            page.wait_for_function(
                """
                () => (
                    window.PyLage &&
                    window.PyLage.socket &&
                    window.PyLage.socket.readyState === WebSocket.OPEN
                )
                """,
                timeout=10000,
            )

            drawer_locator = page.locator(
                f'aside[data-pylage-id="{drawer.id}"]'
            )
            backdrop = page.locator(
                ".pylage-drawer-backdrop"
            )

            expect(drawer_locator).not_to_have_attribute(
                "open"
            )

            open_state.set(True)

            expect(drawer_locator).to_have_attribute(
                "open",
                "",
                timeout=10000,
            )

            expect(backdrop).to_be_visible()

            backdrop.click()

            expect(drawer_locator).not_to_have_attribute(
                "open",
                timeout=10000,
            )

            browser.close()

    finally:
        runtime.stop()

def test_drawer_escape_key_dismisses_open_drawer_in_browser():
    open_state = State(False)

    def dismiss():
        open_state.set(False)

    drawer = Drawer(
        Text("Drawer content"),
        open=open_state,
        on_dismiss=dismiss,
    )

    app = Column(drawer)

    runtime = Runtime(
        app,
        title="PyLage Drawer Escape Browser Test",
        output="test_output/drawer_browser/escape.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded")

                page.wait_for_function(
                    """
                    () => (
                        window.PyLage &&
                        window.PyLage.socket &&
                        window.PyLage.socket.readyState === WebSocket.OPEN
                    )
                    """,
                    timeout=10000,
                )

                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )

                expect(drawer_locator).not_to_have_attribute("open")

                page.keyboard.press("Escape")

                expect(drawer_locator).not_to_have_attribute("open")

                open_state.set(True)

                expect(drawer_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )

                page.keyboard.press("Escape")

                expect(drawer_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )

            finally:
                browser.close()

    finally:
        runtime.stop()

def test_drawer_escape_key_dismisses_topmost_open_drawer_only():
    first_open = State(False)
    second_open = State(False)

    def dismiss_first():
        first_open.set(False)

    def dismiss_second():
        second_open.set(False)

    first = Drawer(
        Text("First drawer"),
        open=first_open,
        on_dismiss=dismiss_first,
    )
    second = Drawer(
        Text("Second drawer"),
        open=second_open,
        on_dismiss=dismiss_second,
    )

    app = Column(first, second)

    runtime = Runtime(
        app,
        title="PyLage Drawer Escape Stack Browser Test",
        output="test_output/drawer_browser/escape_stack.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded")

                page.wait_for_function(
                    """
                    () => (
                        window.PyLage &&
                        window.PyLage.socket &&
                        window.PyLage.socket.readyState === WebSocket.OPEN
                    )
                    """,
                    timeout=10000,
                )

                first_locator = page.locator(
                    f'aside[data-pylage-id="{first.id}"]'
                )
                second_locator = page.locator(
                    f'aside[data-pylage-id="{second.id}"]'
                )

                first_open.set(True)
                second_open.set(True)

                expect(first_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )
                expect(second_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )

                page.keyboard.press("Escape")

                expect(second_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                expect(first_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )

            finally:
                browser.close()

    finally:
        runtime.stop()
