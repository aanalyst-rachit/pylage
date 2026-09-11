"""Granian runtime bridge for PyLage ASGI applications.

The bridge keeps Granian worker construction importable and process-safe.
"""

from __future__ import annotations

import importlib
import socket
import subprocess
import time
from urllib.error import URLError
from urllib.request import urlopen
from typing import Any, Callable

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.runtime.asgi import ASGIApp


def load_factory(path: str) -> Callable[[], Any]:
    """Load a zero-argument application factory from an import path."""
    module_name, separator, attribute_name = path.partition(":")
    if not separator or not module_name or not attribute_name:
        raise ValueError("Factory path must use the form module:callable.")

    module = importlib.import_module(module_name)
    factory: Any = module
    for name in attribute_name.split("."):
        factory = getattr(factory, name)

    if not callable(factory):
        raise TypeError(f"Application factory is not callable: {path}")

    return factory


class GranianRuntime:
    """Manage a PyLage ASGI application through Granian."""

    def __init__(self, factory_path: str, *, host: str = "127.0.0.1", port: int = 0) -> None:
        if not isinstance(factory_path, str) or not factory_path:
            raise ValueError("factory_path must be a non-empty string.")
        self.factory_path = factory_path
        self.host = host
        self.port = port
        self._process: Any = None
        self._url: str | None = None

    @property
    def url(self) -> str:
        if self._url is None:
            raise RuntimeError("Granian runtime is not running.")
        return self._url

    @property
    def running(self) -> bool:
        return self._process is not None

    def start(self) -> str:
        """Start Granian and return the HTTP application URL."""
        if self._process is not None:
            raise RuntimeError("Granian runtime is already running.")

        if self.port == 0:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind((self.host, 0))
                port = int(sock.getsockname()[1])
        else:
            port = self.port

        application = create_asgi_app(self.factory_path)
        del application

        command = [
            "granian",
            self.factory_path,
            "--interface",
            "asgi",
            "--factory",
            "--host",
            self.host,
            "--port",
            str(port),
        ]

        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        url = f"http://{self.host}:{port}/"
        deadline = time.monotonic() + 10.0

        try:
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError(
                        f"Granian exited during startup with code {process.returncode}."
                    )

                try:
                    with urlopen(url, timeout=0.5) as response:
                        if response.status < 500:
                            self._process = process
                            self._url = url
                            return url
                except (OSError, URLError):
                    time.sleep(0.05)

            raise RuntimeError("Granian did not become ready within 10 seconds.")
        except Exception:
            process.terminate()
            try:
                process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2.0)
            raise

    def stop(self) -> None:
        """Stop the Granian process if it is running."""
        process = self._process
        self._process = None
        self._url = None

        if process is None:
            return

        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=3.0)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3.0)


def create_asgi_app(factory_path: str) -> ASGIApp:
    """Construct an ASGI application from an importable factory path."""
    factory = load_factory(factory_path)
    application = factory()

    if isinstance(application, ASGIApp):
        return application

    if isinstance(application, Component):
        return ASGIApp(application)

    raise TypeError(
        "Application factory must return an ASGIApp or Component."
    )
