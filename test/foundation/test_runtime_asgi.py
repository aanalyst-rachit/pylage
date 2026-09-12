import asyncio
import json
from pylage.ENGINE.core.protocol_codec import decode_message
from pathlib import Path

import pylage as pl
from pylage.ENGINE.core.state import State
from pylage.ENGINE.runtime.asgi import ASGIApp
from pylage.ENGINE.runtime.session_store import InMemorySessionStore


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
        and isinstance(message.get("bytes"), (bytes, bytearray))
        and "after" in decode_message(message["bytes"]).to_dict().get("props", {}).get("text", "")
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


def test_asgi_factory_creates_isolated_sessions():
    created = []

    def factory():
        state = State(f"before-{len(created) + 1}")
        root = pl.text(state)
        created.append((state, root))
        return root

    asgi = ASGIApp(app_factory=factory)
    messages_a = []
    messages_b = []
    disconnect_a = asyncio.Event()
    disconnect_b = asyncio.Event()

    async def receive_a():
        await disconnect_a.wait()
        return {"type": "websocket.disconnect"}

    async def receive_b():
        await disconnect_b.wait()
        return {"type": "websocket.disconnect"}

    async def send_a(message):
        messages_a.append(message)

    async def send_b(message):
        messages_b.append(message)

    async def scenario():
        task_a = asyncio.create_task(asgi._websocket({"type": "websocket", "path": "/", "headers": []}, receive_a, send_a))
        task_b = asyncio.create_task(asgi._websocket({"type": "websocket", "path": "/", "headers": []}, receive_b, send_b))

        for _ in range(100):
            if len(created) == 2:
                break
            await asyncio.sleep(0)

        assert len(created) == 2
        state_a = created[0][0]
        state_b = created[1][0]
        root_a = created[0][1]
        root_b = created[1][1]

        assert state_a is not state_b
        assert root_a is not root_b
        assert len(asgi._sessions) == 2

        state_a.set("after-a")
        await asyncio.sleep(0.05)

        assert any(
            message.get("type") == "websocket.send"
            and "after-a" in message.get("text", "")
            for message in messages_a
        )
        assert not any(
            message.get("type") == "websocket.send"
            and "after-a" in message.get("text", "")
            for message in messages_b
        )

        disconnect_a.set()
        disconnect_b.set()
        await asyncio.gather(task_a, task_b)

        assert len(asgi._sessions) == 2

        count_a = len(messages_a)
        count_b = len(messages_b)
        state_a.set("after-disconnect")
        state_b.set("after-disconnect")
        await asyncio.sleep(0.05)

        assert len(messages_a) == count_a
        assert len(messages_b) == count_b

        shutdown_events = asyncio.Queue()

        async def shutdown_receive():
            return await shutdown_events.get()

        async def shutdown_send(message):
            pass

        await shutdown_events.put({"type": "lifespan.shutdown"})
        await asgi._lifespan(shutdown_receive, shutdown_send)

        assert not asgi._sessions
        assert not asgi.session_store.clear()


