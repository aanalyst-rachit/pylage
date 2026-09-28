from pathlib import Path

from playwright.sync_api import expect, sync_playwright

import pylage as pl
from pylage.ENGINE.routing import Router, RoutingRuntime
from pylage.ENGINE.runtime import Runtime


def test_link_click_navigates_internal_route(tmp_path: Path):
    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "index.py").write_text(
        '''import pylage as pl

def page():
    return pl.column(
        pl.link("Dashboard", href="/dashboard"),
        pl.text("Home Page"),
    )
''',
        encoding="utf-8",
    )

    (pages / "dashboard.py").write_text(
        '''import pylage as pl

def page():
    return pl.text("Dashboard Page")
''',
        encoding="utf-8",
    )

    root = pl.column()
    routing = RoutingRuntime(Router(pages), root)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Link Navigation Test",
        output="test_output/link_navigation/index.html",
        navigation_handler=routing.navigate,
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            expect(
                page.get_by_role("link", name="Dashboard")
            ).to_be_visible()
            expect(
                page.get_by_text("Home Page", exact=True)
            ).to_be_visible()

            page.get_by_role("link", name="Dashboard").click()

            expect(
                page.get_by_text("Dashboard Page", exact=True)
            ).to_be_visible()
            expect(
                page.get_by_text("Home Page", exact=True)
            ).not_to_be_visible()

            assert page.url.endswith("/dashboard")

            browser.close()
    finally:
        runtime.stop()


def test_link_failed_navigation_rolls_back_url_and_ui(tmp_path: Path):
    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.column(
        pl.link("Missing", href="/missing"),
        pl.text("Home Page"),
    )
""",
        encoding="utf-8",
    )

    root = pl.column()
    routing = RoutingRuntime(Router(pages), root)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Failed Navigation Test",
        output="test_output/link_navigation/failure.html",
        navigation_handler=routing.navigate,
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            expect(
                page.get_by_text("Home Page", exact=True)
            ).to_be_visible()

            page.get_by_role("link", name="Missing").click()

            expect(
                page.get_by_text("Home Page", exact=True)
            ).to_be_visible()

            expect(page).to_have_url(url)

            browser.close()
    finally:
        runtime.stop()


def test_link_navigates_nested_and_dynamic_routes(tmp_path: Path):
    pages = tmp_path / "pages"
    (pages / "reports").mkdir(parents=True)
    (pages / "users").mkdir(parents=True)

    (pages / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.column(
        pl.link("Reports", href="/reports"),
        pl.link("User 42", href="/users/42"),
        pl.text("Home Page"),
    )
""",
        encoding="utf-8",
    )

    (pages / "reports" / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.text("Reports Page")
""",
        encoding="utf-8",
    )

    (pages / "users" / "[user_id].py").write_text(
        """import pylage as pl

def page(user_id):
    return pl.text(f"User Page: {user_id}")
""",
        encoding="utf-8",
    )

    root = pl.column()
    routing = RoutingRuntime(Router(pages), root)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Link Route Integration Test",
        output="test_output/link_navigation/routes.html",
        navigation_handler=routing.navigate,
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            page.get_by_role("link", name="Reports").click()

            expect(
                page.get_by_text("Reports Page", exact=True)
            ).to_be_visible()
            assert page.url.endswith("/reports")

            page.goto(url, wait_until="domcontentloaded")

            page.get_by_role("link", name="User 42").click()

            expect(
                page.get_by_text("User Page: 42", exact=True)
            ).to_be_visible()
            assert page.url.endswith("/users/42")

            browser.close()
    finally:
        runtime.stop()


def test_external_link_uses_normal_browser_navigation(tmp_path: Path):
    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.link(
        "External",
        href="https://example.com/external",
    )
""",
        encoding="utf-8",
    )

    root = pl.column()
    routing = RoutingRuntime(Router(pages), root)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage External Link Test",
        output="test_output/link_navigation/external.html",
        navigation_handler=routing.navigate,
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            link = page.get_by_role("link", name="External")
            expect(link).to_be_visible()

            assert link.get_attribute("href") == "https://example.com/external"

            with page.expect_navigation():
                link.click()

            assert page.url == "https://example.com/external"

            browser.close()
    finally:
        runtime.stop()


