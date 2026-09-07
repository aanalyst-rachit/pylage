import pylage as pl
from pylage.ENGINE.runtime.runtime import Runtime
from playwright.sync_api import sync_playwright


def test_active_selected_checked_browser_contract():
    active = pl.State(False)
    checked = pl.State(False)

    app = pl.column(
        pl.navigation_item("Active Item", active=active),
        pl.tabs(
            pl.tab("First", value="first"),
            pl.tab("Second", value="second"),
            value="first",
        ),
        pl.checkbox("Check Me", checked=checked),
        pl.switch("Switch Me", checked=checked),
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

            navigation = page.get_by_text("Active Item", exact=True).locator("..")
            checkbox = page.get_by_text("Check Me", exact=True).locator("..")
            switch = page.get_by_text("Switch Me", exact=True).locator("..")

            navigation_initial = navigation.evaluate("element => { const s = getComputedStyle(element); return { background: s.backgroundColor, color: s.color }; }")
            checkbox_initial = checkbox.locator("input").is_checked()
            switch_initial = switch.locator("input").is_checked()

            print("=== ACTIVE SELECTED CHECKED CONTRACT ===")
            print(f"NAV INITIAL: {navigation_initial}")
            print(f"CHECKBOX INITIAL: {checkbox_initial}")
            print(f"SWITCH INITIAL: {switch_initial}")

            assert checkbox_initial is False
            assert switch_initial is False

            checkbox.locator("input").check()
            assert checkbox.locator("input").is_checked() is True

            switch.locator("input").check()
            assert switch.locator("input").is_checked() is True

            navigation.click()
            navigation_after = navigation.evaluate("element => { const s = getComputedStyle(element); return { background: s.backgroundColor, color: s.color }; }")
            print(f"NAV AFTER CLICK: {navigation_after}")

            assert navigation_after["background"] != navigation_initial["background"]

            browser.close()
    finally:
        runtime.stop()
