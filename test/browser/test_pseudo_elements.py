from playwright.sync_api import sync_playwright
from pylage.ENGINE import ResponsiveStyle

import pylage as pl
from pylage.ENGINE.runtime import Runtime


def test_pseudo_elements_render_and_apply_in_browser():
    app = pl.text(
        "Pseudo",
        style=pl.style(
            pseudo={
                "before": pl.style(content='\"B\"', color="rgb(255, 0, 0)"),
                "after": pl.style(content='\"A\"', color="rgb(0, 0, 255)"),
            },
        ),
    )

    runtime = Runtime(
        app,
        title="PyLage Pseudo Element Regression",
        output="test_output/pseudo_elements/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(200)

            element = page.locator('[data-pylage-id]').first

            before = element.evaluate(
                'el => ({content: getComputedStyle(el, "::before").content, color: getComputedStyle(el, "::before").color})'
            )
            after = element.evaluate(
                'el => ({content: getComputedStyle(el, "::after").content, color: getComputedStyle(el, "::after").color})'
            )

            assert before["content"] == '"B"'
            assert before["color"] == "rgb(255, 0, 0)"
            assert after["content"] == '"A"'
            assert after["color"] == "rgb(0, 0, 255)"

            browser.close()

    finally:
        runtime.stop()

def test_responsive_pseudo_elements_change_at_breakpoint():
    app = pl.column(
        pl.text("Responsive Pseudo"),
        style=ResponsiveStyle(
            base=pl.style(
                pseudo={"before": pl.style(content='"B"', color="rgb(255, 0, 0)")},
            ),
            md=pl.style(
                pseudo={"before": pl.style(content='"M"', color="rgb(0, 128, 0)")},
            ),
        ),
    )

    runtime = Runtime(
        app,
        title="PyLage Responsive Pseudo Regression",
        output="test_output/responsive_pseudo_elements/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            small = browser.new_page(viewport={"width": 700, "height": 720})
            small.goto(url, wait_until="domcontentloaded")
            small.wait_for_timeout(200)

            element = small.locator('[data-pylage-id]').first
            before_small = element.evaluate(
                'el => ({content: getComputedStyle(el, "::before").content, color: getComputedStyle(el, "::before").color})'
            )

            assert before_small["content"] == '"B"'
            assert before_small["color"] == "rgb(255, 0, 0)"

            large = browser.new_page(viewport={"width": 1000, "height": 720})
            large.goto(url, wait_until="domcontentloaded")
            large.wait_for_timeout(200)

            element_large = large.locator('[data-pylage-id]').first
            before_large = element_large.evaluate(
                'el => ({content: getComputedStyle(el, "::before").content, color: getComputedStyle(el, "::before").color})'
            )

            assert before_large["content"] == '"M"'
            assert before_large["color"] == "rgb(0, 128, 0)"
            assert before_large["content"] != before_small["content"]

            browser.close()

    finally:
        runtime.stop()
