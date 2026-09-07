from playwright.sync_api import sync_playwright

from pylage import UI as pl
from pylage.ENGINE.runtime.runtime import Runtime


def test_dashboard_header_spacing_probe():
    app = pl.column(
        pl.dashboard_header("Dashboard Title", "Dashboard description"),
        pl.card(heading="Next Section", body="Content"),
    )
    runtime = Runtime(app, title="Dashboard Header Spacing Probe", output="test_output/dashboard_header_spacing_probe/index.html")
    try:
        url = runtime.start()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.goto(url)
            page.wait_for_timeout(100)
            header = page.get_by_text("Dashboard Title", exact=True).locator("xpath=../..")
            card = page.get_by_text("Next Section", exact=True).locator("xpath=..")
            hb = header.bounding_box()
            cb = card.bounding_box()
            parent = header.locator("xpath=..")
            print("=== DASHBOARD HEADER SPACING PROBE ===")
            print("HEADER BOX:", hb)
            print("CARD BOX:", cb)
            print("ACTUAL GAP:", None if hb is None or cb is None else cb["y"] - (hb["y"] + hb["height"]))
            print("HEADER MARGIN TOP:", header.evaluate("el => getComputedStyle(el).marginTop"))
            print("HEADER MARGIN BOTTOM:", header.evaluate("el => getComputedStyle(el).marginBottom"))
            print("HEADER PADDING BOTTOM:", header.evaluate("el => getComputedStyle(el).paddingBottom"))
            print("HEADER BORDER BOTTOM:", header.evaluate("el => getComputedStyle(el).borderBottomWidth"))
            print("HEADER TAG:", header.evaluate("el => el.tagName"))
            print("HEADER HTML:", header.evaluate("el => el.outerHTML"))
            print("CARD TAG:", card.evaluate("el => el.tagName"))
            print("CARD HTML:", card.evaluate("el => el.outerHTML"))
            print("CARD PARENT TAG:", card.locator("xpath=..").evaluate("el => el.tagName"))
            print("CARD PARENT HTML:", card.locator("xpath=..").evaluate("el => el.outerHTML"))
            print("PARENT TAG:", parent.evaluate("el => el.tagName"))
            print("PARENT HTML:", parent.evaluate("el => el.outerHTML"))
            print("PARENT DISPLAY:", parent.evaluate("el => getComputedStyle(el).display"))
            print("PARENT FLEX DIRECTION:", parent.evaluate("el => getComputedStyle(el).flexDirection"))
            print("PARENT GAP:", parent.evaluate("el => getComputedStyle(el).gap"))
            print("PARENT ROW GAP:", parent.evaluate("el => getComputedStyle(el).rowGap"))
            print("PARENT COLUMN GAP:", parent.evaluate("el => getComputedStyle(el).columnGap"))
            browser.close()
    finally:
        runtime.stop()
