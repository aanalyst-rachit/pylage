import asyncio

from websockets.asyncio.client import connect

from pylage.ENGINE import Column
from pylage.ENGINE.core.protocol import EventMessageResponse, NavigateMessage
from pylage.ENGINE.core.protocol_codec import decode_message, encode_message
from pylage.ENGINE.runtime.websocket import WebSocketServer


def test_navigation_message_round_trip():
    message = NavigateMessage("/dashboard/42")
    assert message.to_dict() == {"type": "navigate", "path": "/dashboard/42"}


def test_navigation_handler_binary():
    paths = []
    server = WebSocketServer(
        Column(),
        navigation_handler=paths.append,
    )
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            await websocket.send(encode_message(NavigateMessage("/dashboard/42")))
            raw = await websocket.recv()
            response = decode_message(raw)
            assert isinstance(response, EventMessageResponse)
            assert response.ok is True

    try:
        asyncio.run(run())
    finally:
        server.stop()

    assert paths == ["/dashboard/42"]


def test_navigation_handler_json():
    paths = []
    server = WebSocketServer(
        Column(),
        navigation_handler=paths.append,
    )
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            await websocket.send(NavigateMessage("/analytics").to_json())
            raw = await websocket.recv()
            response = EventMessageResponse.from_json(raw)
            assert response.ok is True

    try:
        asyncio.run(run())
    finally:
        server.stop()

    assert paths == ["/analytics"]


def test_navigation_with_routing_runtime(tmp_path):
    from pathlib import Path
    import pylage as pl
    from pylage.ENGINE.routing import Router, RoutingRuntime

    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / "dashboard.py").write_text(
        "import pylage as pl\n\ndef page():\n    return pl.text(\"Dashboard\")\n",
        encoding="utf-8",
    )
    root = pl.column()
    runtime = RoutingRuntime(Router(pages), root)

    def on_navigate(path: str):
        runtime.navigate(path)
        return None

    server = WebSocketServer(root, navigation_handler=on_navigate)
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            await websocket.send(encode_message(NavigateMessage("/dashboard")))
            raw = await websocket.recv()
            response = decode_message(raw)
            assert isinstance(response, EventMessageResponse)
            assert response.ok is True

    try:
        asyncio.run(run())
    finally:
        server.stop()

    assert runtime.current_path == "/dashboard"
    assert len(list(root.children)) == 1
