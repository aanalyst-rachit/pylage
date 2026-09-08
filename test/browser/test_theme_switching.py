from playwright.sync_api import expect, sync_playwright

from pylage.ENGINE import Column, Heading
from pylage.ENGINE.runtime.runtime import Runtime
from pylage.ENGINE.styling.global_theme import set_global_theme
from pylage.UI.themes.dark import DARK_THEME
from pylage.UI.themes.light import LIGHT_THEME


def test_python_theme_switch_updates_browser():
    set_global_theme(LIGHT_THEME)

    app = Column(
        Heading(text='Theme Test'),
    )

    runtime = Runtime(
        app,
        title='PyLage Theme Switching',
        output='test_output/browser_theme_switching/index.html',
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            theme_style = page.locator('style[data-pylage-theme="true"]')
            expect(theme_style).to_have_count(1)

            light_css = LIGHT_THEME.to_css()
            dark_css = DARK_THEME.to_css()

            assert light_css in theme_style.evaluate("element => element.textContent")
            assert dark_css not in theme_style.evaluate("element => element.textContent")

            set_global_theme(DARK_THEME)

            page.wait_for_timeout(100)
            dark_browser_css = theme_style.evaluate("element => element.textContent")
            assert dark_css in dark_browser_css
            assert light_css not in dark_browser_css

            set_global_theme(LIGHT_THEME)

            page.wait_for_timeout(100)
            light_browser_css = theme_style.evaluate("element => element.textContent")
            assert light_css in light_browser_css
            assert dark_css not in light_browser_css

            browser.close()
    finally:
        runtime.stop()
        set_global_theme(LIGHT_THEME)
