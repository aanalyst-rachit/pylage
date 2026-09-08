import pylage as pl
from pylage.ENGINE.runtime.runtime import Runtime
from playwright.sync_api import sync_playwright


def test_width_height_constraints_browser_contract():
    app = pl.column(
        pl.card(heading="Fixed Size", variant="default", style=pl.style(width="300px", height="120px")),
        pl.card(heading="Min Max Size", variant="default", style=pl.style(min_width="280px", max_width="320px", min_height="100px", max_height="140px")),
    )

    runtime = Runtime(
        app,
        title="PyLage Width Height Contract",
        output="test_output/browser_width_height_contract/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(url)

            fixed = page.get_by_text("Fixed Size", exact=True).locator("..")
            constrained = page.get_by_text("Min Max Size", exact=True).locator("..")

            fixed_width = fixed.evaluate("element => getComputedStyle(element).width")
            fixed_height = fixed.evaluate("element => getComputedStyle(element).height")
            constrained_width = constrained.evaluate("element => getComputedStyle(element).width")
            constrained_height = constrained.evaluate("element => getComputedStyle(element).height")

            print("=== WIDTH HEIGHT CONTRACT ===")
            print(f"FIXED WIDTH: {fixed_width}")
            print(f"FIXED HEIGHT: {fixed_height}")
            print(f"CONSTRAINED WIDTH: {constrained_width}")
            print(f"CONSTRAINED HEIGHT: {constrained_height}")

            assert fixed_width == "300px"
            assert fixed_height == "120px"
            assert float(constrained_width.replace("px", "")) >= 280
            assert float(constrained_width.replace("px", "")) <= 320
            assert float(constrained_height.replace("px", "")) >= 100
            assert float(constrained_height.replace("px", "")) <= 140

            browser.close()
    finally:
        runtime.stop()
