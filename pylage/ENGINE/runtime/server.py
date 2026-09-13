from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import unquote, urlparse

from pylage.ENGINE.runtime.static import content_type_for, prepare_static_response


class _RequestHandler(BaseHTTPRequestHandler):
    directory: Path
    filename: str = "index.html"

    def do_GET(self) -> None:
        request_path = unquote(urlparse(self.path).path)

        if request_path == "/health":
            body = b'{"status":"ok"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if request_path in ("/", f"/{self.filename}"):
            relative_path = Path(self.filename)
        elif request_path.startswith("/"):
            relative_path = Path(request_path.lstrip("/"))
        else:
            self.send_error(404, "Not Found")
            return

        try:
            target = (self.directory / relative_path).resolve()
            root = self.directory.resolve()

            target.relative_to(root)
        except (ValueError, OSError):
            self.send_error(404, "Not Found")
            return

        if not target.is_file():
            self.send_error(404, "Not Found")
            return

        try:
            content = target.read_bytes()
        except OSError:
            self.send_error(404, "Not Found")
            return

        content_type = content_type_for(target)
        cache_control = (
            "no-cache"
            if target.name == self.filename
            else "public, max-age=3600"
        )
        content, headers = prepare_static_response(
            content,
            content_type,
            accept_encoding=self.headers.get("Accept-Encoding", ""),
            cache_control=cache_control,
        )

        self.send_response(200)
        for name, value in headers.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(content)

    def log_message(
        self,
        format: str,
        *args: object,
    ) -> None:
        return


class LocalServer:
    """Small local HTTP server for a rendered PyLage app."""

    def __init__(
        self,
        directory: str | Path,
        host: str = "127.0.0.1",
        port: int = 0,
        filename: str = "index.html",
    ) -> None:
        self.directory = Path(directory).resolve()
        self.host = host
        self.port = port
        self.filename = Path(filename).name

        self._server: ThreadingHTTPServer | None = None
        self._thread: Thread | None = None

    @property
    def url(self) -> str:
        if self._server is None:
            raise RuntimeError("Server is not running.")

        return (
            f"http://{self.host}:"
            f"{self._server.server_port}/"
        )

    def start(self) -> str:
        if self._server is not None:
            raise RuntimeError("Server is already running.")

        handler = type(
            "PyLageRequestHandler",
            (_RequestHandler,),
            {
                "directory": self.directory,
                "filename": self.filename,
            },
        )

        self._server = ThreadingHTTPServer(
            (self.host, self.port),
            handler,
        )

        self._thread = Thread(
            target=self._server.serve_forever,
            daemon=True,
        )
        self._thread.start()

        return self.url

    def stop(self) -> None:
        if self._server is None:
            return

        self._server.shutdown()
        self._server.server_close()

        if self._thread is not None:
            self._thread.join(timeout=2)

        self._thread = None
        self._server = None

    def __enter__(self) -> LocalServer:  # noqa: PYI034 - concrete return type preserves Python 3.10 support
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.stop()