def test_navigation_item_navigates_dynamic_route(tmp_path: Path):
    pages = tmp_path / "pages"
    (pages / "users").mkdir(parents=True)

    (pages / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.navigation_item(
        "User 42",
        href="/users/42",
    )
""",
        encoding="utf-8",
    )

    (pages / "users" / "[user_id].py").write_text(
        """import pylage as pl

def page(user_id):
    return pl.text(f"User Page: {user_id}")
""",
        encoding="utf-8",
    )

    root = pl.column()
    routing = RoutingRuntime(Router(pages), root)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage NavigationItem Dynamic Route Test",
        output="test_output/link_navigation/navigation_item_dynamic.html",
        navigation_handler=routing.navigate,
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            expect(
                page.get_by_role("link", name="User 42")
            ).to_be_visible()

            page.get_by_role("link", name="User 42").click()

            expect(
                page.get_by_text("User Page: 42", exact=True)
            ).to_be_visible()

            assert page.url.endswith("/users/42")

            browser.close()
    finally:
        runtime.stop()


def test_browser_back_and_forward_restore_routed_pages(tmp_path: Path):
    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.link("Dashboard", href="/dashboard")
""",
        encoding="utf-8",
    )

    (pages / "dashboard.py").write_text(
        """import pylage as pl

def page():
    return pl.text("Dashboard Page")
""",
        encoding="utf-8",
    )

    root = pl.column()
    routing = RoutingRuntime(Router(pages), root)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Browser History Navigation Test",
        output="test_output/link_navigation/browser_history.html",
        navigation_handler=routing.navigate,
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            expect(
                page.get_by_role("link", name="Dashboard")
            ).to_be_visible()

            page.get_by_role("link", name="Dashboard").click()

            page.wait_for_url("**/dashboard")

            expect(
                page.get_by_text("Dashboard Page", exact=True)
            ).to_be_visible()
            assert page.url.endswith("/dashboard")

            page.go_back()
            page.wait_for_url("**/")

            expect(
                page.get_by_role("link", name="Dashboard")
            ).to_be_visible()
            assert page.url.endswith("/")

            page.go_forward()
            page.wait_for_url("**/dashboard")

            expect(
                page.get_by_text("Dashboard Page", exact=True)
            ).to_be_visible()
            assert page.url.endswith("/dashboard")

            browser.close()
    finally:
        runtime.stop()


def test_replace_navigation_replaces_browser_history_entry(tmp_path: Path):
    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.column(
        pl.link("Dashboard", href="/dashboard"),
        pl.link("Analytics", href="/analytics"),
        pl.text("Home Page"),
    )
""",
        encoding="utf-8",
    )

    (pages / "dashboard.py").write_text(
        """import pylage as pl

def page():
    return pl.text("Dashboard Page")
""",
        encoding="utf-8",
    )

    (pages / "analytics.py").write_text(
        """import pylage as pl

def page():
    return pl.text("Analytics Page")
""",
        encoding="utf-8",
    )

    root = pl.column()
    routing = RoutingRuntime(Router(pages), root)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Replace Navigation Test",
        output="test_output/link_navigation/replace.html",
        navigation_handler=routing.navigate,
    )

    try:
        url = runtime.start()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")

            page.get_by_role("link", name="Dashboard").click()
            page.wait_for_url("**/dashboard")

            expect(
                page.get_by_text("Dashboard Page", exact=True)
            ).to_be_visible()

            page.evaluate(
                'window.PyLage.navigate("/analytics", {replace: true})'
            )
            page.wait_for_url("**/analytics")

            expect(
                page.get_by_text("Analytics Page", exact=True)
            ).to_be_visible()
            assert page.url.endswith("/analytics")

            page.go_back()
            page.wait_for_url("**/")

            expect(
                page.get_by_text("Home Page", exact=True)
            ).to_be_visible()

            expect(
                page.get_by_text("Analytics Page", exact=True)
            ).not_to_be_visible()

            assert page.url.endswith("/")

            browser.close()
    finally:
        runtime.stop()
