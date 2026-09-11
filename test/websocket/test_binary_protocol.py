import asyncio

from websockets.asyncio.client import connect

from pylage.ENGINE import Button, Column
from pylage.ENGINE.core.protocol import EventMessage, EventMessageResponse
from pylage.ENGINE.core.protocol_codec import decode_message, encode_message
from pylage.ENGINE.runtime.websocket import WebSocketServer


def test_binary_event_round_trip():
    calls = []

    def clicked():
        calls.append("clicked")
        return "handler-ok"

    button = Button("Click me", on_click=clicked)
    server = WebSocketServer(Column(button))
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            message = EventMessage(
                component_id=button.id,
                event="click",
            )
            await websocket.send(encode_message(message))
            raw = await websocket.recv()

            assert isinstance(raw, bytes)
            response = decode_message(raw)
            assert isinstance(response, EventMessageResponse)
            assert response.to_dict()["type"] == "response"
            assert response.to_dict()["ok"] is True
            assert response.to_dict()["result"] == "handler-ok"

    try:
        asyncio.run(run())
    finally:
        server.stop()

    assert calls == ["clicked"]
