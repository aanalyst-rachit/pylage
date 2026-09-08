from pylage import UI as pl
from pylage.ENGINE.runtime.runtime import Runtime
from playwright.sync_api import sync_playwright


def test_card_shadow_variants_browser_contract():
    app = pl.column(
        pl.card(heading="Default Card", variant="default"),
        pl.card(heading="Elevated Card", variant="elevated"),
        pl.card(heading="Outlined Card", variant="outlined"),
        pl.card(heading="Interactive Card", variant="interactive"),
    )

    runtime = Runtime(
        app,
        title="PyLage Card Shadow Contract",
        output="test_output/browser_card_shadow_contract/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            cards = {
                "default": page.get_by_text("Default Card", exact=True).locator(".."),
                "elevated": page.get_by_text("Elevated Card", exact=True).locator(".."),
                "outlined": page.get_by_text("Outlined Card", exact=True).locator(".."),
                "interactive": page.get_by_text("Interactive Card", exact=True).locator(".."),
            }

            shadows = {
                name: locator.evaluate("element => getComputedStyle(element).boxShadow")
                for name, locator in cards.items()
            }

            print("=== CARD SHADOW CONTRACT ===")
            for name, shadow in shadows.items():
                print(f"{name.upper()} SHADOW: {shadow}")

            assert shadows["default"] == "none"
            assert shadows["elevated"] != "none"
            assert shadows["outlined"] == "none"
            assert shadows["interactive"] == "none"

            browser.close()
    finally:
        runtime.stop()
