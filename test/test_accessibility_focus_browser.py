from __future__ import annotations

from playwright.sync_api import expect, sync_playwright

import pylage as pl
from pylage.ENGINE.runtime import Runtime


def test_native_controls_preserve_focus_behavior():
    input_control = pl.input(
        placeholder="Name",
        name="name",
    )
    button_control = pl.button("Continue")

    app = pl.Stack(
        input_control,
        button_control,
    )

    runtime = Runtime(
        app,
        title="PyLage Accessibility Focus Test",
        output="test_output/accessibility_focus_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                input_locator = page.locator("input").first
                button_locator = page.locator(
                    f'[data-pylage-id="{button_control.id}"]'
                )

                input_locator.focus()
                expect(input_locator).to_be_focused()
                assert page.evaluate(
                    "document.activeElement === document.querySelector('input')"
                )

                button_locator.focus()
                expect(button_locator).to_be_focused()
                assert page.evaluate(
                    """document.activeElement === document.querySelector(
                        'button[data-pylage-id="%s"]'
                    )"""
                    % button_control.id
                )

            finally:
                browser.close()

    finally:
        runtime.stop()


def test_form_field_label_is_associated_with_control():
    field = pl.form_field(
        pl.input(placeholder="Email", name="email"),
        label="Email address",
        required=True,
        help_text="Enter your email address.",
    )

    app = pl.Stack(field)

    runtime = Runtime(
        app,
        title="PyLage Accessibility Semantic Label Test",
        output="test_output/accessibility_semantic_label_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                label = page.locator('label').first
                control = page.locator('input').first

                label_for = label.get_attribute('for')
                control_id = control.get_attribute('id')

                assert label_for
                assert control_id
                assert label_for == control_id
                expect(label).to_contain_text('Email address')
                assert control.get_attribute('required') is not None

                label.click()
                expect(control).to_be_focused()

            finally:
                browser.close()

    finally:
        runtime.stop()


def test_interactive_states_render_and_update():
    from pylage import State

    active = State(False)
    navigation = pl.navigation_item("Dashboard", active=active)
    button = pl.button("Save")

    app = pl.Stack(
        navigation,
        button,
    )

    runtime = Runtime(
        app,
        title="PyLage Accessibility Interactive State Test",
        output="test_output/accessibility_interactive_states_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                navigation_locator = page.locator(
                    f'[data-pylage-id="{navigation.id}"]'
                )
                button_locator = page.locator(
                    f'[data-pylage-id="{button.id}"]'
                )

                initial_style = navigation_locator.get_attribute("style") or ""
                assert "var(--color-primary)" not in initial_style

                active.set(True)
                expect(navigation_locator).to_have_attribute("data-pylage-id", navigation.id)

                page.wait_for_timeout(100)
                active_style = navigation_locator.get_attribute("style") or ""
                assert "var(--color-primary)" in active_style

                button_locator.focus()
                expect(button_locator).to_be_focused()

            finally:
                browser.close()

    finally:
        runtime.stop()


def test_dialog_open_state_is_reflected_in_browser():
    from pylage import State

    open_state = State(False)
    component = pl.dialog(
        pl.text("Accessible dialog"),
        open=open_state,
    )

    app = pl.Stack(component)

    runtime = Runtime(
        app,
        title="PyLage Accessibility Modal Test",
        output="test_output/accessibility_modal_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                dialog_locator = page.locator("dialog").first

                assert not dialog_locator.get_attribute("open")
                expect(dialog_locator).not_to_be_visible()

                open_state.set(True)
                page.wait_for_timeout(100)

                assert dialog_locator.get_attribute("open") is not None
                expect(dialog_locator).to_be_visible()

                open_state.set(False)
                page.wait_for_timeout(100)

                assert not dialog_locator.get_attribute("open")
                expect(dialog_locator).not_to_be_visible()

            finally:
                browser.close()

    finally:
        runtime.stop()


def test_navigation_behavior_is_semantic_and_reactive():
    from pylage import State

    active = State(False)
    item = pl.navigation_item("Dashboard", active=active)
    navigation = pl.navigation(item)

    app = pl.Stack(navigation)

    runtime = Runtime(
        app,
        title="PyLage Accessibility Navigation Test",
        output="test_output/accessibility_navigation_browser/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto(url)

                nav_locator = page.locator("nav").first
                item_locator = page.locator(
                    f'[data-pylage-id="{item.id}"]'
                )

                expect(nav_locator).to_be_visible()
                expect(item_locator).to_be_visible()

                initial_style = item_locator.get_attribute("style") or ""
                assert "var(--color-primary)" not in initial_style

                active.set(True)
                page.wait_for_timeout(100)

                active_style = item_locator.get_attribute("style") or ""
                assert "var(--color-primary)" in active_style

                item_locator.focus()
                expect(item_locator).to_be_focused()

            finally:
                browser.close()

    finally:
        runtime.stop()
