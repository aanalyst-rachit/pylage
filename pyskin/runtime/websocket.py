from __future__ import annotations

import asyncio
import threading
from typing import Any, Optional

from websockets.asyncio.server import Server, ServerConnection, serve

from pyskin.core.binding import StateBinding
from pyskin.core.component import Component
from pyskin.core.events import EventDispatcher
from pyskin.core.protocol import EventMessage, UpdateMessage


class WebSocketServer:
    """WebSocket transport for PySkin events and state updates."""

    def __init__(
        self,
        root: Component,
        *,
        host: str = "127.0.0.1",
        port: int = 0,
    ) -> None:
        if not isinstance(root, Component):
            raise TypeError(
                "WebSocketServer expects a Component root."
            )

        self.root = root
        self.host = host
        self.port = port

        self._dispatcher = EventDispatcher(root)

        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._server: Optional[Server] = None
        self._thread: Optional[threading.Thread] = None

        self._connections: set[ServerConnection] = set()
        self._connections_lock = threading.Lock()

        self._ready = threading.Event()
        self._startup_error: Optional[BaseException] = None

        self._binding = StateBinding(
            root,
            self._on_state_change,
        )

    @property
    def running(self) -> bool:
        return self._server is not None

    @property
    def url(self) -> str:
        if self._server is None:
            raise RuntimeError("WebSocket server is not running.")

        return f"ws://{self.host}:{self.port}/"

    def _on_state_change(
        self,
        component: Component,
        props: dict[str, Any],
    ) -> None:
        """Called whenever a bound State changes."""

        message = UpdateMessage(
            component_id=component.id,
            props=props,
        )

        if self._loop is None or self._server is None:
            return

        asyncio.run_coroutine_threadsafe(
            self._broadcast(message.to_json()),
            self._loop,
        )

    async def _broadcast(self, raw_message: str) -> None:
        """Send a state update to every connected browser."""

        with self._connections_lock:
            connections = tuple(self._connections)

        if not connections:
            return

        results = await asyncio.gather(
            *(connection.send(raw_message) for connection in connections),
            return_exceptions=True,
        )

        dead = {
            connection
            for connection, result in zip(connections, results)
            if isinstance(result, Exception)
        }

        if dead:
            with self._connections_lock:
                self._connections.difference_update(dead)

    async def _handle(self, connection: ServerConnection) -> None:
        with self._connections_lock:
            self._connections.add(connection)

        try:
            async for raw_message in connection:
                try:
                    message = EventMessage.from_json(raw_message)

                    result = self._dispatcher.dispatch(
                        message.component_id,
                        message.event,
                        message.payload,
                    )

                    await connection.send(
                        EventMessageResponse.success(result).to_json()
                    )

                except Exception as exc:
                    await connection.send(
                        EventMessageResponse.error(str(exc)).to_json()
                    )
        finally:
            with self._connections_lock:
                self._connections.discard(connection)

    async def _serve(self) -> None:
        try:
            self._server = await serve(
                self._handle,
                self.host,
                self.port,
            )

            socket = next(iter(self._server.sockets))
            self.port = socket.getsockname()[1]

        except BaseException as exc:
            self._startup_error = exc

        finally:
            self._ready.set()

        if self._server is None:
            return

        await self._server.wait_closed()

    def _thread_main(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        try:
            self._loop.run_until_complete(self._serve())
        finally:
            self._loop.close()
            self._loop = None

    def start(self) -> str:
        if self._thread is not None:
            raise RuntimeError(
                "WebSocket server is already running."
            )

        self._startup_error = None
        self._ready.clear()

        self._thread = threading.Thread(
            target=self._thread_main,
            daemon=True,
        )

        self._thread.start()
        self._ready.wait()

        if self._startup_error is not None:
            error = self._startup_error
            self._thread = None
            raise RuntimeError(
                "Failed to start WebSocket server."
            ) from error

        return self.url

    def stop(self) -> None:
        if self._thread is None:
            return

        self._binding.stop()

        if self._loop is not None and self._server is not None:
            self._loop.call_soon_threadsafe(
                self._server.close
            )

        self._thread.join(timeout=2.0)

        self._server = None
        self._thread = None
        self._loop = None

        with self._connections_lock:
            self._connections.clear()


class EventMessageResponse:
    """Transport response envelope."""

    def __init__(
        self,
        *,
        ok: bool,
        result: Any = None,
        error: str | None = None,
    ) -> None:
        self.ok = ok
        self.result = result
        self.error = error

    @classmethod
    def success(cls, result: Any = None) -> "EventMessageResponse":
        return cls(ok=True, result=result)

    @classmethod
    def error(cls, error: str) -> "EventMessageResponse":
        return cls(ok=False, error=error)

    def to_json(self) -> str:
        import json

        data: dict[str, Any] = {
            "type": "response",
            "ok": self.ok,
        }

        if self.ok:
            data["result"] = self.result
        else:
            data["error"] = self.error

        return json.dumps(
            data,
            separators=(",", ":"),
        )
