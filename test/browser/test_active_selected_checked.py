import pylage as pl
from pylage.ENGINE.runtime.runtime import Runtime
from playwright.sync_api import sync_playwright


def test_active_selected_checked_browser_contract():
    active = pl.state(False)
    checked = pl.state(False)

    app = pl.column(
        pl.navigation_item("Active Item", active=active),
        pl.tabs(
            pl.text("First"),
            pl.text("Second"),
            value="first",
        ),
        pl.checkbox(name="check_me", title="Check Me", checked=checked),
        pl.switch(name="switch_me", title="Switch Me", checked=checked),
    )

    runtime = Runtime(
        app,
        title="PyLage Active Selected Checked Contract",
        output="test_output/browser_active_selected_checked_contract/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(url)

            navigation = page.locator(f'[data-pylage-id="{app.children[0].id}"]')
            checkbox = page.locator('input[name="check_me"]')
            switch = page.locator('input[name="switch_me"]')

            navigation_initial = navigation.evaluate("element => { const s = getComputedStyle(element); return { background: s.backgroundColor, color: s.color }; }")
            checkbox_initial = checkbox.is_checked()
            switch_initial = switch.is_checked()

            print("=== ACTIVE SELECTED CHECKED CONTRACT ===")
            print(f"NAV INITIAL: {navigation_initial}")
            print(f"CHECKBOX INITIAL: {checkbox_initial}")
            print(f"SWITCH INITIAL: {switch_initial}")

            assert checkbox_initial is False
            assert switch_initial is False

            checkbox.check()
            assert checkbox.is_checked() is True

            switch.check()
            assert switch.is_checked() is True

            active.set(True)
            page.wait_for_timeout(100)
            navigation_after = navigation.evaluate("element => { const s = getComputedStyle(element); return { background: s.backgroundColor, color: s.color }; }")
            print(f"NAV AFTER ACTIVE SET: {navigation_after}")

            assert navigation_after["background"] != navigation_initial["background"]
            assert navigation_after["color"] != navigation_initial["color"]

            browser.close()
    finally:
        runtime.stop()
