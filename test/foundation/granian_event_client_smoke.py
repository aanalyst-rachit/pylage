import asyncio
import json
import websockets


async def main():
    async with websockets.connect("ws://127.0.0.1:8767/") as websocket:
        message = {"type": "event", "id": "granian-button", "event": "click"}
        await websocket.send(json.dumps(message, separators=(",", ":")))
        raw = await asyncio.wait_for(websocket.recv(), timeout=5)
        response = json.loads(raw)
        print("WS RESPONSE:", response)
        assert response["type"] == "response"
        assert response["ok"] is True
        print("GRANIAN EVENT ROUND-TRIP PASS")


asyncio.run(main())
