from pylage import UI as pl
from pylage.ENGINE.runtime.runtime import Runtime
from pylage.ENGINE.styling.global_theme import set_global_theme
from pylage.UI.themes.dark import DARK_THEME
from pylage.UI.themes.light import LIGHT_THEME
from playwright.sync_api import expect, sync_playwright


def test_theme_visual_consistency_updates_computed_styles():
    set_global_theme(LIGHT_THEME)

    app = pl.column(
        pl.card(
            pl.heading("Theme Card", level=3),
            pl.text("Theme consistency test"),
        ),
        pl.table(
            [[1, "Alpha"], [2, "Beta"]],
            headers=["ID", "Name"],
        ),
    )

    runtime = Runtime(
        app,
        title="PyLage Theme Visual Consistency",
        output="test_output/browser_theme_visual_consistency/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            theme_style = page.locator('style[data-pylage-theme="true"]')
            expect(theme_style).to_have_count(1)

            card = page.locator('h1', has_text='Theme Card').locator('..')
            table_cell = page.locator("table tbody td").first
            table_header = page.locator("table thead th").first

            light_card_bg = card.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )
            light_cell_bg = table_cell.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )
            light_header_bg = table_header.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )

            set_global_theme(DARK_THEME)
            page.wait_for_timeout(100)

            dark_card_bg = card.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )
            dark_cell_bg = table_cell.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )
            dark_header_bg = table_header.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )

            assert dark_card_bg != light_card_bg
            assert dark_cell_bg != light_cell_bg
            assert dark_header_bg != light_header_bg

            dark_css = DARK_THEME.to_css()
            browser_theme_css = theme_style.evaluate(
                "element => element.textContent"
            )
            assert dark_css in browser_theme_css

            set_global_theme(LIGHT_THEME)
            page.wait_for_timeout(100)

            restored_card_bg = card.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )
            restored_cell_bg = table_cell.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )
            restored_header_bg = table_header.evaluate(
                "element => getComputedStyle(element).backgroundColor"
            )

            assert restored_card_bg == light_card_bg
            assert restored_cell_bg == light_cell_bg
            assert restored_header_bg == light_header_bg

            browser.close()
    finally:
        runtime.stop()
        set_global_theme(LIGHT_THEME)
