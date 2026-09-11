import asyncio
from pathlib import Path

import pylage as pl
from pylage.ENGINE.core.state import State
from pylage.ENGINE.runtime.asgi import ASGIApp


def run(coro):
    return asyncio.run(coro)


def test_asgi_http_serves_document():
    app = pl.column(pl.heading("ASGI Test"))
    document = "<html><body><h1>ASGI Test</h1></body></html>"
    asgi = ASGIApp(app, filename="index.html", document=document)
    messages = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    run(asgi({"type": "http", "path": "/", "method": "GET", "headers": []}, receive, send))

    assert messages[0]["type"] == "http.response.start"
    assert messages[0]["status"] == 200
    assert messages[1]["body"] == document.encode("utf-8")


def test_asgi_http_rejects_missing_document():
    app = pl.column(pl.heading("ASGI Test"))
    asgi = ASGIApp(app, filename="index.html", document="<html></html>")
    messages = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    run(asgi({"type": "http", "path": "/missing", "method": "GET", "headers": []}, receive, send))

    assert messages[0]["status"] == 404


def test_asgi_http_serves_static_file(tmp_path: Path):
    static_file = tmp_path / "app.js"
    static_file.write_text("console.log('ok');")
    app = pl.column(pl.heading("ASGI Test"))
    asgi = ASGIApp(app, directory=tmp_path, filename="index.html")
    messages = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    run(asgi({"type": "http", "path": "/app.js", "method": "GET", "headers": []}, receive, send))

    assert messages[0]["status"] == 200
    assert messages[1]["body"] == b"console.log('ok');"


def test_asgi_scope_rejects_unsupported_type():
    app = pl.column(pl.heading("ASGI Test"))
    asgi = ASGIApp(app, document="<html></html>")
    messages = []

    async def receive():
        return {}

    async def send(message):
        messages.append(message)

    run(asgi({"type": "unknown"}, receive, send))

    assert messages[0]["status"] == 500


def test_asgi_websocket_accepts_connection():
    app = pl.column(pl.button("Test"))
    asgi = ASGIApp(app)
    messages = []

    async def receive():
        return {"type": "websocket.disconnect"}

    async def send(message):
        messages.append(message)

    run(asgi({"type": "websocket", "path": "/", "headers": []}, receive, send))

    assert messages[0] == {"type": "websocket.accept"}



def test_asgi_websocket_reactive_state_update():
    state = State("before")
    app = pl.text(state)
    asgi = ASGIApp(app)
    messages = []
    connected = asyncio.Event()
    disconnect = asyncio.Event()

    async def receive():
        await connected.wait()
        await disconnect.wait()
        return {"type": "websocket.disconnect"}

    async def send(message):
        messages.append(message)

    async def scenario():
        loop = asyncio.get_running_loop()
        asgi.websocket.attach_external_loop(loop)
        try:
            task = asyncio.create_task(asgi._websocket({"type": "websocket", "path": "/", "headers": []}, receive, send))
            await asyncio.sleep(0)
            connected.set()
            await asyncio.sleep(0)
            state.set("after")
            await asyncio.sleep(0.05)
            disconnect.set()
            await task
        finally:
            asgi.websocket.detach_external_loop()

    run(scenario())

    assert messages[0] == {"type": "websocket.accept"}
    assert any(
        message.get("type") == "websocket.send"
        and "after" in message.get("text", "")
        for message in messages
    )


def test_asgi_lifespan_startup_and_shutdown():
    app = pl.column(pl.heading("ASGI Lifecycle"))
    asgi = ASGIApp(app)
    messages = []
    events = asyncio.Queue()

    async def receive():
        return await events.get()

    async def send(message):
        messages.append(message)

    async def scenario():
        await events.put({"type": "lifespan.startup"})
        task = asyncio.create_task(asgi._lifespan(receive, send))
        await asyncio.sleep(0)
        assert asgi._loop is asyncio.get_running_loop()
        await events.put({"type": "lifespan.shutdown"})
        await task
        assert asgi._loop is None

    run(scenario())

    assert messages == [
        {"type": "lifespan.startup.complete"},
        {"type": "lifespan.shutdown.complete"},
    ]


def test_asgi_websocket_disconnect_cleans_connection():
    app = pl.column(pl.button("Test"))
    asgi = ASGIApp(app)
    messages = []

    async def receive():
        return {"type": "websocket.disconnect"}

    async def send(message):
        messages.append(message)

    async def scenario():
        asgi.websocket.attach_external_loop(asyncio.get_running_loop())
        try:
            await asgi._websocket(
                {"type": "websocket", "path": "/", "headers": []},
                receive,
                send,
            )
            assert not asgi.websocket._connections
        finally:
            asgi.websocket.detach_external_loop()

    run(scenario())

    assert messages == [{"type": "websocket.accept"}]


def create_granian_smoke_app():
    return ASGIApp(
        pl.column(pl.heading("Granian Smoke")),
        document="<html><body><h1>Granian Smoke</h1></body></html>",
    )

def test_asgi_http_rejects_path_traversal(tmp_path: Path):
    secret_file = tmp_path.parent / "asgi_secret.txt"
    secret_file.write_text("secret")
    app = pl.column(pl.heading("ASGI Test"))
    asgi = ASGIApp(app, directory=tmp_path, filename="index.html")
    messages = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    run(asgi({"type": "http", "path": "/../asgi_secret.txt", "method": "GET", "headers": []}, receive, send))

    assert messages[0]["status"] == 404
