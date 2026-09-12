from pathlib import Path

import pytest

import pylage as pl
from pylage.ENGINE.routing import Router


def write_page(pages: Path, name: str, source: str) -> Path:
    path = pages / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def test_page_module_exposes_callable_page(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()

    write_page(
        pages,
        "dashboard.py",
        "import pylage as pl\n\ndef page():\n    return pl.text(\"Dashboard\")\n",
    )

    router = Router(pages)
    route = router.resolve("/dashboard")

    assert route is not None

    page = router.load_page(route)

    assert callable(page)

    result = page()
    assert router.validate_page_result(result, route) is result


def test_page_module_requires_page_function(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()

    write_page(
        pages,
        "dashboard.py",
        "import pylage as pl\napp = pl.text(\"Dashboard\")\n",
    )

    router = Router(pages)
    route = router.resolve("/dashboard")

    assert route is not None

    with pytest.raises(
        TypeError,
        match=r"must define page\(\.\.\.\)",
    ):
        router.load_page(route)


def test_page_symbol_must_be_callable(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()

    write_page(
        pages,
        "dashboard.py",
        "page = \"not-callable\"\n",
    )

    router = Router(pages)
    route = router.resolve("/dashboard")

    assert route is not None

    with pytest.raises(
        TypeError,
        match="page must be callable",
    ):
        router.load_page(route)


def test_page_must_return_component(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()

    write_page(
        pages,
        "dashboard.py",
        "def page():\n    return \"not-a-component\"\n",
    )

    router = Router(pages)
    route = router.resolve("/dashboard")

    assert route is not None
    page = router.load_page(route)

    with pytest.raises(
        TypeError,
        match="Page /dashboard must return a Component",
    ):
        router.validate_page_result(page(), route)


def test_bare_top_level_component_is_not_a_page(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()

    write_page(
        pages,
        "dashboard.py",
        "import pylage as pl\napp = pl.column(pl.text(\"Dashboard\"))\n",
    )

    router = Router(pages)
    route = router.resolve("/dashboard")

    assert route is not None

    with pytest.raises(TypeError):
        router.load_page(route)
