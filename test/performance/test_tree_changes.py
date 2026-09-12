import asyncio
import json

from pylage.ENGINE.core.protocol_codec import decode_message

from pylage.ENGINE import Column, State
from pylage.ENGINE.runtime.websocket import WebSocketServer
from pylage.UI.components.button import button
from pylage.UI.components.text import text


def test_phase16_ui_kit_unnecessary_tree_changes():
    async def run():
        state = State("Initial")

        target = text(state)
        sibling = text("Static sibling")
        control = button("Save")
        root = Column(target, sibling, control)

        server = WebSocketServer(root)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                state.set("Updated")

                raw = await asyncio.wait_for(ws.recv(), timeout=2)
                message = decode_message(raw).to_dict()

                assert message["type"] == "update"
                assert message["id"] == target.id
                assert message["props"]["text"] == "Updated"

                try:
                    await asyncio.wait_for(ws.recv(), timeout=0.15)
                except asyncio.TimeoutError:
                    pass
                else:
                    raise AssertionError("unexpected extra tree update")

                print()
                print("===== PHASE 16 — UNNECESSARY TREE CHANGES =====")
                print("target component   : updated")
                print("sibling text       : unchanged")
                print("sibling button     : unchanged")
                print("extra messages     : 0")

        finally:
            server.stop()

    asyncio.run(run())


def test_phase16_ui_kit_repeated_state_changes_are_coalesced():
    async def run():
        state = State("Initial")
        target = text(state)
        sibling = text("Static sibling")
        root = Column(target, sibling)

        server = WebSocketServer(root)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                for value in range(1, 101):
                    state.set(f"Value {value}")

                raw = await asyncio.wait_for(ws.recv(), timeout=2)
                message = decode_message(raw).to_dict()

                assert message["type"] == "update"
                assert message["id"] == target.id
                assert message["props"]["text"] == "Value 100"

                try:
                    await asyncio.wait_for(ws.recv(), timeout=0.15)
                except asyncio.TimeoutError:
                    pass
                else:
                    raise AssertionError("unexpected extra update")

                print()
                print("===== PHASE 16 — TREE CHANGE COALESCING =====")
                print("state changes     : 100")
                print("target updates    : 1")
                print("final value       : Value 100")
                print("unrelated updates : 0")

        finally:
            server.stop()

    asyncio.run(run())
