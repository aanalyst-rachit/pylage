from playwright.sync_api import sync_playwright

from pylage import UI as pl
from pylage.ENGINE.runtime.runtime import Runtime
from pylage.ENGINE.styling.global_theme import set_global_theme
from pylage.UI.themes.dark import DARK_THEME
from pylage.UI.themes.light import LIGHT_THEME


def test_theme_root_propagation_probe():
    set_global_theme(LIGHT_THEME)

    app = pl.column(
        pl.navigation_item('Dashboard'),
        pl.heading('Theme Controls', level=2),
        pl.text('Theme propagation test'),
        pl.card(pl.text('Inner Card')),
    )

    runtime = Runtime(
        app,
        title='Theme Root Probe',
        output='test_output/browser_theme_root_probe/index.html',
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            root = page.locator('body')
            column = page.locator('[data-pylage-id]').first
            heading = page.locator('h1')
            card = page.get_by_text('Inner Card').locator('..')

            light_body_bg = root.evaluate("element => getComputedStyle(element).backgroundColor")
            light_body_color = root.evaluate("element => getComputedStyle(element).color")
            light_column_bg = column.evaluate("element => getComputedStyle(element).backgroundColor")
            light_heading_color = heading.evaluate("element => getComputedStyle(element).color")
            light_card_bg = card.evaluate("element => getComputedStyle(element).backgroundColor")

            print('LIGHT BODY BG:', light_body_bg)
            print('LIGHT BODY COLOR:', light_body_color)
            print('LIGHT COLUMN BG:', light_column_bg)
            print('LIGHT HEADING COLOR:', light_heading_color)
            print('LIGHT CARD BG:', light_card_bg)

            set_global_theme(DARK_THEME)
            page.wait_for_timeout(100)

            dark_body_bg = root.evaluate("element => getComputedStyle(element).backgroundColor")
            dark_body_color = root.evaluate("element => getComputedStyle(element).color")
            dark_column_bg = column.evaluate("element => getComputedStyle(element).backgroundColor")
            dark_heading_color = heading.evaluate("element => getComputedStyle(element).color")
            dark_card_bg = card.evaluate("element => getComputedStyle(element).backgroundColor")

            print('DARK BODY BG:', dark_body_bg)
            print('DARK BODY COLOR:', dark_body_color)
            print('DARK COLUMN BG:', dark_column_bg)
            print('DARK HEADING COLOR:', dark_heading_color)
            print('DARK CARD BG:', dark_card_bg)

            assert dark_body_bg != light_body_bg
            assert dark_body_color != light_body_color
            assert dark_card_bg != light_card_bg
            assert dark_heading_color != light_heading_color

            set_global_theme(LIGHT_THEME)
            page.wait_for_timeout(100)

            restored_body_bg = root.evaluate("element => getComputedStyle(element).backgroundColor")
            restored_body_color = root.evaluate("element => getComputedStyle(element).color")

            print('RESTORED BODY BG:', restored_body_bg)
            print('RESTORED BODY COLOR:', restored_body_color)

            assert restored_body_bg == light_body_bg
            assert restored_body_color == light_body_color

            print('THEME ROOT PROPAGATION PROBE: PASS')
            browser.close()
    finally:
        runtime.stop()
        set_global_theme(LIGHT_THEME)
