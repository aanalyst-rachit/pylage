from playwright.sync_api import sync_playwright

import pylage as pl
from pylage.ENGINE.runtime import Runtime


def test_button_hover_uses_semantic_theme_tokens():
    pl.set_theme('dark')

    app = pl.column(
        pl.button('Primary', variant='primary'),
        pl.button('Secondary', variant='secondary'),
    )

    runtime = Runtime(
        app,
        title='PyLage Button Hover Regression',
        output='test_output/button_hover/index.html',
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until='domcontentloaded')
            page.wait_for_timeout(200)

            buttons = page.locator('button')
            assert buttons.count() == 2

            primary = buttons.nth(0)
            secondary = buttons.nth(1)

            primary_normal = primary.evaluate(
                'el => getComputedStyle(el).backgroundColor'
            )
            secondary_normal = secondary.evaluate(
                'el => getComputedStyle(el).backgroundColor'
            )

            primary.hover()
            page.wait_for_timeout(100)
            primary_hover = primary.evaluate(
                'el => getComputedStyle(el).backgroundColor'
            )

            secondary.hover()
            page.wait_for_timeout(100)
            secondary_hover = secondary.evaluate(
                'el => getComputedStyle(el).backgroundColor'
            )

            assert primary_normal == 'rgb(96, 165, 250)'
            assert primary_hover == 'rgb(59, 130, 246)'
            assert primary_hover != primary_normal

            assert secondary_normal == 'rgb(148, 163, 184)'
            assert secondary_hover == 'rgb(100, 116, 139)'
            assert secondary_hover != secondary_normal

            browser.close()

    finally:
        runtime.stop()
        pl.set_theme('light')
