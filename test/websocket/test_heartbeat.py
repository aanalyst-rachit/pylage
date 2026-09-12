import asyncio
import ssl

import pytest

import pylage.ENGINE.runtime.websocket as websocket_runtime

from pylage.ENGINE import Column
from pylage.ENGINE.runtime.websocket import WebSocketServer


class FakeConnection:
    def __init__(self, *, fail_ping=False):
        self.fail_ping = fail_ping
        self.pings = 0
        self.closed = False

    def ping(self):
        self.pings += 1
        if self.fail_ping:
            async def fail():
                raise TimeoutError("pong timeout")
            return fail()
        async def pong():
            return None
        return pong()

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_heartbeat_pings_connections():
    server = WebSocketServer(Column(), heartbeat_interval=0.01)
    connection = FakeConnection()
    server._connections.add(connection)

    task = asyncio.create_task(server._heartbeat())
    await asyncio.sleep(0.035)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)

    assert connection.pings >= 1
    assert connection in server._connections


@pytest.mark.asyncio
async def test_heartbeat_removes_dead_connections():
    server = WebSocketServer(Column(), heartbeat_interval=0.01)
    connection = FakeConnection(fail_ping=True)
    server._connections.add(connection)

    task = asyncio.create_task(server._heartbeat())
    await asyncio.sleep(0.035)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)

    assert connection not in server._connections
    assert connection.closed is True


@pytest.mark.asyncio
async def test_websocket_serve_security_configuration(monkeypatch):
    captured = {}

    class FakeSocket:
        def getsockname(self):
            return ("127.0.0.1", 8765)

    class FakeServer:
        sockets = [FakeSocket()]

        async def wait_closed(self):
            return None

    async def fake_serve(handler, host, port, **kwargs):
        captured.update(kwargs)
        return FakeServer()

    monkeypatch.setattr(websocket_runtime, "serve", fake_serve)

    server = WebSocketServer(
        Column(),
        allowed_origins=["https://example.com"],
        max_message_size=4096,
    )

    await server._serve()

    assert captured["origins"] == ("https://example.com", None)
    assert captured["max_size"] == 4096


@pytest.mark.asyncio
async def test_websocket_serve_propagates_ssl_context(monkeypatch):
    captured = {}

    class FakeSocket:
        def getsockname(self):
            return ("127.0.0.1", 8765)

    class FakeServer:
        sockets = [FakeSocket()]

        async def wait_closed(self):
            return None

    async def fake_serve(handler, host, port, **kwargs):
        captured.update(kwargs)
        return FakeServer()

    monkeypatch.setattr(websocket_runtime, "serve", fake_serve)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    server = WebSocketServer(Column(), ssl_context=ssl_context)

    await server._serve()

    assert captured["ssl"] is ssl_context


def test_websocket_tls_configuration_changes_url_scheme():
    server = WebSocketServer(
        Column(),
        ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER),
    )
    server._server = object()
    server.port = 8765

    assert server.url == "wss://127.0.0.1:8765/"


def test_websocket_tls_configuration_validation():
    with pytest.raises(TypeError, match="ssl_context"):
        WebSocketServer(Column(), ssl_context=object())


def test_websocket_security_defaults():
    server = WebSocketServer(Column())
    assert server.allowed_origins is None
    assert server.max_message_size == 1024 * 1024
    assert server.message_rate_limit == 20.0
    assert server.message_rate_burst == 40


def test_websocket_security_configuration():
    server = WebSocketServer(
        Column(),
        allowed_origins=["https://example.com"],
        max_message_size=4096,
    )
    assert server.allowed_origins == ("https://example.com",)
    assert server.max_message_size == 4096


def test_websocket_message_rate_limit_validation():
    with pytest.raises(ValueError, match="message_rate_limit"):
        WebSocketServer(Column(), message_rate_limit=0)

    with pytest.raises(ValueError, match="message_rate_limit"):
        WebSocketServer(Column(), message_rate_limit=-1)

    with pytest.raises(TypeError, match="message_rate_limit"):
        WebSocketServer(Column(), message_rate_limit=True)

    with pytest.raises(ValueError, match="message_rate_burst"):
        WebSocketServer(Column(), message_rate_burst=0)

    with pytest.raises(ValueError, match="message_rate_burst"):
        WebSocketServer(Column(), message_rate_burst=-1)

    with pytest.raises(TypeError, match="message_rate_burst"):
        WebSocketServer(Column(), message_rate_burst=True)


@pytest.mark.asyncio
async def test_websocket_message_rate_limit_closes_connection():
    from pylage.ENGINE.core.protocol import EventMessage

    class FakeMessageConnection:
        def __init__(self, messages):
            self.messages = iter(messages)
            self.sent = []
            self.closed = []

        def __aiter__(self):
            return self

        async def __anext__(self):
            try:
                return next(self.messages)
            except StopIteration:
                raise StopAsyncIteration

        async def send(self, message):
            self.sent.append(message)

        async def close(self, code=None, reason=None):
            self.closed.append((code, reason))

    button = __import__('pylage.ENGINE', fromlist=['Button']).Button('Click')
    calls = []
    button.events['click'] = lambda: calls.append('clicked')
    server = WebSocketServer(
        Column(button),
        message_rate_limit=1.0,
        message_rate_burst=1,
    )

    message = EventMessage(button.id, 'click').to_json()
    connection = FakeMessageConnection([message, message])

    await server._handle(connection)

    assert calls == ['clicked']
    assert connection.closed == [(1013, 'message rate limit exceeded')]
    assert len(connection.sent) == 1


def test_websocket_message_size_validation():
    with pytest.raises(ValueError, match="max_message_size"):
        WebSocketServer(Column(), max_message_size=0)

    with pytest.raises(ValueError, match="max_message_size"):
        WebSocketServer(Column(), max_message_size=-1)

    with pytest.raises(TypeError, match="max_message_size"):
        WebSocketServer(Column(), max_message_size=True)


def test_heartbeat_interval_validation():
    with pytest.raises(ValueError, match="heartbeat_interval"):
        WebSocketServer(Column(), heartbeat_interval=0)

    with pytest.raises(ValueError, match="heartbeat_interval"):
        WebSocketServer(Column(), heartbeat_interval=-1)
