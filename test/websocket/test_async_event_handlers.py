import asyncio

from websockets.asyncio.client import connect

from pylage.ENGINE import Button, Column
from pylage.ENGINE.core.protocol import EventMessage, EventMessageResponse
from pylage.ENGINE.core.protocol_codec import decode_message, encode_message
from pylage.ENGINE.runtime.websocket import WebSocketServer


def test_async_event_handler_returns_completed_result():
    async def clicked():
        await asyncio.sleep(0.01)
        return "async-ok"

    button = Button("Click me", on_click=clicked)
    server = WebSocketServer(Column(button))
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            await websocket.send(
                encode_message(EventMessage(button.id, "click"))
            )
            response = decode_message(await websocket.recv())
            assert isinstance(response, EventMessageResponse)
            assert response.ok is True
            assert response.result == "async-ok"

    try:
        asyncio.run(run())
    finally:
        server.stop()


def test_async_event_handler_exception_returns_failure_response():
    async def clicked():
        await asyncio.sleep(0)
        raise ValueError("async handler failed")

    button = Button("Click me", on_click=clicked)
    server = WebSocketServer(Column(button))
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            await websocket.send(
                encode_message(EventMessage(button.id, "click"))
            )
            response = decode_message(await websocket.recv())
            assert isinstance(response, EventMessageResponse)
            assert response.ok is False
            assert response.error == "async handler failed"

    try:
        asyncio.run(run())
    finally:
        server.stop()
