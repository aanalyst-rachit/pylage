"""ASGI transport adapter for PyLage runtime.

The ASGI boundary owns HTTP and WebSocket transport while reusing the
existing PyLage rendering and reactive runtime machinery.
"""

from __future__ import annotations

import asyncio
import json
import mimetypes
import secrets
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
from typing import Any, Callable

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.runtime.session_store import InMemorySessionStore, SessionStore
from pylage.ENGINE.runtime.websocket import WebSocketServer


class _ASGIConnection:
    """Adapter exposing an ASGI WebSocket as the existing connection API."""

    def __init__(self, receive: Any, send: Any) -> None:
        self._receive = receive
        self._send = send
        self._closed = False

    def __aiter__(self) -> "_ASGIConnection":
        return self

    async def __anext__(self) -> str | bytes:
        while True:
            message = await self._receive()
            message_type = message.get("type")

            if message_type == "websocket.receive":
                text = message.get("text")
                if text is not None:
                    return text
                data = message.get("bytes")
                if data is not None:
                    return data
                continue

            if message_type == "websocket.disconnect":
                self._closed = True
                raise StopAsyncIteration

            if message_type == "websocket.connect":
                continue

    async def send(self, data: str | bytes) -> None:
        if self._closed:
            return
        if isinstance(data, bytes):
            await self._send({"type": "websocket.send", "bytes": data})
            return
        await self._send({"type": "websocket.send", "text": data})


class ASGIApp:
    """Minimal ASGI application for a PyLage component tree or factory."""

    def __init__(
        self,
        root: Component | None = None,
        *,
        app_factory: Callable[[], Component] | None = None,
        directory: str | Path | None = None,
        filename: str = "index.html",
        document: str | None = None,
        session_store: SessionStore | None = None,
    ) -> None:
        if root is None and app_factory is None:
            raise TypeError("ASGIApp expects a Component root or app_factory.")

        if root is not None and app_factory is not None:
            raise TypeError("ASGIApp accepts either root or app_factory, not both.")

        if root is not None and not isinstance(root, Component):
            raise TypeError("ASGIApp expects a Component root.")

        if app_factory is not None and not callable(app_factory):
            raise TypeError("ASGIApp app_factory must be callable.")

        self.root = root
        self.app_factory = app_factory
        self.directory = Path(directory).resolve() if directory is not None else None
        self.filename = Path(filename).name
        self.document = document
        self.websocket = WebSocketServer(root) if root is not None else None
        self._sessions: set[WebSocketServer] = set()
        self.session_store = session_store or InMemorySessionStore()
        self._loop: Any = None

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        scope_type = scope.get("type")

        if scope_type == "lifespan":
            await self._lifespan(receive, send)
            return

        if scope_type == "http":
            await self._http(scope, send)
            return

        if scope_type == "websocket":
            await self._websocket(scope, receive, send)
            return

        await send({
            "type": "http.response.start",
            "status": 500,
            "headers": [(b"content-type", b"text/plain; charset=utf-8")],
        })
        await send({
            "type": "http.response.body",
            "body": b"Unsupported ASGI scope.",
        })

    async def _lifespan(self, receive: Any, send: Any) -> None:
        while True:
            message = await receive()
            message_type = message.get("type")

            if message_type == "lifespan.startup":
                self._loop = asyncio.get_running_loop()
                if self.websocket is not None:
                    self.websocket.attach_external_loop(self._loop)
                await send({"type": "lifespan.startup.complete"})
            elif message_type == "lifespan.shutdown":
                if self.websocket is not None:
                    self.websocket.detach_external_loop()
                for session in tuple(self._sessions):
                    session.detach_external_loop()
                    self._sessions.discard(session)
                self.session_store.clear()
                self._loop = None
                await send({"type": "lifespan.shutdown.complete"})
                return

    async def _http(self, scope: dict[str, Any], send: Any) -> None:
        path = unquote(urlparse(scope.get("path", "/")).path)

        if self.document is not None and path in ("/", f"/{self.filename}"):
            await self._response(200, self.document.encode("utf-8"), "text/html; charset=utf-8", send)
            return

        if self.directory is None:
            await self._response(404, b"Not Found", "text/plain; charset=utf-8", send)
            return

        relative = Path(self.filename) if path in ("/", f"/{self.filename}") else Path(path.lstrip("/"))

        try:
            target = (self.directory / relative).resolve()
            target.relative_to(self.directory)
        except (ValueError, OSError):
            await self._response(404, b"Not Found", "text/plain; charset=utf-8", send)
            return

        if not target.is_file():
            await self._response(404, b"Not Found", "text/plain; charset=utf-8", send)
            return

        try:
            content = target.read_bytes()
        except OSError:
            await self._response(404, b"Not Found", "text/plain; charset=utf-8", send)
            return

        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        await self._response(200, content, content_type, send)

    def _evict_expired_sessions(self) -> None:
        for _token, session in self.session_store.evict_expired():
            if session in self._sessions:
                session.detach_external_loop()
                self._sessions.discard(session)

    async def _response(
        self,
        status: int,
        body: bytes,
        content_type: str,
        send: Any,
    ) -> None:
        await send({
            "type": "http.response.start",
            "status": status,
            "headers": [
                (b"content-type", content_type.encode("latin-1")),
                (b"content-length", str(len(body)).encode("ascii")),
            ],
        })
        await send({"type": "http.response.body", "body": body})

    async def _websocket(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        await send({"type": "websocket.accept"})
        connection = _ASGIConnection(receive, send)

        if self.app_factory is None:
            if self.websocket is None:
                raise RuntimeError("ASGIApp has no WebSocket server.")
            await self.websocket.handle_external(connection)
            return

        query_string = scope.get("query_string", b"")
        query = parse_qs(query_string.decode("utf-8"), keep_blank_values=False)
        token_values = query.get("session", [])
        token = token_values[0] if token_values else None
        session = self.session_store.get(token) if token else None

        if session is None:
            root = self.app_factory()
            if not isinstance(root, Component):
                raise TypeError("ASGIApp app_factory must return a Component.")

            session = WebSocketServer(root)
            token = secrets.token_urlsafe(32)
            while self.session_store.get(token) is not None:
                token = secrets.token_urlsafe(32)
            self.session_store.put(token, session)
            self._sessions.add(session)

        session.attach_external_loop(asyncio.get_running_loop())
        try:
            await connection.send(json.dumps({"type": "session", "token": token}))
            await session.handle_external(connection)
        finally:
            session.detach_external_loop()
            self.session_store.put(token, session)
            self._evict_expired_sessions()
