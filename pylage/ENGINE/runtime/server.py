from __future__ import annotations

import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Optional
from urllib.parse import unquote, urlparse


class _RequestHandler(BaseHTTPRequestHandler):
    directory: Path
    filename: str = "index.html"

    def do_GET(self) -> None:
        request_path = unquote(urlparse(self.path).path)

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

        content_type = (
            mimetypes.guess_type(target.name)[0]
            or "application/octet-stream"
        )

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
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

        self._server: Optional[ThreadingHTTPServer] = None
        self._thread: Optional[Thread] = None

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

    def __enter__(self) -> "LocalServer":
        self.start()
        return self

    def __exit__(self, *args: object) -> None:
        self.stop()
