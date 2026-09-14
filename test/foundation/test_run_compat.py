from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

import pylage as pl


def test_run_public_api_compatibility(tmp_path):
    app = pl.column(
        pl.heading("Compatibility Test"),
        pl.button("Click me"),
    )

    output = pl.run(
        app,
        title="Compatibility Test",
        output=tmp_path / "compat_output" / "index.html",
        open_browser=False,
    )

    assert isinstance(output, Path)
    assert output.exists()

    html = output.read_text(encoding="utf-8")

    assert "<title>Compatibility Test</title>" in html
    assert "Compatibility Test" in html
    assert "Click me" in html


def test_run_app_factory_renders_output(tmp_path):
    def app_factory():
        return pl.column(
            pl.heading("Factory Test"),
            pl.button("Factory Button"),
        )

    output = pl.run(
        app_factory=app_factory,
        title="Factory Test",
        output=tmp_path / "factory_output" / "index.html",
        open_browser=False,
    )

    assert isinstance(output, Path)
    assert output.exists()

    html = output.read_text(encoding="utf-8")
    assert "<title>Factory Test</title>" in html
    assert "Factory Test" in html
    assert "Factory Button" in html


def test_run_app_factory_validation(tmp_path):
    app = pl.column(pl.heading("Validation"))

    def app_factory():
        return pl.column(pl.heading("Factory"))

    try:
        pl.run(app, app_factory=app_factory, output=tmp_path / "invalid.html")
    except TypeError as exc:
        assert "only one of app, app_factory, or pages_dir" in str(exc)
    else:
        raise AssertionError("Expected TypeError for app + app_factory")

    def invalid_factory():
        return "not a component"

    try:
        pl.run(app_factory=invalid_factory, output=tmp_path / "invalid_factory.html")
    except TypeError as exc:
        assert "app_factory must return a Component" in str(exc)
    else:
        raise AssertionError("Expected TypeError for invalid app_factory return")


def test_run_app_factory_uses_embedded_granian(tmp_path):
    def app_factory():
        return pl.column(pl.heading("Served Factory"))

    class FakeRuntime:
        instances: ClassVar[list] = []

        def __init__(self, application, *, host, port):
            self.application = application
            self.host = host
            self.port = port
            self.started = False
            self.stopped = False
            self.__class__.instances.append(self)

        def start(self):
            self.started = True
            return f"http://{self.host}:{self.port}/"

        def stop(self):
            self.stopped = True

    def interrupt(_delay):
        raise KeyboardInterrupt

    output = tmp_path / "served_factory" / "index.html"

    import importlib

    engine_app = importlib.import_module("pylage.ENGINE.app")

    with (
        patch.object(engine_app, "EmbeddedGranianRuntime", FakeRuntime),
        patch.object(engine_app.time, "sleep", side_effect=interrupt),
        patch.object(engine_app.webbrowser, "open") as browser_open,
    ):
        result = pl.run(
            app_factory=app_factory,
            title="Served Factory",
            output=output,
            serve=True,
            host="127.0.0.1",
            port=8123,
            open_browser=True,
        )

    assert result == output
    assert output.exists()
    assert len(FakeRuntime.instances) == 1

    runtime = FakeRuntime.instances[0]
    assert runtime.started is True
    assert runtime.stopped is True
    assert runtime.host == "127.0.0.1"
    assert runtime.port == 8123
    assert runtime.application.__class__.__name__ == "ASGIApp"
    assert runtime.application.app_factory is app_factory
    browser_open.assert_called_once_with("http://127.0.0.1:8123/")
