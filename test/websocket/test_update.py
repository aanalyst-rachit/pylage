import asyncio
import json
import time

from pylage.ENGINE import State
from pylage.ENGINE.runtime.websocket import WebSocketServer
from pylage.UI.components.text import text


def test_phase16_ui_kit_websocket_update_behavior():
    async def run():
        state = State(0)
        component = text(state)
        server = WebSocketServer(component)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                samples = 100
                start = time.perf_counter()

                for value in range(1, samples + 1):
                    state.set(value)

                    raw = await asyncio.wait_for(
                        ws.recv(),
                        timeout=2,
                    )
                    message = json.loads(raw)

                    assert message["type"] == "update"
                    assert message["id"] == component.id
                    assert message["props"]["text"] == value

                elapsed = time.perf_counter() - start

                print()
                print("===== PHASE 16 — UI KIT WEBSOCKET UPDATE =====")
                print(f"iterations        : {samples}")
                print(f"total             : {elapsed:.9f}s")
                print(f"per update        : {elapsed / samples:.9f}s")

        finally:
            server.stop()

    asyncio.run(run())


def test_phase16_ui_kit_websocket_batching():
    async def run():
        state = State(0)
        component = text(state)
        server = WebSocketServer(component)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                for value in range(1, 101):
                    state.set(value)

                raw = await asyncio.wait_for(
                    ws.recv(),
                    timeout=2,
                )
                message = json.loads(raw)

                assert message["type"] == "update"
                assert message["id"] == component.id
                assert message["props"]["text"] == 100

                print()
                print("===== PHASE 16 — UI KIT WEBSOCKET BATCHING =====")
                print("state changes     : 100")
                print("messages received : 1")
                print("final value       : 100")

                try:
                    await asyncio.wait_for(ws.recv(), timeout=0.1)
                except asyncio.TimeoutError:
                    pass
                else:
                    raise AssertionError("unexpected extra WebSocket update")

        finally:
            server.stop()

    asyncio.run(run())
