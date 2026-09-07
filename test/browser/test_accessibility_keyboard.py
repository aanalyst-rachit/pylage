from __future__ import annotations

from playwright.sync_api import expect, sync_playwright

import pylage as pl
from pylage.ENGINE.runtime import Runtime


def test_keyboard_tab_focus_and_button_activation():
    calls = []

    def handle_first():
        calls.append("first")

    def handle_second():
        calls.append("second")

    first = pl.button("First", on_click=handle_first)
    second = pl.button("Second", on_click=handle_second)

    app = pl.Stack(
        pl.input(
            placeholder="Name",
            name="name",
        ),
        first,
        second,
    )

    runtime = Runtime(
        app,
        title="PyLage Accessibility Keyboard Test",
        output="test_output/accessibility_keyboard_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                input_locator = page.locator("input").first
                first_locator = page.locator(
                    f'[data-pylage-id="{first.id}"]'
                )
                second_locator = page.locator(
                    f'[data-pylage-id="{second.id}"]'
                )

                page.keyboard.press("Tab")
                expect(input_locator).to_be_focused()

                page.keyboard.press("Tab")
                expect(first_locator).to_be_focused()

                page.keyboard.press("Enter")

                for _ in range(50):
                    if calls == ["first"]:
                        break
                    page.wait_for_timeout(100)

                assert calls == ["first"]

                page.keyboard.press("Tab")
                expect(second_locator).to_be_focused()

                page.keyboard.press("Space")

                for _ in range(50):
                    if calls == ["first", "second"]:
                        break
                    page.wait_for_timeout(100)

                assert calls == ["first", "second"]

            finally:
                browser.close()

    finally:
        runtime.stop()


def test_disabled_input_is_skipped_by_keyboard_focus():
    disabled = pl.input(
        placeholder="Disabled",
        name="disabled",
        disabled=True,
    )
    enabled = pl.input(
        placeholder="Enabled",
        name="enabled",
    )

    app = pl.Stack(
        disabled,
        enabled,
    )

    runtime = Runtime(
        app,
        title="PyLage Accessibility Disabled Input Test",
        output="test_output/accessibility_disabled_input_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                disabled_locator = page.locator(
                    f'[data-pylage-id="{disabled.id}"]'
                )
                enabled_locator = page.locator(
                    f'[data-pylage-id="{enabled.id}"]'
                )

                assert disabled_locator.is_disabled()

                page.keyboard.press("Tab")
                expect(enabled_locator).to_be_focused()
                expect(disabled_locator).not_to_be_focused()

            finally:
                browser.close()

    finally:
        runtime.stop()


def test_disabled_button_is_skipped_by_keyboard_focus():
    enabled = pl.button("Enabled")
    disabled = pl.button("Disabled", disabled=True)

    app = pl.Stack(
        pl.input(
            placeholder="Name",
            name="name",
        ),
        disabled,
        enabled,
    )

    runtime = Runtime(
        app,
        title="PyLage Accessibility Disabled Keyboard Test",
        output="test_output/accessibility_disabled_keyboard_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                input_locator = page.locator("input").first
                disabled_locator = page.locator(
                    f'[data-pylage-id="{disabled.id}"]'
                )
                enabled_locator = page.locator(
                    f'[data-pylage-id="{enabled.id}"]'
                )

                page.keyboard.press("Tab")
                expect(input_locator).to_be_focused()

                page.keyboard.press("Tab")
                expect(enabled_locator).to_be_focused()
                expect(disabled_locator).not_to_be_focused()

            finally:
                browser.close()

    finally:
        runtime.stop()
