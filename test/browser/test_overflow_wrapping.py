import pylage as pl
from pylage.ENGINE.runtime.runtime import Runtime
from playwright.sync_api import sync_playwright


def test_overflow_and_text_wrapping_browser_contract():
    app = pl.column(
        pl.card(
            heading="Overflow Contract",
            body="A very long unbroken value for overflow verification",
            style=pl.style(
                overflow="auto",
                overflow_x="scroll",
                overflow_y="hidden",
                text_overflow="ellipsis",
                white_space="nowrap",
            ),
        ),
        pl.card(
            heading="Wrapping Contract",
            body="SuperLongUnbrokenContentThatNeedsWrapping",
            style=pl.style(
                width="240px",
                word_break="break-word",
                overflow_wrap="anywhere",
                hyphens="auto",
            ),
        ),
    )

    runtime = Runtime(
        app,
        title="PyLage Overflow Wrapping Contract",
        output="test_output/browser_overflow_wrapping_contract/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(url)

            overflow = page.get_by_text("Overflow Contract", exact=True).locator("..")
            wrapping = page.get_by_text("Wrapping Contract", exact=True).locator("..")

            overflow_values = overflow.evaluate("element => { const s = getComputedStyle(element); return { overflow: s.overflow, overflowX: s.overflowX, overflowY: s.overflowY, textOverflow: s.textOverflow, whiteSpace: s.whiteSpace }; }")
            wrapping_values = wrapping.evaluate("element => { const s = getComputedStyle(element); return { width: s.width, wordBreak: s.wordBreak, overflowWrap: s.overflowWrap, hyphens: s.hyphens }; }")

            print("=== OVERFLOW WRAPPING CONTRACT ===")
            print(f"OVERFLOW: {overflow_values}")
            print(f"WRAPPING: {wrapping_values}")

            assert overflow_values["overflow"] == "scroll hidden"
            assert overflow_values["overflowX"] == "scroll"
            assert overflow_values["overflowY"] == "hidden"
            assert overflow_values["textOverflow"] == "ellipsis"
            assert overflow_values["whiteSpace"] == "nowrap"

            assert wrapping_values["width"] == "240px"
            assert wrapping_values["wordBreak"] == "break-word"
            assert wrapping_values["overflowWrap"] == "anywhere"
            assert wrapping_values["hyphens"] == "auto"

            browser.close()
    finally:
        runtime.stop()
