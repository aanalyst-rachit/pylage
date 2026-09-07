import asyncio
import json

from pylage.ENGINE import Drawer, State
from pylage.ENGINE.runtime.websocket import WebSocketServer


def test_drawer_reactive_open_close_sends_remove_props():
    async def scenario():
        open_state = State(False)

        drawer = Drawer(
            open=open_state,
            title="Test Drawer",
        )

        server = WebSocketServer(drawer)
        server.start()

        try:
            import websockets

            async with websockets.connect(server.url) as ws:
                # Open drawer.
                open_state.set(True)

                message = json.loads(
                    await asyncio.wait_for(ws.recv(), timeout=2)
                )

                assert message["type"] == "update"
                assert message["id"] == drawer.id
                assert message["props"]["open"] is True
                assert "title" not in message["props"]
                assert "class_name" not in message["props"]
                assert message.get("remove_props", []) == []

                # Close drawer.
                open_state.set(False)

                message = json.loads(
                    await asyncio.wait_for(ws.recv(), timeout=2)
                )

                assert message["type"] == "update"
                assert message["id"] == drawer.id

                # Regression contract:\n                # boolean False is a changed boolean value, not a removed prop.\n                assert message["props"]["open"] is False\n                assert "title" not in message["props"]\n                assert "class_name" not in message["props"]\n                assert message.get("remove_props", []) == []\n
        finally:
            server.stop()

    asyncio.run(scenario())