def test_asgi_factory_resumes_session_after_disconnect():
    created = []

    def factory():
        state = State(f"before-{len(created) + 1}")
        root = pl.text(state)
        created.append((state, root))
        return root

    asgi = ASGIApp(app_factory=factory)
    first_messages = []
    resumed_messages = []
    first_disconnect = asyncio.Event()
    resumed_disconnect = asyncio.Event()

    async def first_receive():
        await first_disconnect.wait()
        return {"type": "websocket.disconnect"}

    async def resumed_receive():
        await resumed_disconnect.wait()
        return {"type": "websocket.disconnect"}

    async def send_first(message):
        first_messages.append(message)

    async def send_resumed(message):
        resumed_messages.append(message)

    async def scenario():
        first_task = asyncio.create_task(
            asgi._websocket(
                {"type": "websocket", "path": "/", "headers": []},
                first_receive,
                send_first,
            )
        )

        for _ in range(100):
            if created:
                break
            await asyncio.sleep(0)

        assert len(created) == 1
        assert first_messages[0] == {"type": "websocket.accept"}

        session_messages = [
            message
            for message in first_messages
            if message.get("type") == "websocket.send"
        ]
        assert session_messages

        handshake = json.loads(session_messages[0]["text"])
        assert handshake["type"] == "session"
        token = handshake["token"]
        assert token
        assert asgi.session_store.get(token) in asgi._sessions

        first_session = asgi.session_store.get(token)
        assert first_session is not None
        first_state = created[0][0]
        first_root = created[0][1]

        first_disconnect.set()
        await first_task

        assert len(created) == 1
        assert asgi.session_store.get(token) is first_session
        assert len(asgi._sessions) == 1

        resumed_task = asyncio.create_task(
            asgi._websocket(
                {
                    "type": "websocket",
                    "path": "/",
                    "query_string": f"session={token}".encode(),
                    "headers": [],
                },
                resumed_receive,
                send_resumed,
            )
        )

        await asyncio.sleep(0)

        assert len(created) == 1
        assert asgi.session_store.get(token) is first_session
        assert created[0][0] is first_state
        assert created[0][1] is first_root

        resumed_handshakes = [
            json.loads(message["text"])
            for message in resumed_messages
            if message.get("type") == "websocket.send"
        ]
        assert resumed_handshakes
        assert resumed_handshakes[0] == {"type": "session", "token": token}

        first_state.set("after-resume")
        await asyncio.sleep(0.05)

        assert any(
            message.get("type") == "websocket.send"
            and isinstance(message.get("bytes"), (bytes, bytearray))
            and "after-resume" in decode_message(message["bytes"]).to_dict().get("props", {}).get("text", "")
            for message in resumed_messages
        )

        resumed_disconnect.set()
        await resumed_task

        assert len(created) == 1
        assert asgi.session_store.get(token) is first_session
        assert len(asgi._sessions) == 1

        shutdown_events = asyncio.Queue()

        async def shutdown_receive():
            return await shutdown_events.get()

        async def shutdown_send(message):
            pass

        await shutdown_events.put({"type": "lifespan.shutdown"})
        await asgi._lifespan(shutdown_receive, shutdown_send)

        assert not asgi._sessions
        assert not asgi.session_store.clear()

    run(scenario())


def test_asgi_factory_unknown_session_token_creates_new_session():
    created = []
    messages = []

    def factory():
        state = State(f"before-{len(created) + 1}")
        root = pl.text(state)
        created.append((state, root))
        return root

    asgi = ASGIApp(app_factory=factory)

    async def receive():
        return {"type": "websocket.disconnect"}

    async def send(message):
        messages.append(message)

    async def scenario():
        await asgi._websocket(
            {
                "type": "websocket",
                "path": "/",
                "query_string": b"session=stale-token",
                "headers": [],
            },
            receive,
            send,
        )

        assert len(created) == 1
        assert len(asgi._sessions) == 1

        handshake_messages = [
            json.loads(message["text"])
            for message in messages
            if message.get("type") == "websocket.send"
        ]
        assert len(handshake_messages) == 1
        assert handshake_messages[0]["type"] == "session"
        assert handshake_messages[0]["token"] != "stale-token"

        shutdown_events = asyncio.Queue()

        async def shutdown_receive():
            return await shutdown_events.get()

        async def shutdown_send(message):
            pass

        await shutdown_events.put({"type": "lifespan.shutdown"})
        await asgi._lifespan(shutdown_receive, shutdown_send)

        assert not asgi._sessions
        assert not asgi.session_store.clear()

    run(scenario())


def test_asgi_factory_requires_component_result():
    asgi = ASGIApp(app_factory=lambda: "not-a-component")
    messages = []

    async def receive():
        return {"type": "websocket.disconnect"}

    async def send(message):
        messages.append(message)

    async def scenario():
        try:
            await asgi._websocket({"type": "websocket", "path": "/", "headers": []}, receive, send)
        except TypeError as exc:
            assert str(exc) == "ASGIApp app_factory must return a Component."
        else:
            raise AssertionError("Expected app_factory result validation to fail.")

    run(scenario())
    assert messages[0] == {"type": "websocket.accept"}

