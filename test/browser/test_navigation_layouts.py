from pathlib import Path

from playwright.sync_api import expect, sync_playwright

import pylage as pl
from pylage.ENGINE.core.state import State
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


def test_navigation_drawer_closes_after_successful_navigation_on_mobile(
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

    open_state = State(True)
    drawer = pl.navigation_drawer(
        pl.navigation_item(
            "Analytics",
            href="/analytics",
            current_path=routing.current_path_state,
        ),
        open=open_state,
        responsive_mode={"base": "overlay", "md": "persistent"},
        title="Navigation Drawer",
    )

    root.set_children(drawer, content)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Navigation Drawer Mobile Close Test",
        output="test_output/navigation_layouts/navigation_drawer_mobile_close.html",
        navigation_handler=routing.navigate,
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 600, "height": 800})
            try:
                url = runtime.start()
                page.goto(url, wait_until="domcontentloaded")

                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )
                expect(drawer_locator).to_have_attribute("open", "")

                drawer_locator.get_by_role(
                    "link", name="Analytics"
                ).click()

                expect(
                    page.get_by_text("Analytics Page", exact=True)
                ).to_be_visible()

                expect(drawer_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                assert open_state.value is False
                assert page.url.endswith("/analytics")
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_navigation_drawer_stays_open_in_persistent_mode(
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

    open_state = State(True)
    drawer = pl.navigation_drawer(
        pl.navigation_item(
            "Analytics",
            href="/analytics",
            current_path=routing.current_path_state,
        ),
        open=open_state,
        responsive_mode={"base": "overlay", "md": "persistent"},
        title="Navigation Drawer",
    )

    root.set_children(drawer, content)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Navigation Drawer Persistent Test",
        output="test_output/navigation_layouts/navigation_drawer_persistent.html",
        navigation_handler=routing.navigate,
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 800, "height": 800})
            try:
                url = runtime.start()
                page.goto(url, wait_until="domcontentloaded")

                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )
                expect(drawer_locator).to_have_attribute("open", "")

                drawer_locator.get_by_role(
                    "link", name="Analytics"
                ).click()

                expect(
                    page.get_by_text("Analytics Page", exact=True)
                ).to_be_visible()
                expect(drawer_locator).to_have_attribute("open", "")
                assert open_state.value is True
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_navigation_drawer_stays_open_when_navigation_fails(
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

    root = pl.column()
    content = pl.column()
    routing = RoutingRuntime(
        Router(pages),
        root,
        content_root=content,
    )

    open_state = State(True)
    drawer = pl.navigation_drawer(
        pl.navigation_item(
            "Missing",
            href="/missing",
            current_path=routing.current_path_state,
        ),
        open=open_state,
        responsive_mode={"base": "overlay", "md": "persistent"},
        title="Navigation Drawer",
    )

    root.set_children(drawer, content)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="PyLage Navigation Drawer Failed Navigation Test",
        output="test_output/navigation_layouts/navigation_drawer_failed_navigation.html",
        navigation_handler=routing.navigate,
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 600, "height": 800})
            try:
                url = runtime.start()
                page.goto(url, wait_until="domcontentloaded")

                drawer_locator = page.locator(
                    f'aside[data-pylage-id="{drawer.id}"]'
                )
                expect(drawer_locator).to_have_attribute("open", "")

                drawer_locator.get_by_role(
                    "link", name="Missing"
                ).click()

                expect(
                    page.get_by_text("Home Page", exact=True)
                ).to_be_visible()
                expect(drawer_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )
                assert open_state.value is True
                assert page.url.endswith("/")
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_mobile_sidebar_mobile_overlay_dismisses_with_backdrop_and_escape():
    open_state = State(True)
    sidebar = pl.mobile_sidebar(
        pl.text("Mobile Sidebar"),
        open=open_state,
        responsive_mode={"base": "overlay", "md": "persistent"},
        title="Mobile Sidebar",
    )

    runtime = Runtime(
        pl.column(sidebar),
        title="Mobile Sidebar Dismiss Browser Test",
        output="test_output/navigation_layouts/mobile_sidebar_dismiss.html",
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 600, "height": 800})
            try:
                url = runtime.start()
                page.goto(url, wait_until="domcontentloaded")

                sidebar_locator = page.locator(
                    f'aside[data-pylage-id="{sidebar.id}"]'
                )
                backdrop = page.locator(".pylage-drawer-backdrop")

                expect(sidebar_locator).to_have_attribute("open", "")
                expect(sidebar_locator).to_have_attribute(
                    "data-pylage-mobile-sidebar",
                    "",
                )
                expect(sidebar_locator).to_have_attribute(
                    "data-pylage-modal",
                    "true",
                )
                expect(backdrop).to_be_visible()

                page.mouse.click(590, 400)

                expect(sidebar_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                assert open_state.value is False

                open_state.set(True)

                expect(sidebar_locator).to_have_attribute(
                    "open",
                    "",
                    timeout=10000,
                )

                page.keyboard.press("Escape")

                expect(sidebar_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                assert open_state.value is False
            finally:
                browser.close()
    finally:
        runtime.stop()


def test_mobile_sidebar_route_change_closes_on_success(tmp_path: Path):
    pages = tmp_path / "pages"
    pages.mkdir()

    (pages / "index.py").write_text(
        "import pylage as pl\n"
        "def page():\n"
        "    return pl.text('Home Page')\n",
        encoding="utf-8",
    )

    (pages / "analytics.py").write_text(
        "import pylage as pl\n"
        "def page():\n"
        "    return pl.text('Analytics Page')\n",
        encoding="utf-8",
    )

    root = pl.column()
    content = pl.column()
    routing = RoutingRuntime(
        Router(pages),
        root,
        content_root=content,
    )

    open_state = State(True)
    sidebar = pl.mobile_sidebar(
        pl.navigation_item(
            "Analytics",
            href="/analytics",
            current_path=routing.current_path_state,
        ),
        open=open_state,
        responsive_mode={"base": "overlay", "md": "persistent"},
        title="Mobile Sidebar",
    )

    root.set_children(sidebar, content)
    routing.navigate("/")

    runtime = Runtime(
        root,
        title="Mobile Sidebar Route Browser Test",
        output="test_output/navigation_layouts/mobile_sidebar_route.html",
        navigation_handler=routing.navigate,
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 600, "height": 800})
            try:
                url = runtime.start()
                page.goto(url, wait_until="domcontentloaded")

                sidebar_locator = page.locator(
                    f'aside[data-pylage-id="{sidebar.id}"]'
                )

                expect(sidebar_locator).to_have_attribute("open", "")

                sidebar_locator.get_by_role(
                    "link",
                    name="Analytics",
                ).click()

                expect(
                    page.get_by_text("Analytics Page", exact=True)
                ).to_be_visible()
                expect(sidebar_locator).not_to_have_attribute(
                    "open",
                    timeout=10000,
                )
                assert open_state.value is False
                assert page.url.endswith("/analytics")
            finally:
                browser.close()
    finally:
        runtime.stop()
