from pathlib import Path

from pylage.ENGINE.routing import Route, Router


def write_page(pages: Path, name: str, source: str = "def page(**params):\n    return params\n") -> Path:
    path = pages / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def test_router_discovers_dynamic_route(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    source = write_page(pages, "dashboard/[user_id].py")

    router = Router(pages)

    assert router.routes == (
        Route("/dashboard/:user_id", source.resolve()),
    )


def test_router_resolves_dynamic_route_and_extracts_params(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(pages, "dashboard/[user_id].py")

    router = Router(pages)

    result = router.resolve("/dashboard/42")

    assert result is not None
    route, params = result
    assert route.path == "/dashboard/:user_id"
    assert params == {"user_id": "42"}


def test_dynamic_route_does_not_match_missing_segment(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(pages, "dashboard/[user_id].py")

    router = Router(pages)

    assert router.resolve("/dashboard") is None


def test_dynamic_route_does_not_match_extra_segment(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(pages, "dashboard/[user_id].py")

    router = Router(pages)

    assert router.resolve("/dashboard/42/profile") is None


def test_static_route_takes_precedence_over_dynamic_route(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    static_source = write_page(pages, "dashboard/settings.py")
    write_page(pages, "dashboard/[user_id].py")

    router = Router(pages)

    result = router.resolve("/dashboard/settings")

    assert result is not None
    assert result.source == static_source.resolve()


def test_dynamic_route_value_is_passed_to_page(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(
        pages,
        "dashboard/[user_id].py",
        "def page(**params):\n    return params[\"user_id\"]\n",
    )

    router = Router(pages)
    route, params = router.resolve("/dashboard/42")
    page = router.load_page(route)

    assert page(**params) == "42"
