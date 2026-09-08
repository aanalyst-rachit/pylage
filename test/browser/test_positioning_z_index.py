import pylage as pl
from pylage.ENGINE.runtime.runtime import Runtime
from playwright.sync_api import sync_playwright


def test_positioning_and_z_index_browser_contract():
    app = pl.column(
        pl.card(
            heading="Relative Contract",
            body="Relative positioning",
            style=pl.style(position="relative", top="10px", left="12px"),
        ),
        pl.card(
            heading="Absolute Contract",
            body="Absolute positioning",
            style=pl.style(position="absolute", top="20px", right="30px"),
        ),
        pl.card(
            heading="Fixed Contract",
            body="Fixed positioning",
            style=pl.style(position="fixed", bottom="10px", left="15px", z_index=1200),
        ),
    )

    runtime = Runtime(
        app,
        title="PyLage Positioning Z Index Contract",
        output="test_output/browser_positioning_z_index_contract/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(url)

            relative = page.get_by_text("Relative Contract", exact=True).locator("..")
            absolute = page.get_by_text("Absolute Contract", exact=True).locator("..")
            fixed = page.get_by_text("Fixed Contract", exact=True).locator("..")

            relative_values = relative.evaluate("element => { const s = getComputedStyle(element); return { position: s.position, top: s.top, left: s.left }; }")
            absolute_values = absolute.evaluate("element => { const s = getComputedStyle(element); return { position: s.position, top: s.top, right: s.right }; }")
            fixed_values = fixed.evaluate("element => { const s = getComputedStyle(element); return { position: s.position, bottom: s.bottom, left: s.left, zIndex: s.zIndex }; }")

            print("=== POSITIONING Z-INDEX CONTRACT ===")
            print(f"RELATIVE: {relative_values}")
            print(f"ABSOLUTE: {absolute_values}")
            print(f"FIXED: {fixed_values}")

            assert relative_values["position"] == "relative"
            assert relative_values["top"] == "10px"
            assert relative_values["left"] == "12px"

            assert absolute_values["position"] == "absolute"
            assert absolute_values["top"] == "20px"
            assert absolute_values["right"] == "30px"

            assert fixed_values["position"] == "fixed"
            assert fixed_values["bottom"] == "10px"
            assert fixed_values["left"] == "15px"
            assert fixed_values["zIndex"] == "1200"

            browser.close()
    finally:
        runtime.stop()
