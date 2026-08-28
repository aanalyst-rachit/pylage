import asyncio
import json

import pyskin as ps
from pyskin.runtime.websocket import WebSocketServer


print("=== PYSKIN AUTOMATIC BROWSER INPUT BINDING TEST ===")

name = ps.State("Dollar")

heading = ps.Heading(name)
input_box = ps.Input(value=name)

app = ps.Column(
    heading,
    input_box,
)

server = WebSocketServer(app)
url = server.start()

print("WebSocket:", url)
print("Heading ID:", heading.id)
print("Input ID:", input_box.id)
print("Initial state:", name.value)


async def test_binding():
    import websockets

    async with websockets.connect(url) as ws:
        print("WebSocket connected: PASS")

        event = {
            "type": "event",
            "id": input_box.id,
            "event": "input",
            "payload": {
                "value": "Racit"
            },
        }

        await ws.send(json.dumps(event))

        response = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        print("Response:", response)

        assert response["type"] == "response"
        assert response["ok"] is True

        update = json.loads(
            await asyncio.wait_for(ws.recv(), timeout=2)
        )

        print("Update:", update)

        assert update["type"] == "update"
        assert update["id"] == heading.id
        assert update["props"]["text"] == "Racit"

        assert name.value == "Racit"

        print()
        print("Browser → WebSocket: PASS")
        print("Automatic Input → State: PASS")
        print("State → UpdateMessage: PASS")
        print("Heading updated: PASS")
        print("Final state:", name.value)
        print()
        print("=== AUTOMATIC BROWSER INPUT BINDING PASS ===")


try:
    asyncio.run(test_binding())
finally:
    server.stop()