def test_asgi_accepts_injected_session_store():
    session_store = InMemorySessionStore()
    asgi = ASGIApp(
        app_factory=lambda: pl.column(pl.button("Test")),
        session_store=session_store,
    )
    messages = []

    async def receive():
        return {"type": "websocket.disconnect"}

    async def send(message):
        messages.append(message)

    async def scenario():
        try:
            await asgi._websocket(
                {"type": "websocket", "path": "/", "headers": []},
                receive,
                send,
            )

            assert asgi.session_store is session_store
            session_messages = [
                message
                for message in messages
                if message.get("type") == "websocket.send"
            ]
            assert session_messages
            handshake = json.loads(session_messages[0]["text"])
            token = handshake["token"]
            session = session_store.get(token)
            assert session is not None
            assert session in asgi._sessions
        finally:
            for session in tuple(asgi._sessions):
                session.detach_external_loop()
                asgi._sessions.discard(session)
            session_store.clear()

    run(scenario())


def test_asgi_shutdown_clears_injected_session_store():
    session_store = InMemorySessionStore()
    asgi = ASGIApp(
        app_factory=lambda: pl.column(pl.button("Test")),
        session_store=session_store,
    )
    messages = []

    async def websocket_receive():
        return {"type": "websocket.disconnect"}

    async def websocket_send(message):
        messages.append(message)

    async def scenario():
        await asgi._websocket(
            {"type": "websocket", "path": "/", "headers": []},
            websocket_receive,
            websocket_send,
        )

        session_messages = [
            message
            for message in messages
            if message.get("type") == "websocket.send"
        ]
        assert session_messages
        token = json.loads(session_messages[0]["text"])["token"]
        assert session_store.get(token) is not None

        events = asyncio.Queue()

        async def lifespan_receive():
            return await events.get()

        async def lifespan_send(message):
            messages.append(message)

        await events.put({"type": "lifespan.startup"})
        task = asyncio.create_task(asgi._lifespan(lifespan_receive, lifespan_send))
        await asyncio.sleep(0)
        await events.put({"type": "lifespan.shutdown"})
        await task

        assert session_store.get(token) is None
        assert not asgi._sessions

    run(scenario())


def test_asgi_expired_session_is_detached_and_removed():
    now = [100.0]

    def clock():
        return now[0]

    session_store = InMemorySessionStore(ttl=10, clock=clock)
    app = pl.column(pl.button("Test"))
    asgi = ASGIApp(app, session_store=session_store)

    async def scenario():
        asgi.websocket.attach_external_loop(asyncio.get_running_loop())
        try:
            session_store.put("expired", asgi.websocket)
            asgi._sessions.add(asgi.websocket)

            now[0] = 110.0
            asgi._evict_expired_sessions()

            assert session_store.get("expired") is None
            assert asgi.websocket not in asgi._sessions
            assert asgi.websocket._loop is None
        finally:
            if asgi.websocket._loop is not None:
                asgi.websocket.detach_external_loop()

    run(scenario())



def test_asgi_websocket_allows_configured_origin():
    app = ASGIApp(
        pl.column(pl.button('Test')),
        allowed_origins=('https://example.com',),
    )
    messages = []

    async def receive():
        return {'type': 'websocket.disconnect'}

    async def send(message):
        messages.append(message)

    run(
        app._websocket(
            {
                'type': 'websocket',
                'path': '/',
                'headers': [(b'origin', b'https://example.com')],
            },
            receive,
            send,
        )
    )

    assert messages[0] == {'type': 'websocket.accept'}


def test_asgi_websocket_rejects_disallowed_origin_before_accept():
    app = ASGIApp(
        pl.column(pl.button('Test')),
        allowed_origins=('https://example.com',),
    )
    messages = []

    async def receive():
        return {'type': 'websocket.disconnect'}

    async def send(message):
        messages.append(message)

    run(
        app._websocket(
            {
                'type': 'websocket',
                'path': '/',
                'headers': [(b'origin', b'https://evil.example')],
            },
            receive,
            send,
        )
    )

    assert messages
    assert messages[0]['type'] == 'websocket.close'
    assert messages[0]['code'] == 1008
    assert not any(message.get('type') == 'websocket.accept' for message in messages)


