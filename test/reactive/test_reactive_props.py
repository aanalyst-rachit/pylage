import asyncio
import json

import pylage as ps
from pylage.ENGINE.core.protocol_codec import decode_message

from pylage.ENGINE import Column, State
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.runtime.websocket import WebSocketServer

print("=== PYLAGE GENERIC REACTIVE PROPS TEST ===")

text = State("Hello")
value = State("100")
disabled = State(False)
title = State("Initial title")

component = Component(
    type="Button",
    props={
        "text": text,
        "value": value,
        "disabled": disabled,
        "title": title,
    },
)

app = Column(component)

server = WebSocketServer(app)
url = server.start()

print("WebSocket:", url)
print("Component ID:", component.id)
print("Initial:")
print("  text =", text.value)
print("  value =", value.value)
print("  disabled =", disabled.value)
print("  title =", title.value)


async def _test_props():
    import websockets

    async with websockets.connect(url) as ws:
        print("WebSocket connected: PASS")

        text.set("World")

        message = decode_message(
            await asyncio.wait_for(ws.recv(), timeout=2)
        ).to_dict()

        print("Received:", message)

        assert message["type"] == "update"
        assert message["id"] == component.id
        assert message["props"]["text"] == "World"

        print("text: PASS")

        value.set("200")

        message = decode_message(
            await asyncio.wait_for(ws.recv(), timeout=2)
        ).to_dict()

        assert message["props"]["value"] == "200"

        print("value: PASS")

        disabled.set(True)

        message = decode_message(
            await asyncio.wait_for(ws.recv(), timeout=2)
        ).to_dict()

        assert message["props"]["disabled"] is True

        print("disabled: PASS")

        title.set("Updated title")

        message = decode_message(
            await asyncio.wait_for(ws.recv(), timeout=2)
        ).to_dict()

        assert message["props"]["title"] == "Updated title"

        print("title: PASS")

        print()
        print("State → UpdateMessage: PASS")
        print("Multiple reactive props: PASS")
        print()
        print("=== GENERIC REACTIVE PROPS PASS ===")


def test_sync_wrapper():
    try:
        asyncio.run(_test_props())
    finally:
        server.stop()
