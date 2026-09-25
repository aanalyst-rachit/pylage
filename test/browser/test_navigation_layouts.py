from pathlib import Path

from playwright.sync_api import expect, sync_playwright

import pylage as pl
from pylage.ENGINE.routing import Router, RoutingRuntime
from pylage.ENGINE.runtime import Runtime


def test_navigation_items_work_inside_layouts(tmp_path: Path):
    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.text("Home Page")
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
    content = pl.column()

    routing = RoutingRuntime(
        Router(pages),
        root,
        content_root=content,
    )

    dashboard_item = pl.navigation_item(
        "Dashboard",
        href="/dashboard",
        current_path=routing.current_path_state,
    )
    analytics_item = pl.navigation_item(
        "Analytics",
        href="/analytics",
        current_path=routing.current_path_state,
    )

    navbar = pl.navbar(
        dashboard_item,
        analytics_item,
    )

    sidebar = pl.sidebar_layout(
        sidebar=pl.navigation(
            pl.navigation_item(
                "Dashboard",
                href="/dashboard",
                current_path=routing.current_path_state,
            ),
            pl.navigation_item(
                "Analytics",
                href="/analytics",
                current_path=routing.current_path_state,
            ),
        ),
    )

    drawer = pl.drawer(
        pl.navigation_item(
            "Dashboard",
            href="/dashboard",
            current_path=routing.current_path_state,
        ),
        pl.navigation_item(
            "Analytics",
            href="/analytics",
            current_path=routing.current_path_state,
        ),
        open=True,
        title="Navigation Drawer",
    )

    root.set_children(
        navbar,
        sidebar,
        drawer,
        content,
    )

    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Navigation Layout Integration Test",
        output="test_output/navigation_layouts/index.html",
        navigation_handler=routing.navigate,
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = runtime.start()

            page.goto(url, wait_until="domcontentloaded")

            expect(
                page.get_by_role("link", name="Dashboard").first
            ).to_be_visible()
            expect(
                page.get_by_role("link", name="Analytics").first
            ).to_be_visible()
            expect(
                page.get_by_text("Home Page", exact=True)
            ).to_be_visible()

            analytics_link = page.locator(
                f'aside[data-pylage-id="{drawer.id}"]'
            ).get_by_role("link", name="Analytics")

            analytics_link.click()

            expect(
                page.get_by_text("Analytics Page", exact=True)
            ).to_be_visible()
            expect(
                page.get_by_text("Home Page", exact=True)
            ).not_to_be_visible()
            assert page.url.endswith("/analytics")

            assert (
                analytics_link.evaluate(
                    "el => getComputedStyle(el).backgroundColor"
                )
                == "rgb(37, 99, 235)"
            )

            expect(
                page.get_by_role("link", name="Analytics").first
            ).to_be_visible()

            dashboard_link = page.locator(
                f'aside[data-pylage-id="{drawer.id}"]'
            ).get_by_role("link", name="Dashboard")

            dashboard_link.click()

            expect(
                page.get_by_text("Dashboard Page", exact=True)
            ).to_be_visible()
            expect(
                page.get_by_text("Analytics Page", exact=True)
            ).not_to_be_visible()
            assert page.url.endswith("/dashboard")

            assert (
                dashboard_link.evaluate(
                    "el => getComputedStyle(el).backgroundColor"
                )
                == "rgb(37, 99, 235)"
            )

            browser.close()
    finally:
        runtime.stop()


def test_navigation_drawer_and_mobile_sidebar_preserve_routed_shell(
    tmp_path: Path,
):
    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "index.py").write_text(
        """import pylage as pl

def page():
    return pl.text("Home Page")
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
    content = pl.column()

    routing = RoutingRuntime(
        Router(pages),
        root,
        content_root=content,
    )

    navigation = pl.navigation(
        pl.navigation_item(
            "Analytics",
            href="/analytics",
            current_path=routing.current_path_state,
        ),
    )

    navigation_drawer = pl.navigation_drawer(
        navigation,
        open=True,
        title="Navigation Drawer",
    )

    mobile_sidebar = pl.mobile_sidebar(
        pl.navigation_item(
            "Analytics",
            href="/analytics",
            current_path=routing.current_path_state,
        ),
        open=False,
        title="Mobile Sidebar",
    )

    root.set_children(
        navigation_drawer,
        mobile_sidebar,
        content,
    )

    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Navigation Drawer Integration Test",
        output="test_output/navigation_layouts/drawer/index.html",
        navigation_handler=routing.navigate,
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = runtime.start()

            page.goto(url, wait_until="domcontentloaded")

            expect(
                page.get_by_role("link", name="Analytics").first
            ).to_be_visible()

            navigation_drawer = page.locator(
                'aside[title="Navigation Drawer"]'
            )

            navigation_drawer.get_by_role(
                "link", name="Analytics"
            ).click()

            expect(
                page.get_by_text("Analytics Page", exact=True)
            ).to_be_visible()
            expect(
                page.get_by_text("Home Page", exact=True)
            ).not_to_be_visible()

            assert page.url.endswith("/analytics")

            expect(
                page.get_by_role("link", name="Analytics").first
            ).to_be_visible()

            browser.close()
    finally:
        runtime.stop()


def test_routed_breadcrumbs_update_with_navigation(tmp_path: Path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()

    (pages_dir / "index.py").write_text(
        "import pylage as pl\n"
        "def page():\n"
        "    return pl.text('Home Page')\n",
        encoding="utf-8",
    )

    dashboard_dir = pages_dir / "dashboard"
    dashboard_dir.mkdir()

    (dashboard_dir / "index.py").write_text(
        "import pylage as pl\n"
        "def page():\n"
        "    return pl.text('Dashboard Page')\n",
        encoding="utf-8",
    )

    reports_dir = dashboard_dir / "reports"
    reports_dir.mkdir()

    (reports_dir / "index.py").write_text(
        "import pylage as pl\n"
        "def page():\n"
        "    return pl.text('Reports Page')\n",
        encoding="utf-8",
    )

    router = Router(pages_dir)

    root = pl.column()
    content = pl.column()

    routing = RoutingRuntime(
        router,
        root,
        content_root=content,
    )

    breadcrumbs = pl.breadcrumb_trail(
        current_path=routing.current_path_state,
    )

    navigation = pl.navigation(
        pl.navigation_item("Dashboard", href="/dashboard"),
    )

    root.set_children(
        navigation,
        breadcrumbs,
        content,
    )

    runtime = Runtime(
        root,
        title="Breadcrumb Test",
        host="127.0.0.1",
        port=8765,
        navigation_handler=routing.navigate,
    )

    routing.navigate("/")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            runtime.start()

            page.goto(
                "http://127.0.0.1:8765/",
                wait_until="domcontentloaded",
            )

            expect(
                page.get_by_text("Home Page", exact=True)
            ).to_be_visible()

            page.get_by_role(
                "link", name="Dashboard"
            ).click()

            page.wait_for_url("**/dashboard")

            expect(
                page.get_by_text("Dashboard Page", exact=True)
            ).to_be_visible()

            expect(
                page.get_by_role("link", name="Home")
            ).to_be_visible()

            expect(
                page.get_by_label("Breadcrumb").get_by_text(
                    "Dashboard",
                    exact=True,
                )
            ).to_be_visible()

            browser.close()
    finally:
        runtime.stop()
