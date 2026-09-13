from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.renderers.html import render_document
from pylage.ENGINE.runtime.logger import log_event
from pylage.ENGINE.runtime.server import LocalServer
from pylage.ENGINE.runtime.websocket import WebSocketServer


class Runtime:
    """Coordinates PyLage rendering and the local HTTP runtime."""

    def __init__(
        self,
        app: Component,
        *,
        title: str = "PyLage App",
        output: str | Path = "index.html",
        host: str = "127.0.0.1",
        port: int = 0,
        document_transform: Callable[[str], str] | None = None,
        navigation_handler: Callable[[str], object] | None = None,
    ) -> None:
        if not isinstance(app, Component):
            raise TypeError(
                "Runtime expects a Component as the root app."
            )

        self.app = app
        self.title = title
        self.output = Path(output)
        self.host = host
        self.port = port
        if navigation_handler is not None and not callable(navigation_handler):
            raise TypeError(
                "navigation_handler must be callable or None."
            )

        self.document_transform = document_transform
        self.navigation_handler = navigation_handler

        self._server: LocalServer | None = None
        self._websocket: WebSocketServer | None = None

    @property
    def url(self) -> str:
        if self._server is None:
            raise RuntimeError("Runtime is not running.")

        return self._server.url

    @property
    def running(self) -> bool:
        return self._server is not None

    def _render_document(self) -> str:
        websocket_url = None
        if self._websocket is not None:
            websocket_url = self._websocket.url

        document = render_document(
            self.app,
            title=self.title,
            websocket_url=websocket_url,
        )
        if self.document_transform is not None:
            document = self.document_transform(document)
        return document

    def render(self) -> Path:
        """Render the current app into an HTML document."""

        document = self._render_document()
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.output.write_text(
            document,
            encoding="utf-8",
        )

        return self.output

    def start(self) -> str:
        """Render the app and start the local HTTP server."""

        if self._server is not None:
            raise RuntimeError("Runtime is already running.")

        self._websocket = WebSocketServer(
            self.app,
            host=self.host,
            port=0,
            navigation_handler=self.navigation_handler,
        )

        try:
            self._websocket.start()

            document = self._render_document()

            output_path = self.output
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                document,
                encoding="utf-8",
            )

            self._server = LocalServer(
                output_path.parent,
                host=self.host,
                port=self.port,
                filename=output_path.name,
            )

            url = self._server.start()
            log_event(
                20,
                "runtime.start",
                lifecycle="start",
                host=self.host,
                port=self._server.port,
            )
            return url

        except Exception as exc:
            log_event(
                40,
                "runtime.start.error",
                lifecycle="error",
                error=exc,
                host=self.host,
                port=self.port,
            )
            if self._websocket is not None:
                self._websocket.stop()
                self._websocket = None

            self._server = None
            raise

    def reload_app(self, app: Component) -> Path:
        """Render and activate a replacement app for development reloads."""
        if not isinstance(app, Component):
            raise TypeError("Runtime expects a Component as the replacement app.")

        document = render_document(
            app,
            title=self.title,
            websocket_url=self._websocket.url if self._websocket is not None else None,
        )
        if self.document_transform is not None:
            document = self.document_transform(document)

        output_path = self.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(document, encoding="utf-8")

        if self._websocket is not None:
            self._websocket.replace_root(app)
            self._websocket.notify_reload()

        self.app = app
        log_event(
            20,
            "runtime.reload",
            lifecycle="reload",
            component_id=app.id,
        )
        return output_path

    def notify_error(self, error: str) -> None:
        """Notify connected development clients about a runtime error."""
        log_event(
            40,
            "runtime.error",
            lifecycle="error",
            error=str(error),
        )
        if self._websocket is not None:
            self._websocket.notify_error(str(error))

    def stop(self) -> None:
        """Stop the local HTTP server."""

        was_running = self._server is not None or self._websocket is not None

        if self._server is not None:
            self._server.stop()
            self._server = None

        if self._websocket is not None:
            self._websocket.stop()
            self._websocket = None

        if was_running:
            log_event(
                20,
                "runtime.stop",
                lifecycle="stop",
            )

    def __enter__(self) -> Runtime:  # noqa: PYI034 - concrete return type preserves Python 3.10 support
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.stop()
