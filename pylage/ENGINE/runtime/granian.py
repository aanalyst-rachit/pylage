"""Granian runtime bridge for PyLage ASGI applications.

The bridge keeps Granian worker construction importable and process-safe.
"""

from __future__ import annotations

import asyncio
import importlib
import os
import socket
import subprocess
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from granian.constants import Interfaces
from granian.server.embed import Server

from pylage.cli import _resolve_app
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.renderers.html import render_document
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


class EmbeddedGranianRuntime:
    """Run a PyLage ASGI application using embedded Granian."""

    def __init__(self, application: ASGIApp, *, host: str = "127.0.0.1", port: int = 8000) -> None:
        if not isinstance(application, ASGIApp):
            raise TypeError("application must be an ASGIApp.")
        if port == 0:
            raise ValueError("Embedded Granian requires an explicit non-zero port.")
        self.application = application
        self.host = host
        self.port = port
        self._server: Server | None = None
        self._thread: threading.Thread | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._error: BaseException | None = None
        self._url: str | None = None

    @property
    def url(self) -> str:
        if self._url is None:
            raise RuntimeError("Embedded Granian runtime is not running.")
        return self._url

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> str:
        if self._thread is not None:
            raise RuntimeError("Embedded Granian runtime is already running.")

        self._server = Server(
            self.application,
            address=self.host,
            port=self.port,
            interface=Interfaces.ASGI,
            websockets=True,
            factory=False,
        )

        def runner() -> None:
            loop = asyncio.new_event_loop()
            self._loop = loop
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self._server.serve())
            except Exception as exc:  # noqa: BLE001 - background server thread must report arbitrary runtime failures
                self._error = exc
            finally:
                self._loop = None
                asyncio.set_event_loop(None)
                loop.close()

        self._thread = threading.Thread(
            target=runner,
            name="pylage-granian",
            daemon=True,
        )
        self._thread.start()

        url = f"http://{self.host}:{self.port}/"
        deadline = time.monotonic() + 10.0

        try:
            while time.monotonic() < deadline:
                if self._error is not None:
                    raise RuntimeError("Embedded Granian exited during startup.") from self._error

                try:
                    with urlopen(url, timeout=0.5) as response:
                        if response.status < 500:
                            self._url = url
                            return url
                except HTTPError as exc:
                    if exc.code < 500:
                        self._url = url
                        return url
                    time.sleep(0.05)
                except (OSError, URLError):
                    time.sleep(0.05)

            raise RuntimeError("Embedded Granian did not become ready within 10 seconds.")
        except Exception:
            self.stop()
            raise

    def stop(self) -> None:
        server = self._server
        loop = self._loop
        thread = self._thread

        if server is None:
            return

        if loop is not None and thread is not None and thread.is_alive():
            loop.call_soon_threadsafe(server.stop)
            thread.join(timeout=5.0)

        self._server = None
        self._thread = None
        self._loop = None
        self._url = None
        self._error = None


class GranianRuntime:
    """Manage a PyLage ASGI application through Granian."""

    def __init__(self, factory_path: str, *, host: str = "127.0.0.1", port: int = 0, loop: str | None = None, ssl_certificate: str | None = None, ssl_keyfile: str | None = None, ssl_keyfile_password: str | None = None) -> None:
        if not isinstance(factory_path, str) or not factory_path:
            raise ValueError("factory_path must be a non-empty string.")
        self.factory_path = factory_path
        self.host = host
        self.port = port
        self.loop = loop
        if (ssl_certificate is None) != (ssl_keyfile is None):
            raise ValueError("ssl_certificate and ssl_keyfile must be provided together.")
        if ssl_certificate is not None and not isinstance(ssl_certificate, str):
            raise TypeError("ssl_certificate must be a string path or None.")
        if ssl_keyfile is not None and not isinstance(ssl_keyfile, str):
            raise TypeError("ssl_keyfile must be a string path or None.")
        if ssl_keyfile_password is not None and not isinstance(ssl_keyfile_password, str):
            raise TypeError("ssl_keyfile_password must be a string or None.")
        self.ssl_certificate = ssl_certificate
        self.ssl_keyfile = ssl_keyfile
        self.ssl_keyfile_password = ssl_keyfile_password
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
        if self.loop is not None:
            command.extend(["--loop", self.loop])
        if self.ssl_certificate is not None:
            command.extend(["--ssl-certificate", self.ssl_certificate])
            command.extend(["--ssl-keyfile", self.ssl_keyfile])
            if self.ssl_keyfile_password is not None:
                command.extend(["--ssl-keyfile-password", self.ssl_keyfile_password])

        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        scheme = "https" if self.ssl_certificate is not None else "http"
        url = f"{scheme}://{self.host}:{port}/"
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



def _align_component_ids(template: Component, instance: Component) -> None:
    if not isinstance(template, Component) or not isinstance(instance, Component):
        raise TypeError("Component ID alignment expects Component trees.")

    if template.type != instance.type:
        raise RuntimeError(
            "Production component tree changed between document render "
            "and session creation: "
            f"{template.type} != {instance.type}."
        )

    template_children = [
        child for child in template.children
        if isinstance(child, Component)
    ]
    instance_children = [
        child for child in instance.children
        if isinstance(child, Component)
    ]

    if len(template_children) != len(instance_children):
        raise RuntimeError(
            "Production component tree shape changed between document render "
            "and session creation."
        )

    instance.id = template.id

    for template_child, instance_child in zip(
        template_children,
        instance_children,
        strict=True,
    ):
        _align_component_ids(template_child, instance_child)


def create_application_from_file() -> ASGIApp:
    """Create the production ASGI application from PYLAGE_APP_FILE."""
    app_path = Path(os.environ.get("PYLAGE_APP_FILE", "app.py")).resolve()
    template = _resolve_app(app_path)
    title = os.environ.get("PYLAGE_TITLE", "PyLage App")
    document = render_document(template, title=title)

    def app_factory() -> Component:
        instance = _resolve_app(app_path)
        _align_component_ids(template, instance)
        return instance

    return ASGIApp(app_factory=app_factory, document=document)
