from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from playground.app import get_app
from playground.runtime import PYLAGE_WHEEL, build_playground_document


class PlaygroundServer:
    """Serve the playground page and its PyLage wheel."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
    ) -> None:
        self.host = host
        self.port = port
        self.root = Path(__file__).resolve().parent.parent
        self.wheel = self.root / "dist" / PYLAGE_WHEEL
        self.server: ThreadingHTTPServer | None = None

    def _handler(self):
        wheel = self.wheel

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                path = urlparse(self.path).path

                if path in {"/", "/index.html"}:
                    content = build_playground_document(
                        get_app(),
                        title="PyLage Playground",
                    ).encode("utf-8")
                    content_type = "text/html; charset=utf-8"

                elif path == f"/dist/{wheel.name}" and wheel.exists():
                    content = wheel.read_bytes()
                    content_type = "application/octet-stream"

                else:
                    self.send_error(404, "Not Found")
                    return

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

        return Handler

    def start(self) -> None:
        self.server = ThreadingHTTPServer(
            (self.host, self.port),
            self._handler(),
        )

        actual_port = self.server.server_port

        print(
            f"PyLage Playground running at "
            f"http://{self.host}:{actual_port}/"
        )
        print("Press Ctrl+C to stop.")

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping PyLage Playground...")
        finally:
            self.server.server_close()


if __name__ == "__main__":
    PlaygroundServer(
        host="0.0.0.0",
        port=8000,
    ).start()
