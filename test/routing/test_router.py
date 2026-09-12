from pathlib import Path

import pytest

from pylage.ENGINE.routing import Route, Router


def make_pages(tmp_path: Path) -> Path:
    pages = tmp_path / "pages"
    (pages / "settings").mkdir(parents=True)

    (pages / "index.py").write_text("PAGE = True", encoding="utf-8")
    (pages / "dashboard.py").write_text("PAGE = True", encoding="utf-8")
    (pages / "analytics.py").write_text("PAGE = True", encoding="utf-8")
    (pages / "settings" / "index.py").write_text("PAGE = True", encoding="utf-8")
    (pages / "settings" / "profile.py").write_text("PAGE = True", encoding="utf-8")
    (pages / "_private.py").write_text("PAGE = False", encoding="utf-8")

    return pages


def test_router_scans_pages_at_startup(tmp_path):
    pages = make_pages(tmp_path)

    router = Router(pages)

    assert router.routes == (
        Route("/", pages.resolve() / "index.py"),
        Route("/analytics", pages.resolve() / "analytics.py"),
        Route("/dashboard", pages.resolve() / "dashboard.py"),
        Route("/settings", pages.resolve() / "settings" / "index.py"),
        Route("/settings/profile", pages.resolve() / "settings" / "profile.py"),
    )


def test_router_resolves_static_routes(tmp_path):
    pages = make_pages(tmp_path)
    router = Router(pages)

    assert router.resolve("/") == router.routes[0]
    assert router.resolve("/dashboard") == router.routes[2]
    assert router.resolve("/dashboard/") == router.routes[2]
    assert router.resolve("dashboard") == router.routes[2]
    assert router.resolve("/missing") is None


def test_router_does_not_rescan_after_startup(tmp_path, monkeypatch):
    pages = make_pages(tmp_path)
    router = Router(pages)

    (pages / "reports.py").write_text("PAGE = True", encoding="utf-8")

    assert router.resolve("/reports") is None
    assert all(route.path != "/reports" for route in router.routes)

    monkeypatch.setattr(Path, "rglob", lambda *args, **kwargs: pytest.fail("filesystem rescan"))

    assert router.resolve("/dashboard") is not None
    assert router.resolve("/reports") is None


def test_router_requires_existing_pages_directory(tmp_path):
    with pytest.raises(
        ValueError,
        match="PyLage pages directory does not exist",
    ):
        Router(tmp_path / "missing")


def test_router_ignores_private_modules(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / "_helpers.py").write_text("HELPER = True", encoding="utf-8")
    (pages / "index.py").write_text("PAGE = True", encoding="utf-8")

    router = Router(pages)

    assert router.routes == (
        Route("/", pages.resolve() / "index.py"),
    )