def test_asgi_websocket_allows_missing_origin_for_non_browser_clients():
    app = ASGIApp(
        pl.column(pl.button('Test')),
        allowed_origins=('https://example.com',),
    )
    messages = []

    async def receive():
        return {'type': 'websocket.disconnect'}

    async def send(message):
        messages.append(message)

    run(
        app._websocket(
            {'type': 'websocket', 'path': '/', 'headers': []},
            receive,
            send,
        )
    )

    assert messages[0] == {'type': 'websocket.accept'}


def test_asgi_websocket_enforces_message_size_limit():
    app = ASGIApp(
        pl.column(pl.button('Test')),
        max_message_size=8,
    )
    messages = []
    received = False

    async def receive():
        nonlocal received
        if not received:
            received = True
            return {'type': 'websocket.receive', 'text': '123456789'}
        return {'type': 'websocket.disconnect'}

    async def send(message):
        messages.append(message)

    run(
        app._websocket(
            {'type': 'websocket', 'path': '/', 'headers': []},
            receive,
            send,
        )
    )

    assert messages[0] == {'type': 'websocket.accept'}
    assert any(
        message.get('type') == 'websocket.close'
        and message.get('code') == 1009
        for message in messages
    )


def test_asgi_websocket_accepts_message_at_size_limit():
    app = ASGIApp(
        pl.column(pl.button('Test')),
        max_message_size=8,
    )
    messages = []

    async def receive():
        return {'type': 'websocket.disconnect'}

    async def send(message):
        messages.append(message)

    connection = app._websocket

    async def scenario():
        await connection(
            {'type': 'websocket', 'path': '/', 'headers': []},
            receive,
            send,
        )

    run(scenario())

    assert messages[0] == {'type': 'websocket.accept'}


def test_asgi_connection_rejects_oversized_binary_message():
    from pylage.ENGINE.runtime.asgi import _ASGIConnection

    messages = []

    async def receive():
        return {'type': 'websocket.receive', 'bytes': b'123456789'}

    async def send(message):
        messages.append(message)

    connection = _ASGIConnection(receive, send, max_message_size=8)

    async def scenario():
        await connection.__anext__()

    import pytest

    with pytest.raises(StopAsyncIteration):
        run(scenario())

    assert messages == [
        {'type': 'websocket.close', 'code': 1009},
    ]

def test_asgi_websocket_rate_limit_configuration():
    app = ASGIApp(
        pl.column(pl.button('Test')),
        message_rate_limit=7.5,
        message_rate_burst=9,
    )

    assert app.message_rate_limit == 7.5
    assert app.message_rate_burst == 9
    assert app.websocket.message_rate_limit == 7.5
    assert app.websocket.message_rate_burst == 9


def test_asgi_websocket_rate_limit_configuration_reaches_factory_session():
    def factory():
        return pl.column(pl.button('Test'))

    app = ASGIApp(
        app_factory=factory,
        message_rate_limit=6.0,
        message_rate_burst=8,
    )
    messages = []

    async def receive():
        return {'type': 'websocket.disconnect'}

    async def send(message):
        messages.append(message)

    run(
        app._websocket(
            {
                'type': 'websocket',
                'path': '/',
                'headers': [],
                'query_string': b'',
            },
            receive,
            send,
        )
    )

    assert messages[0] == {'type': 'websocket.accept'}
    assert len(app._sessions) == 1

    session = next(iter(app._sessions))
    assert session.message_rate_limit == 6.0
    assert session.message_rate_burst == 8


def test_asgi_websocket_rate_limit_configuration_validation():
    import pytest

    app = pl.column(pl.button('Test'))

    with pytest.raises(ValueError):
        ASGIApp(app, message_rate_limit=0)

    with pytest.raises(ValueError):
        ASGIApp(app, message_rate_burst=0)

    with pytest.raises(TypeError):
        ASGIApp(app, message_rate_limit=True)

    with pytest.raises(TypeError):
        ASGIApp(app, message_rate_burst=True)
