from playwright.sync_api import sync_playwright, expect

from pylage.ENGINE.runtime import Runtime
from working_demo.app import get_app


def test_phase18_working_demo_navigation_and_interactions():
    app = get_app()

    runtime = Runtime(
        app,
        title="PyLage UI Kit Phase 18 Working Demo",
        output="test_output/phase18_working_demo/index.html",
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(300)

            assert page.locator("[data-pylage-id]").count() > 0
            assert page.evaluate("() => !!window.PyLage")

            expect(page.get_by_text("PyLage UI Kit", exact=True).first).to_be_visible()
            expect(page.get_by_text("Phase 18 — Example Application", exact=True)).to_be_visible()

            nav_names = [
                "Dashboard",
                "Analytics",
                "Forms",
                "Tables",
                "Navigation",
                "Overlays",
                "Components",
                "Themes",
            ]

            for name in nav_names:
                expect(page.get_by_text(name, exact=True).first).to_be_visible()

            expect(page.get_by_text("Executive Operations Control", exact=True)).to_be_visible()
            expect(page.get_by_text("Global Revenue", exact=True)).to_be_visible()

            page.get_by_text("Analytics", exact=True).first.click()
            expect(page.get_by_text("Platform performance, growth and operational trends.", exact=True)).to_be_visible()
            expect(page.get_by_text("Requests / sec", exact=True)).to_be_visible()

            page.get_by_text("Forms", exact=True).first.click()
            expect(page.get_by_text("Manage workspace and account information.", exact=True)).to_be_visible()
            expect(page.locator("input[name=\"email\"]")).to_have_value("racit@example.com")

            page.get_by_text("Save Changes", exact=True).click()
            expect(page.get_by_text("Latest submission:", exact=True)).to_be_visible()

            page.get_by_text("Tables", exact=True).first.click()
            expect(page.get_by_text("Operational clusters and service status.", exact=True)).to_be_visible()
            expect(page.get_by_text("Alpha", exact=True)).to_be_visible()
            expect(page.get_by_text("Mumbai", exact=True)).to_be_visible()
            expect(page.get_by_text("Current page:", exact=True)).to_be_visible()

            page.get_by_text("Navigation", exact=True).first.click()
            expect(page.get_by_text("Workspace Navigation", exact=True)).to_be_visible()
            expect(page.get_by_text("Overview", exact=True)).to_be_visible()

            page.get_by_text("Overlays", exact=True).first.click()
            expect(page.get_by_text("Drawer, modal and toast interaction examples.", exact=True)).to_be_visible()

            page.get_by_text("Open Drawer", exact=True).click()
            expect(page.get_by_text("Close Drawer", exact=True)).to_be_visible()
            page.get_by_text("Close Drawer", exact=True).click()

            page.get_by_text("Open Modal", exact=True).click()
            expect(page.get_by_text("Confirm this application action?", exact=True)).to_be_visible()
            page.get_by_text("Confirm", exact=True).click()

            page.get_by_text("Show Toast", exact=True).click()
            expect(page.get_by_text("Action completed successfully.", exact=True)).to_be_visible()

            page.get_by_text("Components", exact=True).first.click()
            expect(page.get_by_text("Reusable UI Kit primitives composed into product surfaces.", exact=True)).to_be_visible()
            expect(page.get_by_text("Production", exact=True)).to_be_visible()
            expect(page.get_by_text("Scheduled maintenance tonight.", exact=True)).to_be_visible()

            page.get_by_text("Themes", exact=True).first.click()
            expect(page.get_by_text("Use the public PyLage theme API to switch application appearance.", exact=True)).to_be_visible()
            expect(page.get_by_text("Theme Controls", exact=True)).to_be_visible()

            browser.close()

    finally:
        runtime.stop()
